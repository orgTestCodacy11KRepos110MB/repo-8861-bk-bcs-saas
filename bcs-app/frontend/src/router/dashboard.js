/**
 * @file dashboard router 配置
 */

// const DashboardIndex = () => import(/* webpackChunkName: 'dashboard' */'@/views/dashboard')
const DashboardNamespace = () => import(/* webpackChunkName: 'dashboard-namespace' */'@/views/dashboard/namespace.tsx')
const DashboardWorkloadDeployments = () => import(/* webpackChunkName: 'dashboard-workload' */'@/views/dashboard/workload/deployments.vue')
const DashboardWorkloadDaemonSets = () => import(/* webpackChunkName: 'dashboard-workload' */'@/views/dashboard/workload/daemonsets.vue')
const DashboardWorkloadStatefulSets = () => import(/* webpackChunkName: 'dashboard-workload' */'@/views/dashboard/workload/statefulsets.vue')
const DashboardWorkloadCronJobs = () => import(/* webpackChunkName: 'dashboard-workload' */'@/views/dashboard/workload/cronjobs.vue')
const DashboardWorkloadJobs = () => import(/* webpackChunkName: 'dashboard-workload' */'@/views/dashboard/workload/jobs.vue')
const DashboardWorkloadPods = () => import(/* webpackChunkName: 'dashboard-workload' */'@/views/dashboard/workload/pods.vue')
const DashboardWorkloadDetail = () => import(/* webpackChunkName: 'dashboard-workload-detail' */'@/views/dashboard/workload/detail/index.vue')

// 自定义资源
const DashboardCRD = () => import(/* webpackChunkName: 'dashboard-custom' */'@open/views/dashboard/custom/crd.vue')
const DashboardGameStatefulSets = () => import(/* webpackChunkName: 'dashboard-custom' */'@open/views/dashboard/custom/gamestatefulsets.vue')
const DashboardGameDeployments = () => import(/* webpackChunkName: 'dashboard-custom' */'@open/views/dashboard/custom/gamedeployments.vue')
const DashboardCustomObjects = () => import(/* webpackChunkName: 'dashboard-custom' */'@open/views/dashboard/custom/customobjects.vue')

// network
const DashboardNetworkIngress = () => import(/* webpackChunkName: 'dashboard-network' */'@/views/dashboard/network/ingress.vue')
const DashboardNetworkService = () => import(/* webpackChunkName: 'dashboard-network' */'@/views/dashboard/network/service.vue')
const DashboardNetworkEndpoints = () => import(/* webpackChunkName: 'dashboard-network' */'@/views/dashboard/network/endpoints.vue')

// configs
const DashboardConfigsConfigMaps = () => import(/* webpackChunkName: 'dashboard-configs' */'@/views/dashboard/configuration/config-maps.vue')
const DashboardConfigsSecrets = () => import(/* webpackChunkName: 'dashboard-configs' */'@/views/dashboard/configuration/secrets.vue')

// storage
const DashboardStoragePersistentVolumesClaims = () => import(/* webpackChunkName: 'dashboard-storage' */'@/views/dashboard/storage/persistent-volumes-claims.vue')
const DashboardStoragePersistentVolumes = () => import(/* webpackChunkName: 'dashboard-storage' */'@/views/dashboard/storage/persistent-volumes.vue')
const DashboardStorageStorageClass = () => import(/* webpackChunkName: 'dashboard-storage' */'@/views/dashboard/storage/storage-class.vue')

// rbac
const DashboardRbacServiceAccounts = () => import(/* webpackChunkName: 'dashboard-rbac' */'@/views/dashboard/rbac/service-accounts.vue')

const DashboardResourceUpdate = () => import(/* webpackChunkName: 'dashboard-resource' */'@/views/dashboard/resource-update/resource-update.vue')

// HPA
const DashboardHPA = () => import(/* webpackChunkName: 'dashboard-hpa' */'@/views/dashboard/hpa/hpa.vue')

