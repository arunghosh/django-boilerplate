(function(){
  angular.module('app', ['ui.router', 'ngCookies'])
  .run(run)
  .config(config);

  run.$inject = ['$http'];
  function run($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }

  config.$inject = ['$locationProvider'];
  function config($locationProvider){
    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
  }

})()
