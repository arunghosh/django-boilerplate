var Angular = (function(mm){

  mm.createApp = function(name, params){
    params = params || [];
    params = params.concat(['ui.router', 'ngCookies']);
    var app = angular.module(name, params)
    .run(run)
    .config(config);

    run.$inject = ['$http'];
    function run($http) {
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
    }

    config.$inject = ['$locationProvider'];
    function config($locationProvider){
      //$locationProvider.html5Mode(true);
      //$locationProvider.hashPrefix('!');
      $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
      });
    }

    return app;
  }

  return mm;
  
})(Angular || {});
