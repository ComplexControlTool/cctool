// downstream.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.downstream-analysis')
    .controller('DownstreamController', DownstreamController);

  /** @ngInject */
  function DownstreamController($scope, $log)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'DownstreamController';

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
