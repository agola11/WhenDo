var blockduino = angular.module('blockduino',[])

blockduino.controller('HomeController', ['$scope', '$http', '$interval', function($scope, $http, $interval) {
	scope_ctrl = $scope;
	POLL_DELAY_SECONDS = 500;
	$scope.modules = []
	var pollForNewBlocks = function() {
		$http.get('/api/poll/').success(function(result) {
			if (result.length) {
				$scope.modules.push(result);
			}
		})
	}

	$interval(pollForNewBlocks, POLL_DELAY_SECONDS)
}])
