import requests
from bs4 import BeautifulSoup
from flask import Blueprint, Response, request, render_template

bp = Blueprint("goodreads", __name__)

BASE_URL = "https://goodreads.com"


@bp.route("/")
def index():
    width = request.args.get("width", "600", str)
    height = request.args.get("height", "500", str)
    updates = request.args.get("updates", "3", str)

    widget_response = requests.get(f"{BASE_URL}/widgets/user_update_widget", {
        "height": height,
        "width": width,
        "num_updates": updates,
        "user": 149423144
    })

    soup = BeautifulSoup(widget_response.content, "html.parser")
    content = soup.find("div", {"class": "goodreads_container", "id": "gr_reviews_widget"})

    for link in content.findAll('a'):
        link["href"] = f"{BASE_URL}{link['href']}"

    content_raw = ""
    for child in content.children:
        content_raw += str(child)

    svg = render_template("goodreads.html.jinja2", **{
        "height": height,
        "width": width,
        "content": content_raw,
    })

    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp
