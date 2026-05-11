from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path
from typing import Any


class SymbolCollector(ast.NodeVisitor):
    def __init__(self, module_name: str) -> None:
        self.module_name: str = module_name
        self.class_stack: list[str] = []
        self.function_positions: dict[tuple[int, int], str] = {}

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        parts: list[str] = [self.module_name]

        if self.class_stack:
            parts.extend(self.class_stack)

        parts.append(node.name)

        qualified_name: str = ".".join(parts)

        self.function_positions[(node.lineno, node.col_offset)] = qualified_name

        self.generic_visit(node)


class CallCollector(ast.NodeVisitor):
    def __init__(
        self,
        module_name: str,
        function_positions: dict[tuple[int, int], str],
    ) -> None:
        self.module_name: str = module_name
        self.function_positions: dict[tuple[int, int], str] = function_positions
        self.current_function: str | None = None
        self.edges: set[tuple[str, str]] = set()
        self.class_stack: list[str] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        current: str | None = self.current_function

        parts: list[str] = [self.module_name]

        if self.class_stack:
            parts.extend(self.class_stack)

        parts.append(node.name)

        self.current_function = ".".join(parts)

        self.generic_visit(node)

        self.current_function = current

    def visit_Call(self, node: ast.Call) -> None:
        if self.current_function is None:
            self.generic_visit(node)
            return

        callee: str | None = self._resolve_call(node.func)

        if callee is not None:
            self.edges.add((self.current_function, callee))

        self.generic_visit(node)

    def _resolve_call(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):
            parts: list[str] = []

            current: ast.AST = node

            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value

            if isinstance(current, ast.Name):
                parts.append(current.id)

            parts.reverse()

            return ".".join(parts)

        return None


def run_pyright() -> dict[str, Any]:
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [
            "pyright",
            "--outputjson",
            "main.py",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode not in {0, 1}:
        raise RuntimeError(result.stderr)

    return json.loads(result.stdout)


def collect_python_files(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("*.py")
        if ".venv" not in path.parts and "__pycache__" not in path.parts
    ]


def generate_dot(edges: set[tuple[str, str]], output: Path) -> None:
    lines: list[str] = [
        "digraph G {",
        '    rankdir="TB";',
        "    splines=true;",
        "    overlap=false;",
        "    nodesep=0.3;",
        "    ranksep=0.6;",
        "    node [shape=box];",
    ]

    for caller, callee in sorted(edges):
        lines.append(f'    "{caller}" -> "{callee}";')

    lines.append("}")

    output.write_text("\n".join(lines))


def main() -> None:
    project_root: Path = Path.cwd()

    pyright_data: dict[str, Any] = run_pyright()

    if "generalDiagnostics" in pyright_data:
        for diagnostic in pyright_data["generalDiagnostics"]:
            severity: str = diagnostic.get("severity", "unknown")
            message: str = diagnostic.get("message", "")

            print(f"[{severity}] {message}")

    all_edges: set[tuple[str, str]] = set()

    for file_path in collect_python_files(project_root):
        try:
            source: str = file_path.read_text()
            tree: ast.AST = ast.parse(source)
        except SyntaxError:
            continue

        module_name: str = (
            file_path.relative_to(project_root)
            .with_suffix("")
            .as_posix()
            .replace("/", ".")
        )

        symbol_collector = SymbolCollector(module_name)
        symbol_collector.visit(tree)

        call_collector = CallCollector(
            module_name=module_name,
            function_positions=symbol_collector.function_positions,
        )

        call_collector.visit(tree)

        all_edges.update(call_collector.edges)

    output_path: Path = Path("graph.dot")

    generate_dot(all_edges, output_path)

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
