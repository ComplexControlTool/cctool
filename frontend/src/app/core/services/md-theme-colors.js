// md-theme-colors.service.js
(function()
{
    'use strict';

    angular
        .module('app.core')
        .config(config);

    config.$inject = ['$provide', '$mdThemingProvider'];

    /* @ngInject */
    function config($provide, $mdThemingProvider)
    {
        /**
         * Of form:
         * {
         *  'blue':{ // Palette name
         *      '50': #abcdef, // Color name: color value
         *      '100': #abcdee,
         *          ...
         *      },
         *      ...
         * }
         * @type {{}}
         */
        var colorStore = {};

        // Fetch the colors out of the themeing provider.
        Object.keys($mdThemingProvider._PALETTES).forEach(
            // Vlone the pallete colors to the colorStore var.
            function(palleteName) {
                var pallete = $mdThemingProvider._PALETTES[palleteName];
                var colors  = [];
                colorStore[palleteName]=colors;
                Object.keys(pallete).forEach(function(colorName) {
                    // Use an regex to look for hex colors, ignore the rest.
                    if (/#[0-9A-Fa-f]{6}|0-9A-Fa-f]{8}\b/.exec(pallete[colorName])) {
                        colors[colorName] = pallete[colorName];
                    }
                });
            });


        /**
         * mdThemeColors service
         *
         * The mdThemeColors service will provide easy, programmatic access to the themes that have been configured
         * So that the colors can be used according to intent instead of hard coding color values.
         *
         * e.g.
         *
         * <span ng-style="{background: mdThemeColors.primary['50']}">Hello World!</span>
         *
         * So the theme can change but the code doesn't need to.
         */
        $provide.factory('mdThemeColors', ['$rootScope',
            function($rootScope) {
                var service = {};

                var getThemeColorFactory = function(theme, intent){
                    var colors = $mdThemingProvider._THEMES[theme].colors[intent];
                    var name = colors.name
                    // Append the colors with links like hue-1, etc
                    colorStore[name].default = colorStore[name][colors.hues['default']]
                    colorStore[name].hue1 = colorStore[name][colors.hues['hue-1']]
                    colorStore[name].hue2 = colorStore[name][colors.hues['hue-2']]
                    colorStore[name].hue3 = colorStore[name][colors.hues['hue-3']]
                    return colorStore[name];
                }

                service.getThemeColorFactory = getThemeColorFactory;

                return service;
            }
        ]);
    }
})();