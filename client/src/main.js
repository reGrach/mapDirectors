/* ============
 * Main File
 * ============
 *
 * Will initialize the application.
 */

import Vue from 'vue';

/* ============
 * Plugins
 * ============
 *
 * Import and bootstrap the plugins.
 */

import './plugins/axios';
import { router } from './plugins/vue-router';
import './plugins/bootstrap';
import './plugins/font-awesome';

/* ============
 * Styling
 * ============
 *
 * Import the application styling.
 * Stylus is used for this boilerplate.
 *
 * If you don't want to use Stylus, that's fine!
 * Replace the stylus directory with the CSS preprocessor you want.
 * Import the entry point here & install the webpack loader.
 *
 * It's that easy...
 *
 * http://stylus-lang.com/
 */

import './assets/stylus/app.styl';


/*
 * import google maps.
 */

import * as VueGoogleMaps from "vue2-google-maps";

  Vue.use(VueGoogleMaps, {
    load: {
      key: "PAST_YOUR_KEY",
      libraries: "places" // necessary for places input
    }
  });


/* ============
 * Main App
 * ============
 *
 * Last but not least, we import the main application.
 */


import App from './App';

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  /**
   * Bind the Vue instance to the HTML.
   */
  el: '#app',

  /**
   * The router.
   */
  router,

  /**
   * Will render the application.
   *
   * @param {Function} h Will create an element.
   */
  render: h => h(App),
});
