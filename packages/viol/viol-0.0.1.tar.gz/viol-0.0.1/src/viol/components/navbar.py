from __future__ import annotations
from typing import List, Optional
import uuid
from jinja2 import Template
from viol.core import Event, ComponentBase


class NavItem(ComponentBase):
    def __init__(
        self,
        text: str,
        href: str = "#",
        active: bool = False,
        events: List[Event] = None,
        id: str = None,
    ):
        self.text = text
        self.href = href
        self.active = active
        self.events = events or []
        self.id = id or uuid.uuid4().hex

    def render(self, **context):
        active_class = "active" if self.active else ""
        events = " ".join(map(str, self.events))
        return f"""<li class="nav-item">
            <a class="nav-link {active_class}" id="{self.id}" href="{self.href}" {events}>{self.text}</a>
        </li>"""


def nav_items(items: Optional[List[NavItem | dict]]) -> List[NavItem]:
    itemlist = []
    for item in items or []:
        if isinstance(item, str):
            item = NavItem(item)
        elif isinstance(item, dict):
            item = NavItem(**item)
        itemlist.append(item)
    return itemlist


class NavbarBrand(ComponentBase):
    def __init__(self, text: str, href: str = "/", logo: str = None, id: str = None):
        self.text = text
        self.href = href
        self.logo = logo
        self.id = id or uuid.uuid4().hex

    def render(self, **context):
        logo_html = (
            f'<img src="{self.logo}" width="30" height="30" class="d-inline-block align-top me-2" alt="Logo">'
            if self.logo
            else ""
        )
        return f"""<a class="navbar-brand" id="{self.id}" href="{self.href}">
            {logo_html} {self.text}
        </a>"""


class Navbar(ComponentBase):
    def __init__(
        self,
        brand: NavbarBrand | str,
        items: List[NavItem | dict] = None,
        dark: bool = False,
        bg_color: str = "light",
        fixed_top: bool = False,
        id: Optional[str] = None,
        right_aligned_items: List[NavItem] = None,
    ):
        super().__init__()
        if isinstance(brand, str):
            brand = NavbarBrand(brand)
        self.brand = brand
        self.items = nav_items(items)
        self.right_aligned_items = nav_items(right_aligned_items)
        self.dark = dark
        self.bg_color = bg_color
        self.fixed_top = fixed_top
        self.id = id or uuid.uuid4().hex

    def render(self, **context):
        # Determine navbar theme classes
        theme_class = "navbar-dark" if self.dark else "navbar-light"
        bg_class = f"bg-{self.bg_color}"
        position_class = "fixed-top" if self.fixed_top else ""

        # Render left-aligned nav items
        nav_items_html = ""
        for item in self.items:
            nav_items_html += item.render(**context)

        # Render right-aligned nav items if any
        right_items_html = ""
        if self.right_aligned_items:
            right_items_html = f"""
            <ul class="navbar-nav ms-auto">
                {"".join([item.render(**context) for item in self.right_aligned_items])}
            </ul>
            """

        # Main navbar HTML
        return Template(
            """<nav class="navbar {{theme_class}} {{bg_class}} {{position_class}}" id="{{id}}">
    <div class="container-fluid">
        {{ brand | safe }}
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
            data-bs-target="#navbarNav{{id}}" aria-controls="navbarNav{{id}}" 
            aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav{{id}}">
            <ul class="navbar-nav">
                {{nav_items_html | safe }}
            </ul>
            {{right_items_html | safe }}
        </div>
    </div>
</nav>"""
        ).render(
            id=self.id,
            theme_class=theme_class,
            bg_class=bg_class,
            position_class=position_class,
            brand=self.brand.render(**context),
            nav_items_html=nav_items_html,
            right_items_html=right_items_html,
        )
