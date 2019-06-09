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
    var monitoredGraphId = undefined;
    var monitoredAnalysis = undefined;
    var monitoredAnalysisIsAnalysed = false;
    var monitoredAnalysisTaskInterval = 30000;
    var monitoredAnalysisUpdatesInterval = 90000;
    var lastUpdatedDate = undefined;

    // Functions
    activate();
    vm.initMonitorUpdates = initMonitorUpdates;
    vm.stopMonitorUpdates = stopMonitorUpdates;
    vm.getLatestUpdate = getLatestUpdate;

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' service!');
    }

    function initMonitorUpdates(graphId, analysis, taskInterval, updatesInterval)
    {
      $log.debug(vm.title+'/initMonitorUpdates');
      stopMonitorUpdates();

      if (graphId && !monitoredGraphId)
      {
        monitoredGraphId = graphId;
      }

      if (analysis && !monitoredAnalysis)
      {
        monitoredAnalysis = analysis;
      }

      if (taskInterval)
      {
        monitoredAnalysisTaskInterval = taskInterval;
      }

      if (updatesInterval)
      {
        monitoredAnalysisUpdatesInterval = updatesInterval;
      }

      if (monitoredGraphId)
      {
        monitoredAnalysisIsAnalysed = monitoredAnalysis ? monitoredAnalysis.isAnalysed : monitoredAnalysisIsAnalysed;
        var interval = monitoredAnalysisIsAnalysed ? monitoredAnalysisUpdatesInterval : monitoredAnalysisTaskInterval;
        $log.debug(vm.title+'/initMonitorUpdates with graph id: '+monitoredGraphId+' every '+interval+' milliseconds');
        intervalObj = $interval(
          function()
          {
            requestAndNotify(monitoredGraphId)
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
        monitoredGraphId = undefined;
        monitoredAnalysis = undefined;
        monitoredAnalysisIsAnalysed = undefined;
      }
    }

    function requestAndNotify(graphId)
    {
      $log.debug(vm.title+'/requestAndNotify with graph id: '+graphId);
      var analysisType = 'Controllability Analysis';
      var currentUpdatedDate = monitoredAnalysis ? monitoredAnalysis.updatedAt : '';

      apiResolver.resolve('cctool.analysis.analysed@query', {'graphId': graphId, 'analysisType': analysisType}).then(
        function(data)
        {
          $log.debug(vm.title+'/requestAndNotify api call success with data',data);
          if (data && data[0])
          {
            monitoredAnalysisIsAnalysed = data[0].isAnalysed;
            if (monitoredAnalysisIsAnalysed)
            {
              if (currentUpdatedDate !== lastUpdatedDate)
              {
                apiResolver.resolve('cctool.analysis.full@query', {'graphId': graphId, 'analysisType': analysisType}).then(
                  function(data)
                  {
                    $log.debug(vm.title+'/requestAndNotify api call success with data',data);
                    if (data && data[0])
                    {
                      $log.debug(vm.title+'/requestAndNotify updates available for graph id: '+graphId);
                      monitoredAnalysis = data[0];
                      lastUpdatedDate = data[0].updatedAt;
                      $rootScope.$broadcast('controllabilityAnalysis:hasUpdates',monitoredAnalysis);
                      $log.debug(vm.title+'/requestAndNotify resetting monitoring...');
                      initMonitorUpdates(graphId, monitoredAnalysis);
                    }
                  },
                  function(err)
                  {
                    $log.debug(vm.title+'/requestAndNotify api call unsuccessful!');
                    return false; 
                  });
              }
            }
            else
            {
              apiResolver.resolve('cctool.graph.analyse@get', {'id': graphId, 'analysisType': analysisType}).then(
                function(data)
                {
                  $log.debug(vm.title+'/requestAndNotify api call success with data',data);
                  $log.debug(vm.title+'/requestAndNotify resetting monitoring...');
                  initMonitorUpdates(graphId, monitoredAnalysis);
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
      return monitoredAnalysis;
    }

  }
})();