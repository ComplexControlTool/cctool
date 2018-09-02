// graph-editor.create.controller.js
(function ()
{
    'use strict';

    angular
        .module('app.cctool.pages.graph-editor')
        .controller('CreateGraphController', CreateGraphController);

    /** @ngInject */
    function CreateGraphController($rootScope, $scope, $q, $timeout, $state, $stateParams, $mdToast, $mdMedia, $mdDialog, $cookies, $log, api, settingsService)
    {
        var vm = this;

        vm.title = 'CreateGraphController';
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
          $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
          // Form related
          vm.selectedStep = 0;
          vm.stepProgress = 1;
          vm.processing = false;
          vm.maxStep = 3;
          vm.stepData = [
            { step: 1, completed: false, optional: false, data: {} },
            { step: 2, completed: false, optional: false, data: {graph:{id:''}} },
            { step: 3, completed: false, optional: false, data: {} },
          ];
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
          if (vm.stepData[1].data.network)
          {
            var network = vm.stepData[1].data.network;
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