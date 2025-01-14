<template>
  <div id="app">
    <Transition name="fade">
      <SplashScreen v-if="isLoading" :progress="loadingProgress" />
    </Transition>
    <Transition name="fade">
      <div v-if="!isLoading">
        <Navigation />
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
        <AppFooter />
        <IssueTracker />
      </div>
    </Transition>
  </div>
</template>

<script>
import { ref, onBeforeMount, onMounted } from 'vue'
import { useStore } from 'vuex'
import Navigation from '@/components/Navigation.vue'
import AppFooter from '@/components/AppFooter.vue'
import SplashScreen from '@/components/SplashScreen.vue'
import IssueTracker from '@/components/IssueTracker.vue'
import { checkHealth } from '@/services/api'

export default {
  name: 'App',
  components: {
    Navigation,
    AppFooter,
    SplashScreen,
    IssueTracker,
  },
  setup() {
    const store = useStore()
    const isLoading = ref(true)
    const loadingProgress = ref(0)

    const initializeApp = async () => {
      console.log('Initializing app...')

      // Simulate loading tasks
      await new Promise((resolve) => setTimeout(resolve, 1000))
      loadingProgress.value = 30

      await initializeState()
      loadingProgress.value = 60

      // Perform health check
      try {
        console.log('Attempting health check...')
        const response = await checkHealth()
        console.log('Health check response:', response)
      } catch (error) {
        console.error('Health check failed:', error)
      }

      await new Promise((resolve) => setTimeout(resolve, 1000))
      loadingProgress.value = 100

      setTimeout(() => {
        isLoading.value = false
      }, 500) // Short delay to ensure smooth transition
    }

    const initializeState = async () => {
      const savedState = localStorage.getItem('decimerState')
      if (savedState) {
        await store.dispatch('initializeState', JSON.parse(savedState))
      }
    }

    onBeforeMount(() => {
      initializeApp()
    })

    onMounted(() => {
      window.addEventListener('beforeunload', () => {
        const state = store.state.decimerIt
        localStorage.setItem('decimerState', JSON.stringify(state))
      })
    })

    return {
      isLoading,
      loadingProgress,
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
