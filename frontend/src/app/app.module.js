// app.module.js
(function()
{
  'use strict';

  angular
    .module('appdashboard',
      [
        // Core
        'app.core',
        // Components
        'app.components',
        // Directives
        'app.directives',
        // Pages
        'app.pages',
        // CCTool
        'app.cctool'
      ]
    );

})();
