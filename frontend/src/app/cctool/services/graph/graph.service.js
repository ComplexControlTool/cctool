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
    var monitoredGraphIsProgressed = false;
    var monitoredGraphTaskInterval = 500;
    var monitoredGraphUpdatesInterval = 60000;
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

    function initMonitorUpdates(graph, taskInterval, updatesInterval)
    {
      $log.debug(vm.title+'/initMonitorUpdates');
      stopMonitorUpdates();

      if (graph && !monitoredGraph)
      {
        monitoredGraph = graph;
      }

      if (taskInterval)
      {
        monitoredGraphTaskInterval = taskInterval;
      }

      if (updatesInterval)
      {
        monitoredGraphUpdatesInterval = updatesInterval;
      }

      if (monitoredGraph)
      {
        monitoredGraphIsProgressed = monitoredGraph.isProcessed;
        var interval = monitoredGraphIsProgressed ? monitoredGraphUpdatesInterval : monitoredGraphTaskInterval;
        $log.debug(vm.title+'/initMonitorUpdates with graph id: '+monitoredGraph.id+' every '+interval+' milliseconds');
        intervalObj = $interval(
          function()
          {
            requestAndNotify(monitoredGraph.id)
          },
          interval
         );
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
        monitoredGraphIsProgressed = false;
        ignoredUpdateDates = [];
      }
    }

    function requestAndNotify(graphId)
    {
      $log.debug(vm.title+'/requestAndNotify with graph id: '+graphId);
      var currentUpdatedDate = monitoredGraph.updatedAt;

      apiResolver.resolve('cctool.graph.dateupdated@get', {'id': graphId}).then(
        function(data)
        {
          $log.debug(vm.title+'/requestAndNotify api call success with data',data);
          if (data && data.updatedAt)
          {
            monitoredGraphIsProgressed = data.isProcessed;
            if (monitoredGraphIsProgressed)
            {
              if (currentUpdatedDate !== lastUpdatedDate && ignoredUpdateDates.indexOf(lastUpdatedDate) == -1)
              {
                apiResolver.resolve('cctool.graph.full@get', {'id': graphId}).then(
                  function(data)
                  {
                    $log.debug(vm.title+'/requestAndNotify api call success with data',data);
                    if (data)
                    {
                      $log.debug(vm.title+'/requestAndNotify updates available for graph id: '+graphId);
                      monitoredGraph = lastUpdatedGraph = data
                      lastUpdatedDate = data.updatedAt;
                      $rootScope.$broadcast('graph:hasUpdates',lastUpdatedDate);
                      $log.debug(vm.title+'/requestAndNotify resetting monitoring...');
                      initMonitorUpdates(monitoredGraph);
                    }
                  },
                  function(err)
                  {
                    $log.debug(vm.title+'/requestAndNotify api call unsuccessful.');
                    return false; 
                  });
              }
            }
            else
            {
              lastUpdatedDate = undefined;

              apiResolver.resolve('cctool.graph.map@get', {'id': graphId}).then(
                function(data)
                {
                  $log.debug(vm.title+'/requestAndNotify api call success with data',data);
                  $log.debug(vm.title+'/requestAndNotify resetting monitoring...');
                  initMonitorUpdates(monitoredGraph);
                },
                function(err)
                {
                  $log.debug(vm.title+'/requestAndNotify api call unsuccessful!');
                  return false;
                });
              apiResolver.resolve('cctool.graph.visualize@get', {'id': graphId}).then(
                function(data)
                {
                  $log.debug(vm.title+'/requestAndNotify api call success with data',data);
                  $log.debug(vm.title+'/requestAndNotify resetting monitoring...');
                  initMonitorUpdates(monitoredGraph);
                },
                function(err)
                {
                  $log.debug(vm.title+'/requestAndNotify api call unsuccessful!');
                  return false;
                });
            }
          }
        },
        function(err)
        {
          $log.debug(vm.title+'/requestAndNotify api call unsuccessful!');
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