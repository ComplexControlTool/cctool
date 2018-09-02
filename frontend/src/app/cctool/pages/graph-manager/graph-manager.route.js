// graph-manager.route.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.pages.graph-manager')
    .config(routeConfig);

  /** @ngInject */
  function routeConfig($stateProvider)
  {
    $stateProvider
      .state('app.cctool_graphs_demo',
      {
        url: '/cctool/graphs/demo',
        views:
        {
          'content@app':
          {
            templateUrl: 'app/cctool/pages/graph-manager/graph-manager.html',
            controller: 'GraphManagerController',
            controllerAs: 'graphManagerCtrl'
          },
          'menu@app':
          {
            templateUrl: 'app/cctool/components/menu/menu.html',
            controller: 'MenuController',
            controllerAs: 'menuCtrl'
          },
          'template@app.cctool_graphs_demo':
          {
            templateUrl: 'app/cctool/pages/graph-manager/templates/graph-manager.graphs.html'
          },
          'graphs@app.cctool_graphs_demo':
          {
            templateUrl: 'app/cctool/components/graphs/graphs.html',
            controller: 'GraphsController',
            controllerAs: 'graphsCtrl'
          },
          'toolbar@app.cctool_graphs_demo':
          {
            templateUrl: 'app/cctool/components/toolbar/toolbar.html',
            controller: 'ToolbarController',
            controllerAs: 'toolbarCtrl'
          }
        },
        resolve:
        {
          Graphs: function (apiResolver)
          {
            return apiResolver.resolve('cctool.graphs.demo@get');
          }
        }
      })
      .state('app.cctool_graph_demo',
      {
        url: '/cctool/graphs/demo/:id',
        views:
        {
          'content@app':
          {
            templateUrl: 'app/cctool/pages/graph-manager/graph-manager.html',
            controller: 'GraphManagerController',
            controllerAs: 'graphManagerCtrl'
          },
          'menu@app':
          {
            templateUrl: 'app/cctool/components/menu/menu.html',
            controller: 'MenuController',
            controllerAs: 'menuCtrl'
          },
          'template@app.cctool_graph_demo':
          {
            templateUrl: 'app/cctool/pages/graph-manager/templates/graph-manager.graph.html'
          },
          'graph@app.cctool_graph_demo':
          {
            templateUrl: 'app/cctool/components/graph/graph.html',
            controller: 'GraphController',
            controllerAs: 'graphCtrl'
          },
          'graph-overview@app.cctool_graph_demo':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.overview.html',
          },
          'graph-control-nodes@app.cctool_graph_demo':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.control-nodes.html',
            controller: 'ControlNodesAnalysisController',
            controllerAs: 'controlNodesAnalysisCtrl'
          },
          'graph-up-down-stream@app.cctool_graph_demo':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.node-updownstream.html',
            controller: 'NodeAnalysisController',
            controllerAs: 'nodeAnalysisCtrl'
          },
          'toolbar@app.cctool_graph_demo':
          {
            templateUrl: 'app/cctool/components/toolbar/toolbar.html',
            controller: 'ToolbarController',
            controllerAs: 'toolbarCtrl'
          }
        },
        resolve:
        {
          Graphs: function (apiResolver)
          {
            return apiResolver.resolve('cctool.graphs.demo@get');
          },
          Graph: function (apiResolver, $stateParams)
          {
            return apiResolver.resolve('cctool.graph.demo@get', {'id': $stateParams.id});
          }
        }
      })
      .state('app.cctool_graphs',
      {
        url: '/cctool/graphs',
        views:
        {
          'content@app':
          {
            templateUrl: 'app/cctool/pages/graph-manager/graph-manager.html',
            controller: 'GraphManagerController',
            controllerAs: 'graphManagerCtrl'
          },
          'menu@app':
          {
            templateUrl: 'app/cctool/components/menu/menu.html',
            controller: 'MenuController',
            controllerAs: 'menuCtrl'
          },
          'template@app.cctool_graphs':
          {
            templateUrl: 'app/cctool/pages/graph-manager/templates/graph-manager.graphs.html'
          },
          'graphs@app.cctool_graphs':
          {
            templateUrl: 'app/cctool/components/graphs/graphs.html',
            controller: 'GraphsController',
            controllerAs: 'graphsCtrl'
          },
          'actions@app.cctool_graphs':
          {
            templateUrl: 'app/cctool/components/graphs/templates/graph-actions.html'
          },
          'toolbar@app.cctool_graphs':
          {
            templateUrl: 'app/cctool/components/toolbar/toolbar.html',
            controller: 'ToolbarController',
            controllerAs: 'toolbarCtrl'
          }
        },
        resolve:
        {
          Graphs: function (apiResolver)
          {
            return apiResolver.resolve('cctool.graphs.basicoptions@get');
          }
        }
      })
      .state('app.cctool_graph',
      {
        url: '/cctool/graphs/:id',
        views:
        {
          'content@app':
          {
            templateUrl: 'app/cctool/pages/graph-manager/graph-manager.html',
            controller: 'GraphManagerController',
            controllerAs: 'graphManagerCtrl'
          },
          'menu@app':
          {
            templateUrl: 'app/cctool/components/menu/menu.html',
            controller: 'MenuController',
            controllerAs: 'menuCtrl'
          },
          'template@app.cctool_graph':
          {
            templateUrl: 'app/cctool/pages/graph-manager/templates/graph-manager.graph.html'
          },
          'graph@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/graph/graph.html',
            controller: 'GraphController',
            controllerAs: 'graphCtrl'
          },
          'graph-overview@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.overview.html',
          },
          'graph-control-nodes@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.control-nodes.html',
            controller: 'ControlNodesAnalysisController',
            controllerAs: 'controlNodesAnalysisCtrl'
          },
          'graph-up-down-stream@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.node-updownstream.html',
            controller: 'NodeAnalysisController',
            controllerAs: 'nodeAnalysisCtrl'
          },
          'actions@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph-actions.html'
          },
          'toolbar@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/toolbar/toolbar.html',
            controller: 'ToolbarController',
            controllerAs: 'toolbarCtrl'
          }
        },
        resolve:
        {
          Graphs: function (apiResolver)
          {
            return apiResolver.resolve('cctool.graphs.basic@get');
          },
          Graph: function (apiResolver, $stateParams)
          {
            return apiResolver.resolve('cctool.graph.full@get', {'id': $stateParams.id});
          }
        }
      })
  }

})();