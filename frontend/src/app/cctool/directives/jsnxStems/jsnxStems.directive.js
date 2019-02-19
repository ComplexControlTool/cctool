// jsnxStems.directive.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.directives.jsnxStems')
    .directive('jsnxStem', jsnxStem);

  /* @ngInject */
  function jsnxStem($log, $window, jsnxService, cctoolColorsService)
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
        'stemRoot':'=stemRoot',
        'structure':'=structure',
        'analysis':'=analysis',
        'confIndex':'=confIndex',
        'nodeShape':'=nodeShape'
      }
    };
    return directive;

    function link(scope, element, attrs)
    {
      var isDrawable = false;
      var colors = cctoolColorsService.cctoolColors;
      var color = colors[5]; // (default to grey)

      var structureData = function()
      {
        // Set the variables.
        scope.stemRoot = scope.vm.stemRoot;
        scope.structure = scope.vm.structure;
        scope.stems = scope.vm.analysis && scope.vm.analysis.data.stems && scope.vm.analysis.typeOfAnalysis == 'Controllability' ? scope.vm.analysis.data.stems[scope.vm.confIndex] : {};
        scope.controlConfiguration = scope.vm.analysis && scope.vm.analysis.data.controlConfigurations && scope.vm.analysis.typeOfAnalysis == 'Controllability' ? scope.vm.analysis.data.controlConfigurations[scope.vm.confIndex] : {};
        scope.nodeShape = scope.vm.nodeShape;
        scope.element = element;
      }

      // Re-draw on data change.
      scope.$watch('vm.structure',
        function()
        {
          $log.debug('watch: vm.structure');
          if(!_.isEmpty(scope.vm.structure))
          {
            isDrawable = true;
            structureData();
            try
            {
              drawStems(scope.stemRoot, scope.structure, scope.stems, scope.controlConfiguration, scope.nodeShape, scope.element, color);
            }
            catch(error)
            {
              $log.error('Failed to init/update stems with error',error);
            }
          }
          else
          {
            isDrawable = false;
          }
        },
        true
      );

      // Re-draw on data change.
      scope.$watch('vm.analysis',
        function()
        {
          $log.debug('watch: vm.analysis');
          if(!_.isEmpty(scope.vm.analysis))
          {
            isDrawable = true;
            structureData();
            try
            {
              drawStems(scope.stemRoot, scope.structure, scope.stems, scope.controlConfiguration, scope.nodeShape, scope.element, color);
            }
            catch(error)
            {
              $log.error('Failed to init/update stems with error',error);
            }
          }
          else
          {
            isDrawable = false;
          }
        },
        true
      );

      scope.$watch('vm.confIndex',
        function(oldVal,newVal)
        {
          $log.debug('watch: vm.confIndex');
          if(isDrawable && oldVal != newVal)
          {
            structureData();
            try
            {
              drawStems(scope.stemRoot, scope.structure, scope.stems, scope.controlConfiguration, scope.nodeShape, scope.element, color);
            }
            catch(error)
            {
              $log.error('Failed to init/update stems with error',error);
            }
          }
        }
      );

      scope.$watch('vm.nodeShape',
        function(oldVal,newVal)
        {
          $log.debug('watch: vm.nodeShape');
          if(isDrawable && oldVal != newVal)
          {
            structureData();
            try
            {
              drawStems(scope.stemRoot, scope.structure, scope.stems, scope.controlConfiguration, scope.nodeShape, scope.element, color);
            }
            catch(error)
            {
              $log.error('Failed to init/update stems with error',error);
            }
          }
        }
      );

    }
  }

  // graphId, graphFunctions to delete
  function drawStems(stemRoot, structure, stems, controlConfiguration, nodeShape, stemStructureDOM, color)
  {
    // Function to construct data related to the node of the graph.
    function constructDrawNodeData(node)
    {
      var nodeData = {};
      
      // nodeStyle
      var id = node.id;
      var label = node.label;
      var fillColor = node.color.background; // node circle color.
      var strokeColor = node.color.border; // node circle outline color.
      var strokeWidth = node.borderWidth;

      // choose a lighter fill color for control nodes.
      for (var i in controlConfiguration)
      {
        if (node.id == controlConfiguration[i])
        {
          fillColor = color.ctrlnodeColor;
          strokeWidth = 2;
          break;
        }
      }

      nodeData.nodeId = id;
      nodeData.nodeLabel = label;
      nodeData.nodeStyleFill = fillColor;
      nodeData.nodeStyleStroke = strokeColor;
      nodeData.nodeStyleStrokeWidth = strokeWidth;

      return nodeData;
    };

    // Function to construct data related to the edge of the graph.
    function constructDrawEdgeData(nodeIdFrom, nodeIdTo)
    {
      var edgeData = {};
      
      // Find edge
      var edge = undefined;
      for (var i in structure.edges)
      {
        edge = structure.edges[i];
        if (edge.from == nodeIdFrom && edge.to == nodeIdTo)
        {
          break;
        }
      }

      if (edge == undefined)
      {
        return;
      }

      var fillColor = edge.color.color;
      var sign = '>';
      if (edge.cctool.weight.indexOf('+') != -1)
      {
        sign = '+';
      }
      else if (edge.cctool.weight.indexOf('-') != -1)
      {
        sign = '-';
      }

      edgeData.edgeSign = sign;
      edgeData.edgeStyleFill = fillColor;

      return edgeData;
    };

    var drawNodeData = constructDrawNodeData(structure.nodes[stemRoot]);
    var drawEdgeData = {};

    if(nodeShape === 'ellipse')
    {
      var stemChain = getStemLabelTemplate(drawNodeData.nodeLabel, drawNodeData.nodeStyleFill, drawNodeData.nodeStyleStroke, drawNodeData.nodeStyleStrokeWidth);
    }
    else
    {
      var stemChain = getStemGraphicTemplate(drawNodeData.nodeId, drawNodeData.nodeStyleFill, drawNodeData.nodeStyleStroke, drawNodeData.nodeStyleStrokeWidth);
    }

    while(true)
    {
      var potentialStem = stems[stemRoot];

      // Check if undefined.
      if (potentialStem == undefined)
      {
        break;
      }

      // Check if the node points to the same node.
      if (stemRoot === potentialStem)
      {
        break;
      }

      // Check if the node (a) points to node (b) and node (b) points to node (a). 
      if (stemRoot === stems[potentialStem])
      {
        break;
      }

      drawEdgeData = constructDrawEdgeData(stemRoot,potentialStem);
      stemRoot = parseInt(potentialStem);
      drawNodeData = constructDrawNodeData(structure.nodes[stemRoot]);

      if(nodeShape === 'ellipse')
      {
        stemChain += getLinkLabelTemplate(drawEdgeData.edgeStyleFill, drawEdgeData.edgeSign);
        stemChain += getStemLabelTemplate(drawNodeData.nodeLabel, drawNodeData.nodeStyleFill, drawNodeData.nodeStyleStroke, drawNodeData.nodeStyleStrokeWidth);
      }
      else
      {
        stemChain += getLinkGraphicTemplate(drawEdgeData.edgeStyleFill);
        stemChain += getStemGraphicTemplate(drawNodeData.nodeId, drawNodeData.nodeStyleFill, drawNodeData.nodeStyleStroke, drawNodeData.nodeStyleStrokeWidth);              
      }
    }
    stemStructureDOM.html(stemChain);
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