<template>
  <div class="about">
    <div class="main-content">
      <h1 class="title">About STOUT</h1>
      <div class="content-wrapper">
        <section class="section developers">
          <h2>Our Team</h2>
          <p class="team-description">
            🔬 STOUT was developed by <a href="https://www.linkedin.com/in/kohulanrajan/" target="_blank"
              rel="noopener noreferrer" class="link">Dr. Kohulan Rajan</a> under the supervision of
            <a href="https://www.w-hs.de/service/informationen-zur-person/person/zielesny/" target="_blank"
              rel="noopener noreferrer" class="link">Prof. Achim Zielesny</a> and
            <a href="https://www.linkedin.com/in/steinbeck/" target="_blank" rel="noopener noreferrer"
              class="link">Prof. Christoph Steinbeck</a>.
          </p>
          <div class="team-grid">
            <div class="team-member" v-for="(member, index) in team" :key="index">
              <img :src="member.image" :alt="member.name" class="avatar">
              <h3>{{ member.name }}</h3>
              <p class="role">{{ member.role }}</p>
              <a :href="member.link" target="_blank" rel="noopener noreferrer" class="link">{{ member.linkText }}</a>
            </div>
          </div>          
        </section>

        <section class="section citation">
          <h2>How to cite us?</h2>
          <div class="citation-box" v-for="(citation, index) in citations" :key="index">
            <p>{{ citation.title }}</p>
            <p>{{ citation.text }} <a :href="citation.link" target="_blank" rel="noopener noreferrer" class="link">{{
              citation.linkText }}</a></p>
          </div>
        </section>

        <section class="section data-availability">
          <h2>Data Availability</h2>
          <div class="data-links">
            <div class="data-item">
              <h3>Project Resources</h3>
              <ul>
                <li>
                  <strong>Project Git page:</strong>
                  <a href="https://github.com/Kohulan/Smiles-TO-iUpac-Translator" target="_blank"
                    rel="noopener noreferrer" class="link">
                    https://github.com/Kohulan/Smiles-TO-iUpac-Translator
                  </a>
                </li>
                <li>
                  <strong>Web Application Git page:</strong>
                  <a href="https://github.com/Kohulan/STOUT_WebApp" target="_blank" rel="noopener noreferrer"
                    class="link">
                    https://github.com/Kohulan/STOUT_WebApp
                  </a>
                </li>
                <li>
                  <strong>Models and checkpoints:</strong>
                  <a href="https://zenodo.org/records/13318286" target="_blank" rel="noopener noreferrer" class="link">
                    https://zenodo.org/records/13318286
                  </a>
                </li>
                <li>
                  <strong>Tutorial for Training:</strong>
                  <a href="https://github.com/Kohulan/IWOMI_Tutorials/tree/IWOMI_2024/STOUT_Training" target="_blank"
                    rel="noopener noreferrer" class="link">
                    IWOMI Tutorials - STOUT Training
                  </a>
                </li>
              </ul>
            </div>
            <div class="data-item">
              <h3>Version & License</h3>
              <ul>
                <li><strong>Current version:</strong> <a href="https://github.com/Kohulan/Smiles-TO-iUpac-Translator/releases/tag/v2.1.2" target="_blank" rel="noopener noreferrer"
                    class="link">v2.1.2</a>
                </li>
                <li><strong>License:</strong>
                  <a href="https://opensource.org/license/mit" target="_blank" rel="noopener noreferrer"
                    class="link">MIT</a>
                </li>
                <li><strong>Restrictions for non-academics:</strong> None</li>
              </ul>
            </div>
            <div class="data-item">
              <h3>Documentation</h3>
              <ul>
                <li>
                  <strong>API:</strong>
                  <a href="https://stout.api.decimer.ai/latest/docs" target="_blank" rel="noopener noreferrer"
                    class="link">
                    https://stout.api.decimer.ai/latest/docs
                  </a>
                </li>
                <li>
                  <strong>Python docs:</strong>
                  <a href="https://stout-web-application.readthedocs.io/en/latest/index.html" target="_blank"
                    rel="noopener noreferrer" class="link">
                    https://stout-web-application.readthedocs.io
                  </a>
                </li>
                <li>
                  <strong>PyPI Package:</strong>
                  <a href="https://pypi.org/project/STOUT-pypi/" target="_blank" rel="noopener noreferrer" class="link">
                    https://pypi.org/project/STOUT-pypi/
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </section>

        <section class="section contact">
          <h2>Contact Us</h2>
          <div class="contact-info">
            <div class="map-container">
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2503.2949726059553!2d11.581905350629135!3d50.93352470346138!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47a6a898c3634fbb%3A0xdf22378d9f537b71!2sLessingstra%C3%9Fe%208%2C%2007743%20Jena%2C%20Germany!5e0!3m2!1sen!2s!4v1681045800175!5m2!1sen!2s"
                width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"
                title="Location map"></iframe>
            </div>
            <div class="contact-details">
              <div class="address">
                <h3>Address</h3>
                <p>Institute for Inorganic and Analytical Chemistry, Friedrich Schiller University, Lessingstraße 8,
                  Jena 07743, Germany</p>
              </div>
              <div class="authors">
                <h3>Authors</h3>
                <ul>
                  <li v-for="(author, index) in authors" :key="index">
                    {{ author.name }}: <a :href="'mailto:' + author.email" class="link">{{ author.email }}</a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section class="section acknowledgement">
          <h2>Acknowledgement</h2>
          <p>Research supported with Cloud TPUs from Google's TPU Research Cloud (TRC)</p>
          <a href="https://sites.research.google/trc/about/" target="_blank" rel="noopener noreferrer">
            <img src="@/assets/tpu-research-cloud-logo.png" alt="TPU Research Cloud Logo" width="250" class="tpu-logo">
          </a>
          <p>We greatly acknowledge OpenEye for granting us an academic license to their Lexichem software, without
            which this work would not have been possible.</p>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutPage',
  data() {
    return {
      team: [
        { name: 'Dr. Kohulan Rajan', role: 'Lead Developer', image: require('@/assets/kohulan-rajan.jpg'), link: 'https://www.linkedin.com/in/kohulanrajan/', linkText: 'LinkedIn Profile' },
        { name: 'Prof. Achim Zielesny', role: 'Supervisor', image: require('@/assets/achim-zielesny.jpg'), link: 'https://www.w-hs.de/service/informationen-zur-person/person/zielesny/', linkText: 'University Profile' },
        { name: 'Prof. Christoph Steinbeck', role: 'Supervisor', image: require('@/assets/christoph-steinbeck.jpg'), link: 'https://www.linkedin.com/in/steinbeck/', linkText: 'LinkedIn Profile' }
      ],
      citations: [
        { title: 'For STOUT V1:', text: 'Rajan, K., Zielesny, A. & Steinbeck, C. STOUT: SMILES to IUPAC names using neural machine translation. J Cheminform 13, 34 (2021).', link: 'https://doi.org/10.1186/s13321-021-00512-4', linkText: 'https://doi.org/10.1186/s13321-021-00512-4' },
        { title: 'For STOUT V2:', text: 'Rajan, K., Zielesny, A. & Steinbeck, C. STOUT V2.0: SMILES to IUPAC name conversion using transformer models. J Cheminform 16, 146 (2024)', link: 'https://doi.org/10.1186/s13321-024-00941-x', linkText: 'https://doi.org/10.1186/s13321-024-00941-x' }
      ],
      authors: [
        { name: 'Prof. Dr. Christoph Steinbeck', email: 'christoph.steinbeck@uni-jena.de' },
        { name: 'Prof. Dr. Achim Zielesny', email: 'achim.zielesny@w-hs.de' },
        { name: 'Dr. Kohulan Rajan', email: 'kohulan.rajan@uni-jena.de' }
      ]
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bahnschrift:wght@300;400;700&display=swap');

.about {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Bahnschrift', sans-serif;
  color: #0a2472;
  background-color: #f0f7ff;
  padding: 40px;
  box-sizing: border-box;
}

.main-content {
  width: 100%;
  max-width: 1200px;
  background-color: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.1);
}

.title {
  font-size: 3rem;
  color: #0a2472;
  text-align: center;
  margin-bottom: 40px;
  text-shadow: 2px 2px 4px rgba(10, 36, 114, 0.1);
  animation: fadeInDown 1s ease-out;
}

.content-wrapper {
  display: grid;
  gap: 40px;
}

.section {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.1);
  transition: all 0.3s ease;
  animation: fadeIn 1s ease-out;
}

