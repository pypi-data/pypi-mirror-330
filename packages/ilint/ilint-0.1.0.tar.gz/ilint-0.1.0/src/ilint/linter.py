import ast
import os
from collections import defaultdict
from typing import List, Tuple

from .analyzer.import_visitor import ImportVisitor
from .config.parser import load_config, parse_contract_config
from .validation.contract import LayeredContract


class ImportLinter:
    """Main linter class that analyzes imports across a Python project."""

    def __init__(self, config_path: str):
        self.config = load_config(config_path)
        self.contracts = self._load_contracts()
        self.root_package = self.config.get("importlinter", {}).get("root_package", "")

    def _load_contracts(self) -> List[LayeredContract]:
        """Load contracts from the configuration."""
        contracts = []

        for section in self.config:
            if section.startswith("importlinter:contract:"):
                contract_config = parse_contract_config(self.config[section])
                contracts.append(LayeredContract(contract_config))

        return contracts

    def find_python_files(self, root_dir: str = None) -> List[str]:
        """Find all Python files in the project."""
        if root_dir is None:
            root_dir = os.getcwd()

        python_files = []
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))

        return python_files

    def get_module_name(self, file_path: str) -> str:
        """Convert a file path to a module name."""
        rel_path = os.path.realpath(file_path)
        module_path = os.path.splitext(rel_path)[0].replace(os.sep, ".")

        if module_path.endswith(".__init__"):
            module_path = module_path[:-9]

        parts = module_path.split("src")
        if len(parts) > 1:
            return f"src{parts[-1]}"
        return module_path

    def analyze_file(self, file_path: str) -> List[Tuple[str, str]]:
        """Analyze a Python file for import statements."""
        imports = []
        source_module = self.get_module_name(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)

            visitor = ImportVisitor()
            visitor.visit(tree)

            for imported_module in visitor.imports:
                imports.append((source_module, imported_module))

        except Exception as e:  # noqa: PIE786
            print(f"Error analyzing {file_path}: {str(e)}")

        return imports

    def validate_imports(self, imports: List[Tuple[str, str]]) -> List[str]:
        """Validate all imports against the contracts."""
        errors = []

        # Create an import graph
        import_graph = defaultdict(set)
        for source_module, imported_module in imports:
            import_graph[source_module].add(imported_module)

        # Check each import against each contract
        for source_module, imported_module in imports:
            for contract in self.contracts:
                is_valid, error_msg = contract.validate_import(
                    source_module, imported_module
                )
                if not is_valid:
                    errors.append(f"Contract '{contract.name}': {error_msg}")

        return errors

    def run(self, root_dir: str = None) -> bool:  # noqa: FNE005
        """Run the import linter on the project."""
        if not self.contracts:
            print("No contracts defined. Nothing to check.")
            return True

        self._print_contracts_info()

        python_files = self.find_python_files(root_dir)
        print(f"Found {len(python_files)} Python files to check")

        all_imports = []
        for file_path in python_files:
            all_imports.extend(self.analyze_file(file_path))

        print(f"Found {len(all_imports)} imports to validate")
        errors = self.validate_imports(all_imports)

        if errors:
            for error in errors:
                print(f"  - {error}")
            print(f"\nFound {len(errors)} violations")
            return False

        print("\nSuccess! All imports follow the architecture rules.")
        return True

    def _print_contracts_info(self):
        """Print information about loaded contracts."""
        print("Import Linter: Checking imports according to architecture rules")

        for contract in self.contracts:
            print(f"\nContract: {contract.name}")
            print(f"  Container: {contract.container}")
            print("  Layers (with dependencies):")
            for rule in contract.layer_rules:
                if rule.dependency_type == ">":
                    print(f"    - {' > '.join(rule.parts)}")
                elif rule.dependency_type == "|":
                    print(f"    - {' | '.join(rule.parts)}")
                else:
                    print(f"    - {rule.parts[0]}")

            if contract.external_imports_only_allowed_layers:
                print("  Layers allowed to be imported directly:")
                for layer in contract.external_imports_only_allowed_layers:
                    print(f"    - {layer}")

            if contract.external_imports_only_allowed_imports:
                print("  Modules allowed to be imported directly:")
                for module in contract.external_imports_only_allowed_imports:
                    print(f"    - {module}")
