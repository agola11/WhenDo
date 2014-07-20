var blockduino = angular.module('blockduino',[])

blockduino.directive('when', function() {
	return {
		restrict: 'EA',
		templateUrl: '/directives/when/',
		scope: {
			whenId: '@',
			doIdCount: '=',
			whenIdCount: '=',
			parsedDoId: '=?',
			head: '=?'
		},
		link: function(scope, elem, attrs) {
			scope_when = scope;
			scope.parsedWhenId = parseInt(scope.whenId)
			scope.dosRecieved = 0
			scope.compiledList = []
			scope.compiledDict = {}
			scope.selectModule = function() {
				scope.$emit('$displaySensingModules', scope.parsedWhenId)
			}
			scope.$on('$selectedSenseModule', function(event, module, id) {
				console.log('$selectedSenseModule', module, id)
				if (id == scope.parsedWhenId) {
					scope.selectedModule = module;
				}
			})

			scope.$on('$doneDoCompiling', function(event, parsedWhenId, dict) {
				console.log('done in when', parsedWhenId, scope.parsedWhenId)
				if (parsedWhenId == scope.parsedWhenId) {
					scope.dosRecieved = scope.dosRecieved + 1;
					scope.compiledDict = _.extend(scope.compiledDict, dict)
					if (!scope.head) {
						scope.$emit('$doneWhenCompiling', scope.parsedDoId, scope.compiledList, scope.compiledDict)
					}
					else (scope.$emit('$doneHeadCompiling', scope.parsedDoId, scope.compiledList, scope.compiledDict))
				}
				
			})

			scope.$on('$compileToDict', function() {
				scope.compiledList = [scope.selectedModule.name, scope.selectedAction]
			})
		}
	}
})

blockduino.directive('do', function($compile) {
	return {
		restrict: 'EA',
		templateUrl: '/directives/do/',
		scope: {
			parsedWhenId:'=',
			whenIdCount:'=',
			doIdCount: '=',
			doId: '@'
		},
		link: function(scope, elem, attrs) {
			scope_do = scope;
			scope.whenCount = 0;
			scope.whensRecieved = 0;
			scope.elem = elem;
			scope.compiledDict = {}
			console.log("here",scope.doId, scope.doIdCount)
			scope.parsedDoId = parseInt(scope.doId)
			scope.selectModule = function() {
				scope.$emit('$displayDoingModules', scope.parsedDoId)
			}
			scope.$on('$selectedDoModule', function(event, module, id) {
				console.log('$selectedDoModule', module, id)
				if (id == scope.parsedDoId) {
					scope.selectedModule = module;
				}
			})

			var addHtml = function() {
				elem.append("<div when ng-show='showWhen' when-id='{{whenIdCount}}' when-id-count='whenIdCount' do-id-count='doIdCount' parsed-do-id='parsedDoId'></div>")
        		$compile(elem.contents())(scope);
			}

			scope.goDeeper = function() {
				scope.whenIdCount = scope.whenIdCount + 1;
				scope.doIdCount = scope.doIdCount + 1;
				scope.showWhen = true;
				addHtml();
				scope.whenCount = scope.whenCount + 1;
			}


			scope.$on('$doneWhenCompiling', function(event, parsedDoId, list, dict) {
				if (parsedDoId == scope.parsedDoId) {

					scope.whensRecieved = scope.whensRecieved + 1		

					var tempDict = {}
					var keyNameWhen = 'W' + scope.whensRecieved.toString()
					var keyNameDo = 'D' + scope.whensRecieved.toString()
					tempDict[keyNameWhen] =  list
					tempDict[keyNameDo] =  dict

					scope.compiledDict = _.extend(scope.compiledDict, tempDict)
					if (scope.whensRecieved == scope.whenCount)
						scope.$emit('$doneDoCompiling', scope.parsedWhenId, scope.compiledDict)
				}
				
			})

			scope.$on('$compileToDict', function() {
				scope.compiledDict['main'] = [scope.selectedModule.name, scope.selectedAction]
				if (!scope.whenCount) {
					console.log('here here?')
					scope.$emit('$doneDoCompiling', scope.parsedWhenId, scope.compiledDict)
				}
			});
		}
	}
})


blockduino.controller('HomeController', ['$scope', '$http', '$interval', function($scope, $http, $interval) {
	scope_ctrl = $scope;
	POLL_DELAY_SECONDS = 500;
	$scope.modules = []
	$scope.whenIdCount = 0
	$scope.doIdCount = 0
	$scope.headCount = 1;
	$scope.headsRecieved = 0;
	$scope.compiledDict = {}
	var pollForNewBlocks = function() {
		$http.get('/api/poll/').success(function(result) {
			if (result.length) {
				for (i=0; i<result.length; i++)
					$scope.modules.push(result[i]);
			}
		})
	}

	$scope.$on('$displayDoingModules', function(event, doId) {
		console.log('displayDoingModules', doId)
		$scope.currentDoId = doId;
		$scope.displaySensingModules = true;
	})
	$scope.$on('$displaySensingModules', function(event,whenId) {
		console.log('displaySensingModules', whenId)
		$scope.currentWhenId = whenId;
		$scope.displayDoingModules = true;

	})
	$scope.selectedDoModule = function(module) {
		console.log('$selectedDoModule', module, $scope.currentDoId)
		$scope.$broadcast('$selectedDoModule', module, $scope.currentDoId)
	}

	$scope.selectedSenseModule = function(module) {
		console.log('$selectedSenseModule', module, $scope.currentWhenId)
		$scope.$broadcast('$selectedSenseModule', module, $scope.currentWhenId)
	}

	$scope.done = function(){
		$scope.$broadcast('$compileToDict')
	}

	$scope.$on('$doneHeadCompiling', function(event, parsedDoId, list, dict) {
		

			$scope.headsRecieved = $scope.headsRecieved + 1
			var tempDict = {}
			var keyNameWhen = 'W' + $scope.headsRecieved.toString()
			var keyNameDo = 'D' + $scope.headsRecieved.toString()
			tempDict[keyNameWhen] =  list
			tempDict[keyNameDo] =  dict
			$scope.compiledDict = _.extend($scope.compiledDict, tempDict)
			if ($scope.headsRecieved == $scope.headCount)
				console.log('$doneCompiling', $scope.compiledDict)
		
		
	})

	$interval(pollForNewBlocks, POLL_DELAY_SECONDS)
}])

