// graph.toast.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.graph')
    .controller('GraphToastController', GraphToastController);

  /** @ngInject */
  function GraphToastController($log, $scope, $mdToast, graphService)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'GraphToastController';

    // Functions
    activate();
    vm.dismissAction = dismissAction;
    vm.loadAction = loadAction;

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
    }

    function dismissAction()
    {
      $log.debug(vm.title+'/ dismissAction');
      $mdToast.hide().then(function()
      {
        $log.debug(vm.title+'/ dismissAction: Hiding toast and executing service function');
        graphService.ignoreUpdate();
        graphService.initMonitorUpdates($scope.graphCtrl.content, 10000);
        delete $scope.graphCtrl.graphToastCtrl;
      });
    }

    function loadAction()
    {
      $log.debug(vm.title+'/ loadAction');
      $mdToast.hide().then(function()
      {
        $log.debug(vm.title+'/ loadAction: Hiding toast and executing service function');
        $scope.graphCtrl.content = graphService.getLatestUpdate();
        graphService.initMonitorUpdates($scope.graphCtrl.content, 10000);
        delete $scope.graphCtrl.graphToastCtrl;
      });
    }

  }
})();
