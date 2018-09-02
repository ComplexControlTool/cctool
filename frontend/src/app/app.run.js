// app.run.js
(function()
{
  'use strict';

  angular
    .module('appdashboard')
    .run(runBlock);

  runBlock.$inject = ['$log'];

  /** @ngInject */
  function runBlock($log)
  {
    $log.debug('runBlock end');
  }

})();
