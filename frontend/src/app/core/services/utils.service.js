// utils.service.js
(function()
{
    'use strict';

    angular
        .module('app.core')
        .factory('coreUtils', coreUtilsService);

    coreUtilsService.$inject = [];

    /** @ngInject */
    function coreUtilsService()
    {
        // Private variables
        var mobileDetect = new MobileDetect(window.navigator.userAgent);

        var service = {
        	detectBrowser : detectBrowser,
            isMobile: isMobile,
            decodeHexSequence: decodeHexSequence
        };
        return service;

        ////////////////

        /**
         * Function to determine the user's browser
         */
        function detectBrowser()
        {
        	return bowser._detect(window.navigator.userAgent);
        }

        /**
         * Return if current device is a
         * mobile device or not
         */
        function isMobile()
        {
            return mobileDetect.mobile();
        }

        /**
         * Function to decode hex strings returned in GSA suggestions.
         * Return the decoded string.
         */
        function decodeHexSequence(string)
        {
            return string.replace(/\\x([0-9A-Fa-f]{2})/g, function() {
                return String.fromCharCode(parseInt(arguments[1], 16));
            });
        }
    }
}());