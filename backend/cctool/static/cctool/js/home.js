
$(document).ready(function(e) {
  $('.with-hover-text, .regular-link').click(function(e){
    e.stopPropagation();
  });

  /**********************
  * = Hover text        *
  * Hover text          *
  * for the last slide  *
  ***********************/
  $('.with-hover-text').hover(
    function(e) {
      $(this).css('overflow', 'visible');
      $(this).find('.hover-text')
        .show()
        .css('opacity', 0)
        .delay(200)
        .animate(
          {
            paddingTop: '25px',
            opacity: 1
          },
          'fast',
          'linear'
        );
    },
    function(e) {
      var obj = $(this);
      $(this).find('.hover-text')
        .animate(
          {
            paddingTop: '0',
            opacity: 0
          },
          'fast',
          'linear',
          function() {
            $(this).hide();
            $( obj ).css('overflow', 'hidden');
          }
        );
    }
  );
  
  var img_loaded = 0;
  var j_images = [];
  
  /*************************
  * = Controls active menu *
  * Hover text for the     *
  * last slide             *
  *************************/
  $('#slide-3 img').each(function(index, element) {
    var time = new Date().getTime();
    var oldHref = $(this).attr('src');
    var myImg = $('<img />').attr('src', oldHref + '?' + time );
    
    myImg.load(function(e) {
      img_loaded += 1;;
      if ( img_loaded == $('#slide-3 img').length ) {
        $(function() {
          var pause = 10;
          $(document).scroll(function(e) {
            delay(function() {
              
              var tops = [];
              
              $('.story').each(function(index, element) {
                tops.push( $(element).offset().top - 200 );
              });
        
              var scroll_top = $(this).scrollTop();
              
              var lis = $('.nav > li');
              
              for ( var i=tops.length-1; i>=0; i-- ) {
                if ( scroll_top >= tops[i] ) {
                  menu_focus( lis[i], i+1 );
                  break;
                }
              }
            },
            pause);
          });
          $(document).scroll();
        });
      }
    });
  });
  
});

/******************
* = Gallery width *
******************/
$(function() {
  var pause = 50; // will only process code within delay(function() { ... }) every 100ms.
  $(window).resize(function() {
    delay(function() {
        var gallery_images = $('#slide-3 img');
        
        var images_per_row = 0;
        if ( gallery_images.length % 2 == 0 ) {
          images_per_row = gallery_images.length / 2;
        } else {
          images_per_row = gallery_images.length / 2 + 1;
        }
        
        var gallery_width = $('#slide-3 img').width() * $('#slide-3 img').length;
        gallery_width /= 2;
        if ( $('#slide-3 img').length % 2 != 0 ) {
          gallery_width += $('#slide-3 img').width();
        }
        
        $('#slide-3 .row').css('width', gallery_width );
        
        var left_pos = $('#slide-3 .row').width() - $('body').width();
        left_pos /= -2;
        
        $('#slide-3 .row').css('left', left_pos);
      
      },
      pause
    );
  });
  $(window).resize();
});

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();

function menu_focus( element, i ) {
  if ( $(element).hasClass('active') ) {
    if ( i == 6 ) {
      if ( $('.navbar').hasClass('inv') == false )
        return;
    } else {
      return;
    }
  }
  
  enable_arrows( i );
    
  if ( i == 1 || i == 3 || i == 5 )
    $('.navbar').removeClass('inv');
  else
    $('.navbar').addClass('inv');
  
  $('.nav > li').removeClass('active');
  $(element).addClass('active');
  
  var icon = $(element).find('.fa');
  
  var left_pos = icon.offset().left - $('.nav').offset().left;
  var el_width = icon.width() + $(element).find('.text').width() + 10;
  
  $('.active-menu').stop(false, false).animate(
    {
      left: left_pos,
      width: el_width
    },
    1500,
    'easeInOutExpo'
  );
}

