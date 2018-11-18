// app.route.js
(function()
{
  'use strict';

  angular
    .module('appdashboard')
    .config(routerConfig);

  routerConfig.$inject = ['$stateProvider', '$urlRouterProvider', '$locationProvider'];

  /** @ngInject */
  function routerConfig($stateProvider, $urlRouterProvider, $locationProvider)
  {

    // when enabled, # is removed from URL.
    if(window.history && window.history.pushState)
    {
      $locationProvider.html5Mode({
        enabled: true,
        requireBase: false,
        rewriteLinks: false
      });
    }

    $urlRouterProvider.otherwise('/dashboard');

    // Inject $cookies
    var $cookies;

    angular.injector(['ngCookies']).invoke([
      '$cookies', function (_$cookies)
      {
        $cookies = _$cookies;
      }
    ]);

    $stateProvider
      .state('app',
      {
        abstract: true,
        views:
        {
          '@':
          {
            // templateUrl: 'app/core/layouts/basic.html',
            templateUrl: 'app/cctool/layouts/cctool-layout.html',
            controller: 'AppController',
            controllerAs: 'appCtrl'
          }
        },
        resolve:
        {
          isAdmin: function (apiResolver)
          {
            return apiResolver.resolve('cctool.user@get').then(
              function(data)
              {
                // user is an admin
                return true;
              },
              function(err)
              {
                // not sure what the user is
                return false; 
              });
          }
        }
      });
  }

})();
