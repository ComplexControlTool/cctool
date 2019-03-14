'use strict';

var path = require('path');
var gulp = require('gulp');
var conf = require('./conf');

var browserSync = require('browser-sync');

var $ = require('gulp-load-plugins')({
  pattern: ['gulp-*', 'main-bower-files', 'uglify-save-license', 'del']
});

function isOnlyChange(event) {
  return event.type === 'changed';
}

gulp.task('watch', ['inject'], function () {

  gulp.watch([path.join(conf.paths.src, '/*.html'), 'bower.json'], ['inject-reload']);

  gulp.watch(path.join(conf.paths.src, '/app/**/*.css'), function(event) {
    if(isOnlyChange(event)) {
      browserSync.reload()
      // browserSync.reload(event.path);
    } else {
      gulp.start('inject-reload');
    }
  });

  gulp.watch(path.join(conf.paths.src, '/app/**/*.js'), function(event) {
    if(isOnlyChange(event)) {
      gulp.start('scripts-reload');
    } else {
      gulp.start('inject-reload');
    }
  });

  gulp.watch(path.join(conf.paths.src, '/app/**/*.html'), function(event) {
    browserSync.reload()
    // browserSync.reload(event.path);
  });
});

gulp.task('watch:django', ['watch'], function () {
  browserSync.instance = browserSync.init({
    notify: false,
    proxy: '172.19.0.4:8000'
  });
  return gulp.src(path.join(conf.paths.tmp, '/serve/*.html'))
    .pipe($.rename('index.html'))
    .pipe($.replace(/href="..\/bower_components\/([^"]{2,})"/g, 'href="{% static \'dashboard/vendor/$1\' %}"'))
    .pipe($.replace(/href="assets\/([^"]{2,})"/g, 'href="{% static \'dashboard/assets/$1\' %}"'))
    .pipe($.replace(/href="app\/([^"]{2,})"/g, 'href="{% static \'dashboard/app/$1\' %}"'))
    .pipe($.replace(/src="..\/bower_components\/([^"]*)"/g, 'src="{% static \'dashboard/vendor/$1\' %}"'))
    .pipe($.replace(/src="app\/([^"]*)"/g, 'src="{% static \'dashboard/app/$1\' %}"'))
    .pipe(gulp.dest(path.join(conf.paths.tmp, '/serve')))
});