from webserver import app
from flask import jsonify, request
from crane.Backend.Registry import Registry
from crane.Backend.RegistryProviderFactory import RegistryProviderFactory

registries = Registry(RegistryProviderFactory())


@app.route("/registry", methods=["GET"])
def get_registries():
    return jsonify(result=registries.get_registries())


@app.route("/registry", methods=["POST"])
def add_registry():
    try:
        registries.add_registry(request.get_json())
        return ""
    except:
        return "Failed to add registry to database!", 500

@app.route("/registry/<id>", methods=["POST"])
def update_registry(id):
    try:
        registries.update_registry(id, request.get_json())
        return ""
    except:
        return "Failed to update registry in database!", 500

@app.route("/registry/<registry_id>", methods=["DELETE"])
def delete_registry(registry_id):
    try:
        registries.delete_registry(registry_id)
        return ""
    except:
        return "Failed to delete registry from database!", 500

@app.route("/registry/<registry_id>/repository/<namespace>/<repo_name>/tags")
@app.route("/registry/<registry_id>/repository/<repo_name>/tags", defaults={'namespace': ''})
def get_tags(registry_id, namespace, repo_name):
    return jsonify(result=registries.get_tags(registry_id, namespace, repo_name))


@app.route("/registry/<registry_id>/repository/<namespace>/<repo_name>/image/<image_id>")
@app.route("/registry/<registry_id>/repository/<repo_name>/image/<image_id>", defaults={'namespace': ''})
def get_image(registry_id, namespace, repo_name, image_id):
    return jsonify(result=registries.get_image(registry_id, namespace, repo_name, image_id))


@app.route("/search", methods=["GET"])
def search_registry():
    return jsonify(result=registries.search_registry(request.args.get("q")))
