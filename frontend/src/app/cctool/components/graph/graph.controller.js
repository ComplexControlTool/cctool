// graph.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.graph')
    .controller('GraphController', GraphController);

  /** @ngInject */
  function GraphController(Graph, $log, $scope, $mdToast, $state, graphService)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'GraphController';
    vm.content = Graph ? Graph : undefined;
    vm.tabs = ['Overview'];
    vm.tabs_view = ['graph-overview'];
    vm.network = undefined;

    // Functions
    activate();

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });
    $scope.$on('graph:hasUpdates', function(event,data) {
      showCustomToast()
    });

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');

      if (_.isEmpty(vm.content))
      {
        $log.debug(vm.title+'/ Empty graph object: '+JSON.stringify(vm.content));
      }
      else
      {
        $log.debug(vm.title+'/ Graph object initialised: '+JSON.stringify(vm.content));
        var analyses_tabs = [];
        for (var i in vm.content.analysers)
        {
          var analyser = vm.content.analysers[i]
          vm.tabs.push(analyser);
          vm.tabs_view.push('graph-'+analyser.toLowerCase()+'-analysis');
        }
      }

      if ($state.is('app.cctool_graph'))
      {
        $log.debug(vm.title+'/ Init graph monitor');
        graphService.initMonitorUpdates(vm.content,10000);
      }
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
      $log.debug(vm.title+'/ Cleanup graph monitor');
      graphService.stopMonitorUpdates();
    }

    function showCustomToast()
    {
      $log.debug(vm.title+'/ showCustomToast');
      graphService.stopMonitorUpdates();
      $mdToast.show({
        hideDelay: false,
        position: $scope.appCtrl.toastPosition,
        scope: $scope,
        preserveScope: true,
        controller: 'GraphToastController',
        controllerAs: 'graphToastCtrl',
        templateUrl: 'app/cctool/components/graph/graph.toast.html'
      })
    }

  }
})();
