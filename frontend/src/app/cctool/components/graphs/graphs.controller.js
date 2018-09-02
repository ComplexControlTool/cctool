// graphs.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.graphs')
    .controller('GraphsController', GraphsController);

  /** @ngInject */
  function GraphsController($log, $scope, $state, graphsService)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'GraphsController';
    vm.goToGraph = goToGraph;

    // Functions
    activate();

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });
    $scope.$on('graphs:hasUpdates', function(event,data) {
      $log.debug(vm.title+'/ Updating graphs...');
      loadUpdates(data);
    });

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
      if ($state.is('app.cctool_graphs'))
      {
        $log.debug(vm.title+'/ Init graphs monitor');
        graphsService.initMonitorUpdates($scope.graphManagerCtrl.content, ['showDetails','graphgephicsv','graphgephijson'], 150000);
      }
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
      $log.debug(vm.title+'/ Cleanup graphs monitor');
      graphsService.stopMonitorUpdates();
    }

    function loadUpdates(data)
    {
      $log.debug(vm.title+'/ loadUpdates');
      for (var i in $scope.graphManagerCtrl.content)
      {
        if ($scope.graphManagerCtrl.content[i].showDetails)
        {        
          for (var j in data)
          {
            if ($scope.graphManagerCtrl.content[i].id === data[j].id)
            {
              data[j]['showDetails'] = $scope.graphManagerCtrl.content[i].showDetails;
              break;
            }
          }
        }
      }
      $scope.graphManagerCtrl.content = data;
      $scope.graphManagerCtrl.sortGraphs();
    }

    function goToGraph(id)
    {
      $log.debug(vm.title+'/ goToGraph');
      if (id)
      {
        if ($state.is('app.cctool_graphs'))
        {
          $state.go('app.cctool_graph',{id: id});
        }
        else if ($state.is('app.cctool_graphs_demo'))
        {
          $state.go('app.cctool_graph_demo',{id: id});
        }
      }
    }
  }
})();
