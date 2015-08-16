var Angular = (function(mm){

  mm.createApp = function(name, params){
    params = params || [];
    params = params.concat(['ui.router', 'toastr', 'ngAnimate', 'ngCookies', 'ngResource']);
    var app = angular.module(name, params)
    .run(run)
    .config(config);

    run.$inject = ['$http'];
    function run($http) {
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
      $http.defaults.headers.patch = {
        'Content-Type': 'application/json;charset=utf-8'
      }
    }

    config.$inject = ['$locationProvider', '$resourceProvider'];
    function config($locationProvider, $resourceProvider){
      $resourceProvider.defaults.stripTrailingSlashes = false; 
      // $locationProvider.html5Mode(true);
      // $locationProvider.hashPrefix('!');
    }

    return app;
  }

  return mm;

})(Angular || {});