function enable_arrows( dataslide ) {
  $('#arrows div').addClass('disabled');
  if ( dataslide != 1 ) {
    $('#arrow-up').removeClass('disabled');
  }
  if ( dataslide != 6 ) {
    $('#arrow-down').removeClass('disabled');
  }
  if ( dataslide == 3 ) {
    $('#arrow-left').removeClass('disabled');
    $('#arrow-right').removeClass('disabled');
  }
}

/*************
* = Parallax *
*************/
jQuery(document).ready(function ($) {
  //Cache some variables
  var links = $('.nav').find('li');
  slide = $('.slide');
  button = $('.button');
  mywindow = $(window);
  htmlbody = $('html,body');
  
  //Create a function that will be passed a slide number and then will scroll to that slide using jquerys animate. The Jquery
  //easing plugin is also used, so we passed in the easing method of 'easeInOutExpo' which is available throught the plugin.
  function goToByScroll(dataslide) {
    var offset_top = ( dataslide == 1 ) ? '0px' : $('.slide[data-slide="' + dataslide + '"]').offset().top;
    
    htmlbody.stop(false, false).animate({
      scrollTop: offset_top
    }, 1500, 'easeInOutExpo');
  }
  
  //When the user clicks on the navigation links, get the data-slide attribute value of the link and pass that variable to the goToByScroll function
  links.click(function (e) {
    e.preventDefault();
    dataslide = $(this).attr('data-slide');
    goToByScroll(dataslide);
    $(".nav-collapse").collapse('hide');
  });
  
  //When the user clicks on the navigation links, get the data-slide attribute value of the link and pass that variable to the goToByScroll function
  $('.navigation-slide').click(function (e) {
    e.preventDefault();
    dataslide = $(this).attr('data-slide');
    goToByScroll(dataslide);
    $(".nav-collapse").collapse('hide');
  });
});

/***************
* = Menu hover *
***************/
jQuery(document).ready(function ($) {
  //Cache some variables
  var menu_item = $('.nav').find('li');
  
  menu_item.hover(
    function(e) {
      var icon = $(this).find('.fa');
      
      var left_pos = icon.offset().left - $('.nav').offset().left;
      var el_width = icon.width() + $(this).find('.text').width() + 10;
      
      var hover_bar = $('<div class="active-menu special-active-menu"></div>')
        .css('left', left_pos)
        .css('width', el_width)
        .attr('id', 'special-active-menu-' + $(this).data('slide') );
      
      $('.active-menu').after( hover_bar );
    },
    function(e) {
      $('.special-active-menu').remove();
    }
  );
});

/******************
* = Gallery hover *
******************/
jQuery(document).ready(function ($) {
  //Cache some variables
  var images = $('#slide-3 a');
  
  images.hover(
    function(e) {
      var asta = $(this).find('img');
      $('#slide-3 img').not( asta ).stop(false, false).animate(
        {
          opacity: .5
        },
        'fast',
        'linear'
      );
      var zoom = $('<div class="zoom"></div>');
      if ( $(this).hasClass('video') ) {
        zoom.addClass('video');
      }
      $(this).prepend(zoom);
    },
    function(e) {
      $('#slide-3 img').stop(false, false).animate(
        {
          opacity: 1
        },
        'fast',
        'linear'
      );
      $('.zoom').remove();
    }
  );
});

