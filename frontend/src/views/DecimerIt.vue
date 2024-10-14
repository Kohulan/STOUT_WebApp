<template>
  <div class="decimer-it">
    <div class="main-content">
      <h2 class="title">DECIMER It! - Generate IUPAC Name from Structure or Image</h2>
      <div class="content-wrapper">
        <div class="ketcher-section">
          <h3>Molecular Structure Editor (Ketcher)</h3>
          <div class="ketcher-container">
            <iframe ref="ketcherFrame" src="./standalone/index.html" width="100%" height="600"></iframe>
          </div>
          <div v-if="smiles" class="smiles-output">
            <h4>SMILES Output:</h4>
            <pre>{{ smiles }}</pre>
          </div>
        </div>
        <div class="upload-section">
          <h3>Image Upload and Visualization</h3>
          <input type="file" @change="onFileUpload" accept="image/*" class="file-input">
          <img v-if="processedImage" :src="processedImage" alt="Uploaded Image" class="processed-image">
        </div>
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
        <button @click="generateIupacName" class="generate-button" :disabled="isLoading">
          {{ isLoading ? 'Generating...' : 'Generate IUPAC Name' }}
        </button>
      </div>
      <transition name="fade">
        <div v-if="isLoading" class="loading-overlay">
          <div class="loader"></div>
        </div>
        <div v-else-if="iupacResult" class="result">
          <h3>IUPAC Name Generation Result:</h3>
          <div v-if="outputFormat === 'HTML'" v-html="sanitizedHtml" class="html-result"></div>
          <div v-else class="text-result-container">
            <pre class="text-result">{{ iupacResult }}</pre>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'
import DOMPurify from 'dompurify'

const API_URL = "https://stout.api.decimer.ai"

