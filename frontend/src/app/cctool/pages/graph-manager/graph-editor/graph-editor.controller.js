// graph-editor.controller.js
(function ()
{
    'use strict';

    angular
        .module('app.cctool.pages.graph-editor')
        .controller('GraphEditorController', GraphEditorController);

    /** @ngInject */
    function GraphEditorController($scope, $state, $stateParams, $mdToast, $mdMedia, $mdDialog, $cookies, $log, $q, api, apiResolver)
    {
        var vm = this;
        vm.title = 'GraphEditorController';

        var cookieGraphUploadKey = 'pendingGraphUpload';
        var cookieGraphUpdateKey = 'pendingGraphUpdate';
        var dialogTitle = 'Load unsaved graph?';
        var dialogContent = 'Looks like something went wrong on the last save attempt';
        var dialogOKOption = 'Load';
        var dialogCancelOption = 'Discard';
        var toastPosition = 'bottom left';

        $scope.$mdMedia = $mdMedia;

        vm.graph = undefined;
        vm.selectedItem = undefined;
        vm.availableGraphs = [];

        init();
        vm.querySearch = querySearch;
        vm.selectedItemChange = selectedItemChange;
        vm.searchTextChange   = searchTextChange;
        vm.submitForm = submitForm;

        //////////

        function init()
        {
            // If from update state and graph is not given as a parameter,
            // jump to the graphs page.
            if($state.is('app.cctool_graphs_update_graph'))
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
            if($state.is('app.cctool_graphs_update_graph'))
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
            if($state.is('app.cctool_graphs_update_graph'))
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
                    if($state.is('app.cctool_graphs_update_graph'))
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
                    if($state.is('app.cctool_graphs_update_graph'))
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
        }

        function querySearch(query)
        {
            $log.debug(vm.title+'/querySearch with', query);

            var results;
            var promise = apiResolver.resolve('cctool.graphs.compact@query');

            if (query)
            {
                results = promise.then(function(data){ return cleanUpData(data).filter( createFilterFor(query) ) });
            }
            else
            {
                results = promise.then(function(data){ return cleanUpData(data) });
            }

            var deferred = $q.defer();
            deferred.resolve( results );
            return deferred.promise;
        }

        function cleanUpData(data)
        {
            $log.debug(vm.title+'/cleanUpData with', data);
            if (data)
            {
                $log.debug(vm.title+'/cleanUpData data have graphs, mapping to appropriate output for autocomplete');
                return data.map(
                    function(graph)
                    {
                        return {
                            id: graph.id,
                            value: angular.lowercase(graph.title),
                            display: graph.title
                        }
                    });
            }
        }
    
        function searchTextChange(text)
        {
            $log.debug(vm.title+'/searchTextChange with:',text);
        }

        function selectedItemChange(item)
        {
            $log.debug(vm.title+'/selectedItemChange with', JSON.stringify(item));
        }
    
        function createFilterFor(query)
        {
          var lowercaseQuery = angular.lowercase(query);

          return function filterFn(graph) {
            return (graph.value.indexOf(lowercaseQuery) === 0);
          };
        }

        function submitForm()
        {
            $log.debug(vm.title+'/submitForm with:', vm.selectedItem);
            if (vm.selectedItem && angular.isDefined(vm.selectedItem.id))
            {
                $state.go('app.cctool_graphs_update_graph', {'id': vm.selectedItem.id});
            }
        }
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