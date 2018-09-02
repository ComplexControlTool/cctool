// dashboard.controller.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.pages.dashboard')
    .controller('DashboardController', DashboardController);

  /* @ngInject */
  function DashboardController(isAdmin, $scope, $log, $mdMedia, $mdDialog, navigationService)
  {
    /* jshint validthis: true */
    var vm = this;

    // Data
    vm.title = 'DashboardController';
    vm.navItems = [];
    $scope.$mdMedia = $mdMedia;

    // Functions
    activate();
    vm.showInfo = showInfo;

    // Watchers / Listeners
    $scope.$on('$destroy', function() {
      deactivate();
    });

    function activate()
    {
      $log.debug(vm.title+'/ Activated ' + vm.title + ' controller!');
      prepareNavigation();
    }

    function deactivate()
    {
      $log.debug(vm.title+'/ Deactivated ' + vm.title + ' controller!');
    }

    function prepareNavigation()
    {
      var navItems = navigationService.getNavigation();
      for (var i in navItems)
      {
        if (navItems[i].admin_access)
        {
          if (isAdmin)
          {
            vm.navItems.push(navItems[i]);
          }
        }
        else
        {
          vm.navItems.push(navItems[i]);
        }
      }
    }

    // Info Dialogue

    // Control graph compare dialogue.
    function showInfo(ev)
    {
      var isSmallScreen = $mdMedia('sm') || $mdMedia('xs');
      $mdDialog.show({
        controller: InfoController,
        templateUrl: 'app/cctool/components/info/dialogs/info.html',
        parent: angular.element(document.body),
        targetEvent: ev,
        clickOutsideToClose: true,
        fullscreen: isSmallScreen
      })
      $scope.$watch(
        function() {
          return $mdMedia('xs') || $mdMedia('sm');
        },
        function(wantsFullScreen) {
          isSmallScreen = true;
        }
      );
    }
  }
  // Controller of graph compare dialogue
  function InfoController($scope, $mdDialog, $mdMedia)
  {
    $scope.$mdMedia = $mdMedia;
    $scope.page = 0;
    $scope.infoPages =
    [
      'https://docs.google.com/document/d/1sQNFgtxyUTSVER6ut-18raAyeG9RA6iFTfgw0daqp_g/pub',
      'https://docs.google.com/document/d/1y9IxZT0fbkhVixTNfONKtlOX6q9YtX0hd5JEIGLKgvE/pub',
      'https://docs.google.com/document/d/1arts5tRG0mZBsvgICb7ihNMSxDHC77euh-SNoCAZJtw/pub',
      'https://docs.google.com/document/d/1ykL5UbU_MH78i7L_gMUFYasM-K-UoaUe1wm0oRVPT0A/pub'
    ];

    $scope.hasNextPage = function()
    {
      if ($scope.page >= $scope.infoPages.length-1)
      {
        return false;
      }
      return true;
    }
    $scope.hasPrevPage = function()
    {
      if ($scope.page == 0)
      {
        return false;
      }
      return true;
    }

    $scope.nextPage = function()
    {
      if ($scope.hasNextPage)
      {
        $scope.page += 1;
      }
    }
    $scope.prevPage = function()
    {
      if ($scope.hasPrevPage)
      {
        $scope.page -= 1;
      }
    }

    $scope.hide = function() {
      $mdDialog.hide();
    };
    $scope.cancel = function() {
      $mdDialog.cancel();
    };
    $scope.answer = function(answer) {
      $mdDialog.hide(answer);
    };
  }
})();