<template>
  <div class="health-check">
    <h2 class="title">API Health Check</h2>
    <p class="description">
      Monitor the API status in real-time. Click the button below to check the
      current health status.
    </p>
    <button
      :disabled="loading"
      class="check-button"
      aria-live="polite"
      @click="checkHealth"
    >
      <span v-if="!loading">Check Health</span>
      <span v-else class="loading-spinner" aria-hidden="true" />
    </button>
    <transition name="fade">
      <div
        v-if="status"
        class="status"
        :class="statusClass"
        role="status"
        aria-live="polite"
      >
        <i class="status-icon" :class="iconClass" aria-hidden="true" />
        Health Status: {{ status }}
      </div>
    </transition>
    <transition name="fade">
      <div v-if="lastChecked" class="last-checked">
        Last checked: {{ lastChecked }}
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { checkHealth as fetchHealthStatus } from '@/services/api'
import { useToast } from '@/composables/useToast'

export default {
  name: 'HealthCheck',
  setup() {
    const status = ref(null)
    const loading = ref(false)
    const lastChecked = ref(null)
    const { showToast } = useToast()

    const statusClass = computed(() => ({
      'status-healthy': status.value === 'Healthy',
      'status-unhealthy': status.value === 'Unhealthy',
      'status-error': status.value === 'Error',
    }))

    const iconClass = computed(() => ({
      'icon-check': status.value === 'Healthy',
      'icon-warning': status.value === 'Unhealthy',
      'icon-error': status.value === 'Error',
    }))

    const checkHealth = async () => {
      loading.value = true
      status.value = null
      try {
        const result = await fetchHealthStatus()
        status.value = result.status
        lastChecked.value = new Date().toLocaleString()
        showToast(`Health check complete: ${status.value}`, 'success')
      } catch (error) {
        console.error('Error checking health:', error)
        status.value = 'Error'
        showToast('Error checking health. Please try again.', 'error')
      } finally {
        loading.value = false
      }
    }

    return {
      status,
      loading,
      lastChecked,
      statusClass,
      iconClass,
      checkHealth,
    }
  },
}
</script>

<style scoped>
.health-check {
  font-family: 'Bahnschrift', sans-serif;
  background-color: #ffffff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.title {
  font-size: 3rem;
  font-weight: bold;
  color: #0a2472;
  text-align: center;
  margin-bottom: 40px;
  text-shadow: 2px 2px 4px rgba(10, 36, 114, 0.1);
  animation: fadeInDown 1s ease-out;
}

.description {
  color: #4b5563;
  margin-bottom: 25px;
  text-align: center;
  line-height: 1.6;
  font-size: 1.1rem;
  animation: fadeInUp 0.5s ease-out 0.2s both;
}

.check-button {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 14px 28px;
  font-size: 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: block;
  margin: 0 auto 20px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
  animation: fadeInUp 0.5s ease-out 0.4s both;
}

.check-button:hover:not(:disabled) {
  background-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(37, 99, 235, 0.4);
}

.check-button:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
  box-shadow: none;
}

.loading-spinner {
  display: inline-block;
  width: 24px;
  height: 24px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

.status {
  margin-top: 25px;
  padding: 18px;
  border-radius: 10px;
  font-weight: bold;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.5s ease-out;
}

.status-icon {
  margin-right: 12px;
  font-size: 1.4rem;
}

.status-healthy {
  background-color: #d1fae5;
  color: #065f46;
}

.status-unhealthy {
  background-color: #fef3c7;
  color: #92400e;
}

.status-error {
  background-color: #fee2e2;
  color: #b91c1c;
}

.icon-check::before {
  content: '✓';
}
.icon-warning::before {
  content: '⚠';
}
.icon-error::before {
  content: '✗';
}

.last-checked {
  margin-top: 15px;
  font-size: 0.9rem;
  color: #6b7280;
  animation: fadeInUp 0.5s ease-out;
}

.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.5s,
    transform 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .health-check {
    padding: 20px;
  }

  .title {
    font-size: 2rem;
  }

  .description {
    font-size: 1rem;
  }

  .check-button {
    padding: 12px 24px;
    font-size: 1rem;
  }

  .status {
    font-size: 1rem;
    padding: 15px;
  }
}
</style>
