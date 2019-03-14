// upstream.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.upstream-analysis')
    .controller('UpstreamController', UpstreamController);

  /** @ngInject */
  function UpstreamController($scope, $log)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'UpstreamController';

    // Functions
    activate();

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
    }
  }
})();
