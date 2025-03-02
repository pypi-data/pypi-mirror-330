from __future__ import annotations
from flask import request
from pathlib import Path
import uuid

from viol import Server
from viol.core import ComponentList, Event
from viol.components.button import Button
from viol.components.navbar import Navbar

app = Server(__name__)

navbar = Navbar(
    "Apple",
    items=[
        {"text": "Home", "href": "/home"},
        {"text": "About", "href": "/about"},
        {"text": "Contact", "href": "/contact"},
    ],
)


@app.route("/clicked", methods=["POST", "GET"])
def clicked():
    uid = uuid.uuid4().hex
    return f"<h1>{uid}</h1>"


@app.route("/change-color-result2", methods=["POST", "GET"])
def change_color_result2():
    data = request.form["color"]
    if data == "red":
        return "<h1 style='color:red'>Color Changed</h1>"
    elif data == "green":
        return "<h1 style='color:green'>Color Changed</h1>"
    elif data == "blue":
        return "<h1 style='color:blue'>Color Changed</h1>"
    return "<h1>Color Changed</h1>"


@app.route("/")
def home():
    body = [
        navbar,
        "<h1>Home</h1>",
        "<p>Welcome to the home page</p>",
        Button(
            "Click me",
            events=[
                Event(
                    method="post",
                    rule="/clicked",
                    swap="innerHTML",
                    trigger="click",
                    target="#result",
                )
            ],
        ),
        "<div id='result'></div>",
        # selecto colors with options
        "<form>",
        "<select name='color'>",
        "<option value='red'>Red</option>",
        "<option value='green'>Green</option>",
        "<option value='blue'>Blue</option>",
        "</select>",
        "</form>",
        Button("Do the Thing", id="theButton"),
        Event(
            method="get",
            rule="/clicked",
            swap="innerHTML",
            trigger="click from:#theButton",
            target="#result2",
        ),
        Event(
            method="post",
            rule="/change-color-result2",
            swap="innerHTML",
            trigger="mouseover from:#theButton",
            target="#result2",
            include="[name='color']",
        ),
        "<div id='result2'></div>",
    ]
    # read the template from flask
    index = ComponentList.from_template(Path(app.template_folder) / "index.html")
    body = ComponentList(body).render()
    return index.render(title="Hello World!", body=body)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
