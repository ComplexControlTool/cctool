// graph-editor.constants.js
(function()
{
  'use strict';

  angular
    .module('app.cctool.pages.graph-editor')
    .constant('graphDefaultVisualization', JSON.parse('{"options":{"edges":{"color":{"hover":"#2B7CE9","opacity":1},"arrows":{"to":{"type":"arrow","enabled":true,"scaleFactor":1}},"smooth":{"type":"continuous","enabled":true,"roundness":0.5},"selectionWidth":2},"width":"100%","height":"100%","layout":{"randomSeed":2},"locale":"en","physics":{"enabled":false},"autoResize":true,"clickToUse":true,"interaction":{"hover":true,"navigationButtons":true}},"structure":{}}'));
})();
