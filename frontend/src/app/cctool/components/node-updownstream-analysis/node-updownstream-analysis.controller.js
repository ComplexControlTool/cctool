// node-updownstream-analysis.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.node-updownstream-analysis')
    .controller('NodeAnalysisController', NodeAnalysisController);

  /** @ngInject */
  function NodeAnalysisController($scope, $log)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'NodeAnalysisController';
    vm.graphForAnalysis = undefined;
    vm.nodeLabels = undefined;
    vm.data = undefined;

    // Functions
    activate();
    vm.initAnalysis = initAnalysis;
    vm.computeStream = computeStream;

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

    // Setting up variables before allowing user to start analysing.
    function initAnalysis(graph)
    {
      $log.debug(vm.title+'/ initAnalysis: Setting initial values with arguments: '+JSON.stringify(graph));
      // Get the graph from the ng-repeat of the page.
      vm.graphForAnalysis = graph ? graph : $scope.graphCtrl.content;
      // Get the nodes for the current graph.
      vm.nodeLabels = vm.graphForAnalysis.labels.split(',');
      // Assign an epty array to begine.
      vm.data = {
        leftGraph: {
          network:undefined,
          selectedNodeLabel:'',
          streamMode:'',
          nodesToRemove:{}
        },
        rightGraph: {
          network:undefined,
          selectedNodeLabel:'',
          streamMode:'',
          nodesToRemove:{}
        }
      };
    }

    function computeStream(node, mode)
    {
      $log.debug(vm.title+'/ computeStream');
      // Find index of selected node in labels array
      var key = vm.nodeLabels.indexOf(node);;

      var nodesToKeep = [];
      nodesToKeep.push(key);
      var nodesToKeepLabels = [];
      nodesToKeepLabels.push(vm.nodeLabels[key]);

      if (mode === "UpStream")
      {
        for(var value in vm.graphForAnalysis.graphstructure )
        {
          for(var j=0; j< vm.graphForAnalysis.graphstructure[value].length; j++)
          {
            if(vm.graphForAnalysis.graphstructure[value][j][0] == key)
            {
              nodesToKeep.push( parseInt(value) );
              var name= vm.nodeLabels[value];
              nodesToKeepLabels.push(name);
            }
          }
        }
      }

      if (mode === "DownStream")
      {
        var index = 0;
        while(index < nodesToKeep.length)
        {
          if( typeof vm.graphForAnalysis.graphstructure[ nodesToKeep[index] ] === 'undefined' )
          {
            break;
          }
          for(var i=0; i< vm.graphForAnalysis.graphstructure[ nodesToKeep[index] ].length; i++)
          {
            var value = vm.graphForAnalysis.graphstructure[ nodesToKeep[index] ][i];
            //Get rid of loops
            if(!nodesToKeep.includes( value[0] ))
            {
              nodesToKeep.push( parseInt( value[0] ) );
              var name= vm.nodeLabels[ value[0] ];
              nodesToKeepLabels.push(name);
            }
          }

          index++;

          //Avoid out of index exceptions
          if( typeof vm.graphForAnalysis.graphstructure[ nodesToKeep[index] ] === 'undefined')
          {
            break;
          }

        }
      }

      if (nodesToKeepLabels.length > 0)
      {
        var nodesToRemove = {};
        nodesToRemove["selectedNodeId"] = key;
        nodesToRemove["removeNodesIds"] = computeNodesToRemove(nodesToKeep);
        nodesToRemove["mode"] = mode;
        return nodesToRemove;
      }
      else
      {
        return {};
      }
    }
    
    function computeNodesToRemove(nodesToKeep)
    {
      $log.debug(vm.title+'/ computeNodesToRemove');
      var temp = [];
      //Reverse selection so that we have the nodes we want to remove
      for(var i=0; i<vm.nodeLabels.length; i++)
      {
        if( !nodesToKeep.includes(i) )
        {
          temp.push(i);
        }
      }
      return temp;
    }
  }
})();
