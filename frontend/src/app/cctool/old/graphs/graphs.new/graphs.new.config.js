// graphs.new.config.js
(function ()
{
    'use strict';

    angular
        .module('app.cctool.graphs.new')
        .config(config);

    config.$inject = ['$stateProvider'];

    /** @ngInject */
    function config($stateProvider)
    {
        $stateProvider
            .state('app.cctool_graphs_new',
            {
                url  : '/cctool/new_graph',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/graphs/graphs.new/graphs.new.html',
                        controller : 'NewGraphController as vm'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController as menu'
                    },
                    'toolbar@app.cctool_graphs_new':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: function ($scope)
                        {
                            $scope.name = 'New Graph';
                            $scope.shadow = false;
                        }
                    }
                }
            })
            .state('app.cctool_graphs_new_import',
            {
                url  : '/cctool/new_graph/import',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/graphs/graphs.new/graphs.new.import.html',
                        controller : 'ImportGraphController as import'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController as menu'
                    },
                    'toolbar@app.cctool_graphs_new_import':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: function ($scope)
                        {
                            $scope.name = 'Import Graph';
                            $scope.shadow = false;
                        }
                    }
                }
            })
            .state('app.cctool_graphs_new_create',
            {
                url  : '/cctool/new_graph/create',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/graphs/graphs.new/graphs.new.create.html',
                        controller : 'CreateGraphController as create'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController as menu'
                    },
                    'toolbar@app.cctool_graphs_new_create':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: function ($scope)
                        {
                            $scope.name = 'Create Graph';
                            $scope.shadow = false;
                        }
                    }
                }
            })
            .state('app.cctool_graphs_update',
            {
                url  : '/cctool/update_graph',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/graphs/graphs.new/graphs.new.update.html',
                        controller : 'NewGraphController as vm'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController as menu'
                    },
                    'toolbar@app.cctool_graphs_update':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: function ($scope)
                        {
                            $scope.name = 'Update Graph';
                            $scope.shadow = false;
                        }
                    },
                    'update@app.cctool_graphs_update':
                    {
                        templateUrl: 'app/cctool/graphs/graphs.new/graphs.new.create.html',
                        controller : 'CreateGraphController as create'
                    }
                },
                params:
                {
                    graph: null
                }
            });
    }

})();