/******************
* = Arrows click  *
******************/
jQuery(document).ready(function ($) {
  //Cache some variables
  var arrows = $('#arrows div');
  
  arrows.click(function(e) {
    e.preventDefault();
    
    if ( $(this).hasClass('disabled') )
      return;
    
    var slide = null;
    var datasheet = $('.nav > li.active').data('slide');
    var offset_top = false;
    var offset_left = false;
    
    
    switch( $(this).attr('id') ) {
      case 'arrow-up':
        offset_top = ( datasheet - 1 == 1 ) ? '0px' : $('.slide[data-slide="' + (datasheet-1) + '"]').offset().top;
        break;
      case 'arrow-down':
        offset_top = $('.slide[data-slide="' + (datasheet+1) + '"]').offset().top;
        break;
      case 'arrow-left':
        offset_left = $('#slide-3 .row').offset().left + 452;
        if ( offset_left > 0 ) {
          offset_left = '0px';
        }
        break;
      case 'arrow-right':
        offset_left = $('#slide-3 .row').offset().left - 452;
        if ( offset_left < $('body').width() - $('#slide-3 .row').width() ) {
          offset_left = $('body').width() - $('#slide-3 .row').width();
        }
        break;
    }
    
    if ( offset_top != false ) {
      htmlbody.stop(false, false).animate({
        scrollTop: offset_top
      }, 1500, 'easeInOutExpo');
    }
    
    if ( offset_left != false ) {
      if ( $('#slide-3 .row').width() != $('body').width() ) {
        $('#slide-3 .row').stop(false, false).animate({
          left: offset_left
        }, 1500, 'easeInOutExpo');
      }
    }
  });
});

/******************
* = Demo Graph    *
******************/ 
jQuery(document).ready(function ($) {
  var isMobile = false; //initiate as false
  // device detection
  if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) isMobile = true;
 
  if (!isMobile)
  {

    var G;
    var tick;
    var homeElement = '#slide-1';
    var homeTitleElement = '#home-row-1';
    var homeGraphElement = '#slide-1';
    var homeGraphStructure = {"0":[[12,"+W"]],
                              "1":[[0,"-W"],[2,"+S"],[12,"-W"]],
                              "2":[[0,"-W"]],
                              "3":[[2,"-M"]],
                              "4":[[11,"+M"]],
                              "5":[[2,"-S"]],
                              "6":[[2,"+W"],[8,"-S"],[9,"+S"],[10,"+S"]],
                              "7":[[4,"-W"],[6,"+M"],[9,"+M"],[11,"-W"],[16,"+S"]],
                              "8":[[9,"+M"]],
                              "9":[[10,"+S"],[17,"+W"]],
                              "10":[[0,"-W"],[1,"+W"],[2,"-W"],[11,"+S"],[13,"+M"],[14,"+S"],[18,"+W"]],
                              "11":[[10,"+M"]],
                              "12":[[6,"+W"]],
                              "13":[[12,"+S"]],
                              "14":[[13,"+W"],[15,"+M"]],
                              "15":[[10,"+S"]],
                              "16":[[15,"+S"]],
                              "17":[[15,"+S"]],
                              "18":[[17,"+S"]]};
    function draw() {
      clearTimeout(tick);
      var edges = [];
      for (var key in homeGraphStructure) {
        for (var value in homeGraphStructure[key]) {
          edges.push([parseInt(key),parseInt(homeGraphStructure[key][value][0].toString())]);
        }
      }
      var color = d3.scale.category10();
      G = new jsnx.DiGraph();
      (function t() {
        if (edges.length) {
          var toAdd = edges.shift();
          G.addEdge.apply(G, toAdd);
          tick = setTimeout(t, 1800);
        }
      }());

      jsnx.draw(G, {
        element: homeGraphElement,
        withLabels: true,
        layoutAttr: {
          'charge': -1300,
          'linkDistance': 70,
          'gravity': 0.3
        },
        panZoom: {
          'enabled': false
        },
        stickyDrag: true,
        nodeAttr: {
          'r': 15
        },
        nodeStyle: {
          'fill': 'rgba(255,255,255,0.8)',
          'stroke': '#111',
          'stroke-width': 1
        },
        edgeStyle: {
          'stroke-width': 6,
          'fill': '#ddd'
        },
        labelStyle: {
          'fill': function(d) {
            return color(d.data.group || +d.node % 4);
          },
          'font-size':17
        },
      }, true);
    }
    draw();
    var timer;
    $(window).resize(function() {
      clearTimeout(timer);
      timer = setTimeout(draw, 300);
    });
  }
});