angular.module('crane')

.service('commons',['$modal', function($modal){
    this.showError = function(reason){
        var modalInstance = $modal.open({
            templateUrl: '/frontend/error.jade',
            controller: function($scope, $modalInstance) {
                $scope.reason = reason.data;

                $scope.close = function () {
                    $modalInstance.dismiss('close');
                };
            }
        });
    };
}]);
