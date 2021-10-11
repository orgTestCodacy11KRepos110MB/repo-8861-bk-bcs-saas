/**
 * @file helm router 配置
 */

// Helm应用列表
const helms = () => import(/* webpackChunkName: 'helm' */'@open/views/helm')

// Helm模板列表
const helmTplList = () => import(/* webpackChunkName: 'helm' */'@open/views/helm/tpl-list.vue')

// Helm模板详情
const helmTplDetail = () => import(/* webpackChunkName: 'helm' */'@open/views/helm/tpl-detail.vue')

// Helm实例化
const helmTplInstance = () => import(/* webpackChunkName: 'helm' */'@open/views/helm/tpl-instance.vue')

// Helm app详情
const helmAppDetail = () => import(/* webpackChunkName: 'helm' */'@open/views/helm/app-detail.vue')

const childRoutes = [
    {
        path: 'helm',
        name: 'helms',
        component: helms
    },
    {
        path: 'helm/list',
        name: 'helmTplList',
        component: helmTplList
    },
    {
        path: 'helm/tpl/:tplId',
        name: 'helmTplDetail',
        component: helmTplDetail,
        meta: {
            menuId: 'helmTplList'
        }
    },
    {
        path: 'helm/instance/:tplId',
        name: 'helmTplInstance',
        component: helmTplInstance,
        meta: {
            menuId: 'helmTplList'
        }
    },
    {
        path: 'helm/app/:appId',
        name: 'helmAppDetail',
        component: helmAppDetail,
        meta: {
            menuId: 'helms'
        }
    }
]

export default childRoutes
