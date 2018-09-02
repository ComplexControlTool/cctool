// services.module.js
(function()
{
    'use strict';

    angular
        .module('app.cctool.services',
        [
            'app.cctool.services.colours',
            'app.cctool.services.jsnx',
            'app.cctool.services.graph',
            'app.cctool.services.graphs',
            'app.cctool.services.navigation',
            'app.cctool.services.settings'
        ]);
})();