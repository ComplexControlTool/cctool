// graph-editor.filter.js
(function ()
{
    'use strict';

    angular
        .module('app.cctool.pages.graph-editor')
        .filter('functionValue', functionValueFilter)
        .filter('controllabilityValue', controllabilityValueFilter)
        .filter('vulnerabilityValue', vulnerabilityValueFilter)
        .filter('importanceValue', importanceValueFilter)
        .filter('weightValue', weightValueFilter);

    /** @ngInject */
    function functionValueFilter()
    {
        return function (func)
        {
            var retValue = '';
            switch(func) {
                case 'Linear':
                    retValue = 'L'; 
                    break;
                default:
                    retValue = 'L';
            }
            return retValue;
        };
    }

    /** @ngInject */
    function controllabilityValueFilter()
    {
        return function (controllability)
        {
            var retValue = '';
            switch(controllability) {
                case 'None':
                    retValue = 'N';
                    break;
                case 'Low':
                    retValue = 'L'; 
                    break;
                case 'Medium':
                    retValue = 'M'; 
                    break;
                case 'High':
                    retValue = 'H';
                    break;
                default:
                    retValue = 'N';
            }
            return retValue;
        };
    }

    /** @ngInject */
    function vulnerabilityValueFilter()
    {
        return function (controllability)
        {
            var retValue = '';
            switch(controllability) {
                case 'None':
                    retValue = 'N';
                    break;
                case 'Low':
                    retValue = 'L'; 
                    break;
                case 'Medium':
                    retValue = 'M'; 
                    break;
                case 'High':
                    retValue = 'H';
                    break;
                default:
                    retValue = 'N';
            }
            return retValue;
        };
    }

    /** @ngInject */
    function importanceValueFilter()
    {
        return function (controllability)
        {
            var retValue = '';
            switch(controllability) {
                case 'None':
                    retValue = 'N'; 
                    break;
                case 'Low':
                    retValue = 'L'; 
                    break;
                case 'High':
                    retValue = 'H';
                    break;
                default:
                    retValue = 'N';
            }
            return retValue;
        };
    }

    /** @ngInject */
    function weightValueFilter()
    {
        return function (weight)
        {
            var retValue = '';
            switch(weight) {
                case 'Complex':
                    retValue = 'N'; 
                    break;                    
                case 'Positive Weak':
                    retValue = '+W'; 
                    break;
                case 'Positive Medium':
                    retValue = '+M'; 
                    break;
                case 'Positive Strong':
                    retValue = '+S';
                    break;
                case 'Negative Weak':
                    retValue = '-W'; 
                    break;
                case 'Negative Medium':
                    retValue = '-M'; 
                    break;
                case 'Negative Strong':
                    retValue = '-S';
                    break;
                default:
                    retValue = 'N';
            }
            return retValue;
        };
    }

})();