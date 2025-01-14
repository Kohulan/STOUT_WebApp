<!-- GitHubIssuePopup.vue -->
<template>
  <div>
    <!-- Ultra modern side button -->
    <div class="github-issue-container">
      <button @click="showPopup = true" class="github-issue-button">
        <div class="button-background"></div>
        <div class="button-content">
          <span class="issue-icon pulse-animation">
            <span class="mdi mdi-bug"></span>
          </span>
          <span class="button-text">Report Issue</span>
        </div>
        <div class="particle-container">
          <div v-for="n in 6" :key="n" class="particle"></div>
        </div>
      </button>
    </div>

    <!-- Premium modal with advanced animations -->
    <transition name="modal">
      <div v-if="showPopup" class="modal-overlay" @click.self="showPopup = false">
        <div class="modal-content" :class="{ 'modal-open': showPopup }">
          <!-- Decorative elements -->
          <div class="modal-background">
            <div class="bg-circle circle-1"></div>
            <div class="bg-circle circle-2"></div>
          </div>
          
          <div class="modal-inner">
            <div class="modal-header">
              <div class="title-container">
                <div class="title-icon">
                  <span class="mdi mdi-bug floating"></span>
                </div>
                <h2>Report an Issue</h2>
              </div>
              <button class="close-button" @click="showPopup = false">
                <span class="mdi mdi-close"></span>
                <div class="close-background"></div>
              </button>
            </div>

            <div class="modal-body">
              <div class="message-box glass-card">
                <p class="primary-text">Found something that needs attention?</p>
                <p class="secondary-text">Help us improve by creating a GitHub issue</p>
              </div>
              
              <a 
                :href="githubIssueUrl" 
                target="_blank" 
                rel="noopener noreferrer" 
                class="github-button"
                @click="showPopup = false"
              >
                <div class="button-glow"></div>
                <span class="github-icon mdi mdi-github"></span>
                <span>Create GitHub Issue</span>
                <span class="arrow-icon mdi mdi-arrow-right"></span>
              </a>

              <div class="info-box">
                <div class="info-icon">
                  <span class="mdi mdi-information"></span>
                </div>
                <div class="info-content">
                  <p>Opens GitHub's issue tracker in a new tab</p>
                  <p>GitHub account required</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'GitHubIssuePopup',
  props: {
    repoUrl: {
      type: String,
      required: true,
      default: 'https://github.com/Kohulan/STOUT_WebApp'
    }
  },
  data() {
    return {
      showPopup: false
    }
  },
  computed: {
    githubIssueUrl() {
      return `${this.repoUrl.replace(/\/$/, '')}/issues/new`
    }
  }
}
</script>

<style scoped>
/* Ultra modern animations */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.1); opacity: 1; }
  100% { transform: scale(1); opacity: 0.8; }
}

@keyframes particle {
  0% { transform: translate(0, 0) scale(1); opacity: 0; }
  50% { opacity: 0.5; }
  100% { transform: translate(var(--tx), var(--ty)) scale(0); opacity: 0; }
}

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.floating {
  animation: float 3s ease-in-out infinite;
}

.pulse-animation {
  animation: pulse 2s ease-in-out infinite;
}

/* Side button styling */
.github-issue-container {
  position: fixed;
  right: -160px;
  top: 50%;
  width: 160px;
  height: 48px;
  transform: rotate(-90deg);
  transform-origin: left bottom;
  z-index: 1000;
}

.github-issue-button {
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 16px 16px 0 0;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  padding: 0;
  background: transparent;
}

.button-background {
  position: absolute;
  inset: 0;
  background: linear-gradient(-45deg, #2188ff, #0366d6, #044289, #05264c);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
  opacity: 0.9;
  transition: opacity 0.3s ease;
}

.button-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  height: 100%;
  color: white;
  font-weight: 600;
  font-size: 16px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.particle-container {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: white;
  border-radius: 50%;
  --tx: 0px;
  --ty: 0px;
}

.github-issue-button:hover .particle {
  animation: particle 1s ease-out infinite;
}

.github-issue-button:hover .button-background {
  opacity: 1;
}

/* Modal styling */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.modal-content {
  width: 90%;
  max-width: 540px;
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
}

.modal-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 0;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.circle-1 {
  width: 300px;
  height: 300px;
  background: rgba(33, 136, 255, 0.15);
  top: -100px;
  left: -100px;
}

.circle-2 {
  width: 250px;
  height: 250px;
  background: rgba(46, 164, 79, 0.15);
  bottom: -50px;
  right: -50px;
}

.modal-inner {
  position: relative;
  z-index: 1;
  padding: 32px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.title-container {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #2188ff;
}

.modal-header h2 {
  margin: 0;
  color: white;
  font-size: 1.8rem;
  font-weight: 700;
}

.close-button {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 12px;
  background: transparent;
  cursor: pointer;
  position: relative;
  color: white;
  font-size: 20px;
}

.close-background {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: inherit;
  transition: all 0.3s ease;
}

.close-button:hover .close-background {
  background: rgba(255, 255, 255, 0.2);
}

.message-box {
  text-align: center;
  padding: 24px;
  margin-bottom: 32px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
}

.primary-text {
  color: white;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.secondary-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}

.github-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #2ea44f, #22863a);
  border-radius: 16px;
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.button-glow {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transform: translateX(-100%);
  transition: transform 0.5s ease;
}

.github-button:hover .button-glow {
  transform: translateX(100%);
}

.github-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(46, 164, 79, 0.3);
}

.arrow-icon {
  transition: transform 0.3s ease;
}

.github-button:hover .arrow-icon {
  transform: translateX(4px);
}

.info-box {
  margin-top: 24px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  display: flex;
  gap: 16px;
  align-items: center;
}

.info-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: rgba(255, 255, 255, 0.8);
}

.info-content {
  flex: 1;
}

.info-content p {
  margin: 4px 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Mobile Responsiveness */
@media (max-width: 600px) {
  .modal-content {
    width: 95%;
  }
  
  .modal-inner {
    padding: 24px;
  }
  
  .github-issue-container {
    right: -62px;
    width: 140px;
    height: 44px;
  }

  .button-content {
    font-size: 14px;
  }
  
  .modal-header h2 {
    font-size: 1.5rem;
  }
  
  .title-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
}
</style>