// graph.service.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.services.graph')
    .service('graphService', graphService);

  /* @ngInject */
  function graphService($log, $rootScope, $interval, apiResolver)
  {
    /* jshint validthis: true */
    var vm = this;
    
    // Data
    vm.title = 'graphService';
    var intervalObj = undefined;
    var monitoredGraph = undefined;
    var lastUpdatedDate = undefined;
    var lastUpdatedGraph = undefined;
    var ignoredUpdateDates = [];

    // Functions
    activate();
    vm.initMonitorUpdates = initMonitorUpdates;
    vm.stopMonitorUpdates = stopMonitorUpdates;
    vm.getLatestUpdate = getLatestUpdate;
    vm.ignoreUpdate = ignoreUpdate;

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' service!');
    }

    function initMonitorUpdates(graph, interval)
    {
      $log.debug(vm.title+'/initMonitorUpdates with graph',graph,' and interval',interval);
      stopMonitorUpdates();

      if (graph)
      {
        monitoredGraph = graph;
      }

      if (!interval)
      {
        interval = 2000;
      }

      if (monitoredGraph)
      {
        $log.debug(vm.title+'/initMonitorUpdates using graph: ',monitoredGraph);
        intervalObj = $interval(function(){requestAndNotify(monitoredGraph.id)},
                                interval);
      }
    }

    function stopMonitorUpdates()
    {
      $log.debug(vm.title+'/stopMonitorUpdates');
      if (angular.isDefined(intervalObj))
      {
        $interval.cancel(intervalObj);
        intervalObj = undefined;
        monitoredGraph = undefined;
        ignoredUpdateDates = [];
      }
    }

    function requestAndNotify(graphId)
    {
      $log.debug(vm.title+'/requestAndNotify with graphId',graphId);
      var currentUpdatedDate = monitoredGraph.updatedAt;
      apiResolver.resolve('cctool.graph.dateupdated@get', {'id': graphId}).then(
        function(data)
        {
          $log.debug(vm.title+'/requestAndNotify api call success with data',data);
          if (data && data.updatedAt)
          {
            lastUpdatedDate = data.updatedAt;
            if (currentUpdatedDate !== lastUpdatedDate && ignoredUpdateDates.indexOf(lastUpdatedDate) == -1)
            {
              apiResolver.resolve('cctool.graph.full@get', {'id': graphId}).then(
                function(data)
                {
                  $log.debug(vm.title+'/requestAndNotify api call success with data',data);
                  if (data)
                  {
                    $log.debug(vm.title+'/requestAndNotify updates available for graphId',graphId);
                    monitoredGraph = lastUpdatedGraph = data
                    $rootScope.$broadcast('graph:hasUpdates',lastUpdatedDate);
                  }
                },
                function(err)
                {
                  $log.debug(vm.title+'/requestAndNotify api call unsuccessful.');
                  return false; 
                });
            }
          }
        },
        function(err)
        {
          $log.debug(vm.title+'/requestAndNotify api call unsuccessful.');
          return false; 
        });
    }

    function getLatestUpdate()
    {
      $log.debug(vm.title+'/getLatestUpdate');
      if (lastUpdatedGraph)
      {
        monitoredGraph = lastUpdatedGraph;
      }
      return monitoredGraph;
    }

    function ignoreUpdate()
    {
      $log.debug(vm.title+'/ignoreUpdate');
      if (!lastUpdatedDate)
      {
        return;
      }

      ignoredUpdateDates.push(lastUpdatedDate);
    }

  }
})();