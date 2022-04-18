from flask import Flask

from app.views import goodreads

app = Flask(__name__)

app.register_blueprint(goodreads.bp)
