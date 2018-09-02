// dateString.filter.js
(function()
{
  'use strict';

  angular
    .module('app.cctool')
    .filter('dateString', DateString);

  DateString.$inject = ['moment'];

  function DateString(moment)
  {
    return filterFilter;

    ////////////////

    function filterFilter(date)
    {
      return moment(date).format('DD/MM/YYYY HH:mm  (Z)').toString();
    }
  }

})();