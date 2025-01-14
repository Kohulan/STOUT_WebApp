<h1 align="center">
  <a href="https://stout.decimer.ai/" target="_blank">
    <img src="/frontend/src/assets/STOUT.png" width="600" alt="STOUT Logo">
  </a>
</h1>

<h4 align="center">Smiles TO iUpac Translator Web Application</h4>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT%202.0-blue.svg" alt="License"></a>
  <a href="https://GitHub.com/Kohulan/STOUT_WebApp/graphs/commit-activity"><img src="https://img.shields.io/badge/Maintained%3F-yes-blue.svg" alt="Maintenance"></a>
  <a href="https://GitHub.com/Kohulan/STOUT_WebApp/issues/"><img src="https://img.shields.io/github/issues/Kohulan/STOUT_WebApp.svg" alt="GitHub issues"></a>
  <br>
  <a href="https://GitHub.com/Kohulan/STOUT_WebApp/graphs/contributors/"><img src="https://img.shields.io/github/contributors/Kohulan/STOUT_WebApp.svg" alt="GitHub contributors"></a>
  <a href="https://www.tensorflow.org"><img src="https://img.shields.io/badge/TensorFlow-2.15.0-FF6F00.svg?style=flat&logo=tensorflow" alt="tensorflow"></a>
  <a href="https://www.rdkit.org/"><img src="https://img.shields.io/badge/Powered%20by-RDKit-3838ff.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAFVBMVEXc3NwUFP8UPP9kZP+MjP+0tP////9ZXZotAAAAAXRSTlMAQObYZgAAAAFiS0dEBmFmuH0AAAAHdElNRQfmAwsPGi+MyC9RAAAAQElEQVQI12NgQABGQUEBMENISUkRLKBsbGwEEhIyBgJFsICLC0iIUdnExcUZwnANQWfApKCK4doRBsKtQFgKAQC5Ww1JEHSEkAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wMy0xMVQxNToyNjo0NyswMDowMDzr2J4AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDMtMTFUMTU6MjY6NDcrMDA6MDBNtmAiAAAAAElFTkSuQmCC" alt="RDKit badge"></a>
  <br>
  <a href="https://github.com/Kohulan/STOUT_WebApp/actions/workflows/release-please.yml"><img src="https://github.com/Kohulan/STOUT_WebApp/actions/workflows/release-please.yml/badge.svg" alt="Workflow"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/Framework-FastAPI-blue?style" alt="framework"></a>
  <a href="https://stout.api.decimer.ai/latest/docs"><img src="https://img.shields.io/badge/docs-fastapi-blue" alt="FastAPI Documentation"></a>
  <a href="https://vuejs.org/"><img src="https://img.shields.io/badge/Framework-Vue.js-green?style=flat-square" alt="Vue.js Framework"></a>

<p align="center">
  <a href="#about">About</a> •
  <a href="#deployment">Deployment</a> •
  <a href="#license">License</a> •
  <a href="#citation">Citation</a> •
  <a href="#maintenance">Maintenance</a> •
  <a href="#acknowledgments">Acknowledgments</a>
</p>

<hr>

## About

<p align="center">
  <b>STOUT (Smiles TO iUpac Translator) Web Application</b>
</p>

