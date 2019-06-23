# -*- coding: utf-8 -*-

from flask import get_flashed_messages
from markupsafe import Markup

from kido import app


def render_flashed_messages():
    messages = get_flashed_messages(with_categories=True)
    if not messages:
        return []

    html = []
    for category, message in messages:
        if category == "error":
            category = "warning"
        elif category == "message":
            category = "info"
        html.append(
            Markup('<div class="text-{category}">{message}</div>').format(
                category=category, message=message
            )
        )
    return html


app.jinja_env.globals.update(render_flashed_messages=render_flashed_messages)
