// toolbar.controller.js
(function() 
{
  'use strict';

  angular
    .module('app.cctool.components.toolbar')
    .controller('ToolbarController', ToolbarController);

  /* @ngInject */
  function ToolbarController($state, $scope, $log)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'ToolbarController';

    // Functions
    activate();

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
      vm.shadow = true;
      vm.sites = setBreadcrumb();
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
    }

    function setBreadcrumb()
    {
      $log.debug(vm.title+'/ setBreadcrumb');
      var sites = [];
      var parentControllerName = Object.keys($scope.$parent).filter(function(key) {return !key.startsWith('$')})[0];
      $log.debug(vm.title+'/ Using data from parent controller: ',parentControllerName);
      
      var state = $state.get();
      var url = $state.current.url;
      var urlParts = url.split('/');
      var loop = urlParts.length;

      for (var i=1; i<loop; i++)
      {
        var site = {};
        if (urlParts[i] == ':id')
        {
          var id = $state.params.id;
          var title = $scope[parentControllerName].content.title ? $scope[parentControllerName].content.title : $scope[parentControllerName].content.filter(function(obj) {return obj.id == id})[0].title;
          site.label = title.length > 20 ? title.substring(0,20)+'...' : title;
        }
        else
        {
          site.url = urlParts.slice(0, i+1).join('/');
          site.sref = state.filter(function(obj) { return obj.url == site.url})[0].name;
          site.label = urlParts[i].replace('_',' ');
        }
        if (urlParts.length-1 == i)
        {
          site.url = undefined;
          site.sref = undefined;
        }
        sites.push(site);
      }

      return sites;
    }

  }
})();