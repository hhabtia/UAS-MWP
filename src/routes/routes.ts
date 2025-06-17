import { createRouter, createWebHistory } from 'vue-router'

// Halaman
import LandingPage from '../pages/Landing/landing-page.vue'
import LoginPages from '../pages/Account/LoginPages.vue'
import RegisterPage from '../pages/Account/CreatePages.vue'

// Utilities routing
import { categoryRoute, productRoute, handleRouteMeta } from './route-utils'
import {
	get404PageMeta,
	getCheckoutPageMeta,
	getLandingPageMeta,
} from '../data/meta-utils'

const routes = [
	// Halaman utama
	{
		path: '/',
		name: 'Home',
		component: LandingPage,
		beforeEnter: () => handleRouteMeta(getLandingPageMeta),
		// Jika perlu auth:
		// meta: { requiresAuth: true },
	},

	// Login & Register
	{
		path: '/login',
		name: 'Login',
		component: LoginPages,
	},
	{
		path: '/register',
		name: 'Register',
		component: RegisterPage,
	},

	// Checkout (Contoh: butuh login)
	{
		path: '/checkout',
		component: () => import('../pages/Checkout/checkout-page.vue'),
		beforeEnter: () => handleRouteMeta(getCheckoutPageMeta),
		meta: { requiresAuth: true }, // ✅ user harus login
	},

	// 404 eksplisit
	{
		path: '/404',
		component: () => import('../pages/404/404-page.vue'),
		beforeEnter: () => handleRouteMeta(get404PageMeta),
	},
{
  path: '/search',
  name: 'SearchPage',
  component: () => import('../pages/search.vue'), // ✅ pastikan path-nya sesuai
},
	// Pages
	{
		path: '/scraped-products',
		name: 'ScrapedProducts',
		component: () => import('../pages/Product/scraped-products.vue'),
	},
	{
		path: '/adidas',
		name: 'AdidasProducts',
		component: () => import('../pages/Product/adidas.vue'),
	},
	{
		path: '/converse',
		name: 'ConverseProducts',
		component: () => import('../pages/Product/converse.vue'),
	},
	{
		path: '/about',
		name: 'About',
		component: () => import('../pages/Static/about.vue'),
	},
	
	{
		path: '/contact',
		name: 'Contact',
		component: () => import('../pages/Static/contact.vue'),
	},
	{
  		path: '/compare',
  		name: 'ComparePage',
  		component: () => import('../pages/Compare/compare-pages.vue')
	},

	// Wildcard 404
	{
		path: '/:pathMatch(.*)',
		component: () => import('../pages/404/404-page.vue'),
		beforeEnter: () => handleRouteMeta(get404PageMeta),
	},

	// Kategori
	categoryRoute('keyboards'),
	categoryRoute('keycaps'),
	categoryRoute('deskmats'),

	// Produk
	productRoute('keyboards'),
	productRoute('keycaps'),
	productRoute('deskmats'),
]

const Router = createRouter({
	history: createWebHistory(),
	routes,
	scrollBehavior(_1, _2, savedPosition) {
		return savedPosition || { top: 0 }
	},
})

// ✅ Route guard harus dipanggil setelah Router dideklarasikan
Router.beforeEach((to, from, next) => {
	const isLoggedIn = !!localStorage.getItem('token') // ganti sesuai logic kamu
	if (to.meta.requiresAuth && !isLoggedIn) {
		next('/login')
	} else {
		next()
	}
})

export default Router

