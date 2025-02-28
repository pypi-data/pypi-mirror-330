# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""The pylsp_code_actions plugin module."""

from __future__ import annotations

import collections.abc as cabc
import textwrap
import typing as t

import parso
import parso.python.tree as pytree
import pylsp
import typing_extensions as te


@pylsp.hookimpl
def pylsp_code_actions(
    config,
    workspace,
    document,
    range: Range,
    context,
) -> list[CodeAction]:
    del config, context, workspace
    cursor = (range["start"]["line"] + 1, range["start"]["character"])

    actions: list[CodeAction] = []
    parser = parso.parse(document.source)
    module = parser.get_root_node()
    for node in walk(module):
        if not node.start_pos <= cursor < node.end_pos:
            continue

        if isinstance(node, pytree.Function):
            actions.extend(make_docstring_actions(document.uri, node))

        elif isinstance(node, pytree.Operator):
            actions.extend(make_flip_operator_action(document.uri, node))

    return actions


def make_docstring_actions(
    uri: str, function: pytree.Function
) -> cabc.Iterator[CodeAction]:
    if function.get_doc_node() is not None:
        return

    body = function.children[-1]
    assert isinstance(body, pytree.PythonNode)
    first_statement = body.children[0]
    insert_line = first_statement.end_pos[0]
    if function.children[-2].start_pos[0] == insert_line:
        return

    newline_before_close = False
    fragments = [
        '"""',
        function.name.value.replace("_", " ").strip().capitalize() + ".",
    ]

    params = "\n".join(
        f"{param.name.value}\n    The {param.name.value}."
        for param in function.get_params()
    )
    if params:
        fragments.append("\n\nParameters\n----------\n")
        fragments.append(params)
        newline_before_close = True

    if not function.is_generator():
        if function.annotation is None:
            rettype = "object"
        else:
            rettype = function.annotation.get_code(include_prefix=False)
        fragments.append("\n\nReturns\n-------\n")
        fragments.append(f"{rettype}\n    A {rettype}.")
        newline_before_close = True

    exctypes = set()
    for stmt in function.iter_raise_stmts():
        if not isinstance(stmt, pytree.Keyword):
            exctypes.add(stmt.children[1].children[0].value)
            continue

        stmt = next(
            (i for i in iterancestors(stmt) if isinstance(i, pytree.TryStmt)),
            None,
        )
        if not stmt:
            continue

        for test in stmt.get_except_clause_tests():
            for node in walk(test):
                if isinstance(node, pytree.Name):
                    exctypes.add(node.value)

    if exctypes:
        fragments.append("\n\nRaises\n------\n")
        fragments.append(
            "\n".join(f"{i}\n    Raised if..." for i in sorted(exctypes))
        )
        newline_before_close = True

    if newline_before_close:
        fragments.append("\n")
    fragments.append('"""\n')
    startcol = function.start_pos[1]
    prev = function.get_previous_sibling()
    if isinstance(prev, pytree.Keyword) and prev.value == "async":
        startcol = prev.start_pos[1]
    docstring = textwrap.indent(
        "".join(fragments),
        " " * (startcol + 4),
    )

    start: Position = {
        "line": first_statement.start_pos[0],
        "character": 0,
    }
    yield {
        "title": f"Generate docstring for function {function.name.value}",
        "kind": "quickfix",
        "edit": {
            "changes": {
                uri: [
                    {
                        "range": {"start": start, "end": start},
                        "newText": docstring,
                    }
                ]
            }
        },
    }


def make_flip_operator_action(
    uri: str, operator_node: pytree.Operator
) -> cabc.Iterator[CodeAction]:
    prev_node = operator_node.get_previous_sibling()
    next_node = operator_node.get_next_sibling()
    if prev_node is None or next_node is None:
        return

    yield {
        "title": f"Flip operator '{operator_node.value}'",
        "kind": "",
        "edit": {
            "changes": {
                uri: [
                    {
                        "range": {
                            "start": {
                                "line": prev_node.start_pos[0] - 1,
                                "character": prev_node.start_pos[1],
                            },
                            "end": {
                                "line": prev_node.end_pos[0] - 1,
                                "character": prev_node.end_pos[1],
                            },
                        },
                        "newText": next_node.get_code(False),
                    },
                    {
                        "range": {
                            "start": {
                                "line": next_node.start_pos[0] - 1,
                                "character": next_node.start_pos[1],
                            },
                            "end": {
                                "line": next_node.end_pos[0] - 1,
                                "character": next_node.end_pos[1],
                            },
                        },
                        "newText": prev_node.get_code(False),
                    },
                ]
            }
        },
    }


def walk(start: pytree.BaseNode) -> cabc.Iterator[pytree.BaseNode]:
    yield start
    for i in getattr(start, "children", ()):
        yield from walk(i)


def iterancestors(node):
    while node is not None:
        yield node
        node = node.parent


class Range(te.TypedDict):
    start: Position
    end: Position


class Position(te.TypedDict):
    line: int
    character: int


class CodeAction(te.TypedDict):
    title: str
    kind: t.Literal[
        "",
        "quickfix",
        "refactor",
        "refactor.extract",
        "refactor.inline",
        "refactor.rewrite",
        "source",
        "source.organizeImports",
        "source.fixAll",
    ]
    diagnostics: te.NotRequired[list[t.Any]]
    isPreferred: te.NotRequired[bool]
    edit: te.NotRequired[WorkspaceEdit]
    data: te.NotRequired[t.Any]


class WorkspaceEdit(te.TypedDict):
    changes: dict[str, list[TextEdit]]


class TextEdit(te.TypedDict):
    range: Range
    newText: str
