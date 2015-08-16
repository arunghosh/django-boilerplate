(function(){
  angular.module('app')
  .controller('AllProjectsCtrl', AllProjectsCtrl);

  AllProjectsCtrl.$inject = ['$scope', '$stateParams', '$state', 'Projects', 'commonSrv', 'toastr'];

  function AllProjectsCtrl($scope, $stateParams, $state, Projects, commonSrv, toastr){
    var vm = this;

    vm.projects = Projects.query(angular.noop, commonSrv.handleError);

  }
})();

