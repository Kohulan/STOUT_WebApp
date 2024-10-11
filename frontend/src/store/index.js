import { createStore } from 'vuex'
import { smilesToIupac, searchPubChem } from '@/services/api'

export default createStore({
  state: {
    decimerIt: {
      processedImage: null,
      smiles: '',
      retranslate: false,
      outputFormat: 'HTML',
      iupacResult: null,
    },
    stout: {
      smiles: 'CCO',
      iupacName: '',
      pubchemIupac: '',
      iupacLoading: false,
      pubchemLoading: false,
    },
  },
  mutations: {
    updateDecimerState(state, payload) {
      state.decimerIt = { ...state.decimerIt, ...payload }
    },
    setStoutSmiles(state, value) {
      state.stout.smiles = value
    },
    setStoutIupacName(state, value) {
      state.stout.iupacName = value
    },
    setStoutPubchemIupac(state, value) {
      state.stout.pubchemIupac = value
    },
    setStoutIupacLoading(state, value) {
      state.stout.iupacLoading = value
    },
    setStoutPubchemLoading(state, value) {
      state.stout.pubchemLoading = value
    },
  },
  actions: {
    updateDecimerState({ commit }, payload) {
      commit('updateDecimerState', payload)
    },
    async getStoutIupacName({ commit, state }) {
      if (state.stout.iupacLoading || !state.stout.smiles.trim()) return
      commit('setStoutIupacLoading', true)
      try {
        const result = await smilesToIupac(state.stout.smiles)
        const parser = new DOMParser()
        const htmlDoc = parser.parseFromString(result, 'text/html')
        const iupacName = htmlDoc
          .querySelector('td:last-child')
          .textContent.trim()
        commit('setStoutIupacName', iupacName)
      } catch (error) {
        console.error('Error generating IUPAC name:', error)
        commit('setStoutIupacName', 'Error generating IUPAC name')
      } finally {
        commit('setStoutIupacLoading', false)
      }
    },
    async searchStoutPubChemName({ commit, state }) {
      if (state.stout.pubchemLoading || !state.stout.smiles.trim()) return
      commit('setStoutPubchemLoading', true)
      try {
        const result = await searchPubChem(state.stout.smiles)
        const pubchemIupac = `<a href="${result.url}" target="_blank" rel="noopener noreferrer" class="link">
          ${result.iupacName}
          <span class="sr-only">(opens in a new tab)</span>
        </a>`
        commit('setStoutPubchemIupac', pubchemIupac)
      } catch (error) {
        console.error('Error searching PubChem:', error)
        commit('setStoutPubchemIupac', 'Error searching PubChem')
      } finally {
        commit('setStoutPubchemLoading', false)
      }
    },
  },
  getters: {
    getDecimerState: (state) => state.decimerIt,
    getStoutState: (state) => state.stout,
  },
})
