// explore.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.explore')
    .controller('ExploreController', ExploreController);

  /** @ngInject */
  function ExploreController(Graph, $scope, $log)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'ExploreController';
    vm.graphForAnalysis = Graph ? Graph : undefined;
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
      $log.debug(vm.title+'/ initAnalysis: Setting initial values with arguments: '+JSON.stringify(vm.graphForAnalysis));
      // Get the nodes for the current graph.
      vm.nodeLabels = [];
      for (var i in vm.graphForAnalysis.structure.nodes)
      {
        var node = vm.graphForAnalysis.structure.nodes[i];
        vm.nodeLabels.push(node.label);
      }
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
      var edges = angular.copy(vm.graphForAnalysis.structure.edges)
      var key = vm.nodeLabels.indexOf(node);
      var keys = new Set([key]);

      while(edges.length)
      {
        var subtracted = 0
        for (var i in edges)
        {
          var edge = edges[i];
          if (mode === "UpStream")
          {          
            if (keys.has(edge.to))
            {
              keys.add(edge.from);
              edges.splice(i, 1);
              subtracted++;
            }
          }
          else if (mode === "DownStream")
          {
            if (keys.has(edge.from))
            {
              keys.add(edge.to);
              edges.splice(i, 1);
              subtracted++;
            }
          }
        }
        if (subtracted == 0)
        {
          break;
        }
      }

      if (keys.size > 0)
      {
        var nodesToRemove = {};
        nodesToRemove["selectedNodeId"] = key;
        nodesToRemove["removeNodesIds"] = computeNodesToRemove(Array.from(keys));
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