.section:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(10, 36, 114, 0.15);
}

h2 {
  font-size: 2rem;
  color: #1e40af;
  margin-bottom: 20px;
}

.link {
  color: #2563eb;
  text-decoration: none;
  transition: all 0.3s ease;
}

.link:hover {
  color: #1e40af;
  text-decoration: underline;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.team-member {
  background-color: #f0f7ff;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(10, 36, 114, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeInUp 0.5s ease-out;
}

.team-member:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(10, 36, 114, 0.2);
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 15px;
  border: 4px solid #0a2472;
  transition: all 0.3s ease;
}

.team-member:hover .avatar {
  transform: scale(1.05);
  border-color: #1e40af;
}

.team-member h3 {
  color: #0a2472;
  margin-bottom: 5px;
}

.role {
  color: #2563eb;
  font-weight: bold;
  margin-bottom: 10px;
}

.team-member .link {
  display: inline-block;
  padding: 8px 15px;
  background-color: #0a2472;
  color: white;
  border-radius: 20px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.team-member .link:hover {
  background-color: #1e40af;
  transform: translateY(-2px);
}

.citation-box {
  background-color: #dbeafe;
  padding: 20px;
  border-radius: 12px;
  font-style: italic;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  animation: fadeInLeft 0.5s ease-out;
}

.citation-box:hover {
  background-color: #bfdbfe;
  transform: scale(1.02);
}

.citation-box p {
  margin-bottom: 10px;
}

.citation-box p:first-child {
  font-weight: bold;
  color: #1e40af;
}

.contact-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

.map-container {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 75%;
  /* Aspect ratio 4:3 */
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(10, 36, 114, 0.1);
  transition: all 0.3s ease;
}

.map-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.map-container:hover {
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.2);
  transform: translateY(-5px);
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.address,
.authors {
  background-color: #f0f7ff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(10, 36, 114, 0.05);
  transition: all 0.3s ease;
}

.address:hover,
.authors:hover {
  box-shadow: 0 4px 8px rgba(10, 36, 114, 0.1);
  transform: translateY(-3px);
}

h3 {
  color: #1e40af;
  font-size: 1.5rem;
  margin-bottom: 15px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

li:hover {
  transform: translateX(5px);
}

.tpu-logo {
  display: block;
  margin: 20px auto;
  transition: all 0.3s ease;
  animation: pulse 2s infinite;
}

.tpu-logo:hover {
  transform: scale(1.05);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.05);
  }

  100% {
    transform: scale(1);
  }
}

