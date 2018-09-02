// cctool.config.js
(function()
{
  'use strict';

  angular
    .module('app.cctool')
    .config(config);

  config.$inject = ['$mdThemingProvider', '$resourceProvider', 'AnalyticsProvider'];

  /* @ngInject */
  function config($mdThemingProvider, $resourceProvider, AnalyticsProvider)
  {
    // Themes
    $mdThemingProvider
      .theme('default')
      .primaryPalette('indigo')
      .accentPalette('teal', {'default': '500'})
      .backgroundPalette('grey');

    $mdThemingProvider
      .theme('toolbar_panel')
      .primaryPalette('grey', {'default' : 'A100'})
      .accentPalette('indigo')
      .warnPalette('red');

    $mdThemingProvider
      .theme('dashboard_page')
      .backgroundPalette('blue-grey', {'default' : '200'});

    $mdThemingProvider.alwaysWatchTheme(true);

    // Default routing
    $resourceProvider.defaults.stripTrailingSlashes = false;

    // Google Analytics
    AnalyticsProvider.setAccount('UA-77201439-2');
    // AnalyticsProvider.setDomainName('none');
    // AnalyticsProvider.setDomainName('cctool.herokuapp.com');
    AnalyticsProvider.setDomainName('cctooldev.herokuapp.com');
    AnalyticsProvider.trackPages(true);
    AnalyticsProvider.trackUrlParams(true);
    AnalyticsProvider.logAllCalls(true);
    AnalyticsProvider.setPageEvent('$stateChangeSuccess');
  }
})();