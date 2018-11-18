// graphs.config.js
(function ()
{
    'use strict';

    angular
        .module('app.cctool.graphs')
        .config(config);

    config.$inject = ['$stateProvider'];

    /** @ngInject */
    function config($stateProvider)
    {
        $stateProvider
            .state('app.cctool_admin_graphs',
            {
                url  : '/dashboard/admin/graphs',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/graphs/graphs.grid.html',
                        controller : 'GraphsController as vm'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController as menu'
                    },
                    'frequency@app.cctool_admin_graphs':
                    {
                        templateUrl: 'app/cctool/components/frequency/frequency.html',
                    },
                    'graph@app.cctool_admin_graphs':
                    {
                        templateUrl: 'app/cctool/components/graph/graph.html',
                    },
                    'nodes@app.cctool_admin_graphs':
                    {
                        templateUrl: 'app/cctool/components/nodes/nodes.html',
                    },
                    'right-sidenav@app.cctool_admin_graphs':
                    {
                        templateUrl: 'app/cctool/components/graph/graph.info.html',
                    },
                    'stems@app.cctool_admin_graphs':
                    {
                        templateUrl: 'app/cctool/components/stems/stems.html',
                    },
                    'toolbar@app.cctool_admin_graphs':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: function ($scope)
                        {
                            $scope.name = 'Admin Graphs';
                            $scope.shadow = false;
                            $scope.toolbarExtensionTemplate = 'app/cctool/graphs/graphs.toolbar-extension.html';
                        }
                    }
                },
                resolve:
                {
                    graphs: function (apiResolver)
                    {
                        return apiResolver.resolve('cctool.admingraphs@get');
                    }
                }
            })
            .state('app.cctool_graphs',
            {
                url  : '/dashboard/graphs',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/graphs/graphs.tabs.html',
                        controller : 'GraphsController as vm'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController as menu'
                    },
                    'frequency@app.cctool_graphs':
                    {
                        templateUrl: 'app/cctool/components/frequency/frequency.html',
                    },
                    'graph@app.cctool_graphs':
                    {
                        templateUrl: 'app/cctool/components/graph/graph.html',
                    },
                    'nodes@app.cctool_graphs':
                    {
                        templateUrl: 'app/cctool/components/nodes/nodes.html',
                    },
                    'right-sidenav@app.cctool_graphs':
                    {
                        templateUrl: 'app/cctool/components/graph/graph.info.html',
                    },
                    'stems@app.cctool_graphs':
                    {
                        templateUrl: 'app/cctool/components/stems/stems.html',
                    },
                    'node-updownstream-analysis@app.cctool_graphs':
                    {
                        templateUrl: 'app/cctool/components/node-updownstream-analysis/node-updownstream-analysis.html',
                        controller: 'NodeAnalysisController',
                        controllerAs: 'nodeanalysis'
                    },
                    'toolbar@app.cctool_graphs':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: function ($scope)
                        {
                            $scope.name = 'Graphs';
                            $scope.shadow = false;
                            $scope.toolbarExtensionTemplate = 'app/cctool/graphs/graphs.toolbar-extension.html';
                        }
                    }
                },
                resolve:
                {
                    graphs: function (apiResolver)
                    {
                        return apiResolver.resolve('cctool.graphs@get');
                    }
                }
            })
            .state('app.cctool_graphs_demo',
            {
                url  : '/dashboard/graphs/demo',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/graphs/graphs.tabs.html',
                        controller : 'GraphsController as vm'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController as menu'
                    },
                    'frequency@app.cctool_graphs_demo':
                    {
                        templateUrl: 'app/cctool/components/frequency/frequency.html',
                    },
                    'graph@app.cctool_graphs_demo':
                    {
                        templateUrl: 'app/cctool/components/graph/graph.html',
                    },
                    'nodes@app.cctool_graphs_demo':
                    {
                        templateUrl: 'app/cctool/components/nodes/nodes.html',
                    },
                    'right-sidenav@app.cctool_graphs_demo':
                    {
                        templateUrl: 'app/cctool/components/graph/graph.info.html',
                    },
                    'stems@app.cctool_graphs_demo':
                    {
                        templateUrl: 'app/cctool/components/stems/stems.html',
                    },
                    'toolbar@app.cctool_graphs_demo':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: function ($scope)
                        {
                            $scope.name = 'Graphs Demo';
                            $scope.shadow = false;
                            $scope.toolbarExtensionTemplate = 'app/cctool/graphs/graphs.toolbar-extension.html';
                        }
                    }
                },
                resolve:
                {
                    graphs: function (apiResolver)
                    {
                        return apiResolver.resolve('cctool.demo@get');
                    }
                }
            })
            .state('app.cctool_graphs_compare',
            {
                url  : '/dashboard/compare_graphs',
                views:
                {
                    'content@app':
                    {
                        templateUrl: 'app/cctool/graphs/graphs.compare.html',
                        controller : 'GraphsController as vm'
                    },
                    'menu@app':
                    {
                        templateUrl: 'app/cctool/components/menu/menu.html',
                        controller : 'MenuController as menu'
                    },
                    'frequency@app.cctool_graphs_compare':
                    {
                        templateUrl: 'app/cctool/components/frequency/frequency.html',
                    },
                    'graph@app.cctool_graphs_compare':
                    {
                        templateUrl: 'app/cctool/components/graph/graph.html',
                    },
                    'nodes@app.cctool_graphs_compare':
                    {
                        templateUrl: 'app/cctool/components/nodes/nodes.html',
                    },
                    'stems@app.cctool_graphs_compare':
                    {
                        templateUrl: 'app/cctool/components/stems/stems.html',
                    },
                    'toolbar@app.cctool_graphs_compare':
                    {
                        templateUrl: 'app/cctool/components/toolbar/toolbar.html',
                        controller: function ($scope)
                        {
                            $scope.name = 'Compare Graphs';
                            $scope.shadow = true;
                        }
                    }
                },
                params:
                {
                    graphs: null
                },
                resolve:
                {
                    graphs: function (apiResolver)
                    {
                        return apiResolver.resolve('cctool.empty@get');
                    }
                }
            });
    }

})();