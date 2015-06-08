(function(){
  angular.module('app')
  .directive('busy', function(){
    return {
      restrict:'E',
      scope:{
        status: '=',
      },
      templateUrl: '/static/apps/templates/busy.html'
    }
  }) 
  .directive('loadMore', loadMore)
  .directive('showRating', function() {
    return {
      restrict: 'E',
      transclude: false, 
      scope: {},
      link: function(scope, element, attrs) {
        scope.range = [1,1,1,1,1];
        scope.$parent.$watch(attrs.model, function(newVal, oldVal){
          scope.value = parseInt(newVal);
        });
      },
      template: "<ul class='rating'><li ng-repeat='n in range track by $index' class='glyphicon glyphicon-star' ng-class='{checked:$index < value}'></li></ul>"
    };
  });

  function loadMore(){
    function ctrl($scope, $rootScope){
        $scope.busy = false;
        $scope.loadMore = function(){
          $scope.busy = true;
          $scope.$emit('loadMore');
        };
        $scope.$on('loaded', function(){
          $scope.busy = false;
        })
    }
    return{
      restrict: 'E',
      scope: {},
      controller: ctrl,
      template: '<a href="#" class="load-more btn btn-info" ng-click="loadMore()">Show More <i ng-hide="busy" class="fa fa-chevron-down"></i><i ng-show="busy" class="fa fa-refresh fa-spin"></i></a>'
    };
  }

})();

