import importlib
import traceback
import logging
import json
from typing import Dict, Any, List
import asyncio
from datetime import datetime, timedelta
import re
import os
from pathlib import Path

from colorama import init, Fore, Style
from tabulate import tabulate

from act.nodes.base_node import initialize_registry

from .actfile_parser import ActfileParser, ActfileParserError
from .workflow_engine import WorkflowEngine
from .node_context import NodeContext
from act.nodes import node_registry 


# Initialize colorama for cross-platform color support
init()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExecutionManager:
    def __init__(self, actfile_path: str = 'Actfile', sandbox_timeout: int = 600):
        logger.info(f"Initializing ExecutionManager")
        # Initialize the node registry
        initialize_registry(str(Path(__file__).parent / "nodes"))
        
        self.actfile_path = actfile_path
        self.node_results = {}
        self.execution_queue = asyncio.Queue()
        self.sandbox_timeout = sandbox_timeout
        self.sandbox_start_time = None
        self.load_workflow()
        self.actfile_path = Path(actfile_path)
        self.workflow_engine = WorkflowEngine()
        self.node_loading_status = {}

    def load_workflow(self):
        logger.info("Loading workflow data")
        try:
            parser = ActfileParser(self.actfile_path)
            self.workflow_data = parser.parse()
            self.actfile_parser = parser
        except ActfileParserError as e:
            logger.error(f"Error parsing Actfile: {e}")
            raise

        self.load_node_executors()

    def load_node_executors(self):
        """
        Dynamically loads node executors based on node types in workflow_data.
        Uses node registry first, then falls back to dynamic loading.
        """
        logger.info("Loading node executors")
        node_types = set(node['type'] for node in self.workflow_data['nodes'].values())
        self.node_executors = {}
        self.node_loading_status = {node_type: {'status': 'pending', 'message': ''} for node_type in node_types}

        for node_type in node_types:
            try:
                logger.info(f"Attempting to load node type: {node_type}")
                node_class = get_node_class(node_type)
                
                if node_class:
                    node_instance = self._instantiate_node(node_class)
                    self.node_executors[node_type] = node_instance
                    self.node_loading_status[node_type] = {
                        'status': 'success',
                        'message': f'Loaded from registry'
                    }
                    logger.info(f"Successfully loaded node executor for {node_type}")
                else:
                    # Fall back to dynamic loading if not in registry
                    # Try possible module naming patterns
                    possible_module_names = [
                        f"act.nodes.{node_type.lower()}_node",
                        f"act.nodes.{self._snake_case(node_type)}_node",
                        f"act.nodes.{node_type.lower()}",
                        f"act.nodes.{self._snake_case(node_type)}"
                    ]

                    node_instance = None
                    for module_name in possible_module_names:
                        try:
                            module = importlib.import_module(module_name)
                            logger.debug(f"Successfully imported module: {module_name}")
                            
                            # Try possible class names
                            possible_class_names = [
                                f"{node_type}Node",
                                f"{node_type.capitalize()}Node",
                                node_type,
                                self._pascal_case(f"{node_type}Node")
                            ]

                            for class_name in possible_class_names:
                                if hasattr(module, class_name):
                                    node_class = getattr(module, class_name)
                                    logger.info(f"Found node class: {class_name}")
                                    node_instance = self._instantiate_node(node_class)
                                    self.node_loading_status[node_type] = {
                                        'status': 'success',
                                        'message': f'Loaded from {module_name}.{class_name}'
                                    }
                                    break
                            
                            if node_instance:
                                break

                        except ImportError:
                            logger.debug(f"Could not import module: {module_name}")
                            continue

                    if node_instance:
                        self.node_executors[node_type] = node_instance
                        logger.info(f"Successfully loaded node executor for {node_type}")
                    else:
                        raise ImportError(f"Could not find suitable node class for {node_type}")

            except Exception as e:
                logger.error(f"Error loading node type '{node_type}': {str(e)}")
                logger.error(traceback.format_exc())
                from act.nodes.generic_node import GenericNode
                self.node_executors[node_type] = GenericNode()
                self.node_loading_status[node_type] = {
                    'status': 'fallback',
                    'message': f'Fallback to GenericNode: {str(e)}'
                }
                logger.info(f"Fallback to GenericNode for {node_type}")

        # Print node loading status table
        self._print_node_loading_status()

    def _print_node_loading_status(self):
        """Print a formatted table showing the loading status of all nodes"""
        headers = ["Node Type", "Status", "Message"]
        table_data = []
        
        for node_type, status in self.node_loading_status.items():
            status_symbol = "🟢" if status['status'] == 'success' else "🔴" if status['status'] == 'fallback' else "⚪"
            status_color = (Fore.GREEN if status['status'] == 'success' else 
                            Fore.RED if status['status'] == 'fallback' else 
                            Fore.YELLOW)
            
            table_data.append([
                node_type,
                f"{status_color}{status_symbol} {status['status'].upper()}{Style.RESET_ALL}",
                status['message']
            ])

        table = tabulate(table_data, headers=headers, tablefmt="grid")
        print("\nNode Loading Status:")
        print(table)
        print()  # Add a blank line after the table

    def _instantiate_node(self, node_class):
        """Helper method to instantiate a node with proper parameters"""
        if hasattr(node_class.__init__, '__code__') and 'sandbox_timeout' in node_class.__init__.__code__.co_varnames:
            node_instance = node_class(sandbox_timeout=self.sandbox_timeout)
        else:
            node_instance = node_class()
            
        if hasattr(node_instance, 'set_execution_manager'):
            node_instance.set_execution_manager(self)
            
        return node_instance

    def _snake_case(self, name):
        """Convert string to snake_case"""
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def _pascal_case(self, name):
        """Convert string to PascalCase"""
        return ''.join(word.capitalize() for word in re.split(r'[_\s]+', name))

    def execute_workflow(self) -> Dict[str, Any]:
        logger.info(f"Starting execution of workflow")
        self.node_results = {}
        execution_queue = []
        self.sandbox_start_time = datetime.now()

        try:
            start_node_name = self.actfile_parser.get_start_node()
            if not start_node_name:
                logger.error("No start node specified in Actfile.")
                return {"status": "error", "message": "No start node specified in Actfile.", "results": {}}

            execution_queue.append((start_node_name, None))

            while execution_queue:
                if self.is_sandbox_expired():
                    logger.warning("Sandbox has expired. Stopping execution.")
                    self._print_node_execution_results()
                    return {
                        "status": "warning",
                        "message": "Workflow execution stopped due to sandbox expiration",
                        "results": self.node_results
                    }

                node_name, input_data = execution_queue.pop(0)
                node_result = self.execute_node(node_name, input_data)
                self.node_results[node_name] = node_result

                if node_result.get('status') == 'error':
                    logger.error(f"Node {node_name} execution failed. Stopping workflow.")
                    self._print_node_execution_results()
                    return {
                        "status": "error",
                        "message": f"Workflow execution failed at node {node_name}",
                        "results": self.node_results
                    }

                successors = self.actfile_parser.get_node_successors(node_name)
                for successor in successors:
                    logger.debug(f"Queueing next node: {successor}")
                    execution_queue.append((successor, node_result))

            logger.info("Workflow execution completed")
            self._print_node_execution_results()

            return {
                "status": "success",
                "message": "Workflow executed successfully",
                "results": self.node_results
            }

        except Exception as e:
            logger.error(f"Error during workflow execution: {str(e)}", exc_info=True)
            self._print_node_execution_results()
            return {
                "status": "error",
                "message": f"Workflow execution failed: {str(e)}",
                "results": self.node_results
            }

    async def execute_workflow_async(self) -> Dict[str, Any]:
        """
        Asynchronous version of execute_workflow with the same functionality.
        """
        logger.info(f"Starting async execution of workflow")
        self.node_results = {}
        execution_queue = []
        self.sandbox_start_time = datetime.now()

        try:
            start_node_name = self.actfile_parser.get_start_node()
            if not start_node_name:
                logger.error("No start node specified in Actfile.")
                return {"status": "error", "message": "No start node specified in Actfile.", "results": {}}

            execution_queue.append((start_node_name, None))

            while execution_queue:
                if self.is_sandbox_expired():
                    logger.warning("Sandbox has expired. Stopping execution.")
                    self._print_node_execution_results()
                    return {
                        "status": "warning",
                        "message": "Workflow execution stopped due to sandbox expiration",
                        "results": self.node_results
                    }

                node_name, input_data = execution_queue.pop(0)
                # Use asyncio.to_thread for potentially blocking operations
                node_result = await asyncio.to_thread(self.execute_node, node_name, input_data)
                self.node_results[node_name] = node_result

                if node_result.get('status') == 'error':
                    logger.error(f"Node {node_name} execution failed. Stopping workflow.")
                    self._print_node_execution_results()
                    return {
                        "status": "error",
                        "message": f"Workflow execution failed at node {node_name}",
                        "results": self.node_results
                    }

                successors = self.actfile_parser.get_node_successors(node_name)
                for successor in successors:
                    logger.debug(f"Queueing next node: {successor}")
                    execution_queue.append((successor, node_result))

            logger.info("Workflow execution completed")
            self._print_node_execution_results()

            return {
                "status": "success",
                "message": "Workflow executed successfully",
                "results": self.node_results
            }

        except Exception as e:
            logger.error(f"Error during workflow execution: {str(e)}", exc_info=True)
            self._print_node_execution_results()
            return {
                "status": "error",
                "message": f"Workflow execution failed: {str(e)}",
                "results": self.node_results
            }

    def execute_node(self, node_name: str, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info(f"Executing node: {node_name}")
        try:
            if self.is_sandbox_expired():
                return {"status": "error", "message": "Sandbox expired"}

            node = self.workflow_data['nodes'][node_name]
            node_type = node.get('type')
            node_data = node.copy()

            if input_data:
                node_data['input'] = input_data

            resolved_node_data = self.resolve_placeholders_for_execution(node_data)

            logger.info(f"Node type: {node_type}")
            logger.info(f"Node data after resolving placeholders: {self.log_safe_node_data(resolved_node_data)}")

            executor = self.node_executors.get(node_type)
            if executor:
                logger.info(f"Executor found for node type: {node_type}")

                result = executor.execute(resolved_node_data)
                logger.info(f"Node {node_name} execution result: {self.log_safe_node_data(result)}")

                return result
            else:
                logger.error(f"No executor found for node type: {node_type}")
                return {"status": "error", "message": f"No executor found for node type: {node_type}"}

        except Exception as e:
            logger.error(f"Error executing node {node_name}: {str(e)}")
            logger.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    def is_sandbox_expired(self) -> bool:
        if self.sandbox_start_time is None:
            return False
        elapsed_time = datetime.now() - self.sandbox_start_time
        return elapsed_time.total_seconds() >= (self.sandbox_timeout - 30)  # Give 30 seconds buffer

    def resolve_placeholders_for_execution(self, data: Any) -> Any:
        """
        Resolves placeholders in the data while maintaining type consistency.
        """
        if isinstance(data, dict):
            return {k: self.resolve_placeholders_for_execution(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.resolve_placeholders_for_execution(item) for item in data]
        elif isinstance(data, str):
            # Resolve placeholders in strings
            resolved = self.resolve_placeholder_string(data)
            # Attempt to parse as JSON if it looks like JSON
            # Attempt to parse as JSON if it looks like JSON
            if resolved.startswith('{') and resolved.endswith('}'):
                try:
                    return json.loads(resolved)
                except json.JSONDecodeError:
                    pass  # Keep as string if JSON parsing fails
            return resolved
        return data

    def resolve_placeholder_string(self, text: str) -> str:
        # Handle environment variables
        if text.startswith('${') and text.endswith('}'):
            env_var = text[2:-1]
            return os.environ.get(env_var, text)
        
        pattern = re.compile(r'\{\{(.*?)\}\}')
        matches = pattern.findall(text)
        
        for match in matches:
            parts = match.split('.')
            node_id = parts[0]
            path = '.'.join(parts[1:])
            value = self.fetch_value(node_id, path)
            if value is not None:
                text = text.replace(f"{{{{{match}}}}}", str(value))
        
        return text

    def fetch_value(self, node_id: str, path: str) -> Any:
        logger.info(f"Fetching value for node_id: {node_id}, path: {path}")
        if node_id in self.node_results:
            result = self.node_results[node_id]
            for part in path.split('.'):
                if isinstance(result, dict) and part in result:
                    result = result[part]
                else:
                    return None
            return result
        return None

    @staticmethod
    def log_safe_node_data(node_data):
        if isinstance(node_data, dict):
            # Redact sensitive keys like 'api_key' if needed
            safe_data = {k: ('[REDACTED]' if k == 'api_key' else v) for k, v in node_data.items()}
        else:
            safe_data = node_data
        return json.dumps(safe_data, indent=2)

    @classmethod
    def register_node_type(cls, node_type: str, node_class: Any):
        """Register a node type with the registry"""
        logger.info(f"Registering custom node type: {node_type}")
        node_registry.register(node_type, node_class)

    def get_node_executor(self, node_type: str) -> Any:
        """Get a node executor from the registry"""
        return self.node_executors.get(node_type)

    def _print_node_execution_results(self):
        """
        Print a formatted table showing the execution results of all nodes
        that have been executed so far (stored in self.node_results).
        """
        if not self.node_results:
            print("\nNo nodes have been executed yet.\n")
            return

        headers = ["Node Name", "Status", "Message"]
        table_data = []

        for node_name, node_result in self.node_results.items():
            status = node_result.get('status', 'unknown')
            message = node_result.get('message', '')
            
            # Determine symbol/color based on status
            if status == 'success':
                status_symbol = "🟢"
                status_color = Fore.GREEN
            elif status == 'error':
                status_symbol = "🔴"
                status_color = Fore.RED
            elif status == 'warning':
                status_symbol = "🟡"
                status_color = Fore.YELLOW
            else:
                status_symbol = "⚪"
                status_color = Fore.WHITE

            table_data.append([
                node_name,
                f"{status_color}{status_symbol} {status.upper()}{Style.RESET_ALL}",
                message
            ])

        table = tabulate(table_data, headers=headers, tablefmt="grid")
        print("\nNode Execution Results:")
        print(table)
        print()


if __name__ == "__main__":
    # This block is for testing the ExecutionManager class independently
    async def main():
        execution_manager = ExecutionManager(actfile_path='path/to/your/Actfile', sandbox_timeout=600)
        result = await execution_manager.execute_workflow_async()
        print(json.dumps(result, indent=2))

    # Run the async main function
    asyncio.run(main())
