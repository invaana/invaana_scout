angular.module('InvaanaScoutApp', [])
  .controller('baseController', function($scope, $http) {

    $scope.submitQuery = function(){
        $scope.results_data = null;
        $scope.is_searching = true;
        console.log("im about to make a query");

        $http.get('http://localhost:5000/apis/browse/', {
            params:  {q: $scope.q},
         })
        .then(function(response) {
            console.log(response)
            $scope.is_searching = false;
            $scope.results_data = response.data;
            // Request completed successfully
        }, function(x) {
            $scope.is_searching = false;
            // Request error
        });
    };


    $scope.addNewQuery = function(kw){
        console.log("sending new query keyword");
        $scope.q = kw;
        $scope.submitQuery();
    }



  });