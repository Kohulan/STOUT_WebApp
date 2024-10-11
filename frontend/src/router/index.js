import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SmilesToIupac from '../views/SmilesToIupac.vue'
import StructureToIupac from '../views/StructureToIupac.vue'
import IupacToSmiles from '../views/IupacToSmiles.vue'
import DecimerIt from '../views/DecimerIt.vue'
import HealthCheck from '../views/HealthCheck.vue'
import About from '../views/About.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { keepAlive: true },
  },
  {
    path: '/smiles-to-iupac',
    name: 'SMILES to IUPAC',
    component: SmilesToIupac,
    meta: { keepAlive: true },
  },
  {
    path: '/structure-to-iupac',
    name: 'Structure to IUPAC',
    component: StructureToIupac,
    meta: { keepAlive: true },
  },
  {
    path: '/iupac-to-smiles',
    name: 'IUPAC to SMILES',
    component: IupacToSmiles,
    meta: { keepAlive: true },
  },
  {
    path: '/decimer-it',
    name: 'DECIMER It!',
    component: DecimerIt,
    meta: { keepAlive: true },
  },
  {
    path: '/health-check',
    name: 'Health Check',
    component: HealthCheck,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
