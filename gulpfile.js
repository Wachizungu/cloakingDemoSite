const { src, dest, parallel} = require('gulp');

function javascript(cb) {
    src('./bower_components/jquery/dist/jquery.min.js')
        .pipe(dest('./static/js/'));
    src('./bower_components/bootstrap/dist/js/bootstrap.min.js')
        .pipe(dest('./static/js/'));
    src('./bower_components/detectrtc/DetectRTC.min.js')
        .pipe(dest('./static/js/'));
    cb();
}

function css(cb) {
    src('./bower_components/bootstrap/dist/css/bootstrap.min.css')
        .pipe(dest('./static/css/'));
    cb();
}

exports.dev = parallel(javascript, css);