This repository contains the code running on [stout.decimer.ai](https://stout.decimer.ai)

🧪 STOUT-V2 is a powerful tool that can:

- Translate SMILES to IUPAC names
- Convert IUPAC names back to valid SMILES strings

<hr>

## Deployment 🚀

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git

### Local Deployment Steps

1. Clone the repository

```bash
git clone https://github.com/Kohulan/STOUT_WebApp.git
cd STOUT_WebApp
```

2. Build and start the containers

```bash
docker-compose up -d --build
```

### Accessing the Application

Once the containers are running, you can access:

- Frontend: http://localhost:80
- Backend API: http://localhost:3000
- API Documentation: http://localhost:3000/docs

### Container Structure

The application runs two main containers:

- `frontend`: Vue.js application served by Nginx (Port 80)
- `backend`: FastAPI application running with uvicorn (Port 3000)

### Managing the Application

To stop the containers:

```bash
docker-compose down
```

### Troubleshooting

If you encounter any issues:

1. Check container status:

```bash
docker-compose ps
```

2. View container logs:

```bash
# All containers
docker-compose logs

# Specific container
docker-compose logs frontend
docker-compose logs backend
```

3. Common issues:
   - Port conflicts: Ensure ports 80 and 3000 are available
   - Network issues: Check if the `stout-network` is created properly
   - Build errors: Make sure all dependencies are properly listed in requirements.txt and package.json

<hr>

## Training Details 🧠

STOUT V2 uses a transformer-based sequence-to-sequence model

Training tutorial could be found here: [STOUT Training](https://github.com/Kohulan/IWOMI_Tutorials/tree/IWOMI_2024/STOUT_Training)

### Hardware Requirements

#### Minimum Requirements (Inference)
- CPU: 4 cores
- RAM: 8GB
- Storage: 5GB

#### Recommended Requirements (Training)
- TPU v3-8 or equivalent
- High-speed internet connection for dataset downloads

<hr>

## License :scroll:

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Kohulan/STOUT_WebApp/blob/main/LICENSE) file for details

<hr>

## Citation :newspaper:

### Software:

<blockquote>
Rajan, K., Zielesny, A., & Steinbeck, C. (2024). STOUT_WebApp (Version 1.0.0) [Computer software]. https://doi.org/10.5281/zenodo.1234
</blockquote>

### Paper

<blockquote> Rajan, K., Zielesny, A. & Steinbeck, C. STOUT V2.0: SMILES to IUPAC name conversion using transformer models. J Cheminform 16, 146 (2024). https://doi.org/10.1186/s13321-024-00941-x</blockquote>

<hr>

## Maintenance :wrench:

<p align="center">
🔬 <a href="https://stout.decimer.ai">STOUT </a> and <a href="https://decimer.ai">DECIMER</a> are developed and maintained by <a href="https://kohulanr.com">Kohulan Rajan</a> at the <a href="https://cheminf.uni-jena.de">Steinbeck group</a>, <a href="https://www.uni-jena.de/en/">Friedrich Schiller University</a> Jena, Germany.
</p>

<p align="center">
  The code for this web application is released under the <a href="https://opensource.org/licenses/MIT">MIT license</a>. Copyright © CC-BY-SA 2023
</p>

<p align="center">
  <a href="https://cheminf.uni-jena.de/" target="_blank">
    <img src="https://github.com/Kohulan/DECIMER-Image-to-SMILES/blob/master/assets/CheminfGit.png" width="400" alt="cheminf Logo">
  </a>
</p>

<hr>

## Acknowledgments :bulb:

<p align="center">
  Funded by the <a href="https://www.dfg.de/">Deutsche Forschungsgemeinschaft (DFG, German Research Foundation)</a> under the <a href="https://www.chembiosys.de/en/">ChemBioSys</a> (Project INF) - Project number: <b>239748522 - SFB 1127</b>.
</p>

<p align="center">
  <a href="https://www.chembiosys.de/en/welcome.html" target="_blank">
    <img src="https://github.com/Steinbeck-Lab/cheminformatics-microservice/assets/30716951/45c8e153-8322-4563-a51d-cbdbe4e08627" width="300" alt="Chembiosys Logo">
  </a>
</p>

<p align="center">
  Research supported with Cloud TPUs from Google's TPU Research Cloud (TRC)
</p>

<p align="center">
  <a href="https://sites.research.google/trc/about/" target="_blank">
    <img src="https://user-images.githubusercontent.com/30716951/220350828-913e6645-6a0a-403c-bcb8-160d061d4606.png" width="300" alt="TRC Logo">
  </a>
</p>
<p align="center">
  Made with ❤️ by the <a href="https://cheminf.uni-jena.de">Steinbeck Group</a> 
</p>
