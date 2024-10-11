<template>
  <div class="structure-to-iupac">
    <h2 class="title">Generate IUPAC Name from Structure</h2>
    <div class="content-wrapper">
      <div class="ketcher-section">
        <div class="ketcher-container">
          <iframe ref="ketcherFrame" src="./standalone/index.html" width="100%" height="500" />
        </div>
      </div>
      <div class="control-section">
        <div class="options">
          <label class="checkbox-container">
            <input v-model="retranslate" type="checkbox" />
            <span class="checkmark" />
            Retranslate (OPSIN)
          </label>
          <div class="radio-group">
            <label>Output Format:</label>
            <div class="radio-options">
              <label v-for="format in ['HTML', 'JSON', 'TEXT']" :key="format" class="radio-container">
                <input v-model="outputFormat" type="radio" :value="format" />
                <span class="radio-checkmark" />
                {{ format }}
              </label>
            </div>
          </div>
        </div>
        <button class="generate-button" :disabled="isLoading" @click="generate">
          {{ isLoading ? 'Generating...' : 'Generate' }}
        </button>
        <div class="warning">
          <i class="warning-icon">⚠</i>
          Please ensure your structure is complete before generating the IUPAC
          name.
        </div>
      </div>
    </div>
    <transition name="fade">
      <div v-if="isLoading" class="loading-overlay">
        <div class="loader" />
      </div>
      <div v-else-if="result" class="result">
        <h3>Result:</h3>
        <div v-if="outputFormat === 'HTML'" class="html-result">
          <component :is="renderSafeHtml(sanitizedHtml)" />
        </div>
        <div v-else class="text-result-container">
          <pre class="text-result">{{ result }}</pre>
          <button v-if="outputFormat === 'JSON'" class="copy-button" @click="copyToClipboard">
            {{ copySuccess ? 'Copied!' : 'Copy JSON' }}
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, onMounted, computed, h } from 'vue'
import { structureToIupac } from '@/services/api'
import DOMPurify from 'dompurify'

export default {
  name: 'StructureToIupac',
  setup() {
    const ketcherFrame = ref(null)
    const retranslate = ref(false)
    const outputFormat = ref('HTML')
    const result = ref(null)
    const isLoading = ref(false)
    const copySuccess = ref(false)
    let ketcher = null

    onMounted(() => {
      initKetcher()
    })

    const initKetcher = () => {
      ketcherFrame.value.onload = () => {
        ketcher = ketcherFrame.value.contentWindow.ketcher
      }
    }

    const getStructure = async () => {
      if (!ketcher) {
        console.error('Ketcher is not initialized')
        return null
      }
      try {
        return await ketcher.getSmiles()
      } catch (error) {
        console.error('Error getting structure from Ketcher:', error)
        return null
      }
    }

    const generate = async () => {
      isLoading.value = true
      result.value = null
      const structure = await getStructure()
      if (!structure) {
        isLoading.value = false
        result.value = 'Error: Unable to get structure from Ketcher'
        return
      }

      try {
        result.value = await structureToIupac(
          structure,
          retranslate.value,
          outputFormat.value
        )
      } catch (error) {
        console.error('Error generating IUPAC name:', error)
        result.value = 'Error generating IUPAC name. Please try again.'
      } finally {
        isLoading.value = false
      }
    }

    const sanitizedHtml = computed(() => {
      if (result.value && outputFormat.value === 'HTML') {
        const sanitized = DOMPurify.sanitize(result.value, {
          ADD_TAGS: ['svg'],
        })
        return processSVG(sanitized)
      }
      return ''
    })

    const processSVG = (html) => {
      return html.replace(
        /&lt;\?xml[\s\S]*?&lt;svg[\s\S]*?&lt;\/svg&gt;/g,
        (match) => {
          const decodedSVG = decodeHTMLEntities(match)
          const svgContent = decodedSVG.replace(/<\?xml[^>]*\?>/, '').trim()
          return `<div class="svg-container">${svgContent}</div>`
        }
      )
    }

    const decodeHTMLEntities = (text) => {
      const textarea = document.createElement('textarea')
      textarea.innerHTML = text
      return textarea.value
    }

    const copyToClipboard = () => {
      if (outputFormat.value === 'JSON' && result.value) {
        navigator.clipboard
          .writeText(result.value)
          .then(() => {
            copySuccess.value = true
            setTimeout(() => {
              copySuccess.value = false
            }, 2000)
          })
          .catch((err) => {
            console.error('Failed to copy text: ', err)
          })
      }
    }

    const renderSafeHtml = (html) => {
      const div = document.createElement('div')
      div.innerHTML = DOMPurify.sanitize(html, { ADD_TAGS: ['svg'] })
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

    return {
      ketcherFrame,
      retranslate,
      outputFormat,
      result,
      isLoading,
      copySuccess,
      sanitizedHtml,
      generate,
      copyToClipboard,
      renderSafeHtml,
    }
  },
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bahnschrift:wght@300;400;700&display=swap');

.structure-to-iupac {
  font-family: 'Bahnschrift', sans-serif;
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  padding: 40px;
  background-color: #f0f7ff;
  box-sizing: border-box;
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
  margin-bottom: 40px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.1);
  padding: 40px;
}

.ketcher-section,
.control-section {
  flex: 1;
  min-width: 300px;
}

.ketcher-container {
  width: 100%;
  height: 500px;
  border: 2px solid #0a2472;
  border-radius: 12px;
  overflow: hidden;
}

.options {
  margin-bottom: 30px;
}

.checkbox-container,
.radio-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin-bottom: 15px;
  color: #0a2472;
  font-size: 1.1rem;
}

