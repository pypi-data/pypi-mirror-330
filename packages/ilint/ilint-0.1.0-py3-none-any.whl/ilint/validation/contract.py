from typing import Dict, Optional, Set, Tuple

from ..config.parser import ContractConfig


class LayeredContract:
    """Represents an Layered Architecture contract with defined layers and rules."""

    def __init__(self, config: ContractConfig):
        self.name = config.name
        self.container = config.container
        self.layer_rules = config.layers
        self.external_imports_only_allowed_layers = (
            config.external_imports_only_allowed_layers
        )
        self.external_imports_only_allowed_imports = (
            config.external_imports_only_allowed_imports
        )

        # Build layer hierarchy
        self.layer_hierarchy = self._build_layer_hierarchy()

    def _build_layer_hierarchy(self) -> Dict[str, Dict[str, Set[str]]]:
        """
        Build a hierarchy of layers and their dependencies.

        Returns:
            Dictionary mapping each layer part to its allowed and forbidden imports.
        """
        hierarchy: Dict[str, Dict[str, Set[str]]] = {}

        # Initialize hierarchy for all parts
        for rule in self.layer_rules:
            for part in rule.parts:
                if part not in hierarchy:
                    hierarchy[part] = {"allowed_to_import": set(), "no_import": set()}

        # Process each rule's dependency groups
        for rule in self.layer_rules:
            for parts, operator in rule.dependency_groups:
                if operator == ">":
                    # Chain dependency: each part can import from the next
                    for i in range(len(parts) - 1):
                        hierarchy[parts[i]]["allowed_to_import"].add(parts[i + 1])
                elif operator == "<":
                    # Reverse chain dependency: each part can import from the previous
                    for i in range(len(parts) - 1, 0, -1):
                        hierarchy[parts[i]]["allowed_to_import"].add(parts[i - 1])
                elif operator == "|":
                    # Wall: no imports allowed between parts
                    for i, part in enumerate(parts):
                        for other_part in parts[i + 1 :]:  # noqa: E203
                            hierarchy[part]["no_import"].add(other_part)
                            hierarchy[other_part]["no_import"].add(part)

        return hierarchy

    def get_layer_for_module(self, module_name: str) -> Optional[str]:
        """Get the layer name for a given module."""
        if not module_name.startswith(f"{self.container}."):
            return None

        module_path = module_name[len(self.container) + 1 :]  # noqa: E203
        # Find the longest matching layer part
        matching_layer = None
        max_length = 0
        for layer in self.layer_hierarchy:
            if module_path.startswith(layer + ".") and len(layer) > max_length:
                matching_layer = layer
                max_length = len(layer)
        return matching_layer

    def validate_import(
        self, source_module: str, imported_module: str
    ) -> Tuple[bool, str]:
        """Validate that the import follows the architecture rules."""
        if not imported_module.startswith(f"{self.container}."):
            return True, ""

        if not source_module.startswith(f"{self.container}."):
            return True, ""

        source_layer = self.get_layer_for_module(source_module)
        imported_layer = self.get_layer_for_module(imported_module)

        if source_layer is None or imported_layer is None:
            return True, ""

        # Check if import is explicitly forbidden
        if imported_layer in self.layer_hierarchy[source_layer]["no_import"]:
            return False, (
                f"Illegal import: {source_module} cannot import from {imported_module} "
                f"as their layers ({source_layer} and {imported_layer}) are separated by a wall"
            )

        # Check if import is explicitly allowed
        if imported_layer in self.layer_hierarchy[source_layer]["allowed_to_import"]:
            return True, ""

        # If no explicit rule exists, check layer order in the original configuration
        source_idx = self._get_layer_index(source_layer)
        imported_idx = self._get_layer_index(imported_layer)

        if source_idx > imported_idx:
            return False, (
                f"Illegal import: {source_module} (layer {source_layer}) cannot import "
                f"from {imported_module} (layer {imported_layer}). "
                f"Higher layers can only import from lower layers."
            )

        return True, ""

    def _get_layer_index(self, layer_name: str) -> int:
        """Get the index of a layer in the original configuration."""
        for idx, rule in enumerate(self.layer_rules):
            if layer_name in rule.parts:
                return idx
        return -1
