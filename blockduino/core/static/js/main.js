var blockduino = angular.module('blockduino',[])

blockduino.directive('displayTable', function() {
	return {
		restrict: 'EA',
		templateUrl: '/directives/display_table/',
		scope: {
			showTable: '=',
			selected: '=',
			options: '='
		},
		link: function(scope, elem, attrs) {
			scope_display = scope;
			scope.selectOption = function(option) {
				scope.selected = option;
				scope.showTable = false;
			}

		}
	}
})

blockduino.directive('when', function($filter) {
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
			scope.limitFilter = $filter('limitTo');
			scope.parsedWhenId = parseInt(scope.whenId)
			scope.dosRecieved = 0
			scope.compiledList = []
			scope.compiledDict = {}
			scope.showTable = false;
			scope.selectedAction = '';
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
						console.log('here')
						scope.$emit('$doneWhenCompiling', scope.parsedDoId, scope.compiledList, scope.compiledDict)
					}
					else {
						console.log('her????')
						scope.$emit('$doneHeadCompiling', scope.parsedDoId, scope.compiledList, scope.compiledDict)}
				}
				
			})

			scope.$on('$compileToDict', function() {
				if (scope.selectedModule && scope.selectedAction)
					scope.compiledList = [scope.selectedModule.name, scope.selectedAction]
				else
					scope.compiledList = ["1"]
			})
			scope.displayTable = function() {
				scope.showTable = true;
			}
			scope.clear = function() {
				scope.selectedModule = undefined;
				scope.selectedAction = undefined;
			}
		}
	}
})

blockduino.directive('do', function($compile, $filter) {
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
			var default_do_html = "Do: <span class='do_module_abbrev' ng-show='selectedModule'>{{selectedModule.name}}</span><span><button ng-show='!selectedModule' ng-click='selectModule()'class='btn-primary btn'>  +  </button></span><span> <button ng-show='selectedModule && !selectedAction' ng-click='displayTable()' class='btn-primary btn'> + </button> <button ng-show='selectedModule && selectedAction' ng-click='displayTable()' class='btn-primary btn'> {{selectedAction}}</button> <button ng-show='selectedModule && selectedAction && selectedModule[selectedAction] && !actionAfterAction' ng-click='displayTable(\"actionAfter\")' class='btn-primary btn'> + </button> <button ng-show='actionAfterAction' ng-click='displayTable(\"actionAfter\")' class='btn-primary btn'> {{actionAfterAction}}</button><button ng-click='goDeeper()' class='btn-primary btn'>deeper</button></span><button ng-show='selectedModule' class='btn-danger btn' ng-click='clear()'>-</button><display-table ng-hide='selectedAction && getActionAfterOptions' show-table='showTable' selected='selectedAction' options='getOptions()'></display-table><display-table ng-show='selectedAction && getActionAfterOptions' show-table='showTable' selected='actionAfterAction' options='getOptions()'></display-table>"
			scope_do = scope;
			scope.showTable = false;
			scope.selectedAction = '';
			scope.actionAfterAction = '';
			scope.limitFilter = $filter('limitTo');
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

			var clearHtml = function() {
				elem.empty()
				elem.append(default_do_html)
				$compile(elem.contents())(scope);
			}
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
				if (scope.selectedModule && scope.selectedAction)
					if (scope.actionAfterAction)
						scope.compiledDict['M'] = [scope.selectedModule.name, scope.selectedAction, scope.actionAfterAction]
					else scope.compiledDict['M'] = [scope.selectedModule.name, scope.selectedAction]
				else scope.compiledDict['M'] = ['None']
				if (!scope.whenCount) {
					scope.$emit('$doneDoCompiling', scope.parsedWhenId, scope.compiledDict)
				}
			});

			scope.displayTable = function(action_after) {
				if (action_after) scope.getActionAfterOptions = true;
				else scope.getActionAfterOptions = false;
				scope.showTable = true;
			}

			scope.getOptions = function() {
				if (scope.getActionAfterOptions) {
					if (scope.selectedModule)
						return scope.selectedModule[scope.selectedAction]
					else return undefined
				}
				else if (scope.selectedModule) {
					return scope.selectedModule.attribs
				}
				else return undefined
			}

			scope.clear = function() {
				scope.selectedModule = undefined;
				scope.selectedAction = undefined;
				scope.actionAfterAction = '';
				scope.getActionAfterOptions = true;
				scope.whenCount = 0;
				clearHtml();
			}
			scope.moduleActionAttribs = function() {
				if (scope.selectedModule)
					return scope.selectedModule[scope.selectedAction]
				return false;
			}
			scope.$watch('selectedAction', function(newVal) {
				if (newVal) scope.actionAfterAction = '';
			})
		}
	}
})


