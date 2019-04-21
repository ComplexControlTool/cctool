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
        url: '/dashboard/graphs/demo',
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
        url: '/dashboard/graphs/demo/:id',
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
          'graph-controllability-analysis@app.cctool_graph_demo':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.controllability-analysis.html',
            controller: 'ControllabilityAnalysisController',
            controllerAs: 'controllabilityAnalysisCtrl'
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
        url: '/dashboard/graphs',
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
            return apiResolver.resolve('cctool.graphs.basic@query');
          }
        }
      })
      .state('app.cctool_graph',
      {
        url: '/dashboard/graphs/:id',
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
          'graph-explore@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/explore/explore.html',
            controller: 'ExploreController',
            controllerAs: 'exploreCtrl'
          },
          'graph-controllability-analysis@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.controllability-analysis.html',
            controller: 'ControllabilityAnalysisController',
            controllerAs: 'controllabilityAnalysisCtrl'
          },
          'graph-downstream-analysis@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.downstream-analysis.html',
            controller: 'DownstreamAnalysisController',
            controllerAs: 'downstreamAnalysisCtrl'
          },
          'graph-upstream-analysis@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.upstream-analysis.html',
            controller: 'UpstreamAnalysisController',
            controllerAs: 'upstreamAnalysisCtrl'
          },
          'graph-subjectivelogic-analysis@app.cctool_graph':
          {
            templateUrl: 'app/cctool/components/graph/templates/graph.subjective-logic-analysis.html',
            controller: 'SubjectiveLogicAnalysisController',
            controllerAs: 'subjectiveLogicAnalysisCtrl'
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
            return apiResolver.resolve('cctool.graphs.basic@query');
          },
          Graph: function (apiResolver, $stateParams)
          {
            return apiResolver.resolve('cctool.graph.basic@get', {'id': $stateParams.id});
          }
        }
      })
  }

})();