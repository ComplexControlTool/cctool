// graphs.service.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.services.graphs')
    .service('graphsService', graphsService);

  /* @ngInject */
  function graphsService($log, $rootScope, $interval, apiResolver)
  {
    /* jshint validthis: true */
    var vm = this;
    
    // Data
    vm.title = 'graphsService';
    var intervalObj = undefined;
    var monitoredGraphs = undefined;
    var lastUpdatedGraphs = undefined;

    // Functions
    activate();
    vm.initMonitorUpdates = initMonitorUpdates;
    vm.stopMonitorUpdates = stopMonitorUpdates;
    vm.getLatestUpdate = getLatestUpdate;

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' service!');
    }

    function initMonitorUpdates(graphs, ignoredFields, interval)
    {
      $log.debug(vm.title+'/initMonitorUpdates with graphs',graphs,' and interval',interval);
      stopMonitorUpdates();

      if (graphs)
      {
        monitoredGraphs = graphs;
      }

      if (!interval)
      {
        interval = 2000;
      }

      if (monitoredGraphs)
      {
        $log.debug(vm.title+'/initMonitorUpdates using graphs: ',monitoredGraphs);
        intervalObj = $interval(function(){requestAndNotify(ignoredFields)},
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
        monitoredGraphs = undefined;
      }
    }

    function requestAndNotify(ignoredFields)
    {
      $log.debug(vm.title+'/requestAndNotify');
      apiResolver.resolve('cctool.graphs.basic@query').then(
        function(data)
        {
          $log.debug(vm.title+'/requestAndNotify api call success with data',data);
          if (data)
          {
            var compareDict = angular.copy(monitoredGraphs)
            for (var i in compareDict)
            {
              for (var j in ignoredFields)
              {
                delete compareDict[i][ignoredFields[j]];
              }
            }
            if (angular.toJson(compareDict) !== angular.toJson(data))
            {
              $log.debug(vm.title+'/requestAndNotify updates available');
              monitoredGraphs = lastUpdatedGraphs = data;
              $rootScope.$broadcast('graphs:hasUpdates',lastUpdatedGraphs);
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
      if (lastUpdatedGraphs)
      {
        monitoredGraphs = lastUpdatedGraphs;
      }
      return monitoredGraphs;
    }

  }
})();