.checkbox-container input,
.radio-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark,
.radio-checkmark {
  height: 24px;
  width: 24px;
  background-color: #f0f7ff;
  border: 2px solid #0a2472;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.checkmark {
  border-radius: 6px;
}

.radio-checkmark {
  border-radius: 50%;
}

.checkbox-container:hover input~.checkmark,
.radio-container:hover input~.radio-checkmark {
  background-color: #d0e1ff;
}

.checkbox-container input:checked~.checkmark,
.radio-container input:checked~.radio-checkmark {
  background-color: #0a2472;
}

.checkmark:after,
.radio-checkmark:after {
  content: '';
  display: none;
}

.checkbox-container input:checked~.checkmark:after,
.radio-container input:checked~.radio-checkmark:after {
  display: block;
}

.checkmark:after {
  content: '✓';
  color: white;
  font-size: 16px;
}

.radio-checkmark:after {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: white;
}

.radio-group>label {
  display: block;
  margin-bottom: 15px;
  color: #0a2472;
  font-weight: bold;
  font-size: 1.2rem;
}

.radio-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
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

.result {
  margin-top: 40px;
  padding: 30px;
  background-color: white;
  border-radius: 16px;
  border: 2px solid #0a2472;
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.1);
}

.text-result-container {
  position: relative;
}

.text-result {
  max-height: 500px;
  overflow-y: auto;
  padding: 20px;
  background-color: #f8faff;
  border-radius: 8px;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 1.1rem;
  color: #0a2472;
}

.copy-button {
  position: absolute;
  top: 15px;
  right: 15px;
  background-color: #0a2472;
  color: white;
  border: none;
  padding: 10px 16px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.copy-button:hover {
  background-color: #1e40af;
  transform: translateY(-2px);
}

.html-result :deep(table) {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 8px rgba(10, 36, 114, 0.1);
}

.html-result :deep(th),
.html-result :deep(td) {
  border: 1px solid #d0e1ff;
  padding: 16px;
  text-align: left;
}

.html-result :deep(th) {
  background-color: #0a2472;
  color: white;
  font-weight: bold;
}

.html-result :deep(.svg-container) {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.html-result :deep(svg) {
  max-width: 100%;
  height: auto;
  box-shadow: 0 4px 8px rgba(10, 36, 114, 0.1);
  border-radius: 8px;
}

.warning {
  margin-top: 30px;
  color: #92400e;
  background-color: #fef3c7;
  border: 2px solid #fde68a;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  font-size: 1.1rem;
}

.warning-icon {
  margin-right: 15px;
  font-size: 1.5rem;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 1200px) {
  .content-wrapper {
    flex-direction: column;
  }

  .ketcher-section,
  .control-section {
    width: 100%;
  }

  .ketcher-container {
    height: 400px;
  }
}
</style>
