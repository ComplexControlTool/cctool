// app.controller.js
(function()
{
  'use strict';

  angular
    .module('appdashboard')
    .controller('AppController', AppController);

  /* @ngInject */
  function AppController(isAdmin, $scope, $log, $state, $window, $timeout, $mdMedia, $mdSidenav, $transitions, cctoolParams)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'AppController';
    vm.cctoolUser = cctoolParams.userId;
    vm.cctoolAdmin = isAdmin;
    vm.$state = $state;
    vm.$mdMedia = $mdMedia;
    vm.customScreenSize = undefined;
    vm.isOffline = false;
    vm.isLoading = true;
    vm.toastPosition = 'bottom left';

    // Functions
    activate();
    vm.openLink = openLink;
    vm.toggleSidenav = toggleSidenav;

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
      setupWathcers();
      $timeout(function() {
        vm.isLoading = false;
      }, 350);
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
    }

    function watchStateStatus()
    {
      $transitions.onStart({},
        function(transition)
        {
          $log.debug(vm.title+'/ UI Route transition onStart');
          vm.isLoading = true;
        }
      );

      $transitions.onSuccess({},
        function(transition)
        {
          $log.debug(vm.title+'/ UI Route transition onSuccess');
          $timeout(function() {
            vm.isLoading = false;
          }, 350);
        }
      );
    }

    function watchOnlineStatus()
    {
      Offline.on('confirmed-down',
        function ()
        {
          vm.isOffline = true;
        }
      );
      Offline.on('confirmed-up',
        function ()
        {
          vm.isOffline = false;
        }
      );    
    }

    function watchScreenSize()
    {
      $scope.$watch(
        function()
        {
          if ($mdMedia('(max-width: 400px)'))
          {
            return 'xxs';
          }
          if ($mdMedia('(min-width: 2300px)'))
          {
            return 'gt-xl';
          }
          else
          {
            return undefined;
          }
        }, 
        function(size)
        {
          vm.customScreenSize = size;
        }
      );
    }

    function setupWathcers()
    {
      watchStateStatus();
      watchOnlineStatus();
      watchScreenSize();
    }

    // Function used to open the result's link to a new tab.
    function openLink(url, reload)
    {
      var protocol= url.substring(0, url.indexOf('://'));
      var tempUrl = url.substring(url.indexOf('://')+3, url.length);
      if(protocol === 'smb' || protocol === 'nfs'){
        url = '/' + protocol + '/' + tempUrl
      }else if(protocol === 'googledb://'){
        url = '/' + db + '/' + tempUrl
      }else if(protocol === 'unc'){
        url = 'file://' + tempUrl
      }
      if (reload) {
        $window.open(url, '_self');
      } else {
        $window.open(url, '_target');
      }
    }

    function toggleSidenav(navId)
    {
      $mdSidenav(navId).toggle();
    }

  }
})();