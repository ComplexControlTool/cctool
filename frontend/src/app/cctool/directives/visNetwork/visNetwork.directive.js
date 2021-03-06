// visNetwork.directive.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.directives.visNetwork')
    .directive('visNetwork', visNetwork);

  /* @ngInject */
  function visNetwork($log, $mdDialog, $mdMedia, cctoolColorsService)
  {
    // Usage:
    //
    // Creates:
    //
    var directive = {
      bindToController: true,
      controller: Controller,
      controllerAs: 'vm',
      link: link,
      restrict: 'A',
      scope: {
        'network':'=network',
        'analysis':'=analysis',
        'visualization':'=visualization',
        'index':'=index',
        'nodesToHide' : '=nodesToHide',
        'nodeShape':'=nodeShape',
        'editGraph':'=editGraph',
        'reload':'=reload',
      }
    };
    return directive;

    function link(scope, element, attrs)
    {
      var isDrawable = false;
      var editGraph = scope.vm.editGraph ? scope.vm.editGraph : false;
      var nodeData = new vis.DataSet();
      var edgeData = new vis.DataSet();
      var data = { nodes: nodeData, edges: edgeData };
      var options = {};
      var manipulation_options = {
        enabled: editGraph,
        addNode: function (data, callback) {
          manipulationAddNode(scope, data, callback);
        },
        editNode: function (data, callback) {
          manipulationEditNode(scope, data, callback);
        },
        addEdge: function (data, callback) {
          manipulationAddEdge(scope, data, callback);
        },
        // editEdge: function (data, callback) {
        //   manipulationEditEdge(scope, data, callback);
        // }
      };
      options['manipulation'] = manipulation_options;
      var colors = cctoolColorsService.cctoolColors;
      var color = colors[5]; // (default to grey)

      var structureData = function()
      {
        // Set scope variables.
        scope.options = scope.vm.visualization && scope.vm.visualization.options ? Object.assign({}, scope.vm.visualization.options, options) : options
        scope.structure = scope.vm.visualization && scope.vm.visualization.structure ? scope.vm.visualization.structure : {}
        if (scope.vm.index in scope.structure)
        {
          scope.structure = scope.structure[scope.vm.index];
        }
        scope.controlConfiguration = {}
        if (scope.vm.analysis && scope.vm.analysis.typeOfAnalysis == 'Controllability Analysis' && scope.vm.analysis.data)
        {
          if (scope.vm.analysis.data.rankedByNodeControllability)
          {
            scope.controlConfiguration = scope.vm.analysis.data.rankedByNodeControllability.controlConfigurations[scope.vm.index];
          }
          else if(scope.vm.analysis.data.controlConfigurations)
          {
            scope.controlConfiguration = scope.vm.analysis.data.controlConfigurations[scope.vm.index];
          }
        }
        scope.element = element;
      }

      // Re-draw on data change.
      scope.$watch('vm.analysis',
        function()
        {
          $log.debug('watch: vm.analysis');
          if(!_.isEmpty(scope.vm.analysis))
          {
            $log.debug('inside watch: vm.analysis / init');
            structureData();
            try
            {
              initData($log, nodeData, edgeData, scope.structure, scope.vm.nodeShape, scope.controlConfiguration);
              scope.vm.network = initNetwork($log, scope.element, data, scope.options);
              if (!scope.vm.editGraph)
              {
                initOnClick(scope.vm.network, data.nodes, data.edges);
              }
            }
            catch(error)
            {
              $log.error('Failed to init/update graph with error',error);
            }
          }
        },
        true
      );

      // Re-draw on data change.
      scope.$watch('vm.visualization',
        function()
        {
          $log.debug('watch: vm.visualization');
          if(!_.isEmpty(scope.vm.visualization) || scope.vm.editGraph)
          {
            $log.debug('inside watch: vm.visualization / init');
            isDrawable = true;
            structureData();
            try
            {
              if (nodeData.length == 0 && edgeData.length == 0)
              {
                initData($log, nodeData, edgeData, scope.structure, scope.vm.nodeShape, scope.controlConfiguration);
                scope.vm.network = initNetwork($log, scope.element, data, scope.options);
                if (!scope.vm.editGraph)
                {
                  initOnClick(scope.vm.network, data.nodes, data.edges);
                }
              }
              else
              {
                updateData($log, nodeData, edgeData, scope.structure, scope.vm.nodeShape, scope.controlConfiguration);
                if (!scope.vm.editGraph)
                {
                  initOnClick(scope.vm.network, data.nodes, data.edges);
                }
              }
            }
            catch(error)
            {
              $log.error('Failed to init/update graph with error',error)
            }
          }
          else
          {
            isDrawable = false;
          }
        },
        true
      );

      // TODO: add one more (from above) for analysis object

      // Hide nodes according to explore card.
      scope.$watch('vm.nodesToHide',
        function()
        {
          $log.debug('watch vm.nodesToHide');
          if(isDrawable && scope.vm.nodesToHide && !_.isEmpty(scope.vm.nodesToHide))
          {
            $log.debug('inside watch: vm.nodesToHide');
            try
            {
              initData($log, nodeData, edgeData, scope.structure, scope.vm.nodeShape, scope.controlConfiguration);
              scope.vm.network = initNetwork($log, scope.element, data, scope.options);
              if (scope.vm.nodesToHide.removeNodesIds && scope.vm.nodesToHide.removeNodesIds.length > 0)
              {
                hideGivenNodes(nodeData, scope.vm.nodesToHide.removeNodesIds);
                scope.vm.network = initNetwork($log, scope.element, data, scope.options);
                repositionRootNode(scope.vm.network, nodeData, scope.vm.nodesToHide.selectedNodeId, scope.vm.nodesToHide.mode)
              }
            }
            catch(error)
            {
              $log.error('Failed to init/update graph with error',error)
            }
          }
        }
      );

      // Re-draw on nodeShape attribute change.
      scope.$watch('vm.nodeShape',
        function()
        {
          $log.debug('watch vm.nodeShape');
          if(isDrawable)
          {
            $log.debug('inside watch: vm.nodeShape');
            try
            {
              updateData($log, nodeData, edgeData, scope.structure, scope.vm.nodeShape, scope.controlConfiguration);
              changeNodeShape(nodeData, edgeData, scope.vm.nodeShape);
              if (!scope.vm.editGraph)
              {
                initOnClick(scope.vm.network, data.nodes, data.edges);
              }
            }
            catch(error)
            {
              $log.error('Failed to init/update graph with error',error)
            }
          }
        }
      );

      // Enable/Disable graph editing.
      scope.$watch('vm.editGraph',
        function()
        {
          $log.debug('watch vm.editGraph');
          if(isDrawable && scope.vm.editGraph)
          {
            $log.debug('inside watch: vm.editGraph');
            try
            {
              options.manipulation.enabled = scope.vm.editGraph || false;
              scope.vm.network = initNetwork($log, scope.element, data, scope.options);
            }
            catch(error)
            {
              $log.error('Failed to init/update graph with error',error)
            }
          }
        }
      );

      // Re-draw on reload attribute change.
      scope.$watch('vm.reload',
        function()
        {
          $log.debug('watch vm.reload');
          if(isDrawable && scope.vm.reload)
          {
            $log.debug('inside watch: vm.reload');
            try
            {
              initData($log, nodeData, edgeData, scope.structure, scope.vm.nodeShape, scope.controlConfiguration);
              if (scope.vm.network)
              {
                destroyNetwork(scope.vm.network);
              }
              scope.vm.network = initNetwork($log, scope.element, data, scope.options);
              if (!scope.vm.editGraph)
              {
                initOnClick(scope.vm.network, data.nodes, data.edges);
              }
              scope.vm.nodeShape = true;
              scope.vm.reload = false;
            }
            catch(error)
            {
              $log.error('Failed to init/update graph with error',error)
            }
          }
        }
      );

    }
  }

  function manipulationAddNode(scope, data, callback)
  {
    var dialogData = { template:'app/cctool/pages/graph-manager/graph-editor/dialogs/graph.new.addNode.html', nodeData: {}, edgeData: {} };

    scope.showPopUp(dialogData).then(
      function(inputData) {
        data.label = inputData.nodeData.nodeLabel;
        data.cctool = {};
        data.cctool['function'] = inputData.nodeData.nodeFunction;
        data.cctool['controllability'] = inputData.nodeData.nodeControllability;
        data.cctool['vulnerability'] = inputData.nodeData.nodeVulnerability;
        data.cctool['importance'] = inputData.nodeData.nodeImportance;
        data.cctool['tags'] = inputData.nodeData.nodeTags;
        callback(data);
      },
      function() {
        callback();
      }
    );
  }

  function manipulationEditNode(scope, data, callback)
  {
    var dialogData = { template:'app/cctool/pages/graph-manager/graph-editor/dialogs/graph.new.addNode.html', nodeData: data, edgeData: {} };

    scope.showPopUp(dialogData).then(
      function(inputData) {
        data.label = inputData.nodeData.nodeLabel;
        data.cctool['function'] = inputData.nodeData.nodeFunction;
        data.cctool['controllability'] = inputData.nodeData.nodeControllability;
        data.cctool['vulnerability'] = inputData.nodeData.nodeVulnerability;
        data.cctool['importance'] = inputData.nodeData.nodeImportance;
        data.cctool['tags'] = inputData.nodeData.nodeTags;
        callback(data);
      },
      function() {
        callback();
      }
    );
  }

  function manipulationAddEdge(scope, data, callback)
  {
    var dialogData = { template:'app/cctool/pages/graph-manager/graph-editor/dialogs/graph.new.addEdge.html', nodeData: {}, edgeData: {} };

    scope.showPopUp(dialogData).then(
      function(inputData) {
        data.label = inputData.edgeData.edgeLabel;
        data.cctool = {};
        data.cctool['weight'] = inputData.edgeData.edgeWeight;
        data.cctool['tags'] = inputData.edgeData.edgeTags;
        callback(data);
      },
      function() {
        callback();
      }
    );
  }

  function manipulationEditEdge(scope, data, callback)
  {
    var dialogData = { template:'app/cctool/pages/graph-manager/graph-editor/dialogs/graph.new.addEdge.html', nodeData: {}, edgeData: data };

    scope.showPopUp(dialogData).then(
      function(inputData) {
        data.label = inputData.edgeData.edgeLabel;
        data.cctool['weight'] = inputData.edgeData.edgeWeight;
        data.cctool['tags'] = inputData.edgeData.edgeTags;
        callback(data);
      },
      function() {
        callback();
      }
    );
  }

  function updateControlNodes(nodeData, controlConfiguration)
  {
    var nodesToUpdate = [];
    // Update control nodes of current set
    for (var i in controlConfiguration)
    {
      var nodeId = controlConfiguration[i];
      var data = nodeData.get(nodeId);

      // Update background colour
      var highlight = { 'background':'#FDD835' };
      var oldBorder = data['color']['border'];
      data['color'] = { 'background':'#FDD835', 'border':oldBorder, 'highlight':highlight };
      // Update border width
      data['borderWidth'] = 3;
      // Update title
      data['title'] += '<p>Control Node: <strong>Yes</strong></p>';

      nodesToUpdate.push(data);
    }
    nodeData.update(nodesToUpdate);
  }

  function changeNodeShape(nodeData, edgeData, nodeShape)
  {
    var data = nodeData.get();

    for(var i in data)
    {
      if (data[i].hasOwnProperty('shapeProperties'))
      {
        if (data[i]['shapeProperties']['static'])
        {
          continue
        }
      }
      data[i]['shape'] = nodeShape;
    }
    
    nodeData.update(data);
  }

  // Update data for use with the network.
  function updateData($log, nodeData, edgeData, DataSets, nodeShape, controlConfiguration)
  {
    $log.debug('Update Data Called');
    if(_.isEmpty(DataSets))
    {
      return;
    }

    nodeData.update(DataSets.nodes);
    edgeData.update(DataSets.edges);

    if(controlConfiguration)
    {
      updateControlNodes(nodeData, controlConfiguration);
    }
  }

  // Initialise data for use with the network.
  function initData($log, nodeData, edgeData, DataSets, nodeShape, controlConfiguration)
  {
    $log.debug('Init Data Called');
    nodeData.clear();
    edgeData.clear();
    
    updateData($log, nodeData, edgeData, DataSets, nodeShape, controlConfiguration);
  }

  // Function to render the network's structure.
  function initNetwork($log, element, data, options)
  {
    $log.debug('Init Network Called');
    var container = element[0];
    var network = new vis.Network(container, data, options);
    network.fit();

    network.once('stabilizationProgress',
      function()
      {
        element.css({'pointer-events': 'none'});
        var overlay = element.find('div.vis-overlay');
        if (overlay)
        {
          overlay.css({'background-color': 'rgb(255,255,255)'});
          var styles = 'position:relative; float:left; top:50%; left:50%; transform:translate(-50%, -50%);';
          overlay.html('<div style="'+styles+'">LOADING...</div>');
        }
      }
    );
    network.once('stabilized',
      function()
      {
        element.css({'pointer-events': 'auto'});
        var overlay = element.find('div.vis-overlay');
        if (overlay)
        {
          overlay.css({'background-color': 'transparent'});
          overlay.html('');
        }
        network.fit();
      }
    );
    return network;
  }

  // Function to destroy the network.
  function destroyNetwork(network)
  {
    network.destroy();
  }

  function hideGivenNodes(nodeData, nodesToRemove)
  {   
    for (var i in nodesToRemove)
    {
      nodeData.remove(nodesToRemove[i]);
    }
  }

  function repositionRootNode(network, nodeData, rootNodeId, mode)
  {
    var positions = network.getPositions();

    if (_.isEmpty(positions))
    {
      return;
    }

    // Find the smallest x, largest y.
    var minX = positions[Object.keys(positions)[0]].x;
    var maxX = positions[Object.keys(positions)[0]].x;
    var minY = positions[Object.keys(positions)[0]].y;
    var maxY = positions[Object.keys(positions)[0]].y;
    for(var i in positions)
    {
      // Range of X-axis
      if (positions[i].x < minX)
      {
        minX = positions[i].x;
      }
      if (positions[i].x > maxX)
      {
        maxX = positions[i].x;
      }
      // Range of Y-axis.
      if (positions[i].y < minY)
      {
        minY = positions[i].y;
      }
      if (positions[i].y > maxX)
      {
        maxX = positions[i].y;
      }
    }
    
    // Update root node to be at the
    // top if downstream analysis and
    // bottom if upstream analysis.
    var updatedX = Math.ceil( (minX + maxX) / 2);
    // var updatedY = (mode==='DownStream') ? minY - 200 : maxY + 200;
    var updatedY = minY - 200;
    var rootNodeData = nodeData.get(rootNodeId);
    rootNodeData.x = updatedX;
    rootNodeData.y = updatedY;
    nodeData.update(rootNodeData);
  }

  function initOnClick(network, nodes, edges)
  {
    // remove previous onClick Event
    network.off('click');

    // Cache network data.
    var nodeArr = nodes.get();
    var edgeArr = edges.get();
    var cachedNodeArr = [];
    var cachedEdgeArr = [];
    cachedNodeArr = JSON.parse( JSON.stringify(nodeArr) );
    cachedEdgeArr = JSON.parse( JSON.stringify(edgeArr) );

    // add onClick Event
    network.on('click',function(clickData)
    {
      onClick(clickData, nodes, cachedNodeArr, edges, cachedEdgeArr);
    });

  }

  function onClick(clickData, nodes, cachedNodeArr, edges, cachedEdgeArr)
  {
    var nodeId;
    var degrees = 2;

    if ( clickData.nodes.length == 0 )
    {
      // Restore on unselect.
      nodes.update(cachedNodeArr);
      edges.update(cachedEdgeArr);
      return;
    }
    else
    {
      // Get nodes and edges as arrays.
      var nodeArr = nodes.get();
      var edgeArr = edges.get();
      // clear level of seperation in all nodes.
      clearLevel(nodeArr);
      // collect all the connected nodes we want to highlight.
      var connectedNodes = clickData.nodes;
      var connectedEdges = clickData.edges;
      // store into levels of separation - use this to define color per level.
      assignLevel(connectedNodes, 0, nodeArr);
      // redefined connected nodes.
      for (var i=1; i<degrees+1; i++)
      {
        appendConnectedNodes(connectedNodes, edgeArr);
        assignLevel(connectedNodes, i, nodeArr);
      }

      // Node editing.
      var colorLevel1 = 'rgba(200,200,200,0.65)';
      var colorLevel2 = 'rgba(200,200,200,0.15)';
      for (var i in nodeArr)
      {
        // Remove any coordinates.
        nodeArr[i].x = undefined;
        nodeArr[i].y = undefined;
        // Cache values that we are changing.

        if (nodeArr[i].color !== colorLevel1
            &&
            nodeArr[i].color !== colorLevel2)
        {
          nodeArr[i].cachedColor = nodeArr[i].color;
        }
        if (nodeArr[i].label !== '')
        {
          nodeArr[i].cachedLabel = nodeArr[i].label;
        }

        if (nodeArr[i]['inConnectionList'] == true)
        {
          if (nodeArr[i]['levelOfSeperation'] !== undefined)
          {
            if (nodeArr[i]['levelOfSeperation'] >= 2)
            {
              nodeArr[i].color = colorLevel1;
              nodeArr[i].label = nodeArr[i].cachedLabel;
            }
            else
            {
              nodeArr[i].color = nodeArr[i].cachedColor;
              nodeArr[i].label = nodeArr[i].cachedLabel;
            }
          }
        }
        else
        {
          nodeArr[i].color = colorLevel2;
          nodeArr[i].label = '    ';
        }
      }

      // Edge editing
      appendConnectedEdges(connectedEdges, clickData.nodes[0], edgeArr);
      for (var i in edgeArr)
      {
        // Cache values that we are changing.
        if (!edgeArr[i].color.inherit)
        {
          edgeArr[i].cachedColor = edgeArr[i].color;
        }
        var edgeId = edgeArr[i].id;
        if (connectedEdges.indexOf(edgeId) == -1)
        {
          edgeArr[i].color = {inherit: 'from'};
        }
        else
        {
          edgeArr[i].color = edgeArr[i].cachedColor;
        }
      }


      // Update nodes and edges.
      nodes.update(nodeArr);
      edges.update(edgeArr);
    }
  }

  function assignLevel(connectedNodes, level, nodeArr)
  {
    for (var i in connectedNodes)
    {
      var id = connectedNodes[i];
      if (nodeArr[id]['levelOfSeperation'] === undefined)
      {
        nodeArr[id]['levelOfSeperation'] = level;
      }
      nodeArr[id]['inConnectionList'] = true;
    }
  }

  function clearLevel(nodeArr)
  {
    for (var i in nodeArr)
    {
      nodeArr[i]['levelOfSeperation'] = undefined;
      nodeArr[i]['inConnectionList'] = undefined;
    }
  }

  function appendConnectedNodes(connectedNodes, edgeArr)
  {
    var tempConnectedNodes = [];
    // copy of the nodes.
    for (var i in connectedNodes)
    {
      tempConnectedNodes.push(connectedNodes[i]);
    }

    for (var i in tempConnectedNodes)
    {
      var id = tempConnectedNodes[i];
      if (connectedNodes.indexOf(id) == -1)
      {
        connectedNodes.push(id);
      }
      addUnique( getConnectedNodes(id, edgeArr), connectedNodes );
    }
    tempConnectedNodes = null;
  }

  function appendConnectedEdges(connectedEdges, selectedNodeId, edgeArr)
  {
    var tempConnectedEdges = [];
    var edgeIds = [];
    // copy of the edges, note ids that are connected with the selected node.
    for (var i in connectedEdges)
    {
      var id = connectedEdges[i];
      var additionalIds = id.split('-');
      edgeIds.push(additionalIds[0]);
      edgeIds.push(additionalIds[1]);

      tempConnectedEdges.push(connectedEdges[i]);
    }

    for (var i in edgeIds)
    {
      var id = edgeIds[i];
      addUnique( getConnectedEdges(id, edgeArr), connectedEdges );
    }
    tempConnectedEdges = null;
  }

  function getConnectedNodes(nodeId, edgeArr)
  {
    var connectedNodes = [];

    for (var i in edgeArr)
    {
      var edge = edgeArr[i];
      if (edge.to == nodeId)
      {
        connectedNodes.push(edge.from);
      }
      else if (edge.from == nodeId)
      {
        connectedNodes.push(edge.to);
      }
    }
    return connectedNodes;
  }

  function getConnectedEdges(edgeId, edgeArr)
  {
    var connectedEdges = [];

    for (var i in edgeArr)
    {
      var edge = edgeArr[i];
      if (edge.from == edgeId)
      {
        connectedEdges.push(edge.id);
      }
    }
    return connectedEdges;
  }

  function addUnique(fromArray, toArray)
  {
    for (var i = 0; i < fromArray.length; i++)
    {
      if (toArray.indexOf(fromArray[i]) == -1)
      {
        toArray.push(fromArray[i]);
      }
    }
  }

  function getNodeCoordinates(network)
  {
    return network.getPositions();
  }

  /* @ngInject */
  function Controller($scope, $element, $window, $mdMedia, $mdDialog)
  {
    $scope.showPopUp = showPopUp;

    function showPopUp(data, element)
    {
      var isSmallScreen = $mdMedia('sm') || $mdMedia('xs');
      $scope.$watch(
        function() {
          return $mdMedia('xs') || $mdMedia('sm');
        },
        function(wantsFullScreen) {
          isSmallScreen = true;
        }
      );

      var dialog = $mdDialog.show({
        controller: DialogController,
        templateUrl: data.template,
        parent: element,
        locals: {data : data},
        clickOutsideToClose: false,
        fullscreen: isSmallScreen
      });

      return dialog;
    }
  }

  function DialogController($scope, $mdDialog, data)
  {
    $scope.nodeData = {
      nodeLabel: data.nodeData.label ? data.nodeData.label : '',
      nodeFunction: data.nodeData.cctool ? data.nodeData.cctool['function'] : 'L',
      nodeControllability: data.nodeData.cctool ? data.nodeData.cctool.controllability : 'N',
      nodeVulnerability: data.nodeData.cctool ? data.nodeData.cctool.vulnerability : 'N',
      nodeImportance: data.nodeData.cctool ? data.nodeData.cctool.importance : 'N',
      nodeTags: data.nodeData.cctool && data.nodeData.cctool.tags ? data.nodeData.cctool.tags : [],
    };
    $scope.edgeData = {
      edgeLabel: data.edgeData.label ? data.edgeData.label : '',
      edgeWeight : data.edgeData.weight ? data.edgeData.weight : 'N',
      edgeTags: data.edgeData.cctool && data.edgeData.cctool.tags ? data.edgeData.cctool.tags : [],
    };

    data = { nodeData: $scope.nodeData, edgeData: $scope.edgeData};

    $scope.nodeFunctionList = ('Linear').split(' ').map(function (nodeFunction)
    {
        return {abbrev: nodeFunction};
    });
    $scope.nodeControllabilityList = ('None Low Medium High').split(' ').map(function (nodeControllability)
    {
        return {abbrev: nodeControllability};
    });
    $scope.nodeVulnerabilityList = ('None Low Medium High').split(' ').map(function (nodeVulnerability)
    {
        return {abbrev: nodeVulnerability};
    });
    $scope.nodeImportanceList = ('None Low High').split(' ').map(function (nodeImportance)
    {
        return {abbrev: nodeImportance};
    });
    $scope.edgeWeightList = ('Complex,Positive Weak,Positive Medium,Positive Strong,Negative Weak,Negative Medium,Negative Strong').split(',').map(function (edgeWeight)
    {
        return {abbrev: edgeWeight};
    });

    $scope.hide = function() {
      $mdDialog.hide();
    };
    $scope.cancel = function() {
      $mdDialog.cancel();
    };
    $scope.submit = function() {
      $mdDialog.hide(data);
    };    
  }
})();
