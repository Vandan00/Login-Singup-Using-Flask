from app import app
from flask import render_template, request

@app.errorhandler(404)
def not_found(e):
    app.logger.error(f'Page not Found {e}, route: {request.url}')

    return render_template("404.html")
