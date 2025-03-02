from __future__ import annotations
from flask import Flask
from pathlib import Path

__all__ = [
    "Server",
]


class Server(Flask):
    def __init__(self, *args, **kwargs):
        kwargs["static_folder"] = Path(__file__).parent / "static"
        kwargs["template_folder"] = Path(__file__).parent / "templates"
        super(Server, self).__init__(*args, **kwargs)
