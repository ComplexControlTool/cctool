// graphs.new.controller.js
(function ()
{
    'use strict';

    angular
        .module('app.cctool.graphs.new')
        .controller('NewGraphController', NewGraphController);

    /** @ngInject */
    function NewGraphController($scope, $state, $stateParams, $mdToast, $mdMedia, $mdDialog, $cookies, api)
    {
        var vm = this;

        var cookieGraphUploadKey = 'pendingGraphUpload';
        var cookieGraphUpdateKey = 'pendingGraphUpdate';
        var dialogTitle = 'Load unsaved graph?';
        var dialogContent = 'Looks like something went wrong on the last save attempt';
        var dialogOKOption = 'Load';
        var dialogCancelOption = 'Discard';
        var toastPosition = 'bottom left';

        $scope.$mdMedia = $mdMedia;

        vm.graph = undefined;

        init();

        //////////

        function init()
        {
            // If from update state and graph is not given as a parameter,
            // jump to the graphs page.
            if($state.is('app.cctool_graphs_update'))
            {
                // If cookie is detected, then prompt user.
                if($cookies.get(cookieGraphUpdateKey + '-' + vm.graph.id))
                {
                    showDialog();
                }
                else if ($stateParams.graph)
                {
                    readData($stateParams.graph);
                }
                else
                {
                    $state.go('app.cctool_graphs_new');
                }
            }
            if($state.is('app.cctool_graphs_new'))
            {
                // If cookie is detected, then prompt user.
                if($cookies.get(cookieGraphUploadKey))
                {
                    showDialog();
                }
            }

        }

        function readData(data)
        {
            if (!data)
            {
                return;
            }
            else
            {
                vm.graph = data;
            }
        }

        function writeToCookie(data)
        {
            if($state.is('app.cctool_graphs_update'))
            {
                $cookies.putObject(cookieGraphUpdateKey + '-' + vm.graph.id, data);
            }
            if($state.is('app.cctool_graphs_new'))
            {
                $cookies.putObject(cookieGraphUploadKey, data);
            }
        }

        function removeCookie()
        {
            if($state.is('app.cctool_graphs_update'))
            {
                $cookies.remove(cookieGraphUpdateKey + '-' + vm.graph.id);
            }
            if($state.is('app.cctool_graphs_new'))
            {
                $cookies.remove(cookieGraphUploadKey);                       
            }
        }

        function showDialog(ev)
        {
            // Appending dialog to document.body to cover sidenav in docs app
            var confirm = $mdDialog.confirm()
                .title(dialogTitle)
                .textContent(dialogContent)
                .ariaLabel('')
                .targetEvent(ev)
                .ok(dialogOKOption)
                .cancel(dialogCancelOption);
            $mdDialog.show(confirm).then(
                function()
                {
                    if($state.is('app.cctool_graphs_update'))
                    {
                        readData($cookies.getObject(cookieGraphUpdateKey + '-' + vm.graph.id));
                    }
                    if($state.is('app.cctool_graphs_new'))
                    {
                        readData($cookies.getObject(cookieGraphUploadKey));
                    }
                },
                function()
                {
                    if($state.is('app.cctool_graphs_update'))
                    {
                        readData($stateParams.graph);
                        // Remove cookie.
                        removeCookie();
                    }
                    if($state.is('app.cctool_graphs_new'))
                    {
                        // Remove cookie.
                        removeCookie();                       
                    }
                }
            );
        };
    }
    
    function DialogController($scope, $mdDialog)
    {
      $scope.hide = function()
      {
        $mdDialog.hide();
      };
      $scope.cancel = function()
      {
        $mdDialog.cancel();
      };
      $scope.answer = function(answer)
      {
        $mdDialog.hide(answer);
      };
    }
})();