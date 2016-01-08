// loads various gulp modules
var gulp = require('gulp');
var concat = require('gulp-concat');
var minifyCSS = require('gulp-minify-css');
var rename = require('gulp-rename');
var uncss = require('gulp-uncss');

// create task
gulp.task('css', function(){
  gulp.src('css/**/*')
    .pipe(concat('style.css'))
    .pipe(minifyCSS())
    .pipe(uncss({
        html: ['en/index.html']
    }))
    .pipe(rename('style.min.css'))
    .pipe(gulp.dest('css'))
});

gulp.task('default', ['css']);