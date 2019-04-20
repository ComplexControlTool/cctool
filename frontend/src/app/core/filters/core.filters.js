// core.filter.js
(function()
{
    'use strict';

    angular
        .module('app.core')
        .filter('toTrustAsHtml', toTrustAsHtmlFilter)
        .filter('toTrustAsUrl', toTrustAsUrlFilter)
        .filter('toTrustAsResourceUrl', toTrustAsResourceUrlFilter)
        .filter('toTrustAsJs', toTrustAsJsFilter)
        .filter('isEmpty', isEmpty);

    toTrustAsHtmlFilter.$inject = ['$sce'];
    toTrustAsUrlFilter.$inject = ['$sce'];
    toTrustAsResourceUrlFilter.$inject = ['$sce'];
    toTrustAsJsFilter.$inject = ['$sce'];
    isEmpty.$inject = [];

    /** @ngInject */
    function toTrustAsHtmlFilter($sce)
    {
        return trustAsHtml;

        ////////////////

        function trustAsHtml(val)
        {
            return $sce.trustAsHtml(val);
        }
    }

    /** @ngInject */
    function toTrustAsUrlFilter($sce)
    {
        return trustAsUrl;

        ////////////////

        function trustAsUrl(val)
        {
            return $sce.trustAsUrl(val);
        }
    }

    /** @ngInject */
    function toTrustAsResourceUrlFilter($sce)
    {
        return trustAsResourceUrl;

        ////////////////

        function trustAsResourceUrl(val)
        {
            return $sce.trustAsResourceUrl(val);
        }
    }

    /** @ngInject */
    function toTrustAsJsFilter($sce)
    {
        return trustAsJs;

        ////////////////

        function trustAsJs(val)
        {
            return $sce.trustAsJs(val);
        }
    }

    /** @ngInject */
    function isEmpty()
    {
        return filterFilter;

        ////////////////

        function filterFilter(obj)
        {
            return _.isEmpty(obj);
        }
    }

})();