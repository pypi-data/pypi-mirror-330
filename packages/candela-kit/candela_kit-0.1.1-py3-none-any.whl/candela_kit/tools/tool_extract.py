import ast
from typing import List, Type

import black
from IPython import get_ipython

from ..dtos import ToolModule
from ..tools import BaseTool


def _get_nb_cell_nodes_of_type(*types):
    nodes = []
    for cell in reversed(get_ipython().user_ns["In"]):
        try:
            for node in ast.walk(ast.parse(cell)):
                if isinstance(node, types):
                    nodes.append(node)
        except Exception:
            continue
    return nodes


def _extract_imports_from_notebook() -> List[str]:
    imports = []

    for node in _get_nb_cell_nodes_of_type(ast.Import, ast.ImportFrom):
        line = ast.unparse(node)
        if line not in imports:
            imports.append(line)

    return imports


def _extract_class_def_from_notebook(cls: Type[BaseTool]) -> str:
    for node in _get_nb_cell_nodes_of_type(ast.ClassDef):
        if node.name == cls.__name__:
            return ast.unparse(node)

    raise ValueError(f"No class definition found in notebook for {cls.__name__}")


def _should_include_import(import_line: str, class_defs: List[str]) -> bool:
    if "," in import_line:
        items = [s.strip() for s in import_line.split("import")[-1].split(",")]
    else:
        items = [import_line.split()[-1]]

    return any(any(istr in class_def for istr in items) for class_def in class_defs)


def _is_valid_tool_class(obj: Type) -> bool:
    return isinstance(obj, type) and issubclass(obj, BaseTool) and obj != BaseTool


def list_all_tools_in_notebook() -> List[Type[BaseTool]]:
    namespace_values = get_ipython().user_ns.values()
    unique_tools = {obj for obj in namespace_values if _is_valid_tool_class(obj)}
    return [tool for tool in unique_tools if tool.__module__ == "__main__"]


def _map_imports(imports: List[str]) -> List[str]:

    map_dict = [
        ("candela_kit.ignite", "candela.circuits.intent"),
        ("candela_kit.tools", "candela.circuits.tools"),
        ("candela_kit as", "candela as"),
    ]

    for import_line in imports:
        for s1, s2 in map_dict:
            import_line = import_line.replace(s1, s2)

        yield import_line


def _filter_imports(imports: List[str], class_defs: List[str]) -> List[str]:
    return [line for line in imports if _should_include_import(line, class_defs)]


def tool_module_from_notebook(*tools: Type[BaseTool]) -> ToolModule | None:
    """Creates a ToolModule data object by extracting tool classes and their required imports from the current Jupyter notebook.

    Args:
        *tools: Variable number of BaseTool subclasses to extract. If no tools are provided, all BaseTool
               subclasses found in the notebook will be extracted.

    Returns:
        ToolModule: A module containing the extracted tool classes and their required imports. The module content
                   is formatted with separate sections for imports and class definitions.

    Examples:
        Extract specific tools:
        >>> tool_module = tool_module_from_notebook(MyTool1, MyTool2)

        Extract all tools from notebook:
        >>> tool_module = tool_module_from_notebook()
    """

    if len(tools) == 0:
        tools = list_all_tools_in_notebook()

    if len(tools) == 0:
        return None

    class_defs = [_extract_class_def_from_notebook(cls) for cls in tools]

    imports = _extract_imports_from_notebook()
    imports = _filter_imports(imports, class_defs)
    imports = _map_imports(imports)

    import_block = "\n".join(imports)
    class_def_block = "\n".join(sorted(class_defs))

    content = f'''"""Tool module extracted from jupyter notebook using candela_kit tool_module_from_notebook   
"""
{import_block}
{class_def_block}
'''
    return ToolModule(content=black.format_str(content, mode=black.FileMode()))
