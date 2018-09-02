// jsnxStems.directive.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.directives.jsnxStems')
    .directive('jsnxStem', jsnxStem);

  jsnxStem.$inject = ['$window', 'jsnxService', 'cctoolColorsService'];

  /* @ngInject */
  function jsnxStem($window, jsnxService, cctoolColorsService)
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
        'graph':'=ngModel',
        'stemRoot':'=stemRoot',
        'confIndex':'=confIndex',
        'nodeShape':'=nodeShape'
      }
    };
    return directive;

    function link(scope, element, attrs)
    {
      var isDrawable = false;
      var labels = '';
      var colors = cctoolColorsService.cctoolColors;
      var color = colors[5]; // (default to grey)

      var structureData = function()
      {
      // Set the variables.
      scope.id = scope.vm.graph.id;
      scope.stemRoot = scope.vm.stemRoot;
      scope.stems = scope.vm.graph.graphcontrolconfstems ? scope.vm.graph.graphcontrolconfstems[scope.vm.confIndex] : {};
      scope.structure = scope.vm.graph.graphstructure;
      scope.labels = scope.vm.graph.labels ? scope.vm.graph.labels.split(",") : '';
      scope.controllability = scope.vm.graph.controllability ? scope.vm.graph.controllability.split(" ") : '';
      scope.functions = scope.vm.graph.functions ? scope.vm.graph.functions.split(" ") : '';
      scope.controlNodes = scope.vm.graph.graphcontrolconf ? scope.vm.graph.graphcontrolconf[scope.vm.confIndex] : {};
      scope.nodeFrequency = scope.vm.graph.graphnodefrequencies ? scope.vm.graph.graphnodefrequencies : {};
      scope.element = element;

      if(scope.vm.nodeShape === 'ellipse')
      {
        labels = scope.labels;
      }
      }

      // Re-draw on data change.
      scope.$watch('vm.graph',
      function()
      {
        if(!angular.equals({}, scope.vm.graph))
        {
        isDrawable = true;
        structureData();
        try
        {
          drawStems(scope.id, scope.stemRoot, scope.stems, scope.structure, labels, scope.controllability, scope.functions, scope.controlNodes, scope.nodeFrequency, scope.element, color);
        }
        catch(error)
        {

        }
        }
      },
      true
      );

      scope.$watch('vm.confIndex',
      function(oldVal,newVal)
      {
        if(isDrawable && oldVal != newVal)
        {
        structureData();
        try
        {
          drawStems(scope.id, scope.stemRoot, scope.stems, scope.structure, labels, scope.controllability, scope.functions, scope.controlNodes, scope.nodeFrequency, scope.element, color);
        }
        catch(error)
        {

        }
        }
      }
      );

      scope.$watch('vm.nodeShape',
      function()
      {
        if(scope.vm.nodeShape === 'ellipse')
        {
        labels = scope.labels;
        }
        else
        {
        labels = '';
        }
        if(isDrawable)
        {
        try
        {
          drawStems(scope.id, scope.stemRoot, scope.stems, scope.structure, labels, scope.controllability, scope.functions, scope.controlNodes, scope.nodeFrequency, scope.element, color);
        }
        catch(error)
        {
          
        }
        }
      }
      );

    }
  }

  function drawStems(graphId, stemRoot, stemStructure, graphStructure, graphLabels, graphControllability, graphFunctions, graphControlNodes, graphNodeFrequency, stemStructureDOM, color)
  {
    // Function to construct data related to the node of the graph.
    function constructDrawNodeData(node)
    {
      var nodeData = {};

      // nodeAttr
      var defaultR = 13;
      var value = 0;
      if (graphNodeFrequency[1] && graphNodeFrequency[0][0]) {
      value = ( graphNodeFrequency[1][node] / graphNodeFrequency[0][0] ) * 15;
      }
      var radius = defaultR + value;
      nodeData.nodeAttr = radius;
      
      // nodeStyle
      var fillColor = color.nodeColor; // node circle color.
      var strokeColor = color.nodeStroke; // node circle outline color.
      var strokeWidth = 1;

      // choose green (easy) - orange (medium) - red (hard) according to controllability
      for (var i in graphControllability)
      {
      if (node == i)
      {
        switch(graphControllability[i])
        {
        case "E":
          fillColor = color.easynodeColor;
          strokeColor = color.easynodeStrokeColor;
          break;
        case "M":
          fillColor = color.mednodeColor;
          strokeColor = color.mednodeStrokeColor;
          break;
        case "H":
          fillColor = color.hardnodeColor;
          strokeColor = color.hardnodeStrokeColor;
          break;
        }
        break;
      }
      }

      // choose a lighter fill color for control nodes.
      for (var i in graphControlNodes)
      {
      if (node == graphControlNodes[i])
      {
        fillColor = color.ctrlnodeColor;
        strokeWidth = 2;
        break;
      }
      }

      nodeData.nodeStyleFill = fillColor;
      nodeData.nodeStyleStroke = strokeColor;
      nodeData.nodeStyleStrokeWidth = strokeWidth;

      return nodeData;
    };

    // Function to construct data related to the edge of the graph.
    function constructDrawEdgeData(edge)
    {
      var edgeData = {};

      var label = '';
      var sign = '>';
      var fillColor = color.nodeStroke; // node link color.
      var strokeWidth = 7;
      var linkDistance = 140;
      
      // Current node.
      var edgeFrom = graphStructure[edge[0]];
      // In the weights dictionary, get the connections.
      for (var edgeTo in edgeFrom)
      {
      if ( edgeFrom[edgeTo][0] === (+edge[1]) )
      {
        label = edgeFrom[edgeTo][1];
        // Get the value of the weight and return a color.
        switch ( edgeFrom[edgeTo][1] )
        {
        case "+W":
          sign = '+';
          fillColor = color.weakplus;
          strokeWidth = 6;
          linkDistance = 180;
          break;
        case "+M":
          sign = '+';
          fillColor = color.mediumplus;
          strokeWidth = 7;
          linkDistance = 140;
          break;
        case "+S":
          sign = '+';
          fillColor = color.strongplus;
          strokeWidth = 8;
          linkDistance = 100;
          break;
        case "-W":
          sign = '-';
          fillColor = color.weakminus;
          strokeWidth = 6;
          linkDistance = 180;
          break;
        case "-M":
          sign = '-';
          fillColor = color.mediumminus;
          strokeWidth = 7;
          linkDistance = 140;
          break;
        case "-S":
          sign = '-';
          fillColor = color.strongminus;
          strokeWidth = 8;
          linkDistance = 100;
          break;
        }
        break;
      }
      }
      edgeData.edgeLabel = label;
      edgeData.edgeSign = sign;
      edgeData.edgeStyleFill = fillColor;
      edgeData.edgeStyleStroke = strokeWidth;
      edgeData.edgeLinkDistance = linkDistance;

      return edgeData;
    };

    var stemFillColor = color.nodeColor; // node circle color.;
    var stemStrokeColor = color.nodeStroke; // node circle outline color.;
    var stemStrokeWidth = 1;
    var linkFillColor = color.nodeStroke; // node link color.

    var stem = stemRoot;
    var drawNodeData = constructDrawNodeData(stem);
    var drawEdgeData = {};

    if(graphLabels)
    {
      var stems = getStemLabelTemplate(graphLabels[stem],drawNodeData.nodeStyleFill,drawNodeData.nodeStyleStroke,drawNodeData.nodeStyleStrokeWidth);
    }
    else
    {
      var stems = getStemGraphicTemplate(stem,drawNodeData.nodeStyleFill,drawNodeData.nodeStyleStroke,drawNodeData.nodeStyleStrokeWidth);
    }
    while(true)
    {
      var potentialStem = stemStructure[stem];
      // Check if undefined.
      if (!potentialStem)
      {
      break;
      }
      // Check if the node points to the same node.
      if (stem === potentialStem)
      {
      break;
      }
      // Check if the node (a) points to node (b) and node (b) points to node (a). 
      if (stem === stemStructure[potentialStem])
      {
      break;
      }
      drawEdgeData = constructDrawEdgeData([stem,potentialStem]);
      stem = parseInt(potentialStem);
      drawNodeData = constructDrawNodeData(stem);

      if(graphLabels)
      {
      stems += getLinkLabelTemplate(drawEdgeData.edgeStyleFill,drawEdgeData.edgeSign);
      stems += getStemLabelTemplate(graphLabels[stem],drawNodeData.nodeStyleFill,drawNodeData.nodeStyleStroke,drawNodeData.nodeStyleStrokeWidth);
      }
      else
      {
      stems += getLinkGraphicTemplate(drawEdgeData.edgeStyleFill);
      stems += getStemGraphicTemplate(stem,drawNodeData.nodeStyleFill,drawNodeData.nodeStyleStroke,drawNodeData.nodeStyleStrokeWidth);              
      }
    }
    stemStructureDOM.html(stems);
  }

  function getStemGraphicTemplate(label, fillColor, strokeColor, strokeWidth)
  {
    return '<svg class="jsnx" width="30px" height="30px" style="opacity: 1;"><g><g class="nodes"><g class="node" transform="translate(15,15)scale(1)"><circle class="node-shape" r="13" style="stroke:'+strokeColor+'; fill:'+fillColor+'; stroke-width:'+strokeWidth+';"></circle><text style="text-anchor: middle; dominant-baseline: central; cursor: pointer; -webkit-user-select: none; fill: #ffffff; font-size: 15px; font-weight: bold; font-variant: small-caps;">'+label+'</text></g></g></g></svg>';
  }

  function getStemLabelTemplate(label, fillColor, strokeColor, strokeWidth)
  {
    return '<div class="chip" style="background:'+fillColor+'; border:'+strokeWidth+'px solid '+strokeColor+';"><div class="chip-content"><span>'+label+'</span></div></div>';
  }

  function getLinkGraphicTemplate(fillColor)
  {
    return '<svg class="jsnx" width="42px" height="30px" style="opacity: 1;"><g><g class="edges"><g class="edge" transform="translate(-21,15)"><path class="line" d="M 21.5 0 L 21.5 -3 L 50.901531782132565 -3 L 50.901531782132565 -6 L 62.901531782132565 0 z" style="fill:'+fillColor+'; stroke-width: 0px;"></path></g></g></g></svg>';
  }

  function getLinkLabelTemplate(fillColor, sign)
  {
    return '<div class="chip-sign" style="color:'+fillColor+'">'+sign+'</div>';
  }

  /* @ngInject */
  function Controller()
  {

  }
})();