@media (max-width: 1024px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }

  .contact-info {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .about {
    padding: 20px;
  }

  .main-content {
    padding: 20px;
  }

  .title {
    font-size: 2.5rem;
  }

  h2 {
    font-size: 1.8rem;
  }

  .section {
    padding: 20px;
  }

  .team-grid {
    grid-template-columns: 1fr;
  }

  .map-container {
    padding-bottom: 56.25%;
    /* Aspect ratio 16:9 for smaller screens */
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 2rem;
  }

  h2 {
    font-size: 1.5rem;
  }

  .team-member {
    padding: 15px;
  }

  .avatar {
    width: 120px;
    height: 120px;
  }

  .citation-box {
    padding: 15px;
  }

  .address,
  .authors {
    padding: 15px;
  }

  h3 {
    font-size: 1.3rem;
  }
}

.data-availability {
  margin-top: 40px;
}

.data-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 20px;
}

.data-item {
  background-color: #f0f7ff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(10, 36, 114, 0.05);
  transition: all 0.3s ease;
}

.data-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.1);
}

.data-item h3 {
  color: #1e40af;
  font-size: 1.3rem;
  margin-bottom: 15px;
  border-bottom: 2px solid #bfdbfe;
  padding-bottom: 8px;
}

.data-item ul {
  list-style-type: none;
  padding: 0;
}

.data-item li {
  margin-bottom: 15px;
  line-height: 1.5;
}

.data-item strong {
  color: #1e40af;
  display: block;
  margin-bottom: 4px;
}

@media (max-width: 768px) {
  .data-links {
    grid-template-columns: 1fr;
  }

  .data-item {
    padding: 15px;
  }
}
</style>