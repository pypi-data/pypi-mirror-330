import configparser
import os
import re
import sys
from typing import Dict, List, NamedTuple, Tuple


class LayerDependencyRule(NamedTuple):
    """
    Represents a layer dependency rule with optional partitioning.

    Attributes:
        name: Original layer definition string
        parts: List of layer parts in dependency order
        dependency_type: Type of dependency between parts
        dependency_groups: List of groups of parts with their relationships
    """

    name: str
    parts: List[str]
    dependency_type: str  # '>', '<', '|', 'single', or 'mixed'
    dependency_groups: List[Tuple[List[str], str]]  # [(parts, operator), ...]


class ContractConfig(NamedTuple):
    """Represents a parsed contract configuration."""

    name: str
    layers: List[LayerDependencyRule]
    container: str
    external_imports_only_allowed_layers: List[str]
    external_imports_only_allowed_imports: List[str]


def tokenize_layer_definition(value: str) -> List[Tuple[str, str]]:
    """
    Tokenize a layer definition into parts and operators.

    Args:
        value: String containing layer definition with operators

    Returns:
        List of tuples (part, operator), where operator can be '>', '<', '|', or ''

    Example:
        "service.a > service.b | service.c > service.d" ->
        [("service.a", ">"), ("service.b", "|"), ("service.c", ">"), ("service.d", "")]
    """
    # Split the definition into tokens while preserving operators
    pattern = r"([^<>|\s]+)\s*([<>|]?)(?:\s*|$)"
    matches = re.finditer(pattern, value)
    return [(match.group(1).strip(), match.group(2)) for match in matches]


def parse_layer_rule(layer_definition: str) -> LayerDependencyRule:
    """
    Parse a layer definition into parts and dependency types.

    Supports:
    - Chain dependencies: 'A > B > C' (A imports B imports C)
    - Reverse dependencies: 'A < B' (B imports A)
    - Walls: 'A | B' (no imports between A and B)
    - Mixed chains: 'A > B > C | D' (A imports B imports C, no imports with D)

    Examples:
        'service.scenario > service.interfaces > service.utils'
        'service.api | service.impl > service.core'
        'service.handlers < service.core > service.utils'
    """
    # Handle single layer case
    if not any(op in layer_definition for op in [">", "<", "|"]):
        return LayerDependencyRule(
            name=layer_definition,
            parts=[layer_definition],
            dependency_type="single",
            dependency_groups=[([layer_definition], "single")],
        )

    # Tokenize the layer definition
    tokens = tokenize_layer_definition(layer_definition)

    # Process the tokens to build dependency groups
    parts = []
    dependency_groups = []
    current_group = []
    current_operator = None

    for part, operator in tokens:
        parts.append(part)
        current_group.append(part)

        if operator:
            if operator != current_operator and current_group:
                if current_operator:  # Finish the previous group
                    dependency_groups.append((current_group.copy(), current_operator))
                    current_group = [part]
                current_operator = operator
        elif current_group:  # Last part in a group
            dependency_groups.append(
                (current_group.copy(), current_operator or "single")
            )
            current_group = []

    # Handle any remaining group
    if current_group:
        dependency_groups.append((current_group, current_operator or "single"))

    # Determine overall dependency type
    if len(set(group[1] for group in dependency_groups)) == 1:
        dependency_type = dependency_groups[0][1]
    else:
        dependency_type = "mixed"

    return LayerDependencyRule(
        name=layer_definition,
        parts=parts,
        dependency_type=dependency_type,
        dependency_groups=dependency_groups,
    )


def load_config(config_path: str) -> Dict:
    """Load and parse the configuration file."""
    if not os.path.exists(config_path):
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_path)

    result: Dict[str, Dict[str, str | List[str]]] = {}
    for section in config.sections():
        result[section] = {}
        for key, value in config.items(section):
            if key in [
                "layers",
                "external_imports_only_allowed_layers",
                "external_imports_only_allowed_imports",
            ]:
                result[section][key] = [
                    item.strip() for item in value.strip().split("\n") if item.strip()
                ]
            else:
                result[section][key] = value

    return result


def parse_contract_config(config_section: Dict) -> ContractConfig:
    """Parse a contract section into a ContractConfig object."""
    name = config_section.get("name", "")
    raw_layers = config_section.get("layers", [])
    container = config_section.get("container", "")
    external_allowed_layers = config_section.get(
        "external_imports_only_allowed_layers", []
    )
    external_allowed_imports = config_section.get(
        "external_imports_only_allowed_imports", []
    )

    layer_rules = [parse_layer_rule(layer) for layer in raw_layers]

    return ContractConfig(
        name=name,
        layers=layer_rules,
        container=container,
        external_imports_only_allowed_layers=external_allowed_layers,
        external_imports_only_allowed_imports=external_allowed_imports,
    )
