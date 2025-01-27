/**
 * This file loads the necessary plugins for Vue and loads the components.
 */

require('./bootstrap');

window.Vue = require('vue');
global.$ = require('jquery');
window.jQuery = $;
require('jquery.redirect');

import VueAxios from 'vue-axios';
import axios from 'axios';
import VTooltip from 'v-tooltip';
import VueTour from 'vue-tour';

import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue';
import VuejsDialog from 'vuejs-dialog';
import VueCookie from 'vue-cookie';
import VueCarousel from 'vue-carousel';
import VueApexCharts from 'vue-apexcharts'
import VueWordCloud from 'vuewordcloud';

import 'hooper/dist/hooper.css';
import 'vuejs-dialog/dist/vuejs-dialog.min.css';
require('vue-tour/dist/vue-tour.css')

/**
 * The following block of code may be used to automatically register your
 * Vue components. It will recursively scan this directory for the Vue
 * components and automatically register them with their "basename".
 *
 * Eg. ./components/ExampleComponent.vue -> <example-component></example-component>
 */

const files = require.context('./', true, /\.vue$/i)
files.keys().map(key => {
    Vue.component(key.split('/').pop().split('.')[0], files(key).default)
})

Vue.use(VueAxios, axios);
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(VTooltip);
Vue.use(VuejsDialog);
Vue.use(VueTour);
Vue.use(VueCookie);
Vue.use(VueCarousel);

Vue.component('apexchart', VueApexCharts);
Vue.component(VueWordCloud.name, VueWordCloud)


/**
 * Next, we will create a fresh Vue application instance and attach it to
 * the page. Then, you may begin adding components to this application
 * or customize the JavaScript scaffolding to fit your unique needs.
 */

const app = new Vue({
    el: '#app',
    components: {
    }
});
