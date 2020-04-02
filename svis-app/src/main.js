import Vue from 'vue'
import App from './App.vue'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

Vue.config.productionTip = false


//import * as VueThreejs from 'vue-threejs'
//Vue.use(VueThreejs)
import vb from 'vue-babylonjs';
Vue.use(vb);

new Vue({
  render: h => h(App),
}).$mount('#app')
