// loads various gulp modules
var gulp = require('gulp');
var concat = require('gulp-concat');
var minifyCSS = require('gulp-minify-css');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var imagemin = require('gulp-imagemin');
var pngquant = require('imagemin-pngquant');
var htmlmin = require('gulp-htmlmin');
var critical = require('critical').stream;

// css optimisation
gulp.task('css', function(){
  gulp.src(['css/**/*.css', '!css/style.min.css'])
    .pipe(concat('style.css'))
    .pipe(minifyCSS())
    .pipe(rename('style.min.css'))
    .pipe(gulp.dest('css'))
});

// js optimisation
gulp.task('js', function(){
  return gulp.src([
      '!js/jquery-ui.min.js',
      '!js/jquery.min.js',
      'js/lang.js',
      'js/scripts.js',
      'js/welcomesystem.js',
      'js/guidedtoursystem.js',
      'js/filesystem.js',
      'js/folders.js',
      'js/systemoverlay.js',
      'js/systemmenu.js',
      'js/internetsystem.js',
      'js/emailsystem.js',
      'js/systemsettings.js',
      'js/email.js',
      'js/errormessage.js',
      'js/ubuntuonesystem.js',
      'js/file.js',
      'js/shotwellsystem.js',
      'js/shutdownSystem.js',
      'js/movieplayersystem.js',
      'js/libresystem.js',
      'js/softwaresystem.js',
      'js/notificationsystem.js',
      'js/analytics.js'
    ])
    .pipe(concat('script.js'))
    .pipe(uglify())
    .pipe(rename('script.min.js'))
    .pipe(gulp.dest('js'));
});

// img optimisation
gulp.task('img-min', function(){
   return gulp.src('img/**/*', {base: '.'})
    .pipe(imagemin({
        progressive: true,
        svgoPlugins: [{removeViewBox: false}],
        use: [pngquant()]
    }))
    .pipe(gulp.dest('.'));
});

// html minification
gulp.task('html-minify', function() {
  return gulp.src('en/src/*.html')
    .pipe(htmlmin({collapseWhitespace: true}))
    .pipe(gulp.dest('en'))
});

// Generate & Inline Critical-path CSS
gulp.task('critical', function () {
  return gulp.src('en/src/index.html')
      .pipe(critical({base: 'en/src', inline: true, css: ['css/style.min.css']}))
      .pipe(gulp.dest('en/src'));
});

gulp.task('default', ['css', 'js', 'img-min', 'critical', 'html-minify']);
