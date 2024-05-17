import { createApp } from 'vue';
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
  { path: '/', name: 'home', component: Home },
  { path: '/about', name: 'about', component: About },
  { path: '/dna-barcoding', name: 'dna-barcoding', component: DNABarcoding },
  { path: '/data', name: 'data', component: Data },
  {
    path: '/priority-species',
    name: 'priority-species',
    component: PrioritySpecies,
  },
  {
    path: '/related-projects',
    name: 'related-projects',
    component: RelatedProjects,
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount('#app');
