import Vue from 'vue';
import Router from 'vue-router';
import Index from '@/components/Index';
import Gates from '@/components/Gates';
import Cards from '@/components/Cards';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
    },
    {
      path: '/gates',
      name: 'Gates',
      component: Gates,
    },
    {
      path: '/cards',
      name: 'Cards',
      component: Cards,
    },
  ],
});
