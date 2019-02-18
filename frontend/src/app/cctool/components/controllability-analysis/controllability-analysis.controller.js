// controllability-analysis.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.controllability-analysis')
    .controller('ControllabilityAnalysisController', ControllabilityAnalysisController);

  /** @ngInject */
  function ControllabilityAnalysisController($scope, $log, $mdToast, $element, $window, controllabilityAnalysisService)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'ControllabilityAnalysisController';
    vm.content = undefined;
    vm.graphForAnalysis = undefined;
    vm.network = undefined;
    vm.selectedConfIndex = 0;
    vm.reloadGraph = false;
    vm.progressLinear = {active:true, mode:'', value:'', bufferValue:''};
    var analysisServerRefreshInMs = 500 //every 0.5 second
    var serverRefreshInMs = 300000 // every 5 minutes

    // Functions
    vm.initAnalysis = initAnalysis;
    vm.drawGraph = drawGraph;
    vm.isControlNode = isControlNode;
    
    activate();

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });

    $scope.$on('controllabilityAnalysis:hasUpdates', function(event,data) {
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
      controllabilityAnalysisService.stopMonitorUpdates();
    }

    // Setting up variables before allowing user to start analysing.
    function initAnalysis(graph)
    {
      $log.debug(vm.title+'/ initAnalysis: Setting initial values with arguments:',JSON.stringify(graph));
      // Get the graph from the ng-repeat of the page.
      vm.graphForAnalysis = graph ? graph : $scope.graphCtrl.content;
      // Request analysis from server.
      showProgressLinear();
      controllabilityAnalysisService.initMonitorUpdates(vm.graphForAnalysis.id, vm.content, analysisServerRefreshInMs, serverRefreshInMs);
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

    function drawGraph(confTabIndex)
    {
      $log.debug(vm.title+'/ drawGraph: arguments:\nconfTabIndex:',confTabIndex);
      if (!_.isEmpty(vm.content) && vm.selectedConfIndex === confTabIndex)
      {
        return true;
      }
      return false;
    }

    function isControlNode(nodeIndex)
    {
      $log.debug(vm.title+'/ isControlNode: arguments:\nnodeIndex:',nodeIndex);
      var index = isNaN( parseInt(nodeIndex) ) ? -1 : parseInt(nodeIndex);

      if (_.isEmpty(vm.content) || _.isEmpty(vm.content.analysis.data.controlConfigurations))
      {
        return false;
      }

      if (vm.content.analysis.data.controlConfigurations[vm.selectedConfIndex].indexOf(index) == -1)
      {
        return false;
      }

      return true;
    }

  }
})();
