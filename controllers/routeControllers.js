var controllerApp = angular.module('descant.controllers.routing', ['descant.config']);

app.controller('PostViewController', function($scope, $routeParams) {
	$scope.topicId = $routeParams.topicId;
});

app.controller('UserViewController', function($scope, $location, $routeParams) {
	if ($routeParams.userId != -1) {
		$scope.userId = $routeParams.userId;
	}
	else {
		$location.path('/users');
	}
});


app.controller('TagTopicViewController', function($scope, $routeParams) {
	$scope.tagId = $routeParams.tagId;
});

app.controller('ActivateController', function($http, descantConfig, $location, $routeParams) {
	var req = $http.post(descantConfig.backend + "/api/auth/activate/", {"uid": $routeParams.uid, "token": $routeParams.token});
	req.success(function(data) {
		$location.path('/login');
	});
	req.error(function(data) {
		alert("Error while activating account!");
	});
});