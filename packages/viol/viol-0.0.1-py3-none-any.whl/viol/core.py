from __future__ import annotations
import abc
from dataclasses import dataclass
from typing import Any, Iterable, List, Optional
from flask import render_template_string

__all__ = [
    "ComponentBase",
    "Event",
    "ComponentList",
]


def unwrap(children: Iterable[Any]):
    for child in children:
        if isinstance(child, (str, ComponentBase)):
            yield child
        else:
            yield from unwrap(child)


class ComponentBase(abc.ABC):
    @abc.abstractmethod
    def render(self, **context: Any) -> str:
        pass


@dataclass
class Event(ComponentBase):
    rule: Optional[str] = None
    method: Optional[str] = None
    trigger: Optional[str] = None
    target: Optional[str] = None
    swap: Optional[str] = None
    include: Optional[str] = None

    def __repr__(self):
        attr = " ".join(
            [
                f'{k}="{v}"'
                for k, v in {
                    f"hx-{self.method}": self.rule,
                    "hx-trigger": self.trigger,  # click, mouseover, etc
                    "hx-target": self.target,
                    "hx-swap": self.swap,
                    "hx-include": self.include,
                }.items()
                if v
            ]
        )
        return attr.strip()

    def render(self, **context: Any) -> str:
        return f"<div {self}></div>"


class ComponentList(ComponentBase):
    def __init__(self, children: str | List[Any] = None):
        self.children = []
        if isinstance(children, str):
            children = [children]
        self.children.extend(children or [])

    def render(self, **context: Any) -> str:
        innerHTML = ""
        for child in unwrap(self.children):
            innerHTML += (
                render_template_string(child, **context)
                if isinstance(child, str)
                else child.render(**context)
            )
        return innerHTML

    @staticmethod
    def from_template(path: str) -> ComponentList:
        with open(path) as f:
            children = f.read()
        return ComponentList(children)
