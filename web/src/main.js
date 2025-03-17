import { createApp, nextTick } from 'vue';
import './style.css';
import App from './App.vue';
import Home from './components/Home.vue';
import About from './components/pages/About.vue';
import DNABarcoding from './components/pages/DNABarcoding.vue';
import Data from './components/pages/Data.vue';
import PrioritySpecies from './components/pages/PrioritySpecies.vue';
import RelatedProjects from './components/pages/RelatedProjects.vue';
import NotFound from './components/pages/NotFound.vue';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { path: '/', name: 'home', component: Home, meta: { title: 'Home' } },
  { path: '/about', name: 'about', component: About, meta: { title: 'About' } },
  {
    path: '/dna-barcoding',
    name: 'dna-barcoding',
    component: DNABarcoding,
    meta: { title: 'DNA Barcoding' },
  },
  {
    path: '/data/:taxonId?',
    name: 'data',
    component: Data,
    meta: { title: 'Data' },
  },
  {
    path: '/priority-species',
    name: 'priority-species',
    component: PrioritySpecies,
    meta: { title: 'Priority Species' },
  },
  {
    path: '/related-projects',
    name: 'related-projects',
    component: RelatedProjects,
    meta: { title: 'Related Projects' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: 'Not Found' },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.afterEach(async (to, from) => {
  await nextTick(() => {
    document.title = `UKBoL - ${to.meta.title}`;
  });
});

createApp(App).use(router).mount('#app');
