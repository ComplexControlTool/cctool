// menu.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.components.menu')
    .controller('MenuController', MenuController);

  /** @ngInject */
  function MenuController(isAdmin, $scope, $log, navigationService, settingsService)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'MenuController';
    vm.navItems = [];
    vm.activeSettings = settingsService.activeSettings;
    vm.sortItems = settingsService.getSortSettings();
    vm.visualItems = settingsService.getVisualSettings();
    vm.legendItems = settingsService.getLegendSettings();

    // Functions
    vm.setActiveSortingSetting = setActiveSortingSetting;
    vm.setActiveVisualisationSetting = setActiveVisualisationSetting;
    vm.setActiveLegendSetting = setActiveLegendSetting;

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });

    activate();

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
      getActiveSortingSetting();
      getActiveVisualisationSetting();
      getActiveLegendSetting();
      prepareNavigation();
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
    }

    function prepareNavigation()
    {
      var navItems = navigationService.getNavigation();
      for (var i in navItems)
      {
        if (navItems[i].admin_access)
        {
          if (isAdmin)
          {
            vm.navItems.push(navItems[i]);
          }
        }
        else
        {
          vm.navItems.push(navItems[i]);
        }
      }
    }

    function getActiveSortingSetting()
    {
      settingsService.getActiveSortSetting();
    }

    function setActiveSortingSetting(item)
    {
      settingsService.setActiveSortSetting(item.id);
    }

    function getActiveVisualisationSetting()
    {
      settingsService.getActiveVisualSetting();
    }

    function setActiveVisualisationSetting(item)
    {
      settingsService.setActiveVisualSetting(item.id);
    }

    function getActiveLegendSetting()
    {
      settingsService.getActiveLegendSetting();
    }

    function setActiveLegendSetting(value)
    {
      var item = vm.legendItems[0];
      if (!value)
      {
        item = vm.legendItems[1];
      }
      settingsService.setActiveLegendSetting(item.id);
    }

  }
})();
