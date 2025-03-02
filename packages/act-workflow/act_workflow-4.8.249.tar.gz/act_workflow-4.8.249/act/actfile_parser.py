import configparser
import os
import re
import json
from typing import Dict, Any, List, Union
from pathlib import Path

class ActfileParserError(Exception):
    """Custom exception for Actfile parsing errors."""
    pass

class ActfileParser:
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        self.parsed_data: Dict[str, Any] = {}

    def parse(self) -> Dict[str, Any]:
        if not self.file_path.exists():
            raise ActfileParserError(f"Actfile not found: {self.file_path}")

        try:
            with open(self.file_path, 'r') as file:
                content = file.read()
            
            sections = self._split_sections(content)
            
            self.parsed_data = {
                "parameters": self._parse_parameters(sections.get('parameters', '')),
                "workflow": self._parse_section(sections.get('workflow', '')),
                "nodes": self._parse_nodes(sections),
                "edges": self._parse_edges(sections.get('edges', '')),
                "dependencies": self._parse_dependencies(sections.get('dependencies', '')),
                "env": self._parse_env(sections.get('env', '')),
                "settings": self._parse_settings(sections.get('settings', ''))
            }

            self._replace_parameters()
            self._validate_parsed_data()

        except Exception as e:
            raise ActfileParserError(f"Error parsing Actfile: {e}")

        return self.parsed_data

    def _split_sections(self, content: str) -> Dict[str, str]:
        pattern = r'\[([^\]]+)\](.*?)(?=\n\[|$)'
        matches = re.findall(pattern, content, re.DOTALL)
        return {match[0].strip(): match[1].strip() for match in matches}

    def _parse_section(self, content: str) -> Dict[str, Any]:
        lines = content.split('\n')
        section_data = {}
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                section_data[key.strip()] = self._parse_value(value.strip())
        return section_data

    def _parse_value(self, value: str) -> Any:
        """
        Parses values, resolving JSON objects, strings, and placeholders.
        """
        if value.startswith('{') and value.endswith('}'):
            try:
                return json.loads(value)  # Parse as JSON object
            except json.JSONDecodeError:
                return value  # Return as-is if parsing fails
        elif value.startswith('"') and value.endswith('"'):
            return value.strip('"')  # Remove quotes
        elif value.startswith('{{') and value.endswith('}}'):
            return value  # Placeholder, leave as is
        return value


    def _parse_nodes(self, sections: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
        nodes = {}
        for section_name, content in sections.items():
            if section_name.startswith('node:'):
                node_name = section_name.split('node:')[1]
                node_data = self._parse_section(content)
                if 'type' not in node_data:
                    raise ActfileParserError(f"Node '{node_name}' must have a 'type' field")
                nodes[node_name] = node_data
        return nodes

    def _parse_edges(self, content: str) -> Dict[str, List[str]]:
        edges = {}
        for line in content.split('\n'):
            line = line.strip()
            if line and '=' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    source, targets = parts
                    source = source.strip()
                    if source.startswith(';'):
                        raise ActfileParserError(f"Invalid edge definition: '{line}'. Remove the leading semicolon.")
                    targets = [t.strip() for t in targets.split(',') if t.strip()]
                    edges[source] = targets
                else:
                    raise ActfileParserError(f"Invalid edge definition: '{line}'. Expected format: 'source = target1, target2'")
        return edges

    def _parse_dependencies(self, content: str) -> Dict[str, List[str]]:
        dependencies = {}
        for line in content.split('\n'):
            if '=' in line:
                node_type, deps = line.split('=', 1)
                dependencies[node_type.strip()] = [d.strip() for d in deps.split(',')]
        return dependencies

    def _parse_env(self, content: str) -> Dict[str, str]:
        env_vars = {}
        for line in content.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if value.startswith('${') and value.endswith('}'):
                    env_var_name = value[2:-1]
                    env_vars[key] = os.environ.get(env_var_name, '')
                else:
                    env_vars[key] = value
        return env_vars

    def _parse_settings(self, content: str) -> Dict[str, Any]:
        settings = {}
        for line in content.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                try:
                    settings[key] = json.loads(value)
                except json.JSONDecodeError:
                    settings[key] = value
        return settings

    def _parse_parameters(self, content: str) -> Dict[str, Any]:
        parameters = {}
        for line in content.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                parameters[key.strip()] = self._parse_value(value.strip())
        return parameters

    def _replace_parameters(self):
        def replace_in_dict(d):
            for key, value in d.items():
                if isinstance(value, str):
                    d[key] = self._replace_parameter_in_string(value)
                elif isinstance(value, dict):
                    replace_in_dict(value)
                elif isinstance(value, list):
                    d[key] = [self._replace_parameter_in_string(item) if isinstance(item, str) else item for item in value]

        replace_in_dict(self.parsed_data)

    def _replace_parameter_in_string(self, s):
        for key, value in self.parsed_data['parameters'].items():
            s = s.replace(f"{{{{.Parameter.{key}}}}}", str(value))
        return s

    def _validate_parsed_data(self):
        # Validate that all nodes mentioned in edges exist in the nodes section
        all_nodes = set(self.parsed_data['nodes'].keys())
        for source, targets in self.parsed_data['edges'].items():
            if source not in all_nodes:
                raise ActfileParserError(f"Edge source node '{source}' not defined in nodes")
            for target in targets:
                if target not in all_nodes:
                    raise ActfileParserError(f"Edge target node '{target}' not defined in nodes")

        # Validate that all dependencies refer to existing node types
        node_types = set(node['type'] for node in self.parsed_data['nodes'].values())
        for dep_node_type in self.parsed_data['dependencies'].keys():
            if dep_node_type not in node_types:
                raise ActfileParserError(f"Dependency defined for non-existent node type: {dep_node_type}")

    def get_node_dependencies(self, node_type: str) -> List[str]:
        return self.parsed_data['dependencies'].get(node_type, [])

    def get_workflow_name(self) -> str:
        return self.parsed_data['workflow']['name']

    def get_workflow_description(self) -> str:
        return self.parsed_data['workflow']['description']

    def get_start_node(self) -> str:
        # Use the start_node specified in the workflow section
        return self.parsed_data['workflow'].get('start_node')

    def get_node_successors(self, node_name: str) -> List[str]:
        return self.parsed_data['edges'].get(node_name, [])

    def get_env_var(self, key: str, default: Any = None) -> Any:
        return self.parsed_data['env'].get(key, default)

    def get_setting(self, key: str, default: Any = None) -> Any:
        return self.parsed_data['settings'].get(key, default)

    def to_json(self) -> str:
        return json.dumps(self.parsed_data, indent=2)

    def validate_node_config(self, node_name: str, required_fields: List[str]) -> None:
        node_config = self.parsed_data['nodes'].get(node_name)
        if not node_config:
            raise ActfileParserError(f"Node '{node_name}' not found in configuration")
        
        for field in required_fields:
            if field not in node_config:
                raise ActfileParserError(f"Missing required field '{field}' in node '{node_name}' configuration")

    @staticmethod
    def find_actfile(start_dir: Union[str, Path] = None) -> Path:
        """Find the Actfile by searching in the current directory and its parents."""
        current_dir = Path(start_dir or os.getcwd())
        while True:
            actfile_path = current_dir / 'Actfile'
            if actfile_path.is_file():
                return actfile_path
            if current_dir.parent == current_dir:
                raise ActfileParserError("Actfile not found in current directory or any parent directory")
            current_dir = current_dir.parent