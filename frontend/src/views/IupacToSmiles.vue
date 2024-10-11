<template>
  <div class="iupac-to-smiles">
    <h2 class="title">Convert IUPAC Name to SMILES</h2>
    <div class="content-wrapper">
      <div class="input-section">
        <input v-model="iupacName" placeholder="Enter IUPAC Name" class="iupac-input" />
        <div class="options">
          <div class="option-group">
            <label>Converter:</label>
            <div class="toggle-bar">
              <button :class="{ active: converter === 'stout' }" @click="setConverter('stout')">
                STOUT
              </button>
              <button :class="{ active: converter === 'opsin' }" @click="setConverter('opsin')">
                OPSIN
              </button>
            </div>
          </div>
          <div class="option-group">
            <label>Visualization:</label>
            <div class="toggle-bar">
              <button :class="{ active: visualize === '2D' }" @click="setVisualize('2D')">
                2D
              </button>
              <button :class="{ active: visualize === '3D' }" @click="setVisualize('3D')">
                3D
              </button>
            </div>
          </div>
        </div>
        <button class="generate-button" :disabled="!iupacName.trim() || isLoading" @click="generate">
          <span v-if="!isLoading">Generate</span>
          <span v-else class="loading-spinner" />
        </button>
      </div>
      <div v-if="isLoading || result" class="result-container">
        <transition name="fade">
          <div v-if="isLoading" class="loading-overlay">
            <div class="loader" />
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
            <div class="divider" />
            <h3>Depiction:</h3>
            <div class="depiction-container">
              <transition name="fade" mode="out-in">
                <div v-if="visualize === '2D'" key="2D" class="svg-container">
                  <component :is="renderSafeHtml(result.Depiction)" />
                </div>
                <iframe v-else-if="visualize === '3D'" key="3D" :srcdoc="sanitizeHtml(result.Depiction)"
                  class="iframe-container" sandbox="allow-scripts" />
              </transition>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, h } from 'vue'
import { iupacToSmiles } from '@/services/api'
import DOMPurify from 'dompurify'

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
        result.value = await iupacToSmiles(
          iupacName.value,
          converter.value,
          visualize.value
        )
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

    const renderSafeHtml = (html) => {
      const sanitizedHtml = DOMPurify.sanitize(html)
      const div = document.createElement('div')
      div.innerHTML = sanitizedHtml
      return Array.from(div.childNodes).map((node) => {
        if (node.nodeType === Node.ELEMENT_NODE) {
          return h(node.tagName.toLowerCase(), {
            innerHTML: node.innerHTML,
            ...Array.from(node.attributes).reduce((attrs, attr) => {
              attrs[attr.name] = attr.value
              return attrs
            }, {}),
          })
        }
        return node.textContent
      })
    }

    const sanitizeHtml = (html) => {
      return DOMPurify.sanitize(html, {
        ADD_TAGS: ['script'],
        ADD_ATTR: ['src'],
      })
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
      setVisualize,
      renderSafeHtml,
      sanitizeHtml,
    }
  },
}
</script>
<style scoped>
.iupac-to-smiles {
  font-family: 'Bahnschrift', sans-serif;
  width: 100%;
  padding: 40px;
  background-color: #f0f7ff;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 80px);
}

.title {
  color: #0a2472;
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 40px;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(10, 36, 114, 0.1);
}

.content-wrapper {
  display: flex;
  gap: 40px;
  flex-grow: 1;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.1);
  padding: 40px;
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
  padding: 12px;
  font-size: 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  text-transform: uppercase;
  display: flex;
  justify-content: center;
  align-items: center;
}

.generate-button:hover:not(:disabled) {
  background-color: #1e40af;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(10, 36, 114, 0.2);
}

.generate-button:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
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
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #0a2472;
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

@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }

  .input-section {
    flex: none;
    width: 100%;
  }

  .iupac-to-smiles {
    padding: 20px;
  }

  .title {
    font-size: 2rem;
  }
}
</style>
