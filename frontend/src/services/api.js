import axios from 'axios'

const getApiUrl = () => {
  if (process.env.NODE_ENV === 'production') {
    // In production, use the current origin (host) with the backend port
    const host = window.location.hostname
    return `http://${host}:3000`
  }
  // In development, use the environment variable or default to localhost
  return process.env.VUE_APP_API_URL || 'http://localhost:3000'
}

const API_URL = getApiUrl()
console.log('API URL:', API_URL)

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

export const smilesToIupac = async (
  smiles,
  retranslate = false,
  format = 'HTML'
) => {
  try {
    const response = await api.post('/latest/stout/SMILE2IUPAC', smiles, {
      params: {
        retranslate: retranslate.toString(),
        format: format.toLowerCase(),
      },
      headers: { 'Content-Type': 'text/plain' },
    })
    return response.data
  } catch (error) {
    console.error('Error in smilesToIupac:', error)
    throw error
  }
}

export const structureToIupac = async (
  structure,
  retranslate = false,
  format = 'HTML'
) => {
  try {
    const response = await api.post('/latest/stout/SMILE2IUPAC', structure, {
      params: {
        retranslate: retranslate.toString(),
        format: format.toLowerCase(),
      },
      headers: { 'Content-Type': 'text/plain' },
    })
    return response.data
  } catch (error) {
    console.error('Error in structureToIupac:', error)
    throw error
  }
}

export const iupacToSmiles = async (
  iupacName,
  converter = 'stout',
  visualize = '2D'
) => {
  try {
    const response = await api.get('/latest/stout/IUPAC2SMILES', {
      params: { input_text: iupacName, converter, visualize },
    })
    return response.data
  } catch (error) {
    console.error('Error in iupacToSmiles:', error)
    throw error
  }
}

export const decimerit = async (formData) => {
  try {
    const response = await api.post('/latest/decimer/image2SMILES', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  } catch (error) {
    console.error('Error in decimerit:', error)
    throw error
  }
}

export const checkHealth = async () => {
  try {
    const url = `${API_URL}/latest/stout/health`
    console.log(`Checking health at: ${url}`)
    const response = await api.get('/latest/stout/health')
    return response.data
  } catch (error) {
    console.error('Error in checkHealth:', error)
    throw error
  }
}

export const searchPubChem = async (smiles) => {
  try {
    const response = await axios.get(
      `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/${encodeURIComponent(smiles)}/property/IUPACName/JSON`
    )
    const iupacName = response.data.PropertyTable.Properties[0].IUPACName
    const cid = response.data.PropertyTable.Properties[0].CID
    const url = `https://pubchem.ncbi.nlm.nih.gov/compound/${cid}`
    return { iupacName, url }
  } catch (error) {
    console.error('Error in searchPubChem:', error)
    throw error
  }
}
