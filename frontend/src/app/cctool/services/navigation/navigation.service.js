// navigation.service.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.services.navigation')
    .service('navigationService', NavigationService);

  NavigationService.$inject = [];

  /* @ngInject */
  function NavigationService()
  {
    var navigation =
    [
      {id:'new_graph', label:'New Graph', link:'app.cctool_graphs_new', icon: 'add', admin_access: 0},
      {id:'edit_graph', label:'Edit Graph', link:'app.cctool_graphs_update', icon: 'edit', admin_access: 0},
      {id:'graphs', label:'Graphs', link:'app.cctool_graphs', icon: 'bubble_chart', admin_access: 0}//,
      // {id:'graphs_demo', label:'Graphs Demo', link:'app.cctool_graphs_demo', icon: 'play_arrow', admin_access: 0}
    ];

    this.getNavigation = getNavigation;

    ////////////////

    function getNavigation()
    {
      return navigation;
    }
  }
})();