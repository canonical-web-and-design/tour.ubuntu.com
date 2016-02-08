// loads various gulp modules
var gulp = require('gulp');
var imagemin = require('gulp-imagemin');
var pngquant = require('imagemin-pngquant');
var htmlmin = require('gulp-htmlmin');
var inlinesource = require('gulp-inline-source');


// html minification and inlining
gulp.task('compress-html', function() {
  return gulp.src('*/index.html', {base: '.'})
    .pipe(inlinesource())
    .pipe(htmlmin({
      collapseWhitespace: true,
      removeComments: true
    }))
    .pipe(gulp.dest('.'));
});

// img optimisation
gulp.task('compress-images', function(){
   return gulp.src('img/**/*', {base: '.'})
    .pipe(imagemin({
        progressive: true,
        svgoPlugins: [{removeViewBox: false}],
        use: [pngquant()]
    }))
    .pipe(gulp.dest('.'));
});
