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
    vm.graphForAnalysis = undefined;
    vm.network = undefined;
    vm.selectedConfIndex = 0;
    vm.reloadGraph = false;
    vm.progressLinear = {active:false, mode:'', value:'', bufferValue:''};
    vm.isAnalysed = false;
    vm.data = undefined;

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
      vm.data = data;
      if (data.isAnalysed)
      {
        vm.isAnalysed = data.isAnalysed;
        controllabilityAnalysisService.stopMonitorUpdates();
        // clearProgressLinear();
      }
    });

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
      initAnalysis();
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
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
      vm.progressLinear = {active:false, mode:'', value:'', bufferValue:''};
    }

    // Setting up variables before allowing user to start analysing.
    function initAnalysis(graph)
    {
      $log.debug(vm.title+'/ initAnalysis: Setting initial values with arguments: '+JSON.stringify(graph));
      // Get the graph from the ng-repeat of the page.
      vm.graphForAnalysis = graph ? graph : $scope.graphCtrl.content;
      // Request analysis from server.
      showProgressLinear();
      controllabilityAnalysisService.initMonitorUpdates(vm.graphForAnalysis.id,10000);
    }

    function drawGraph(confTabIndex)
    {
      if (!_.isEmpty(vm.data) && vm.selectedConfIndex === confTabIndex)
      {
        return true;
      }
      return false;
    }

    function isControlNode(nodeIndex)
    {
      $log.debug(vm.title+'/ isControlNode: arguments:\nnodeIndex:'+JSON.stringify(nodeIndex));
      var index = isNaN( parseInt(nodeIndex) ) ? -1 : parseInt(nodeIndex);

      if (_.isEmpty(vm.data) || _.isEmpty(vm.data.analysis.data.controlConfigurations))
      {
        return false;
      }

      if (vm.data.analysis.data.controlConfigurations[vm.selectedConfIndex].indexOf(index) == -1)
      {
        return false;
      }

      return true;
    }

  }
})();
