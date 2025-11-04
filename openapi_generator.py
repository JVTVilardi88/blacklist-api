# openapi_generator.py
from flask import Flask, jsonify, Blueprint, send_from_directory
from werkzeug.routing import Rule
import os

def generate_openapi_spec(app: Flask):
    """
    Genera un diccionario con la especificación OpenAPI basada en las rutas registradas en Flask.
    """
    paths = {}

    for rule in app.url_map.iter_rules():
        if rule.endpoint == "static":
            continue

        methods = list(rule.methods - {"HEAD", "OPTIONS"})
        path_item = {}
        for method in methods:
            path_item[method.lower()] = {
                "summary": f"Endpoint {rule.endpoint}",
                "parameters": [],
                "responses": {
                    "200": {"description": "OK"}
                }
            }
        paths[str(rule)] = path_item

    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "Blacklist API",
            "version": "1.0.0",
            "description": "Documentación OpenAPI generada automáticamente."
        },
        "servers": [{"url": "http://localhost:5000"}],
        "paths": paths
    }

    return spec


def register_openapi_endpoint(app: Flask):
    """
    Agrega un endpoint /openapi.json que devuelve el esquema OpenAPI dinámico.
    """
    @app.route("/openapi.json")
    def openapi_json():
        return jsonify(generate_openapi_spec(app))


def register_static_openapi_route(app: Flask, docs_dir: str = "docs"):
    """
    Permite servir el archivo estático /docs/openapi.json una vez generado.
    """
    @app.route("/docs/<path:filename>")
    def serve_docs(filename):
        return send_from_directory(docs_dir, filename)
