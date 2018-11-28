import Vue from 'vue';
import Router from 'vue-router';
import store from './store';

import Index from '@/components/Index';
import Gates from '@/components/Gates';
import Cards from '@/components/Cards';
import CardCreate from '@/components/CardCreate';
import CardTests from '@/components/CardTests';
import Attendances from '@/components/Attendances';
import Config from '@/components/Config';
import ConfigIntervalTask from '@/components/ConfigIntervalTask';
import ConfigCrontabTask from '@/components/ConfigCrontabTask';
import ConfigSystemConfig from '@/components/ConfigSystemConfig';
import ConfigOtherDatabase from '@/components/ConfigOtherDatabase';
import BackgroundTask from '@/components/BackgroundTask';
import LastFailedUpload from '@/components/LastFailedUpload';
import Login from '@/components/Login';
import ConfigClassTime from '@/components/ConfigClassTime';
import card_number_convertor_config from '@/components/card_number_convertor_config';

Vue.use(Router);

export const router = new Router({
  mode: 'history',
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
      path: '/login',
      name: 'login',
      component: Login,
    },

    {
      path: '/last-failed-upload',
      name: 'LastFailedUpload',
      component: LastFailedUpload,
    },

    {
      path: '/config',
      name: 'Config',
      component: Config,
      children: [
        {
          path: 'system-config',
          name: 'system-config',
          component: ConfigSystemConfig,
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
        {
          path: 'other-database',
          name: 'other-database',
          component: ConfigOtherDatabase,
        },
        {
          path: 'background-task',
          name: 'background-task',
          component: BackgroundTask,
        },
        {
          path: 'class-time-config',
          name: 'class-time-config',
          component: ConfigClassTime,
        },

        {
          path: 'card_number_convertor_config',
          name: 'card_number_convertor_config',
          component: card_number_convertor_config,
        },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  // 限制访问的 route
  const guarded_routes = [
    'Gates',
    'Cards',
    'CardCreate',
    'CardEdit',
    'Config',
    'class-time-config',
    'background-task',
    'other-database',
    'crontab-task',
    'interval-task',
    'system-config',
    'card_number_convertor_config',
  ];
  // 如果是限制访问的 route, 进行检测
  if (guarded_routes.includes(to.name)) {
    // 如果已登录, 则放行:
    if (store.getters.is_authenticated) {
      next();
    }
    // 如果未登录, 则到首页
    else {
      next({ name: 'Index' });
    }
  }
  // 不是限制访问的 route, 则放行
  else {
    next();
  }
});
