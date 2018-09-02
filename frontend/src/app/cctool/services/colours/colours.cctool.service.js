// colours.cctool.service.js
(function()
{
    'use strict';

    angular
        .module('app.cctool.services.colours')
        .service('cctoolColorsService', cctoolColorsService);

    cctoolColorsService.$inject = ['colorbrewerService'];

    /* @ngInject */
    function cctoolColorsService(colorbrewerService)
    {
        this.cctoolColors = cctoolColors();

        ////////////////

        function cctoolColors()
        {
          var colorbrewer = colorbrewerService.colorbrewer;

          var palettes =
          {
            0: {'palette':colorbrewer.Purples[9]},
            1: {'palette':colorbrewer.Blues[9]},
            2: {'palette':colorbrewer.Greens[9]},
            3: {'palette':colorbrewer.Oranges[9]},
            4: {'palette':colorbrewer.Reds[9]},
            5: {'palette':colorbrewer.Greys[9]}
          };
          var controlNode = '#FDD835'
          var easyNodeColor = colorbrewer.Greens[9][4];
          var medNodeColor = colorbrewer.Oranges[9][3];
          var hardNodeColor = colorbrewer.Reds[9][4];
          var ctrlNodeStrokeColor = '#FF3399';
          var easyNodeStrokeColor = colorbrewer.Greens[9][6];
          var medNodeStrokeColor = colorbrewer.Oranges[9][4];
          var hardNodeStrokeColor = colorbrewer.Reds[9][6];
          var colors =
          {
            0: {'palette':palettes[0].palette, 'nodeColor':palettes[0].palette[5], 'ctrlnodeColor':controlNode, 'nodeStroke':palettes[0].palette[6], 'ctrlnodeStroke':ctrlNodeStrokeColor, 'easynodeColor':easyNodeColor, 'mednodeColor':medNodeColor, 'hardnodeColor':hardNodeColor, 'easynodeStrokeColor':easyNodeStrokeColor, 'mednodeStrokeColor':medNodeStrokeColor, 'hardnodeStrokeColor':hardNodeStrokeColor, 'weakplus':palettes[0].palette[2], 'mediumplus':palettes[0].palette[5], 'strongplus':palettes[0].palette[8], 'weakminus':palettes[5].palette[2], 'mediumminus':palettes[5].palette[4], 'strongminus':palettes[5].palette[6],},
            1: {'palette':palettes[1].palette, 'nodeColor':palettes[1].palette[5], 'ctrlnodeColor':controlNode, 'nodeStroke':palettes[1].palette[6], 'ctrlnodeStroke':ctrlNodeStrokeColor, 'easynodeColor':easyNodeColor, 'mednodeColor':medNodeColor, 'hardnodeColor':hardNodeColor, 'easynodeStrokeColor':easyNodeStrokeColor, 'mednodeStrokeColor':medNodeStrokeColor, 'hardnodeStrokeColor':hardNodeStrokeColor, 'weakplus':palettes[1].palette[2], 'mediumplus':palettes[1].palette[5], 'strongplus':palettes[1].palette[8], 'weakminus':palettes[5].palette[2], 'mediumminus':palettes[5].palette[4], 'strongminus':palettes[5].palette[6],},
            2: {'palette':palettes[2].palette, 'nodeColor':palettes[2].palette[5], 'ctrlnodeColor':controlNode, 'nodeStroke':palettes[2].palette[6], 'ctrlnodeStroke':ctrlNodeStrokeColor, 'easynodeColor':easyNodeColor, 'mednodeColor':medNodeColor, 'hardnodeColor':hardNodeColor, 'easynodeStrokeColor':easyNodeStrokeColor, 'mednodeStrokeColor':medNodeStrokeColor, 'hardnodeStrokeColor':hardNodeStrokeColor, 'weakplus':palettes[2].palette[2], 'mediumplus':palettes[2].palette[5], 'strongplus':palettes[2].palette[8], 'weakminus':palettes[5].palette[2], 'mediumminus':palettes[5].palette[4], 'strongminus':palettes[5].palette[6],},
            3: {'palette':palettes[3].palette, 'nodeColor':palettes[3].palette[5], 'ctrlnodeColor':controlNode, 'nodeStroke':palettes[3].palette[6], 'ctrlnodeStroke':ctrlNodeStrokeColor, 'easynodeColor':easyNodeColor, 'mednodeColor':medNodeColor, 'hardnodeColor':hardNodeColor, 'easynodeStrokeColor':easyNodeStrokeColor, 'mednodeStrokeColor':medNodeStrokeColor, 'hardnodeStrokeColor':hardNodeStrokeColor, 'weakplus':palettes[3].palette[2], 'mediumplus':palettes[3].palette[5], 'strongplus':palettes[3].palette[8], 'weakminus':palettes[5].palette[2], 'mediumminus':palettes[5].palette[4], 'strongminus':palettes[5].palette[6],},
            4: {'palette':palettes[4].palette, 'nodeColor':palettes[4].palette[5], 'ctrlnodeColor':controlNode, 'nodeStroke':palettes[4].palette[6], 'ctrlnodeStroke':ctrlNodeStrokeColor, 'easynodeColor':easyNodeColor, 'mednodeColor':medNodeColor, 'hardnodeColor':hardNodeColor, 'easynodeStrokeColor':easyNodeStrokeColor, 'mednodeStrokeColor':medNodeStrokeColor, 'hardnodeStrokeColor':hardNodeStrokeColor, 'weakplus':palettes[4].palette[2], 'mediumplus':palettes[4].palette[5], 'strongplus':palettes[4].palette[8], 'weakminus':palettes[5].palette[2], 'mediumminus':palettes[5].palette[4], 'strongminus':palettes[5].palette[6],},
            5: {'palette':palettes[5].palette, 'nodeColor':palettes[5].palette[4], 'ctrlnodeColor':controlNode, 'nodeStroke':palettes[5].palette[5], 'ctrlnodeStroke':ctrlNodeStrokeColor, 'easynodeColor':easyNodeColor, 'mednodeColor':medNodeColor, 'hardnodeColor':hardNodeColor, 'easynodeStrokeColor':easyNodeStrokeColor, 'mednodeStrokeColor':medNodeStrokeColor, 'hardnodeStrokeColor':hardNodeStrokeColor, 'weakplus':palettes[2].palette[2], 'mediumplus':palettes[2].palette[5], 'strongplus':palettes[2].palette[8], 'weakminus':palettes[4].palette[2], 'mediumminus':palettes[4].palette[4], 'strongminus':palettes[4].palette[6],}
          };

          return colors;
        }
    }
})();