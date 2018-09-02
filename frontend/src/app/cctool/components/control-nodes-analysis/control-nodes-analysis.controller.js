// control-nodes-analysis.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.control-nodes-analysis')
    .controller('ControlNodesAnalysisController', ControlNodesAnalysisController);

  /** @ngInject */
  function ControlNodesAnalysisController($scope, $log, $mdToast, $element, $window, api)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'ControlNodesAnalysisController';
    vm.graphForAnalysis = undefined;
    vm.nodeLabels = undefined;
    vm.network = undefined;
    vm.selectedConfIndex = 0;
    vm.reloadGraph = false;
    vm.progressLinear = {active:false, mode:'', value:'', bufferValue:''};

    // Functions
    activate();
    vm.initAnalysis = initAnalysis;
    vm.drawGraph = drawGraph;
    vm.isControlNode = isControlNode;
    vm.requestAnalysis = requestAnalysis;

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
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
      // Get the nodes for the current graph.
      vm.nodeLabels = vm.graphForAnalysis.labels.split(',');
      // Request analysis from server.
      if (!vm.graphForAnalysis.graphanalysed)
      {
        requestAnalysis();
      }
    }

    function drawGraph(confTabIndex)
    {
      if (vm.graphForAnalysis.graphanalysed && vm.selectedConfIndex === confTabIndex)
      {
        return true;
      }
      return false;
    }

    function isControlNode(nodeIndex)
    {
      $log.debug(vm.title+'/ isControlNode: arguments:\nnodeIndex:'+JSON.stringify(nodeIndex));
      var index = isNaN( parseInt(nodeIndex) ) ? -1 : parseInt(nodeIndex);

      if (!vm.graphForAnalysis.graphanalysed || !vm.graphForAnalysis.graphcontrolconf)
      {
        return false;
      }

      if (vm.graphForAnalysis.graphcontrolconf[vm.selectedConfIndex].indexOf(index) == -1)
      {
        return false;
      }

      return true;
    }

    function requestAnalysis()
    {
      $log.debug(vm.title+'/ requestAnalysis with id: ',vm.graphForAnalysis.id);
      showProgressLinear();
      var params = {id:vm.graphForAnalysis.id};

      var successfulCall1 = function(response)
      {
        $log.debug(vm.title+'/ Successful requestAnalysis call 1 with response',response);
        api.cctool.graph.full.get(params,successfulCall2,unsuccessfulCall);
      };
      var successfulCall2 = function(response)
      {
        $log.debug(vm.title+'/ Successful requestAnalysis call 2 with response',response);
        clearProgressLinear();
        vm.graphForAnalysis = response
      };
      var unsuccessfulCall = function(response)
      {
        $log.debug(vm.title+'/ Unsuccessful onGraphAnalyse call with response',response);
        clearProgressLinear();
        $mdToast.show(
          $mdToast.simple()
          .textContent('Unable to analyse graph!')
          .position($scope.appCtrl.toastPosition)
          .hideDelay(3000)
        );
      };
      api.cctool.graphImplications.get(params,successfulCall1,unsuccessfulCall);
    }

  }
})();
