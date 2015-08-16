(function(){
  angular.module('app')
  .factory('Projects', Projects);

  Projects.$inject = ['$http', '$resource', 'commonSrv'];
  console.log('123');
  function Projects($http, $resource, commonSrv){
    var URL = '/api/projects/'
    var Project = $resource(URL + ':id/:sub/', {
      id:'@id',
    },{
    });
    return Project;
  }
})();
