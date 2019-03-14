// dateString.filter.js
(function()
{
  'use strict';

  angular
    .module('app.cctool')
    .filter('dateString', DateString)
    .filter('recentDate', RecentDate);

  DateString.$inject = ['moment'];
  RecentDate.$inject = ['moment'];

  function DateString(moment)
  {
    return filterFilter;

    ////////////////

    function filterFilter(date)
    {
      return moment(date).format('DD/MM/YYYY HH:mm  (Z)').toString();
    }
  }

  function RecentDate(moment)
  {
    return filterFilter;

    ////////////////

    function filterFilter(date)
    {
      return moment(date).isAfter(moment().subtract(1, 'days'));
    }
  }

})();