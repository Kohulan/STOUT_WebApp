<template>
  <div class="iupac-to-smiles">
    <div class="main-content">
      <h2 class="title">Convert IUPAC Name to SMILES</h2>
      <div class="content-wrapper">
        <div class="input-section">
          <input v-model="iupacName" placeholder="Enter IUPAC Name" class="iupac-input" />
          <div class="options">
            <div class="option-group">
              <label>Converter:</label>
              <div class="toggle-bar">
                <button @click="setConverter('stout')" :class="{ active: converter === 'stout' }">STOUT</button>
                <button @click="setConverter('opsin')" :class="{ active: converter === 'opsin' }">OPSIN</button>
              </div>
            </div>
            <div class="option-group">
              <label>Visualization:</label>
              <div class="toggle-bar">
                <button @click="setVisualize('2D')" :class="{ active: visualize === '2D' }">2D</button>
                <button @click="setVisualize('3D')" :class="{ active: visualize === '3D' }">3D</button>
              </div>
            </div>
          </div>
          <button @click="generate" class="generate-button" :disabled="!iupacName.trim() || isLoading">
            {{ isLoading ? 'Generating...' : 'Generate' }}
          </button>
        </div>
        <div class="result-container" v-if="isLoading || result">
          <transition name="fade">
            <div v-if="isLoading" class="loading-overlay">
              <div class="loader"></div>
            </div>
          </transition>
          <transition name="fade">
            <div v-if="result" class="result">
              <h3>Generated SMILES:</h3>
              <div class="result-item">
                <strong>Input name:</strong> {{ iupacName }}
              </div>
              <div class="result-item">
                <strong>Output SMILES:</strong> {{ result.SMILES }}
              </div>
              <div class="divider"></div>
              <h3>Depiction:</h3>
              <div class="depiction-container">
                <transition name="fade" mode="out-in">
                  <div v-if="visualize === '2D'" key="2D" v-html="result.Depiction" class="svg-container"></div>
                  <iframe v-else-if="visualize === '3D'" key="3D" :srcdoc="result.Depiction"
                    class="iframe-container"></iframe>
                </transition>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { iupacToSmiles } from '@/services/api'

export default {
  name: 'IupacToSmiles',
  setup() {
    const iupacName = ref('1,3,7-trimethylpurine-2,6-dione')
    const converter = ref('stout')
    const visualize = ref('2D')
    const result = ref(null)
    const isLoading = ref(false)

    const generate = async () => {
      if (!iupacName.value.trim() || isLoading.value) return

      isLoading.value = true
      result.value = null

      try {
        result.value = await iupacToSmiles(iupacName.value, converter.value, visualize.value)
      } catch (error) {
        console.error('Error generating SMILES:', error)
        result.value = { error: 'Error generating SMILES. Please try again.' }
      } finally {
        isLoading.value = false
      }
    }

    const setConverter = (newConverter) => {
      converter.value = newConverter
      if (result.value) {
        generate()
      }
    }

    const setVisualize = (newVisualize) => {
      visualize.value = newVisualize
      if (result.value) {
        generate()
      }
    }

    watch(iupacName, () => {
      result.value = null
    })

    return {
      iupacName,
      converter,
      visualize,
      result,
      isLoading,
      generate,
      setConverter,
      setVisualize
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bahnschrift:wght@300;400;700&display=swap');

.iupac-to-smiles {
  font-family: 'Bahnschrift', sans-serif;
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f0f7ff;
  padding: 40px;
  box-sizing: border-box;
}

.main-content {
  width: 100%;
  max-width: 1600px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.1);
  padding: 40px;
}

.title {
  color: #0a2472;
  font-size: 3rem;
  margin-bottom: 40px;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(10, 36, 114, 0.1);
}

.content-wrapper {
  display: flex;
  gap: 40px;
}

.input-section {
  flex: 0 0 300px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.iupac-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #0a2472;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.iupac-input:focus {
  outline: none;
  border-color: #1e40af;
  box-shadow: 0 0 0 3px rgba(10, 36, 114, 0.2);
}

.options {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  color: #0a2472;
  font-size: 1rem;
  font-weight: bold;
}

.toggle-bar {
  display: flex;
  border: 2px solid #0a2472;
  border-radius: 8px;
  overflow: hidden;
}

.toggle-bar button {
  flex: 1;
  padding: 10px;
  background-color: #f0f7ff;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  color: #0a2472;
}

.toggle-bar button.active {
  background-color: #0a2472;
  color: white;
}

.generate-button {
  background-color: #0a2472;
  color: white;
  border: none;
  padding: 16px 24px;
  font-size: 1.2rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.generate-button:hover:not(:disabled) {
  background-color: #1e40af;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(10, 36, 114, 0.2);
}

.generate-button:disabled {
  background-color: #a3bffa;
  cursor: not-allowed;
}

.result-container {
  flex-grow: 1;
  position: relative;
  background-color: #f8fafc;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 8px rgba(10, 36, 114, 0.1);
  overflow: auto;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader {
  width: 60px;
  height: 60px;
  border: 6px solid #f3f3f3;
  border-top: 6px solid #0a2472;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.result h3 {
  color: #0a2472;
  margin-top: 0;
  font-size: 1.3rem;
  padding-bottom: 12px;
}

.result-item {
  margin-bottom: 16px;
  font-size: 1rem;
  line-height: 1.5;
  color: #0a2472;
}

.divider {
  height: 2px;
  background-color: #e2e8f0;
  margin: 24px 0;
}

.depiction-container {
  margin-top: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.svg-container {
  width: 80%;
  height: 350px;
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
}

.iframe-container {
  width: 100%;
  height: 300px;
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 1200px) {
  .content-wrapper {
    flex-direction: column;
  }

  .input-section {
    flex: none;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .iupac-to-smiles {
    padding: 20px;
  }

  .main-content {
    padding: 20px;
  }

  .title {
    font-size: 2.5rem;
  }

  .generate-button {
    font-size: 1rem;
    padding: 12px 18px;
  }
}

@media (max-width: 480px) {
  .iupac-to-smiles {
    padding: 10px;
  }

  .main-content {
    padding: 15px;
  }

  .title {
    font-size: 2rem;
  }
}
</style>