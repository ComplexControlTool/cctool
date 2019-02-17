// controllability-analysis.service.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.services.controllability-analysis')
    .service('controllabilityAnalysisService', controllabilityAnalysisService);

  /* @ngInject */
  function controllabilityAnalysisService($log, $rootScope, $interval, apiResolver)
  {
    /* jshint validthis: true */
    var vm = this;
    
    // Data
    vm.title = 'controllabilityAnalysisService';
    var intervalObj = undefined;
    var monitoredAnalysis = undefined;
    var monitoredGraphId = undefined;

    // Functions
    activate();
    vm.initMonitorUpdates = initMonitorUpdates;
    vm.stopMonitorUpdates = stopMonitorUpdates;
    vm.getLatestUpdate = getLatestUpdate;

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' service!');
    }

    function initMonitorUpdates(graphId, interval)
    {
      $log.debug(vm.title+'/initMonitorUpdates for Controllability analysis with graph id',graphId,' and interval',interval);
      stopMonitorUpdates();

      if (graphId)
      {
        monitoredGraphId = graphId;
      }

      if (!interval)
      {
        interval = 2000;
      }

      if (monitoredGraphId)
      {
        $log.debug(vm.title+'/initMonitorUpdates for Controllability analysis with graph',monitoredGraphId);
        intervalObj = $interval(function(){requestAndNotify(monitoredGraphId)},
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
        monitoredAnalysis = undefined;
        monitoredGraphId = undefined;
      }
    }

    function requestAndNotify(graphId)
    {
      $log.debug(vm.title+'/requestAndNotify with graphId',graphId);
      var isAnalysed = false;
      var analysisType = 'Controllability';
      apiResolver.resolve('cctool.analysis.analysed@query', {'graphId': graphId, 'analysisType': analysisType}).then(
        function(data)
        {
          $log.debug(vm.title+'/requestAndNotify api call success with data',data);
          if (data && data[0])
          {
            isAnalysed = data[0].isAnalysed;
            if (isAnalysed)
            {
              apiResolver.resolve('cctool.analysis.full@query', {'graphId': graphId, 'analysisType': analysisType}).then(
                function(data)
                {
                  $log.debug(vm.title+'/requestAndNotify api call success with data',data);
                  if (data && data[0])
                  {
                    $log.debug(vm.title+'/requestAndNotify updates available for Controllability analysis with graph id',graphId);
                    monitoredAnalysis = data[0];
                    $rootScope.$broadcast('controllabilityAnalysis:hasUpdates',monitoredAnalysis);
                  }
                },
                function(err)
                {
                  $log.debug(vm.title+'/requestAndNotify api call unsuccessful.');
                  return false; 
                });
            }
            else
            {
              console.log('** HERE **');
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
      if (monitoredAnalysis.isAnalysed)
      {
        return monitoredAnalysis;
      }
      return false;
    }

  }
})();