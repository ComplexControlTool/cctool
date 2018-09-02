// fileUpload.directive.js
(function()
{
  'use strict';

  angular
    .module('app.directives.fileUpload')
    .directive('fileUpload', fileUpload);

  fileUpload.$inject = [];

  /** @ngInject */
  function fileUpload()
  {
    // Usage:
    //   e.g.
    //      <div file-upload="[image/png, image/jpeg, image/gif]" file="image" file-name="imageFileName" data-max-file-size="maxSize"></div>
    //
    // Creates:
    //
    var directive =
    {
      restrict: 'A',
      link: link,
      templateUrl : 'app/directives/fileUpload/fileUpload.template.html',
      scope:{
        file: '=',
        fileName: '='
      },
      controller: FileUploadController,
      controllerAs: 'vm',
      bindToController: true
    };

    return directive;

    function link(scope, element, attrs)
    {
      var validMimeTypes, checkSize, isTypeValid, readFile, processDragOverOrEnter, processDrop, openFilesystem;
      var input = $(element[0].querySelector('#fileInput'));
      var button = $(element[0].querySelector('#uploadButton'));
      var dropzone = $(element[0].querySelector('#uploadDrop'));
      var textInput = $(element[0].querySelector('#textInput'));

      validMimeTypes = attrs.fileUpload;
      
      checkSize = function(size)
      {
        var _ref;
        if (((_ref = attrs.maxFileSize) === (void 0) || _ref === '') || (size / 1024) / 1024 < attrs.maxFileSize) {
          return true;
        } else {
          alert("File must be smaller than " + attrs.maxFileSize + " MB");
          return false;
        }
      };

      isTypeValid = function(type)
      {
        if ((validMimeTypes === (void 0) || validMimeTypes === '') || validMimeTypes.indexOf(type) > -1) {
          return true;
        } else {
          alert("Invalid file type.  File must be one of following types " + validMimeTypes);
          return false;
        }
      };

      readFile = function(file)
      {
        var file, name, reader, size, type;
        reader = new FileReader();
        reader.onload = function(evt) {
          if (checkSize(size) && isTypeValid(type)) {
            return scope.$apply(function() {
              scope.vm.file = evt.target.result;
              if (angular.isString(scope.vm.fileName)) {
                return scope.vm.fileName = name;
              }
            });
          }
        };
        name = file.name;
        type = file.type;
        size = file.size;
        reader.readAsText(file);
        return false;
      };

      processDragOverOrEnter = function(event)
      {
        if (event != null) {
          event.preventDefault();
        }
        event = event.originalEvent;
        event.dataTransfer.effectAllowed = 'copy';
        return false;
      };

      processDrop = function(event)
      {
        var file, name, reader, size, type;
        if (event != null) {
          event.preventDefault();
        }
        event = event.originalEvent;
        file = event.dataTransfer.files[0];
        readFile(file);
        return false;
      };

      openFilesystem = function(event)
      {
        var files = event.target.files;
        if (files[0])
        {
          readFile(files[0])
        }
        scope.$apply();
      };

      if (input.length && button.length && textInput.length)
      {
        button.click(function(event)
        {
          input.click();
        });
        textInput.click(function(event) {
          input.click();
        });
      }

      dropzone.on('dragover', processDragOverOrEnter);
      dropzone.on('dragenter', function(event){
        $(this).css("background-color","#fefefe");
        $(this).css("border-color","#444");
        processDragOverOrEnter(event);
      });
      dropzone.on('dragleave', function(event){
        $(this).css("background-color","transparent");
        $(this).css("border-color","#ddd");
      });
      dropzone.on('drop', function(event){
        $(this).css("background-color","transparent");
        $(this).css("border-color","#ddd");
        processDrop(event);
      });
      input.on('change', openFilesystem)

      return
    }

    /** @ngInject */
    function FileUploadController($scope) {}


  }

})();