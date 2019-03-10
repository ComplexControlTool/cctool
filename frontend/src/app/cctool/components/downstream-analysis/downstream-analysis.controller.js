// downstream-analysis.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.downstream-analysis')
    .controller('DownstreamAnalysisController', DownstreamAnalysisController);

  /** @ngInject */
  function DownstreamAnalysisController($scope, $log, $mdToast, $element, $window, downstreamAnalysisService)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'DownstreamAnalysisController';
    vm.content = undefined;
    vm.graphForAnalysis = undefined;
    vm.network = undefined;
    vm.selectedIndex = 0;
    vm.reloadGraph = false;
    vm.progressLinear = {active:true, mode:'', value:'', bufferValue:''};
    var analysisServerRefreshInMs = 1000 //every second
    var serverRefreshInMs = 300000 // every 5 minutes

    // Functions
    vm.initAnalysis = initAnalysis;
    vm.drawGraph = drawGraph;
    
    activate();

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });

    $scope.$on('downstreamAnalysis:hasUpdates', function(event,data) {
      analysisHasUpdates(data);
    });

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
      initAnalysis();
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
      $log.debug(vm.title+'/ Cleanup analysis monitor');
      downstreamAnalysisService.stopMonitorUpdates();
    }

    // Setting up variables before allowing user to start analysing.
    function initAnalysis(graph)
    {
      $log.debug(vm.title+'/ initAnalysis: Setting initial values with arguments:',JSON.stringify(graph));
      // Get the graph from the ng-repeat of the page.
      vm.graphForAnalysis = graph ? graph : $scope.graphCtrl.content;
      // Request analysis from server.
      showProgressLinear();
      downstreamAnalysisService.initMonitorUpdates(vm.graphForAnalysis.id, vm.content, analysisServerRefreshInMs, serverRefreshInMs);
    }

    function analysisHasUpdates(data)
    {
      $log.debug(vm.title+'/ analysisHasUpdates: arguments:\ndata:',JSON.stringify(data));
      vm.content = data;
      if (data.isAnalysed)
      {
        clearProgressLinear();
      }
      else
      {
        showProgressLinear();
      }
    }

    // Display any progress bar.
    function showProgressLinear()
    {
      $log.debug(vm.title+'/ showProgressLinear');
      vm.progressLinear.active = true;
      vm.progressLinear.mode = 'indeterminate';
    }

    // Remove any progress bar.
    function clearProgressLinear()
    {
      $log.debug(vm.title+'/ clearProgressLinear');
      vm.progressLinear = {active:false, mode:'', value:'', bufferValue:''};
    }

    function drawGraph(tabIndex)
    {
      $log.debug(vm.title+'/ drawGraph: arguments:\nconfTabIndex:',tabIndex);
      if (!_.isEmpty(vm.content) && vm.selectedIndex === tabIndex)
      {
        return true;
      }
      return false;
    }

  }
})();
