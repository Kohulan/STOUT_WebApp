<template>
  <div class="decimer-it">
    <h2 class="title">
      Generate IUPAC Name from Structure or Image
    </h2>
    <div class="content-wrapper">
      <div class="upload-section">
        <h3>Image Upload and Visualization</h3>
        <input type="file" accept="image/*" class="file-input" @change="onFileUpload" />
        <img v-if="processedImage" :src="processedImage" alt="Uploaded Image" class="processed-image" />
      </div>
      <div class="ketcher-section">
        <h3>Molecular Structure Editor (Ketcher)</h3>
        <div class="ketcher-container">
          <iframe ref="ketcherFrame" src="./standalone/index.html" width="100%" height="500" />
        </div>
        <div v-if="smiles" class="smiles-output">
          <h4>SMILES Output:</h4>
          <pre>{{ smiles }}</pre>
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
        <button class="generate-button" :disabled="isLoading" @click="generateIupacName">
          {{ isLoading ? 'Generating...' : 'Generate IUPAC Name' }}
        </button>
      </div>
    </div>
    <transition name="fade">
      <div v-if="isLoading" class="loading-overlay">
        <div class="loader" />
      </div>
      <div v-else-if="iupacResult" class="result">
        <h3>IUPAC Name Generation Result:</h3>
        <div v-if="outputFormat === 'HTML'" class="html-result">
          <component :is="renderSafeHtml(sanitizedHtml)" />
        </div>
        <div v-else class="text-result-container">
          <pre class="text-result">{{ iupacResult }}</pre>
          <button v-if="outputFormat === 'JSON'" class="copy-button" @click="copyToClipboard">
            {{ copySuccess ? 'Copied!' : 'Copy JSON' }}
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, h } from 'vue'
import { useStore } from 'vuex'
import DOMPurify from 'dompurify'
import { structureToIupac, decimerit, searchPubChem } from '@/services/api'

export default {
  name: 'DecimerIt',
  setup() {
    const store = useStore()

    const state = computed(() => store.getters.getDecimerState)

    const processedImage = computed({
      get: () => state.value.processedImage,
      set: (value) =>
        store.dispatch('updateDecimerState', { processedImage: value }),
    })

    const smiles = computed({
      get: () => state.value.smiles,
      set: (value) => store.dispatch('updateDecimerState', { smiles: value }),
    })

    const retranslate = computed({
      get: () => state.value.retranslate,
      set: (value) =>
        store.dispatch('updateDecimerState', { retranslate: value }),
    })

    const outputFormat = computed({
      get: () => state.value.outputFormat,
      set: (value) =>
        store.dispatch('updateDecimerState', { outputFormat: value }),
    })

    const iupacResult = computed({
      get: () => state.value.iupacResult,
      set: (value) =>
        store.dispatch('updateDecimerState', { iupacResult: value }),
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
          const response = await decimerit(formData)
          smiles.value = response.SMILES
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
        const response = await structureToIupac(
          structure,
          retranslate.value,
          outputFormat.value
        )
        iupacResult.value =
          outputFormat.value === 'HTML'
            ? response.replace(/\\n/g, '')
            : response

        // Search PubChem for additional information
        try {
          const pubChemData = await searchPubChem(structure)
          iupacResult.value += `\n\nPubChem IUPAC Name: ${pubChemData.iupacName}\nPubChem URL: ${pubChemData.url}`
        } catch (pubChemError) {
          console.error('Error searching PubChem:', pubChemError)
          // Don't alert the user, just log the error
        }
      } catch (error) {
        console.error('Error generating IUPAC name:', error)
        alert('Error generating IUPAC name. Please try again.')
      } finally {
        isLoading.value = false
      }
    }

    const sanitizedHtml = computed(() => {
      if (iupacResult.value && outputFormat.value === 'HTML') {
        const sanitized = DOMPurify.sanitize(iupacResult.value, {
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

    const copyToClipboard = () => {
      if (outputFormat.value === 'JSON' && iupacResult.value) {
        navigator.clipboard
          .writeText(JSON.stringify(iupacResult.value))
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
      copyToClipboard,
      renderSafeHtml,
    }
  },
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bahnschrift:wght@300;400;700&display=swap');

.decimer-it {
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
  margin-bottom: 5px;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(10, 36, 114, 0.1);
}

.content-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  margin-bottom: 40px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.1);
  padding: 40px;
}

.upload-section,
.ketcher-section,
.control-section {
  flex: 1 1 300px;
}

.ketcher-container {
  width: 100%;
  height: 500px;
  border: 2px solid #0a2472;
  border-radius: 12px;
  overflow: hidden;
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
</style>
