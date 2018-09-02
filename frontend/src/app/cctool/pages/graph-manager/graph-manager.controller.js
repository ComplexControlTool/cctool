// graph-manager.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.pages.graph-manager')
    .controller('GraphManagerController', GraphManagerController);

  /** @ngInject */
  function GraphManagerController(Graphs, $scope, $log, $filter, $window, $state, settingsService)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'GraphManagerController';
    vm.activeSettings = settingsService.activeSettings;
    vm.content = Graphs.results ? Graphs.results : [];
    vm.hasNoGraphs = true;

    // Functions
    activate();
    vm.sortGraphs = sortGraphs;
    vm.saveAsImage = saveAsImage;
    vm.exportCSV = exportCSV;
    vm.exportJSON = exportJSON;
    vm.graphEdit = graphEdit;

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');

      if (_.isEmpty(vm.content))
      {
        $log.debug(vm.title+'/ Empty graphs object: '+JSON.stringify(vm.content));
        vm.hasNoGraphs = true;
        // TODO: Jump back to dashboard and show message saying Couldn't load graphs
      }
      else
      {
        $log.debug(vm.title+'/ Graphs object initialised: '+JSON.stringify(vm.content));
        vm.hasNoGraphs = false;
        watchSettings();
      }
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
    }

    function watchSettings()
    {
      $log.debug(vm.title+'/ watchSettings: Monitoring settings changes');
      $scope.$watch('graphManagerCtrl.activeSettings',
        function(newVal, oldVal)
        {
          $log.debug(vm.title+'/ graphManagerCtrl.activeSettings watch:\nnewVal: '+JSON.stringify(newVal)+'\noldVal: '+JSON.stringify(newVal));
          
          if (newVal && newVal.graphsSorting)
          {
            sortGraphs(newVal.graphsSorting);
          }
          
        },
        true)
    }

    function sortGraphs(sortConf)
    {
      if (!sortConf)
      {
        sortConf = vm.activeSettings.graphsSorting;
      }
      $log.debug(vm.title+'/ sortGraphs: Sorting graphs with config: '+JSON.stringify(sortConf));
      vm.content = $filter('orderBy')(vm.content, sortConf.value, sortConf.reversed);
    }

    function saveAsImage(graph, elemId)
    {
      $log.debug(vm.title+'/ saveAsImage: Capturing map as image with arguments:\ngraph', graph, '\nelemId:'+JSON.stringify(elemId));
      var map_element = angular.element(document.querySelector(elemId));
      
      var canvasTitle = graph.title;
      var canvasSubtitle = 'Generated by CCTool (cctool.herokuapp.com)';

      var canvasElem = map_element.find('canvas')[0];
      var ctx = canvasElem.getContext('2d');
      ctx.font = '18px Roboto';
      ctx.fillText(canvasTitle,10,30);
      ctx.font = '10px Roboto';
      ctx.fillText(canvasSubtitle,10,40);
      var imgUrl = canvasElem.toDataURL('image/png').replace(/^data:image\/[^;]*/, 'data:application/octet-stream');
      $window.open(imgUrl, '_blank');
    }

    function exportCSV(graph)
    {
      $log.debug(vm.title+'/ exportCSV: Exporting CSV of the map with arguments:\ngraph:', graph);
      var csvContent = "data:text/csv;charset=utf-8," + graph.graphgephicsv;
      var encodedUri = encodeURI(csvContent);
      $window.open(encodedUri, '_blank');
    }

    function exportJSON(graph)
    {

      $log.debug(vm.title+'/ exportJSON: Exporting JSON of the map with arguments:\ngraph:', graph);
      var jsonContent = "data:text/json;charset=utf-8," + JSON.stringify( graph.graphgephijson );
      var encodedUri = encodeURI(jsonContent);
      $window.open(encodedUri, '_blank');
    }

    function graphEdit(graph)
    {
      $log.debug(vm.title+'/ graphEdit: Going to edit mode for graph:', graph);
      $state.go('app.cctool_graphs_update_graph', {'id': graph.id});
    }

  }

})();