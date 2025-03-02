from __future__ import annotations
from typing import List, Any
import uuid
from viol.core import Event, ComponentBase


class Button(ComponentBase):
    def __init__(
        self,
        children: str | List[Any] = None,
        events: List[Event] = None,
        id: str = None,
    ):
        if isinstance(children, str):
            children = [children]
        self.children = []
        self.children.extend(children or [])
        self.events = []
        if events:
            if isinstance(events, Event):
                events = [events]
            self.events.extend(events)
        self.id = id or uuid.uuid4().hex

    def render(self, **context):
        body = ""
        for child in self.children:
            if not isinstance(child, str):
                child = child.render(**context)
            body += child
        bootstrap = 'class="btn btn-primary"'
        events = " ".join(map(str, self.events))
        return f"""<button id={self.id} {bootstrap} {events}>{body}</button>"""