const childRoutes = [
    // dashboard 首页
    // {
    //     path: 'dashboard',
    //     name: 'dashboard',
    //     component: DashboardIndex
    // },
    {
        path: ':clusterId/dashboard',
        name: 'dashboard',
        redirect: {
            name: 'dashboardNamespace'
        },
        meta: { isDashboard: true }
    },
    // dashboard 命名空间
    {
        path: ':clusterId/dashboard/namespace',
        name: 'dashboardNamespace',
        component: DashboardNamespace,
        meta: { isDashboard: true }
    },
    // dashboard workload
    {
        path: ':clusterId/dashboard/workload',
        name: 'dashboardWorkload',
        redirect: {
            name: 'dashboardWorkloadDeployments'
        },
        meta: { isDashboard: true }
    },
    // dashboard workload deployments
    {
        path: ':clusterId/dashboard/workload/deployments',
        name: 'dashboardWorkloadDeployments',
        component: DashboardWorkloadDeployments,
        meta: { isDashboard: true }
    },
    // dashboard workload daemonsets
    {
        path: ':clusterId/dashboard/workload/daemonsets',
        name: 'dashboardWorkloadDaemonSets',
        component: DashboardWorkloadDaemonSets,
        meta: { isDashboard: true }
    },
    // dashboard workload statefulsets
    {
        path: ':clusterId/dashboard/workload/statefulsets',
        name: 'dashboardWorkloadStatefulSets',
        component: DashboardWorkloadStatefulSets,
        meta: { isDashboard: true }
    },
    // dashboard workload cronjobs
    {
        path: ':clusterId/dashboard/workload/cronjobs',
        name: 'dashboardWorkloadCronJobs',
        component: DashboardWorkloadCronJobs,
        meta: { isDashboard: true }
    },
    // dashboard workload jobs
    {
        path: ':clusterId/dashboard/workload/jobs',
        name: 'dashboardWorkloadJobs',
        component: DashboardWorkloadJobs,
        meta: { isDashboard: true }
    },
    // dashboard workload pods
    {
        path: ':clusterId/dashboard/workload/pods',
        name: 'dashboardWorkloadPods',
        component: DashboardWorkloadPods,
        meta: { isDashboard: true }
    },
    {
        path: ':clusterId/dashboard/custom/crd',
        name: 'dashboardCRD',
        component: DashboardCRD,
        meta: { isDashboard: true }
    },
    // dashboard gamestatefulsets
    {
        path: ':clusterId/dashboard/custom/gamestatefulsets',
        name: 'dashboardGameStatefulSets',
        component: DashboardGameStatefulSets,
        meta: { isDashboard: true }
    },
    // dashboard gamedeployments
    {
        path: ':clusterId/dashboard/custom/gamedeployments',
        name: 'dashboardGameDeployments',
        component: DashboardGameDeployments,
        meta: { isDashboard: true }
    },
    // dashboard customobjects
    {
        path: ':clusterId/dashboard/custom/customobjects',
        name: 'dashboardCustomObjects',
        component: DashboardCustomObjects,
        meta: { isDashboard: true }
    },
    // dashboard workload detail
    {
        path: ':clusterId/dashboard/workload/:category/:namespace/:name/detail',
        name: 'dashboardWorkloadDetail',
        props: (route) => ({ ...route.params, kind: route.query.kind }),
        component: DashboardWorkloadDetail,
        meta: { isDashboard: true }
    },
    // network
    {
        path: ':clusterId/dashboard/network',
        name: 'dashboardNetwork',
        redirect: {
            name: 'dashboardNetworkIngress'
        },
        meta: { isDashboard: true }
    },
    // network ingress
    {
        path: ':clusterId/dashboard/network/ingress',
        name: 'dashboardNetworkIngress',
        component: DashboardNetworkIngress,
        meta: { isDashboard: true }
    },
    // network service
    {
        path: ':clusterId/dashboard/network/service',
        name: 'dashboardNetworkService',
        component: DashboardNetworkService,
        meta: { isDashboard: true }
    },
    // network endpoints
    {
        path: ':clusterId/dashboard/network/endpoints',
        name: 'dashboardNetworkEndpoints',
        component: DashboardNetworkEndpoints,
        meta: { isDashboard: true }
    },
    // storage
    {
        path: ':clusterId/dashboard/storage',
        name: 'dashboardStorage',
        redirect: {
            name: 'dashboardStoragePersistentVolumes'
        },
        meta: { isDashboard: true }
    },
    // storage persistent-volumes
    {
        path: ':clusterId/dashboard/storage/persistent-volumes',
        name: 'dashboardStoragePersistentVolumes',
        component: DashboardStoragePersistentVolumes,
        meta: { isDashboard: true }
    },
    // storage persistent-volumes-claims
    {
        path: ':clusterId/dashboard/storage/persistent-volumes-claims',
        name: 'dashboardStoragePersistentVolumesClaims',
        component: DashboardStoragePersistentVolumesClaims,
        meta: { isDashboard: true }
    },
    // storage storage-class
    {
        path: ':clusterId/dashboard/storage/storage-class',
        name: 'dashboardStorageStorageClass',
        component: DashboardStorageStorageClass,
        meta: { isDashboard: true }
    },
    // configs
    {
        path: ':clusterId/dashboard/configs',
        name: 'dashboardConfigs',
        redirect: {
            name: 'dashboardConfigsConfigMaps'
        },
        meta: { isDashboard: true }
    },
    // configs config-maps
    {
        path: ':clusterId/dashboard/configs/config-maps',
        name: 'dashboardConfigsConfigMaps',
        component: DashboardConfigsConfigMaps,
        meta: { isDashboard: true }
    },
    // configs secrets
    {
        path: ':clusterId/dashboard/configs/secrets',
        name: 'dashboardConfigsSecrets',
        component: DashboardConfigsSecrets,
        meta: { isDashboard: true }
    },
    // rbac
    {
        path: ':clusterId/dashboard/rbac',
        name: 'dashboardRbac',
        redirect: {
            name: 'dashboardRbacServiceAccounts'
        },
        meta: { isDashboard: true }
    },
    // rbac service accounts
    {
        path: ':clusterId/dashboard/rbac/service-accounts',
        name: 'dashboardRbacServiceAccounts',
        component: DashboardRbacServiceAccounts,
        meta: { isDashboard: true }
    },
    // resource update
    {
        path: ':clusterId/dashboard/resource/:namespace?/:name?',
        name: 'dashboardResourceUpdate',
        props: (route) => ({ ...route.params, ...route.query }),
        component: DashboardResourceUpdate,
        meta: { isDashboard: true }
    },
    // hpa
    {
        path: ':clusterId/dashboard/hpa',
        name: 'dashboardHPA',
        component: DashboardHPA,
        meta: { isDashboard: true }
    }
]

export default childRoutes
