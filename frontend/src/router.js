import Vue from 'vue';
import Router from 'vue-router';
import Index from '@/components/Index';
import Gates from '@/components/Gates';
import Cards from '@/components/Cards';
import CardCreate from '@/components/CardCreate';
import CardTests from '@/components/CardTests';
import Attendances from '@/components/Attendances';
import Config from '@/components/Config';
import ConfigIntervalTask from '@/components/ConfigIntervalTask';
import ConfigCrontabTask from '@/components/ConfigCrontabTask';
import SystemConfig from '@/components/SystemConfig';

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
      path: '/card-create/',
      name: 'CardCreate',
      component: CardCreate,
    },
    {
      path: '/card-edit/:card_id',
      name: 'CardEdit',
      component: CardCreate,
    },
    {
      path: '/card-tests',
      name: 'CardTests',
      component: CardTests,
    },

    {
      path: '/attendances',
      name: 'Attendances',
      component: Attendances,
    },

    {
      path: '/config',
      name: 'Config',
      component: Config,
      children: [
        {
          path: 'system-config',
          name: 'system-config',
          component: SystemConfig,
        },

        {
          path: 'interval-task',
          name: 'interval-task',
          component: ConfigIntervalTask,
        },
        {
          path: 'crontab-task',
          name: 'crontab-task',
          component: ConfigCrontabTask,
        },
      ],
    },
  ],
});
