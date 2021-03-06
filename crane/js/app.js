(function(){

angular.module('crane', ['ngRoute','ui.bootstrap'])

.config(separatorConfig)
.config(router);

function separatorConfig($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}

function router($routeProvider){
  $routeProvider
  .when("/hosts",
    {
      templateUrl: "/frontend/hosts.jade",
      controller: "HostController"
    })
  .when("/containers",
    {
      templateUrl: "/frontend/containers.jade",
      controller: "ContainerController"
    })
  .when("/templates",
    {
      templateUrl: "/frontend/templates.jade",
      controller: "TemplatesControl"
    })
  .when("/environments",
    {
      templateUrl: "/frontend/environments.jade",
      controller: "EnvironmentsController"
    })
  .when("/registry",
    {
      templateUrl: "/frontend/registry.jade",
      controller: "RegistryControl"
    })
  .when("/repository/:registry_id/:reponame",
    {
      templateUrl: "/frontend/repository.jade",
      controller: "RepositoryControl"
    })
  .when("/index",
    {
      templateUrl: "/frontend/index.jade",
      controller: "IndexController"
    })
  .otherwise({ redirectTo: '/index' });
}

})();
