import Vue from 'vue';
import Router from 'vue-router';
import Index from '@/components/Index';
import Gates from '@/components/Gates';
import Cards from '@/components/Cards';
import CardCreate from '@/components/CardCreate';
import CardTests from '@/components/CardTests';

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
    {
      path: '/card-create',
      name: 'CardCreate',
      component: CardCreate,
    },
    {
      path: '/card-tests',
      name: 'CardTests',
      component: CardTests,
    },
  ],
});
