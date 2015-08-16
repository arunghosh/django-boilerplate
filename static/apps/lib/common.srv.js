(function(){
  angular.module('app')
  .factory('commonSrv', commonSrv);

  commonSrv.$inject = ['$http', '$q', 'toastr', '$resource'];

  function commonSrv($http, $q, toastr, $resource){
    return{
      getResponseData: getResponseData,
      handleError: handleError,
      createResorceSrv: createResorceSrv,
    }

    function createResorceSrv(url){
      var Srv = $resource(url + ':id/', {
        id:'@id',
      },{
        update: {method:'PUT'},
      });
      return Srv
    }

    function handleError(error){
      console.log(error);
      toastr.error('Failed!!! ' + error.statusText);
    }

    function getResponseData(request){
      var deffered = $q.defer();
      request.then(function(response){
        deffered.resolve(response.data);
      }).catch(function(){
        // TODO
      });
      return deffered.promise;
    }
  }
})();

