//angular.module('InvaanaScoutApp', [], function($interpolateProvider) {
//            $interpolateProvider.startSymbol('[{');
//            $interpolateProvider.endSymbol('}]');
//});


angular.module('InvaanaScoutApp', [])
  .controller('baseController', function($scope, $http) {

    console.log("Hello World! ");


    $scope.submitQuery = function(){
        console.log("im about to make a query");

        $http.get('http://localhost:5000/apis/browse/', {
            params:  {q: $scope.q},
         })
        .then(function(response) {
            console.log(response)
            $scope.results_data = response.data;
            // Request completed successfully
        }, function(x) {
            // Request error
        });
    };



  });