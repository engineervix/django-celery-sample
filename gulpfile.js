const gulp = require("gulp");
const npmDist = require("gulp-npm-dist");
const rename = require("gulp-rename");
const sass = require("gulp-sass");
const sourcemaps = require("gulp-sourcemaps");
const bourbon = require("bourbon").includePaths;
const autoprefixer = require("gulp-autoprefixer");
const del = require("del");
const uglify = require("gulp-uglify");
const cleanCss = require("gulp-clean-css");
const babel = require("gulp-babel");
const browserSync = require("browser-sync").create();

// strongly recommended that you set this explicitly for
// forwards-compatibility in case the default ever changes.
sass.compiler = require("node-sass");

// Task to copy vendor libraries
gulp.task("copy-libs", async function () {
  gulp
    .src(
      npmDist({
        excludes: ["sandbox/**/*"],
      }),
      { base: "./node_modules/" }
    )
    .pipe(
      rename(function (path) {
        path.dirname = path.dirname.replace(/\/dist/, "").replace(/\\dist/, "");
      })
    )
    .pipe(gulp.dest("celery_project/static/vendors"));
});

// Task to delete target: contents of the vendor lib folder
gulp.task("clean", function () {
  return del([
    "celery_project/static/vendors/**",
    "!celery_project/static/vendors",
    "!celery_project/static/vendors/.gitignore",
  ]);
});

gulp.task("sass", function () {
  return gulp
    .src("celery_project/static/scss/**/*.scss") // Gets all files ending with .scss in static/scss and children dirs
    .pipe(sourcemaps.init())
    .pipe(
      sass({
        includePaths: [bourbon],
      }).on("error", sass.logError)
    )
    .pipe(
      autoprefixer({
        // browsers: ["cover 99.5%"], not recommended to do this
        cascade: false,
      })
    )
    .pipe(sourcemaps.write("./maps"))
    .pipe(gulp.dest("celery_project/static/css"))
    .pipe(browserSync.stream());
});

gulp.task("lint-css", function lintCssTask() {
  const gulpStylelint = require("gulp-stylelint");

  return gulp
    .src("celery_project/static/scss/**/*.scss")
    .pipe(
      gulpStylelint({
        reporters: [{ formatter: "verbose", console: true }],
        debug: true,
        fix: true,
      })
    )
    .pipe(gulp.dest("celery_project/static/scss"));
});

// Transpile ES6 code into ES5 code using babel
// then Uglify Javascript
gulp.task("uglify", async function () {
  return gulp
    .src("celery_project/static/js/!(*.min).js") // see https://stackoverflow.com/a/58470327
    .pipe(babel({ presets: ["@babel/preset-env"] }))
    .pipe(uglify())
    .pipe(rename({ suffix: ".min" }))
    .pipe(gulp.dest("celery_project/static/js"));
});

// Minify CSS
gulp.task("minify", function () {
  return gulp
    .src("celery_project/static/css/!(*.min).css") // grab everything that doesn't end with *.min.css
    .pipe(cleanCss({ compatibility: "ie9" }))
    .pipe(rename({ suffix: ".min" }))
    .pipe(gulp.dest("celery_project/static/css"));
});

// A simple task to reload the page
gulp.task("reload", function (done) {
  browserSync.reload();
  done();
});

// browserSync init
gulp.task("bs_init", function (done) {
  browserSync.init({
    proxy: "http://127.0.0.1:8000",
    files: [
      "celery_project/static/scss/**/*.scss",
      "celery_project/static/js/**/*.*",
      "celery_project/static/css/**/*.*",
      "celery_project/**/*.html",
      "celery_project/**/*.py",
      "config/**/*.py",
    ],
    port: 3000,
    localOnly: true,
    // Wait for 0.3 seconds before any browsers should try to inject/reload a file
    reloadDelay: 300,
    // Wait 0.5 seconds after a reload event before allowing more
    reloadDebounce: 500,
  });
  // simple static server (from current dir)
  // browserSync.init(null, {
  //   server: {
  //     baseDir: "./",
  //   },
  //   online: true,
  // });
  done();
});

// Watch SCSS, CSS, JS, HTML & .py files for changes
gulp.task("watch", function () {
  gulp.watch("celery_project/static/scss/**/*.scss", gulp.series("sass"));
  gulp.watch("celery_project/static/css/!(*.min).css", gulp.series("minify", "reload"));
  gulp.watch("celery_project/static/js/!(*.min).js", gulp.series("uglify", "reload"));
  gulp.watch("celery_project/**/*.html", gulp.series("reload"));
  gulp.watch("celery_project/**/*.py", gulp.series("reload"));
});

gulp.task("cp", gulp.series("clean", "copy-libs"));
gulp.task("min", gulp.series("sass", "minify", "uglify"));
gulp.task(
  "default",
  gulp.series("sass", "minify", "uglify", "bs_init", "watch")
);
