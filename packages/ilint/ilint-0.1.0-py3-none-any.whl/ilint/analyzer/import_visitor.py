import ast
from typing import Set


class ImportVisitor(ast.NodeVisitor):
    """AST visitor that collects all import statements in a Python file."""

    def __init__(self) -> None:
        self.imports: Set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        """Process 'import x' statements."""
        for name in node.names:
            self.imports.add(name.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        """Process 'from x import y' statements."""
        if node.module is not None:
            self.imports.add(node.module)
        self.generic_visit(node)
