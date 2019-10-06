// graph-editor.create.controller.js
(function ()
{
    'use strict';

    angular
        .module('app.cctool.pages.graph-editor')
        .controller('CreateGraphController', CreateGraphController);

    /** @ngInject */
    function CreateGraphController($rootScope, $scope, $q, $timeout, $state, $stateParams, $mdToast, $mdMedia, $mdDialog, $cookies, $log, api, settingsService, graphDefaultVisualization, availableGraphAnalyses)
    {
        var vm = this;

        vm.title = 'CreateGraphController';
        vm.activeSettings = settingsService.activeSettings;
        vm.availableGraphAnalyses = availableGraphAnalyses;

        var toastPosition = 'bottom left';
        
        init();

        vm.toggleAllAnalysis = toggleAllAnalysis;
        vm.isAllSelectedAnalysis = isAllSelectedAnalysis;
        vm.isSomeSelectedAnalysis = isSomeSelectedAnalysis;
        vm.toggleAnalysis = toggleAnalysis;
        vm.isSelectedAnalysis = isSelectedAnalysis;
        vm.enableNextStep = enableNextStep;
        vm.moveToPreviousStep = moveToPreviousStep;
        vm.processStep = processStep;
        vm.processGraph = processGraph;
        vm.submitGraph = submitGraph;

        //////////

        function init()
        {
          $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
          // Form related
          vm.selectedStep = 0;
          vm.stepProgress = 1;
          vm.processing = false;
          vm.maxStep = 3;
          vm.stepData = [
            { step: 1, completed: false, optional: false, data: {'analysisTypes':[]} },
            { step: 2, completed: false, optional: false, data: {graph:{id:'',visualization:graphDefaultVisualization}} },
            { step: 3, completed: false, optional: false, data: {} },
          ];
        }

        function toggleAllAnalysis()
        {
          if (vm.stepData[0].data['analysisTypes'] == undefined)
          {
            return
          }
          if (vm.stepData[0].data['analysisTypes'].length === Object.keys(availableGraphAnalyses).length) {
            vm.stepData[0].data['analysisTypes'] = [];
          } else if (vm.stepData[0].data['analysisTypes'].length === 0 || vm.stepData[0].data['analysisTypes'].length > 0) {
            vm.stepData[0].data['analysisTypes'] = _.values(availableGraphAnalyses);
          }
        }

        function isAllSelectedAnalysis()
        {
          if (vm.stepData[0].data['analysisTypes'] == undefined)
          {
            return
          }
          return vm.stepData[0].data['analysisTypes'].length === Object.keys(availableGraphAnalyses).length;
        }

        function isSomeSelectedAnalysis()
        {
          if (vm.stepData[0].data['analysisTypes'] == undefined)
          {
            return
          }
          return (vm.stepData[0].data['analysisTypes'].length !== 0 &&
            vm.stepData[0].data['analysisTypes'].length !== Object.keys(availableGraphAnalyses).length);
        }

        function toggleAnalysis(value, list)
        {
          if (list == undefined)
          {
            return
          }
          var idx = list.indexOf(value);
          if (idx > -1) {
            list.splice(idx, 1);
          }
          else {
            list.push(value);
          }
        }

        function isSelectedAnalysis(value, list)
        {
          if (list == undefined)
          {
            return
          }
          return list.indexOf(value) > -1;
        }

        function enableNextStep()
        {
            //do not exceed into max step
            if (vm.selectedStep >= vm.maxStep) {
                return;
            }
            //do not increment vm.stepProgress when submitting from previously completed step
            if (vm.selectedStep === vm.stepProgress - 1) {
                vm.stepProgress = vm.stepProgress + 1;
            }
            vm.selectedStep = vm.selectedStep + 1;
        }

        function moveToPreviousStep()
        {
            if (vm.selectedStep > 0) {
                vm.selectedStep = vm.selectedStep - 1;
            }
        }

        function processStep(stepId, isSkip)
        {
          vm.processing = true;
          if (!vm.stepData[stepId].completed && !isSkip)
          {
              // some time delay for 'processing'
              $timeout(function () {
                vm.processing = false;
                vm.stepData[stepId].completed = true;
                enableNextStep();
              }, 1000)
            }
            else
            {
              vm.processing = false;
              enableNextStep();
            }
        }

        function processGraph(stepId)
        {
          var graphStepId = stepId + 1;
          vm.processing = true;
          while (!vm.stepData[graphStepId].data.network){}
          vm.stepData[stepId].completed = true;
          vm.processing = false;
          enableNextStep();
        }

        function generateDataSets()
        {
          var dataSets = {};

          // Retrieve graph's details.
          dataSets['title'] = vm.stepData[0].data.title ? vm.stepData[0].data.title : 'Untitled';
          dataSets['description'] = vm.stepData[0].data.description ? vm.stepData[0].data.description : '';

          // Retrieve graph's nodes and edges.
          var structure = {'nodes':[], 'edges':[]};
          if (vm.stepData[1].data.network)
          {
            var network = vm.stepData[1].data.network;
            var nodeDataset = network.body.data.nodes
            var edgeDataset = network.body.data.edges

            // Make sure we update node location
            for (var node_id in network.body.nodes)
            {
              var positionX = network.body.nodes[node_id]['x'];
              var positionY = network.body.nodes[node_id]['y'];
              nodeDataset.update({id:node_id, x:positionX, y:positionY})
            }
          }
          structure.nodes = nodeDataset.get();
          structure.edges = edgeDataset.get();

          dataSets['structure'] = structure;
          dataSets['analysisTypes'] = vm.stepData[0].data['analysisTypes'] || [];

          return dataSets;
        }

        function submitGraph(stepId)
        {
          var successfulCall = function(response)
          {
            vm.processing = false;
            vm.stepData[stepId].completed = true;
            enableNextStep();
          };
          var unsuccessfulCall = function(response)
          {
            $mdToast.show(
              $mdToast.simple()
                .textContent('Unable to add graph!')
                .position(toastPosition)
                .hideDelay(3000)
            );
            vm.processing = false;
            vm.stepData[stepId].completed = false;
          };

          if (!vm.stepData[stepId].completed)
          {
            vm.processing = true;
            var data = generateDataSets();
            var Graph = api.cctool.graphs.full;
            var newGraph = new Graph(data);
            newGraph.$save(successfulCall,unsuccessfulCall);
          }
        }
    }
})();