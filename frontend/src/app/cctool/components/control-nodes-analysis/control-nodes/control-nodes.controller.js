// control-nodes.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.control-nodes-analysis')
    .controller('ControlNodesController', ControlNodesController);

  /** @ngInject */
  function ControlNodesController($scope, $log)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'ControlNodesController';

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
