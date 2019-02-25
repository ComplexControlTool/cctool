// services.module.js
(function()
{
    'use strict';

    angular
        .module('app.cctool.services',
        [
            'app.cctool.services.colours',
            'app.cctool.services.controllability-analysis',
            'app.cctool.services.downstream-analysis',
            'app.cctool.services.jsnx',
            'app.cctool.services.graph',
            'app.cctool.services.graphs',
            'app.cctool.services.navigation',
            'app.cctool.services.settings',
            'app.cctool.services.upstream-analysis'
        ]);
})();