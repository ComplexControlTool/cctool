// stems.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.control-nodes-analysis')
    .controller('StemsController', StemsController);

  /** @ngInject */
  function StemsController($scope, $log)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'StemsController';

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
