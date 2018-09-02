// pages.module.js
(function()
{
    'use strict';

    angular
        .module('app.cctool.pages',
        [
            'app.cctool.pages.dashboard',
            'app.cctool.pages.graph-editor',
            'app.cctool.pages.graph-manager'
        ]);
})();