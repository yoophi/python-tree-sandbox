from flask import Flask, jsonify, url_for, redirect
from sqlalchemy import func

from tree_app.config import Config
from tree_app.database import db
from tree_app.extensions import ma
from tree_app.models import Node
from tree_app.schema import NodeSchema


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)

    @app.route('/')
    def index():
        root = db.session.query(Node).filter(func.nlevel(Node.path) == 1).first()
        return redirect(url_for('node_detail', id=root.id))

    @app.route('/<id>')
    def node_detail(id):
        node = db.session.query(Node).filter_by(id=id).first()
        return jsonify(NodeSchema().dump(node))

    return app
