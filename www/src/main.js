import Vue from 'vue'
import Vuetify from 'vuetify'
import App from './App.vue'
import neo4j from './neo4j';

import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'

Vue.use(neo4j);
Vue.use(Vuetify);
const opts = {}

Vue.config.productionTip = false

const vuetify = new Vuetify(opts);

new Vue({
    vuetify,
    render: h => h(App)
}).$mount('#app')