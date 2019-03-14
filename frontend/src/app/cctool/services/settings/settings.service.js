// settings.service.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.services.settings')
    .service('settingsService', SettingsService);

  SettingsService.$inject = ['$cookies'];

  /* @ngInject */
  function SettingsService($cookies)
  {
    var cookieSortSettingsKey = 'cctool-sort-graph-by';
    var cookieVisualSettingsKey = 'cctool-visual-graph';
    var activeSettings =
    {
      graphsSorting: undefined,
      graphVisualisation: undefined
    }
    var sortSettings =
    [
      {id:'sort_by_name_a', label:'Title', text:'Title (Ascending)', icon: 'sort', value:'title', reversed:0, default:1, active:1},
      {id:'sort_by_name_d', label:'Title', text:'Title (Descending)', icon: 'sort', value:'title', reversed:1, default:0, active:0},
      {id:'sort_by_date_created_a', label:'Date created', text:'Date created (Ascending)', icon: 'sort', value:'createdAt', reversed:0, default:0, active:0},
      {id:'sort_by_date_created_d', label:'Date created', text:'Date created (Descending)', icon: 'sort', value:'createdAt', reversed:1, default:0, active:0},
      {id:'sort_by_date_updated_a', label:'Date updated', text:'Date updated (Ascending)', icon: 'sort', value:'updatedAt', reversed:0, default:0, active:0},
      {id:'sort_by_date_updated_d', label:'Date updated', text:'Date updated (Descending)', icon: 'sort', value:'updatedAt', reversed:1, default:0, active:0}
    ];
    var visualSettings =
    [
      {id:'visual_circle', label:'Circle', text:'Circle with text underneath', value:'dot', default: 0, active:0},
      {id:'visual_ellipse', label:'Ellipse', text:'Ellipse with text', value:'ellipse', default: 1, active:1},
    ];

    this.activeSettings = activeSettings;

    this.getSettings = getSettings;
    this.getSortSettings = getSortSettings;
    this.getVisualSettings = getVisualSettings;
    this.getActiveSortSetting = getActiveSortSetting;
    this.setActiveSortSetting = setActiveSortSetting;
    this.getActiveVisualSetting = getActiveVisualSetting;
    this.setActiveVisualSetting = setActiveVisualSetting;

    ////////////////

    function getSettings()
    {
      var settings = { graphsSorting:getSortSettings(),
                       graphVisualisation:getVisualSettings() };

      return settings;
    }

    function getSortSettings()
    {
      return sortSettings;
    }

    function getVisualSettings()
    {
      return visualSettings;
    }

    function getActiveSortSetting()
    {
      // Retrieve from cookie if present.
      var cachedValue = $cookies.getObject(cookieSortSettingsKey);
      // Loop through the settings,
      for (var i in sortSettings)
      {
        var item = sortSettings[i];
        if (item.active)
        {
          if (!cachedValue)
          {
            // If it is active (default) and there is no cache value.
            activeSettings.graphsSorting = item;
            return;
          }
          else
          {
            // Remove predefined active.
            item.active = 0;
          }
        }
        if (item.id === cachedValue)
        {
          // Save new active and return.
          item.active = 1;
          activeSettings.graphsSorting = item;
          return;
        }
      }
    }

    function setActiveSortSetting(sortItemId)
    {
      // Loop through the settings,
      for (var i in sortSettings)
      {
        var item = sortSettings[i];
        if (item.active)
        {
          // Remove old active.
          item.active = 0;
        }
        if (item.id === sortItemId)
        {
          // Set new active and save in cookie.
          item.active = 1;
          activeSettings.graphsSorting = item;
          $cookies.putObject(cookieSortSettingsKey, item.id);
        }
      }
    }

    function getActiveVisualSetting()
    {
      // Retrieve from cookie if present.
      var cachedValue = $cookies.getObject(cookieVisualSettingsKey);
      // Loop through the settings,
      for (var i in visualSettings)
      {
        var item = visualSettings[i];
        if (item.active)
        {
          if (!cachedValue)
          {
            // If it is active (default) and there is no cache value.
            activeSettings.graphVisualisation = item;
            return;
          }
          else
          {
            // Remove predefined active.
            item.active = 0;
          }
        }
        if (item.id === cachedValue)
        {
          // Save new active and return.
          item.active = 1;
          activeSettings.graphVisualisation = item;
          return;
        }
      }
    }

    function setActiveVisualSetting(sortItemId)
    {
      // Loop through the settings,
      for (var i in visualSettings)
      {
        var item = visualSettings[i];
        if (item.active)
        {
          // Remove old active.
          item.active = 0;
        }
        if (item.id === sortItemId)
        {
          // Set new active and save in cookie.
          item.active = 1;
          activeSettings.graphVisualisation = item;
          $cookies.putObject(cookieVisualSettingsKey, item.id);
        }
      }
    }
  }
})();