// cctool.run.js
(function()
{
  'use strict';

  angular
    .module('app.cctool')
    .run(runBlock);

  runBlock.$inject = ['$log', 'Analytics', 'cctoolParams'];

  /** @ngInject */
  function runBlock($log, Analytics, cctoolParams)
  {
    $log.debug('runBlock end');
    Analytics.set('&uid', cctoolParams.userId);
  }

})();
