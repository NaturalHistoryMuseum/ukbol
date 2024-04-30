import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import Home from './components/Home.vue';
import About from './components/About.vue';
import DNABarcoding from './components/DNABarcoding.vue';
import Data from './components/Data.vue';
import PrioritySpecies from './components/PrioritySpecies.vue';
import RelatedProjects from './components/RelatedProjects.vue';
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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount('#app');
