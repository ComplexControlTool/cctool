// app.config.js
(function()
{
  'use strict';

  angular
    .module('appdashboard')
    .config(config);

  config.$inject = ['$logProvider', '$compileProvider', '$httpProvider'];

  /** @ngInject */
  function config($logProvider, $compileProvider, $httpProvider)
  {
    // Enable log
    $logProvider.debugEnabled(true);
    $compileProvider.debugInfoEnabled(true);
    $httpProvider.useApplyAsync(true);
  }

})();
