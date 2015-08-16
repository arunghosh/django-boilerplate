(function(){

  angular.module('app')
  .config(config);

  config.$inject = ['$stateProvider', '$urlRouterProvider'];

  function config($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/projects/");
    $stateProvider
    .state('projects', {
      url: '/projects/',
      data: {title: 'Project'},
      views:{
        'nav':{
          template: '<div>Projects</div>',
          controller: 'NavProjectsCtrl',
          controllerAs: 'navprj'
        },
        'main':{
          templateUrl: '/static/apps/projects/html/all.projects.html',
          controller: 'AllProjectsCtrl',
          controllerAs: 'allprj'
        }
      }
    })
  }

})();
