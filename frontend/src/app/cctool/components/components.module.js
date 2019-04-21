// components.module.js
(function()
{
    'use strict';

    angular
        .module('app.cctool.components',
        [
          'app.cctool.components.controllability-analysis',
          'app.cctool.components.downstream-analysis',
          'app.cctool.components.explore',
          'app.cctool.components.graph',
          'app.cctool.components.graphs',
        	'app.cctool.components.menu',
          'app.cctool.components.subjective-logic-analysis',
          'app.cctool.components.toolbar',
          'app.cctool.components.upstream-analysis'
        ]);
})();