blockduino.controller('HomeController', ['$scope', '$http', '$interval', function($scope, $http, $interval) {
	scope_ctrl = $scope;
	POLL_DELAY_SECONDS = 500;
	$scope.modules = []
	$scope.whenDoId = 1
	$scope.whenDos = [1]
	$scope.whenIdCount = 0
	$scope.doIdCount = 0
	$scope.headCount = 1;
	$scope.headsRecieved = 0;
	$scope.compiledDict = {}
	$scope.initList = [];
	$scope.setupList = [];
	$scope.numLEDS = 0
	$scope.numServos = 0
	$scope.numAccel = 0
	$scope.numPushButton = 0

	var initListMap = {
		'servo': 'B_Servo',
		'led': 'B_LED',
		'push_button': 'B_PushButton',
		'accel': 'B_Accel',
		'led_g': 'B_LEDGroup'
	}
	var led_attribs = ['turn_on', 'turn_off']

	var pollForNewBlocks = function() {
		$http.get('/poll_new/').success(function(result) {
			if (result.length) {
				for (i=0; i<result.length; i++) {
					if (result[i].name == 'led') {

						$scope.numLEDS++;

						result[i].name = 'led' + $scope.numLEDS.toString()
						$scope.initList.push([initListMap['led'], result[i].name])
						$scope.setupList.push([result[i].name, "init", result[i].power.toString()])
					}
					if (result[i].name == 'servo') {

						$scope.numServos++;

						result[i].name = 'servo' + $scope.numServos.toString()
						$scope.initList.push([initListMap['servo'], result[i].name])
						$scope.setupList.push([result[i].name, "init", result[i].data_pin.toString()])
					}
					if (result[i].name == 'push_button') {

						$scope.numPushButton++;

						result[i].name = 'push_button' + $scope.numPushButton.toString()
						$scope.initList.push([initListMap['push_button'], result[i].name])
						$scope.setupList.push([result[i].name, "init", result[i].power.toString()])
					}
					if (result[i].name == 'accel') {

						$scope.numAccel++;

						result[i].name = 'accel' + $scope.numAccel.toString()
						$scope.initList.push([initListMap['accel'], result[i].name])
						$scope.setupList.push([result[i].name, "init", result[i].data_pin.toString()])

					}
					$scope.modules.push(result[i]);
				}
					
			}
		})
	}

	$scope.$on('$displayDoingModules', function(event, doId) {
		console.log('displayDoingModules', doId)
		$scope.currentDoId = doId;
		$scope.displayDoingModules = true;
		$scope.displaySensingModules = false;
	})
	$scope.$on('$displaySensingModules', function(event,whenId) {
		console.log('displaySensingModules', whenId)
		$scope.currentWhenId = whenId;
		$scope.displaySensingModules = true;
		$scope.displayDoingModules = false;

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
			console.log('head DONE')
			$scope.headsRecieved = $scope.headsRecieved + 1
			var tempDict = {}
			var keyNameWhen = 'W' + $scope.headsRecieved.toString()
			var keyNameDo = 'D' + $scope.headsRecieved.toString()
			tempDict[keyNameWhen] =  list
			tempDict[keyNameDo] =  dict
			$scope.compiledDict = _.extend($scope.compiledDict, tempDict)
			if ($scope.headsRecieved == $scope.headCount) {
				console.log('$doneCompiling', $scope.compiledDict)
				$scope.finalDict = {'setup_list': $scope.setupList, 'init_list': $scope.initList, 'whendo_dict':$scope.compiledDict}
				$http.post('/compile/', $scope.finalDict).success(function() {
					console.log('successful post')
				})
			}
				
		
		
	})

	$scope.addWhenDo = function() {
		$scope.whenDoId++;
		$scope.whenDos.push($scope.whenDoId)
	}
	$scope.deleteWhenDo = function(index) {
		$scope.whenDos.splice(index, 1)
	}

	$scope.$watch('numLEDS',function(newVal) {
		if (newVal == 3) {
			var led_g_dict = {name: 'led_g', attribs:['get_next', 'get_current'], get_next: led_attribs, get_current: led_attribs, sense:false}
			$scope.modules.push(led_g_dict)
			$scope.initList.push([initListMap['led_g'],led_g_dict.name, 'LED1', 'LED2','LED3'])

		}
	})

	$interval(pollForNewBlocks, POLL_DELAY_SECONDS)
}])

