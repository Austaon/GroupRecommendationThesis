const mix = require('laravel-mix');

require('laravel-mix-imagemin');
require('laravel-mix-svg-vue');
require('laravel-mix-mjml');

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */

mix.js('resources/js/app.js', 'public/js')
    .copy('resources/img', 'public/img')
    .styles(['resources/css/main.css'], 'public/css/main.css')
    .sass('resources/sass/app.scss', 'public/css')
    .sass('resources/sass/result.scss', 'public/css')
    .mjml('resources/mail', 'resources/views/emails')
    .svgVue({
        svgPath: 'resources/img/icon'
    });
