(function(){

  angular.module('app')
  .config(configRoute);
  
  configRoute.$inject = ['$stateProvider', '$urlRouterProvider'];

  function configRoute($stateProvider, $urlRouterProvider){
    //$urlRouterProvider.otherwise("home");
    
    $stateProvider
    .state('home', {
      url: '/',
      templateUrl: templateUrl('index.html'),
    })
    .state('register', {
      url: '/register',
      controller: 'RegisterCtrl',
      controllerAs: 'vm',
      templateUrl: templateUrl('auth/register.html'),
    })
    .state('login', {
      url: '/login',
      controller: 'LoginCtrl',
      controllerAs: 'vm',
      templateUrl: templateUrl('auth/login.html'),
    })

    function templateUrl(url){
      return '/static/apps/' + url;
    }

  };


})();