export default {
  name: 'DecimerIt',
  setup() {
    const store = useStore()

    const state = computed(() => store.getters.getDecimerState)

    const processedImage = computed({
      get: () => state.value.processedImage,
      set: (value) => store.dispatch('updateDecimerState', { processedImage: value })
    })

    const smiles = computed({
      get: () => state.value.smiles,
      set: (value) => store.dispatch('updateDecimerState', { smiles: value })
    })

    const retranslate = computed({
      get: () => state.value.retranslate,
      set: (value) => store.dispatch('updateDecimerState', { retranslate: value })
    })

    const outputFormat = computed({
      get: () => state.value.outputFormat,
      set: (value) => store.dispatch('updateDecimerState', { outputFormat: value })
    })

    const iupacResult = computed({
      get: () => state.value.iupacResult,
      set: (value) => store.dispatch('updateDecimerState', { iupacResult: value })
    })

    const isLoading = ref(false)
    const copySuccess = ref(false)
    const ketcherFrame = ref(null)
    let ketcher = null

    onMounted(() => {
      initKetcher()
    })

    const initKetcher = () => {
      if (ketcherFrame.value) {
        ketcherFrame.value.onload = () => {
          ketcher = ketcherFrame.value.contentWindow.ketcher
          if (smiles.value) {
            ketcher.setMolecule(smiles.value)
          }
        }
      }
    }

    watch(smiles, (newSmiles) => {
      if (ketcher && newSmiles) {
        ketcher.setMolecule(newSmiles)
      }
    })

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

    const onFileUpload = async (event) => {
      const file = event.target.files[0]
      if (file) {
        isLoading.value = true
        try {
          const formData = new FormData()
          formData.append('file', file)
          const response = await axios.post(`${API_URL}/latest/decimer/image2SMILES`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          smiles.value = response.data.SMILES
          processedImage.value = URL.createObjectURL(file)
          if (ketcher) {
            await ketcher.setMolecule(smiles.value)
          }
        } catch (error) {
          console.error('Error processing image with DECIMER:', error)
          alert('An error occurred while processing the image')
        } finally {
          isLoading.value = false
        }
      }
    }

    const generateIupacName = async () => {
      isLoading.value = true
      iupacResult.value = null
      const structure = await getStructure()
      if (!structure) {
        isLoading.value = false
        alert('Error: Unable to get structure from Ketcher')
        return
      }

      try {
        const response = await axios.post(`${API_URL}/latest/stout/SMILE2IUPAC`, structure, {
          params: {
            retranslate: retranslate.value.toString(),
            format: outputFormat.value.toLowerCase()
          },
          headers: { 'Content-Type': 'text/plain', 'Accept': 'application/json' }
        })
        iupacResult.value = outputFormat.value === 'HTML' ? response.data.replace(/\\n/g, '') : response.data
      } catch (error) {
        console.error('Error generating IUPAC name:', error)
        alert('Error generating IUPAC name. Please try again.')
      } finally {
        isLoading.value = false
      }
    }

    const sanitizedHtml = computed(() => {
      if (iupacResult.value && outputFormat.value === 'HTML') {
        const sanitized = DOMPurify.sanitize(iupacResult.value, { ADD_TAGS: ['svg'] })
        return processSVG(sanitized)
      }
      return ''
    })

    const processSVG = (html) => {
      return html.replace(/&lt;\?xml[\s\S]*?&lt;svg[\s\S]*?&lt;\/svg&gt;/g, (match) => {
        const decodedSVG = decodeHTMLEntities(match)
        const svgContent = decodedSVG.replace(/<\?xml[^>]*\?>/, '').trim()
        return `<div class="svg-container">${svgContent}</div>`
      })
    }

    const decodeHTMLEntities = (text) => {
      const textarea = document.createElement('textarea')
      textarea.innerHTML = text
      return textarea.value
    }

    const copyToClipboard = () => {
      if (outputFormat.value === 'JSON' && iupacResult.value) {
        navigator.clipboard.writeText(JSON.stringify(iupacResult.value)).then(() => {
          copySuccess.value = true
          setTimeout(() => {
            copySuccess.value = false
          }, 2000)
        }).catch(err => {
          console.error('Failed to copy text: ', err)
        })
      }
    }

    return {
      ketcherFrame,
      processedImage,
      smiles,
      retranslate,
      outputFormat,
      iupacResult,
      isLoading,
      copySuccess,
      sanitizedHtml,
      onFileUpload,
      generateIupacName,
      copyToClipboard
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bahnschrift:wght@300;400;700&display=swap');

.decimer-it {
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
  font-size: 2.5rem;
  margin-bottom: 40px;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(10, 36, 114, 0.1);
}

.content-wrapper {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
}

.ketcher-section {
  flex: 2;
}

.upload-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.ketcher-container {
  width: 100%;
  height: 600px;
  border: 2px solid #0a2472;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
}

.file-input {
  margin-bottom: 20px;
}

.processed-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(10, 36, 114, 0.1);
}

.smiles-output {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8faff;
  border-radius: 8px;
  border: 1px solid #d0e1ff;
}

.smiles-output pre {
  white-space: pre-wrap;
  word-break: break-all;
}

.control-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.checkbox-container,
.radio-container {
  display: flex;
  align-items: center;
  cursor: pointer;
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

.radio-group {
  display: flex;
  align-items: center;
}

.radio-group>label {
  margin-right: 15px;
  color: #0a2472;
  font-weight: bold;
  font-size: 1.1rem;
}

.radio-options {
  display: flex;
  gap: 20px;
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

  .upload-section,
  .ketcher-section,
  .control-section {
    width: 100%;
  }

  .ketcher-container {
    height: 400px;
  }
}

@media (max-width: 1200px) {
  .content-wrapper {
    flex-direction: column;
  }

  .ketcher-section,
  .upload-section {
    width: 100%;
  }

  .ketcher-container {
    height: 500px;
  }
}

@media (max-width: 768px) {
  .decimer-it {
    padding: 20px;
  }

  .main-content {
    padding: 20px;
  }

  .title {
    font-size: 2rem;
  }

  .ketcher-container {
    height: 400px;
  }

  .options {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .radio-group {
    flex-direction: column;
    align-items: flex-start;
  }

  .radio-options {
    flex-direction: column;
    gap: 10px;
  }

  .generate-button {
    font-size: 1rem;
    padding: 12px 18px;
  }
}

@media (max-width: 480px) {
  .decimer-it {
    padding: 10px;
  }

  .main-content {
    padding: 15px;
  }

  .title {
    font-size: 1.8rem;
  }

  .ketcher-container {
    height: 300px;
  }
}
</style>