from crane.webserver import db
from crane.Backend.Models.RegistryModel import RegistryModel

class Registry:
    def __init__(self, providerfactory):
        self.providerfactory = providerfactory

    def get_registries(self):
        registries = db.session.execute(RegistryModel.__table__ .select())
        transformed_registries = map(lambda x: dict(x), registries)
        return transformed_registries

    def get_registry_by_id(self, registry_id):
        return RegistryModel.query.filter_by(id=registry_id).first()

    def add_registry(self, data):
        registry = RegistryModel(
            data['name'],
            data['url'],
            data.get('username', ""),
            data.get('password', ""),
            data['provider'])
        db.session.add(registry)
        db.session.commit()
        return registry.id

    def update_registry(self, registry_id, data):
        registry = self.get_registry_by_id(registry_id)
        registry.name = data['name']
        registry.url = data['url']
        registry.username = data['username']
        registry.password = data['password'] if 'password' in data else ""
        registry.provider = data['provider']
        db.session.add(registry)
        db.session.commit()

    def delete_registry(self, registry_id):
        registry = self.get_registry_by_id(registry_id)
        if registry:
            db.session.delete(registry)
            db.session.commit()

    def get_tags(self, registry_id, namespace, repo_name):
        if namespace != "":
            repo_name = "{0}/{1}".format(namespace, repo_name)
        registry = self.get_registry_by_id(registry_id)
        provider = self._get_provider(registry)
        result = provider.tags(repo_name)
        return result

    def get_image(self, registry_id, namespace, repo_name, image_id):
        if namespace != "":
            repo_name = "{0}/{1}".format(namespace, repo_name)
        registry = self.get_registry_by_id(registry_id)
        provider = self._get_provider(registry)
        result = provider.image(repo_name, image_id)
        return result

    def search_registry(self, query):
        registries = RegistryModel.query.all()
        results = []
        for registry in registries:
            provider = self._get_provider(registry)
            results = results + self._expand_results_with_registry_name(provider.search(query), registry)
        return results

    def _expand_results_with_registry_name(self, results, registry):
        for result in results:
            result['registry'] = registry.name
            result['registry_id'] = registry.id
        return results

    def _get_provider(self, registry):
        return self.providerfactory.create_provider(registry)
