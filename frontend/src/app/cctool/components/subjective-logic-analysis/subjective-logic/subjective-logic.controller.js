// subjective-logic.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.subjective-logic-analysis')
    .controller('SubjectiveLogicController', SubjectiveLogicController);

  /** @ngInject */
  function SubjectiveLogicController($scope, $log)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'SubjectiveLogicController';

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
