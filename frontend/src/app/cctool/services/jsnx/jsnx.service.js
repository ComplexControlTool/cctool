// jsnx.service.js
(function()
{
    'use strict';

    angular
        .module('app.cctool.services.jsnx')
        .factory('jsnxService', JsnxService);

    JsnxService.$inject = ['$document', '$q', '$rootScope'];

    /* @ngInject */
    function JsnxService($document, $q, $rootScope)
    {
        var d = $q.defer();
        init();
        
        var service = {
            jsnx: getJsnx
        };
        return service;

        ////////////////

        function init()
        {
          // Create a script tag with jsnx as the source
          // and call our onScriptLoad callback when it
          // has been loaded
          var scriptTag = $document[0].createElement('script');
          
          scriptTag.type = 'text/javascript'; 
          scriptTag.async = true;
          scriptTag.src = 'app/cctool/lib/jsnetworkx.js';

          scriptTag.onreadystatechange = function () {
            if (this.readyState == 'complete') onScriptLoad();
          }

          scriptTag.onload = onScriptLoad;
     
          var s = $document[0].getElementsByTagName('body')[0];
          s.appendChild(scriptTag);
        }

        function onScriptLoad()
        {
          // Load client in the browser
          $rootScope.$apply(function() { d.resolve(window.jsnx); });
        }

        function getJsnx()
        {
          return d.promise;
        }
    }
})();
 
