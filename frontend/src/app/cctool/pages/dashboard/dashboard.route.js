// dashboard.route.js
(function()
{
    'use strict';

    angular
        .module('app.cctool.pages.dashboard')
        .config(routeConfig);

    /* @ngInject */
    function routeConfig($stateProvider)
    {
        $stateProvider
            .state('app.cctool_dashboard',
            {
                url  : '/cctool',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/pages/dashboard/dashboard.html',
                        controller : 'DashboardController',
                        controllerAs: 'dashboardCtrl'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController',
                        controllerAs: 'menuCtrl'
                    },
                    'toolbar@app.cctool_dashboard':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: 'ToolbarController',
                        controllerAs: 'toolbarCtrl'
                    }
                }
            })
    }

})();