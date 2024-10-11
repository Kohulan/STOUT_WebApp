<template>
  <Transition name="fade">
    <div v-if="isVisible" class="splash-screen">
      <div class="splash-content">
        <div class="logo-container">
          <img src="@/assets/STOUT.png" alt="STOUT Logo" class="logo" />
        </div>
        <p class="subtitle">Smiles TO iUpac Translator</p>
        <div class="progress-bar">
          <div class="progress" :style="{ width: `${progress}%` }" />
        </div>
      </div>
      <div class="background-animation" />
    </div>
  </Transition>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue'

export default {
  name: 'SplashScreen',
  props: {
    progress: {
      type: Number,
      default: 0,
      validator: (value) => value >= 0 && value <= 100,
    },
  },
  emits: ['loading-complete'],
  setup(props, { emit }) {
    const animationFrameId = ref(null)
    const time = ref(0)
    const isVisible = ref(true)

    const animate = () => {
      time.value += 0.005
      animationFrameId.value = requestAnimationFrame(animate)
    }

    watch(
      () => props.progress,
      (newProgress) => {
        if (newProgress === 100) {
          setTimeout(() => {
            isVisible.value = false
            emit('loading-complete')
          }, 500) // Delay to show 100% for a moment
        }
      }
    )

    onMounted(() => {
      animate()
    })

    onUnmounted(() => {
      if (animationFrameId.value) {
        cancelAnimationFrame(animationFrameId.value)
      }
    })

    return { time, isVisible }
  },
}
</script>

<style scoped>
.splash-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center,
      #e6f3ff 0%,
      #ffffff 50%,
      #cae2ff 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  overflow: hidden;
}

.splash-content {
  text-align: center;
  color: rgb(0, 0, 0);
  z-index: 2;
}

.logo-container {
  position: relative;
  width: 350px;
  height: 350px;
  margin: 0 auto 20px;
  animation: pulse 2s infinite ease-in-out;
}

.logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 0 15px rgba(42, 42, 56, 0.7));
}

.subtitle {
  font-size: 2rem;
  font-family: 'BahnSchrift', sans-serif;
  font-weight: bold;
  margin-bottom: 30px;
  opacity: 0.9;
  animation: fadeIn 1.5s ease-out;
}

.progress-bar {
  width: 250px;
  height: 6px;
  background-color: rgba(255, 255, 255, 0.3);
  margin: 0 auto;
  border-radius: 3px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: rgb(0, 3, 68);
  transition: width 0.3s ease;
  border-radius: 3px;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
}

.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 20%,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 20%),
    radial-gradient(circle at 80% 80%,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 20%);
  animation: backgroundMove 20s infinite linear;
  z-index: 1;
}

@keyframes pulse {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.05);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 0.9;
  }
}

@keyframes backgroundMove {
  0% {
    background-position: 0% 0%;
  }

  100% {
    background-position: 100% 100%;
  }
}

@media (max-width: 768px) {
  .logo-container {
    width: 140px;
    height: 140px;
  }

  .subtitle {
    font-size: 1.2rem;
  }

  .progress-bar {
    width: 200px;
  }
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
