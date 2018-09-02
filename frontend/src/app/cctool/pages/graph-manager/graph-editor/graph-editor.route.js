// graph-editor.route.js
(function ()
{
    'use strict';

    angular
        .module('app.cctool.pages.graph-editor')
        .config(config);

    config.$inject = ['$stateProvider'];

    /** @ngInject */
    function config($stateProvider)
    {
        $stateProvider
            .state('app.cctool_graphs_new',
            {
                url  : '/cctool/graphs/new',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/pages/graph-manager/graph-editor/graph-editor.new.html',
                        controller : 'GraphEditorController',
                        controllerAs: 'graphEditorCtrl'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController',
                        controllerAs: 'menuCtrl'
                    },
                    'toolbar@app.cctool_graphs_new':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: 'ToolbarController',
                        controllerAs: 'toolbarCtrl'
                    }
                }
            })
            .state('app.cctool_graphs_new_import',
            {
                url  : '/cctool/graphs/new/import',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/pages/graph-manager/graph-editor/import/graph-editor.import.html',
                        controller : 'ImportGraphController',
                        controllerAs: 'importGraphCtrl'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController',
                        controllerAs: 'menuCtrl'
                    },
                    'toolbar@app.cctool_graphs_new_import':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: 'ToolbarController',
                        controllerAs: 'toolbarCtrl'
                    }
                }
            })
            .state('app.cctool_graphs_new_create',
            {
                url  : '/cctool/graphs/new/create',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/pages/graph-manager/graph-editor/create/graph-editor.create.html',
                        controller : 'CreateGraphController',
                        controllerAs: 'createGraphCtrl'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController',
                        controllerAs: 'menuCtrl'
                    },
                    'toolbar@app.cctool_graphs_new_create':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: 'ToolbarController',
                        controllerAs: 'toolbarCtrl'
                    }
                }
            })
            .state('app.cctool_graphs_update',
            {
                url  : '/cctool/graphs/edit',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/pages/graph-manager/graph-editor/graph-editor.update.html',
                        controller : 'GraphEditorController',
                        controllerAs: 'graphEditorCtrl'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController',
                        controllerAs: 'menuCtrl'
                    },
                    'toolbar@app.cctool_graphs_update':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: 'ToolbarController',
                        controllerAs: 'toolbarCtrl'
                    }
                }
            })
            .state('app.cctool_graphs_update_graph',
            {
                url  : '/cctool/graphs/edit/:id',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/pages/graph-manager/graph-editor/update/graph-editor.update.html',
                        controller : 'UpdateGraphController',
                        controllerAs: 'updateGraphCtrl'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController',
                        controllerAs: 'menuCtrl'
                    },
                    'toolbar@app.cctool_graphs_update_graph':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: 'ToolbarController',
                        controllerAs: 'toolbarCtrl'
                    }
                },
                resolve:
                {
                  Graph: function (apiResolver, $stateParams)
                  {
                    return apiResolver.resolve('cctool.graph.update@get', {'id': $stateParams.id});
                  }
                }
            });
    }

})();