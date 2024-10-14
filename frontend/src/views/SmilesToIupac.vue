<template>
  <div class="smiles-to-iupac">
    <div class="main-content">
      <h2 class="title">Generate IUPAC Name from SMILES</h2>
      <div class="content-wrapper">
        <div class="input-section">
          <textarea v-model="smiles" placeholder="Enter SMILES string(s) - one per line - max. 50 lines" rows="10"
            class="smiles-input"></textarea>
        </div>
        <div class="control-section">
          <div class="options">
            <label class="checkbox-container">
              <input type="checkbox" v-model="retranslate">
              <span class="checkmark"></span>
              Retranslate (OPSIN)
            </label>
            <div class="radio-group">
              <label>Output Format:</label>
              <div class="radio-options">
                <label class="radio-container" v-for="format in ['HTML', 'JSON', 'TEXT']" :key="format">
                  <input type="radio" v-model="outputFormat" :value="format">
                  <span class="radio-checkmark"></span>
                  {{ format }}
                </label>
              </div>
            </div>
          </div>
          <button @click="generate" class="generate-button" :disabled="!smiles.trim() || isLoading">
            {{ isLoading ? 'Generating...' : 'Generate' }}
          </button>
        </div>
      </div>
      <transition name="fade">
        <div v-if="isLoading" class="loading-overlay">
          <div class="loader"></div>
        </div>
        <div v-else-if="result" class="result">
          <h3>Result:</h3>
          <div v-if="outputFormat === 'HTML'" v-html="sanitizedHtml" class="html-result"></div>
          <div v-else class="text-result-container">
            <pre class="text-result">{{ result }}</pre>
            <button v-if="outputFormat === 'JSON'" @click="copyToClipboard" class="copy-button">
              {{ copySuccess ? 'Copied!' : 'Copy JSON' }}
            </button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { smilesToIupac } from '@/services/api'
import DOMPurify from 'dompurify'

export default {
  name: 'SmilesToIupac',
  data() {
    return {
      smiles: '',
      retranslate: false,
      outputFormat: 'HTML',
      result: null,
      isLoading: false,
      copySuccess: false
    }
  },
  computed: {
    sanitizedHtml() {
      if (this.result && this.outputFormat === 'HTML') {
        const sanitized = DOMPurify.sanitize(this.result, { ADD_TAGS: ['svg'] })
        return this.processSVG(sanitized)
      }
      return ''
    }
  },
  methods: {
    async generate() {
      if (!this.smiles.trim() || this.isLoading) return;

      this.isLoading = true;
      this.result = null;

      try {
        this.result = await smilesToIupac(this.smiles, this.retranslate, this.outputFormat)
      } catch (error) {
        console.error('Error generating IUPAC name:', error)
        this.result = 'Error generating IUPAC name. Please try again.'
      } finally {
        this.isLoading = false;
      }
    },
    processSVG(html) {
      return html.replace(/&lt;\?xml[\s\S]*?&lt;svg[\s\S]*?&lt;\/svg&gt;/g, (match) => {
        const decodedSVG = this.decodeHTMLEntities(match)
        const svgContent = decodedSVG.replace(/<\?xml[^>]*\?>/, '').trim()
        return `<div class="svg-container">${svgContent}</div>`
      })
    },
    decodeHTMLEntities(text) {
      const textarea = document.createElement('textarea')
      textarea.innerHTML = text
      return textarea.value
    },
    copyToClipboard() {
      if (this.outputFormat === 'JSON' && this.result) {
        navigator.clipboard.writeText(this.result).then(() => {
          this.copySuccess = true;
          setTimeout(() => {
            this.copySuccess = false;
          }, 2000);
        }).catch(err => {
          console.error('Failed to copy text: ', err);
        });
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bahnschrift:wght@300;400;700&display=swap');

.smiles-to-iupac {
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
  margin-bottom: 40px;
}

.input-section,
.control-section {
  flex: 1;
  min-width: 300px;
}

.smiles-input {
  width: 100%;
  height: 100%;
  min-height: 300px;
  padding: 20px;
  border: 2px solid #0a2472;
  border-radius: 12px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  resize: vertical;
  background-color: #f8faff;
  color: #0a2472;
}

.smiles-input:focus {
  outline: none;
  border-color: #1e40af;
  box-shadow: 0 0 0 4px rgba(10, 36, 114, 0.2);
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
  content: "";
  display: none;
}

.checkbox-container input:checked~.checkmark:after,
.radio-container input:checked~.radio-checkmark:after {
  display: block;
}

.checkmark:after {
  content: "✓";
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

  .input-section,
  .control-section {
    width: 100%;
  }

  .smiles-input {
    min-height: 200px;
  }
}
</style>