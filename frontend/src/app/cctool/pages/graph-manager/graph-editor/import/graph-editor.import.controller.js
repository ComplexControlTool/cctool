// graph-editor.import.controller.js
(function ()
{
    'use strict';

    angular
        .module('app.cctool.pages.graph-editor')
        .controller('ImportGraphController', ImportGraphController);

    ImportGraphController.$inject = ['$rootScope', '$scope', '$q', '$timeout', '$state', '$stateParams', '$mdToast', '$mdMedia', '$mdDialog', '$cookies', 'api', 'settingsService'];

    /** @ngInject */
    function ImportGraphController($rootScope, $scope, $q, $timeout, $state, $stateParams, $mdToast, $mdMedia, $mdDialog, $cookies, api, settingsService)
    {
        var vm = this;

        vm.title = 'ImportGraphController';
        vm.activeSettings = settingsService.activeSettings;

        var toastPosition = 'bottom left';

        init();

        vm.enableNextStep = enableNextStep;
        vm.moveToPreviousStep = moveToPreviousStep;
        vm.processStep = processStep;
        vm.processGraph = processGraph;
        vm.submitGraph = submitGraph;

        //////////

        function init()
        {
          // File related
          vm.maxFileSize = 10;
          isGraphChanged();
          // Instructions related
          vm.gephiToolUrl = 'https://gephi.org/plugins/#/plugin/jsonexporter-plugin';
          vm.gephiToolInstructionsUrl = '';
          // Form related
          vm.selectedStep = 0;
          vm.stepProgress = 1;
          vm.processing = false;
          vm.maxStep = 4;
          vm.stepData = [
            { step: 1, completed: false, optional: false, data: {} },
            { step: 2, completed: false, optional: false, data: {gephiGraphFile:undefined, graphFileName:''} },
            { step: 3, completed: false, optional: false, data: {parsedGraph:undefined} },
            { step: 4, completed: false, optional: false, data: {} },
          ];
        }

        function isGraphChanged()
        {
          $scope.$watch('importGraphCtrl.stepData[1].data.graphFileName', function(newVal, oldVal)
          {
            if(newVal !== oldVal)
            {
              loadGraphFromJson();
            }
          });
        }

        function loadGraphFromJson()
        {
            var jsonFile = JSON.parse(vm.stepData[1].data.gephiGraphFile);
            var structure = vis.network.gephiParser.parseGephi(jsonFile);
            // Set default values for node cctool atributes.
            for (var i in structure.nodes)
            {
              structure.nodes[i]['cctool'] = {};
              structure.nodes[i]['cctool']['function'] = 'L';
              structure.nodes[i]['cctool']['controllability'] = '0';
              structure.nodes[i]['cctool']['importance'] = '0';              
            }
            // Set default values from edge cctool atributes.
            for (var i in structure.edges)
            {
              structure.edges[i]['cctool'] = {};
              structure.edges[i]['cctool']['weight'] = '1';
            }
            vm.stepData[2].data.parsedGraph = {};
            vm.stepData[2].data.parsedGraph['graphvisdatasets'] = structure;
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
          dataSets = {'details':{}, 'nodes':[], 'edges':[]};

          // Retrieve graph's details.
          dataSets.details['title'] = vm.stepData[0].data.title ? vm.stepData[0].data.title : 'Untitled';
          dataSets.details['description'] = vm.stepData[0].data.description ? vm.stepData[0].data.description : 'No description provided!';
          dataSets.details['moredescription'] = vm.stepData[0].data.moredescription ? vm.stepData[0].data.moredescription : '';

          // Retrieve graph's nodes and edges.
          if (vm.stepData[2].data.network)
          {
            var network = vm.stepData[2].data.network;
            network.storePositions();
            dataSets.nodes = network.body.data.nodes.get();
            dataSets.edges = network.body.data.edges.get();
          }

          dataSets['title'] = 'dummy';
          dataSets['description'] = 'dummy';
          dataSets['structure'] = 'dummy';
          dataSets['labels'] = 'dummy';
          dataSets['functions'] = 'dummy';
          dataSets['controllability'] = 'dummy';
          dataSets['importance'] = 'dummy';

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