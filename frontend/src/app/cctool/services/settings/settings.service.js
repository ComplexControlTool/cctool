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
    var cookieLegendSettingsKey = 'cctool-legend-graph';
    var activeSettings =
    {
      graphsSorting: undefined,
      graphVisualisation: undefined,
      graphLegend: undefined
    }
    var sortSettings =
    [
      {id:'sort_by_name_a', label:'Title', text:'Title (Ascending)', icon: 'sort', value:'title', reversed:0, active:1},
      {id:'sort_by_name_d', label:'Title', text:'Title (Descending)', icon: 'sort', value:'title', reversed:1, active:0},
      {id:'sort_by_date_created_a', label:'Date created', text:'Date created (Ascending)', icon: 'sort', value:'createdAt', reversed:0, active:0},
      {id:'sort_by_date_created_d', label:'Date created', text:'Date created (Descending)', icon: 'sort', value:'createdAt', reversed:1, active:0},
      {id:'sort_by_date_updated_a', label:'Date updated', text:'Date updated (Ascending)', icon: 'sort', value:'updatedAt', reversed:0, active:0},
      {id:'sort_by_date_updated_d', label:'Date updated', text:'Date updated (Descending)', icon: 'sort', value:'updatedAt', reversed:1, active:0}
    ];
    var visualSettings =
    [
      {id:'visual_circle', label:'Circle', text:'Compact', value:'dot', active:0},
      {id:'visual_ellipse', label:'Ellipse', text:'Text', value:'ellipse', active:1}
    ];

    var legendSettings =
    [
      {id:'legend_show', label:'Show Legends', text:'Show Map Legends', value:true, active:1},
      {id:'legend_hide', label:'Show Legends', text:'Show Map Legends', value:false, active:0}
    ];

    this.activeSettings = activeSettings;

    this.getSettings = getSettings;
    this.getSortSettings = getSortSettings;
    this.getVisualSettings = getVisualSettings;
    this.getLegendSettings = getLegendSettings;
    this.getActiveSortSetting = getActiveSortSetting;
    this.setActiveSortSetting = setActiveSortSetting;
    this.getActiveVisualSetting = getActiveVisualSetting;
    this.setActiveVisualSetting = setActiveVisualSetting;
    this.getActiveLegendSetting = getActiveLegendSetting;
    this.setActiveLegendSetting = setActiveLegendSetting;

    ////////////////

    function getSettings()
    {
      var settings = { graphsSorting:getSortSettings(),
                       graphVisualisation:getVisualSettings(),
                       graphLegend:getLegendSettings() };

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

    function getLegendSettings()
    {
      return legendSettings;
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

    function setActiveSortSetting(itemId)
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
        if (item.id === itemId)
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

    function setActiveVisualSetting(itemId)
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
        if (item.id === itemId)
        {
          // Set new active and save in cookie.
          item.active = 1;
          activeSettings.graphVisualisation = item;
          $cookies.putObject(cookieVisualSettingsKey, item.id);
        }
      }
    }

    function getActiveLegendSetting()
    {
      // Retrieve from cookie if present.
      var cachedValue = $cookies.getObject(cookieLegendSettingsKey);
      // Loop through the settings,
      for (var i in legendSettings)
      {
        var item = legendSettings[i];
        if (item.active)
        {
          if (!cachedValue)
          {
            // If it is active (default) and there is no cache value.
            activeSettings.graphLegend = item;
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
          activeSettings.graphLegend = item;
          return;
        }
      }
    }

    function setActiveLegendSetting(itemId)
    {
      // Loop through the settings,
      for (var i in legendSettings)
      {
        var item = legendSettings[i];
        if (item.active)
        {
          // Remove old active.
          item.active = 0;
        }
        if (item.id === itemId)
        {
          // Set new active and save in cookie.
          item.active = 1;
          activeSettings.graphLegend = item;
          $cookies.putObject(cookieLegendSettingsKey, item.id);
        }
      }
    }
  }
})();