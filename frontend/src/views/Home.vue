<template>
  <div class="home">
    <div class="main-content">
      <header class="header">
        <img src="@/assets/STOUT.png" alt="STOUT Logo" class="logo">
      </header>
      <h1 class="title">Smiles TO iUpac Translator</h1>

      <div class="content-wrapper">
        <div class="input-section">
          <label for="smiles-input" class="sr-only">Enter Molecule SMILES</label>
          <input v-model.lazy="smiles" id="smiles-input" placeholder="Enter Molecule SMILES" class="input-field"
            :disabled="iupacLoading || pubchemLoading" />
          <div class="button-group">
            <button @click="getIupacName" class="btn btn-primary"
              :disabled="iupacLoading || pubchemLoading || !smiles.trim()">
              <span v-if="!iupacLoading">Get IUPAC name</span>
              <span v-else class="loading-spinner" aria-hidden="true"></span>
            </button>
            <button @click="searchPubChemName" class="btn btn-secondary"
              :disabled="pubchemLoading || iupacLoading || !smiles.trim()">
              <span v-if="!pubchemLoading">Search PubChem</span>
              <span v-else class="loading-spinner" aria-hidden="true"></span>
            </button>
          </div>
        </div>

        <transition name="fade">
          <div class="result-section" v-if="iupacName || pubchemIupac">
            <h2 class="result-title">Results:</h2>
            <div class="result-card" v-if="iupacName">
              <h3>STOUT IUPAC</h3>
              <p>{{ iupacName }}</p>
            </div>
            <div class="result-card" v-if="pubchemIupac">
              <h3>PubChem IUPAC</h3>
              <p v-html="pubchemIupac"></p>
            </div>
          </div>
        </transition>

        <div class="info-section">
          <p class="info-text">To draw a structure, please visit the <router-link to="/structure-to-iupac"
              class="link">Structure to IUPAC tab</router-link>.</p>
          <img :src="stoutGif" alt="STOUT Animation" class="stout-gif">
          <p class="info-text">The first open-source SMILES to IUPAC name Translator, <strong>STOUT</strong>: Bridging
            the Gap Between Molecules and Names!</p>
        </div>

        <div class="warning-container">
          <div class="warning" role="alert">
            <span aria-hidden="true">⚠️</span> Disclaimer: STOUT is a language model that can make mistakes
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { smilesToIupac, searchPubChem } from '@/services/api'
import stoutGif from '@/assets/stout.gif'

export default {
  name: 'HomePage',
  setup() {
    const store = useStore()

    const smiles = computed({
      get: () => store.state.stout.smiles,
      set: (value) => store.commit('setStoutSmiles', value)
    })
    const iupacName = computed(() => store.state.stout.iupacName)
    const pubchemIupac = computed(() => store.state.stout.pubchemIupac)
    const iupacLoading = computed({
      get: () => store.state.stout.iupacLoading,
      set: (value) => store.commit('setStoutIupacLoading', value)
    })
    const pubchemLoading = computed({
      get: () => store.state.stout.pubchemLoading,
      set: (value) => store.commit('setStoutPubchemLoading', value)
    })

    const getIupacName = async () => {
      if (iupacLoading.value || !smiles.value.trim()) return
      iupacLoading.value = true
      try {
        const result = await smilesToIupac(smiles.value)
        const parser = new DOMParser()
        const htmlDoc = parser.parseFromString(result, 'text/html')
        store.commit('setStoutIupacName', htmlDoc.querySelector('td:last-child').textContent.trim())
      } catch (error) {
        console.error('Error generating IUPAC name:', error)
        store.commit('setStoutIupacName', 'Error generating IUPAC name')
      } finally {
        iupacLoading.value = false
      }
    }

    const searchPubChemName = async () => {
      if (pubchemLoading.value || !smiles.value.trim()) return
      pubchemLoading.value = true
      try {
        const result = await searchPubChem(smiles.value)
        const pubchemIupacHtml = `<a href="${result.url}" target="_blank" rel="noopener noreferrer" class="link">
          ${result.iupacName}
          <span class="sr-only">(opens in a new tab)</span>
        </a>`
        store.commit('setStoutPubchemIupac', pubchemIupacHtml)
      } catch (error) {
        console.error('Error searching PubChem:', error)
        store.commit('setStoutPubchemIupac', 'Error searching PubChem')
      } finally {
        pubchemLoading.value = false
      }
    }

    return {
      smiles,
      iupacName,
      pubchemIupac,
      iupacLoading,
      pubchemLoading,
      stoutGif,
      getIupacName,
      searchPubChemName
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bahnschrift:wght@300;400;700&display=swap');

.home {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Bahnschrift', 'Arial', sans-serif;
  color: #0a2472;
  background-color: #f0f7ff;
  padding: 40px;
  box-sizing: border-box;
}

.main-content {
  width: 100%;
  max-width: 800px;
  background-color: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.1);
}

.header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
}

.logo {
  width: 400px;
  height: auto;
  margin: 0;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.title {
  font-size: 2.5rem;
  color: #0a2472;
  margin: 0 0 2rem;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(10, 36, 114, 0.1);
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-section {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.input-field {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 2px solid #0a2472;
  border-radius: 8px;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.input-field:focus {
  outline: none;
  border-color: #1e40af;
  box-shadow: 0 0 0 3px rgba(10, 36, 114, 0.2);
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  width: 100%;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 150px;
  font-weight: bold;
}

.btn-primary {
  background-color: #0a2472;
  color: white;
}

.btn-secondary {
  background-color: #1e40af;
  color: white;
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(10, 36, 114, 0.2);
}

.btn-primary:hover:not(:disabled) {
  background-color: #1e40af;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn:disabled {
  opacity: 0.65;
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

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.result-section {
  width: 100%;
  text-align: center;
  margin-bottom: 2rem;
}

.result-title {
  font-size: 1.5rem;
  color: #0a2472;
  margin-bottom: 1rem;
}

.result-card {
  background-color: #f0f7ff;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 6px rgba(10, 36, 114, 0.1);
  transition: all 0.3s ease;
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(10, 36, 114, 0.15);
}

.result-card h3 {
  color: #0a2472;
  margin-bottom: 0.5rem;
}

.info-section {
  width: 100%;
  text-align: center;
  margin-bottom: 2rem;
}

.info-text {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  color: #0a2472;
}

.stout-gif {
  max-width: 150px;
  margin: 1rem auto;
  display: block;
  pointer-events: none;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(10, 36, 114, 0.1);
}

.warning-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.warning {
  background-color: #fef3c7;
  border-left: 5px solid #f59e0b;
  color: #92400e;
  padding: 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  max-width: 80%;
  transition: all 0.3s ease;
}

.warning:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(146, 64, 14, 0.1);
}

.link {
  color: #1e40af;
  text-decoration: none;
  transition: all 0.3s ease;
}

.link:hover {
  color: #2563eb;
  text-decoration: underline;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

@media (max-width: 768px) {
  .home {
    padding: 20px;
  }

  .main-content {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }

  .title {
    font-size: 2rem;
  }
}
</style>