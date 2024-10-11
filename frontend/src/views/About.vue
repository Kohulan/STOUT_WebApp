<template>
  <div class="about">
    <h1 class="title">About STOUT</h1>
    <div class="content-wrapper">
      <section class="section developers">
        <h2>Our Team</h2>
        <div class="team-grid">
          <div class="team-member">
            <img src="@/assets/kohulan-rajan.jpg" alt="Dr. Kohulan Rajan" class="avatar" />
            <h3>Dr. Kohulan Rajan</h3>
            <p class="role">Lead Developer</p>
            <a href="https://www.linkedin.com/in/kohulanrajan/" target="_blank" rel="noopener noreferrer"
              class="link">LinkedIn Profile</a>
          </div>
          <div class="team-member">
            <img src="@/assets/achim-zielesny.jpg" alt="Prof. Achim Zielesny" class="avatar" />
            <h3>Prof. Achim Zielesny</h3>
            <p class="role">Supervisor</p>
            <a href="https://www.w-hs.de/service/informationen-zur-person/person/zielesny/" target="_blank"
              rel="noopener noreferrer" class="link">University Profile</a>
          </div>
          <div class="team-member">
            <img src="@/assets/christoph-steinbeck.jpg" alt="Prof. Christoph Steinbeck" class="avatar" />
            <h3>Prof. Christoph Steinbeck</h3>
            <p class="role">Supervisor</p>
            <a href="https://www.linkedin.com/in/steinbeck/" target="_blank" rel="noopener noreferrer"
              class="link">LinkedIn Profile</a>
          </div>
        </div>
        <h2 />
        <p>
          🔬 STOUT was developed by
          <a href="https://www.linkedin.com/in/kohulanrajan/" target="_blank" rel="noopener noreferrer" class="link">Dr.
            Kohulan Rajan</a>
          under the supervision of
          <a href="https://www.w-hs.de/service/informationen-zur-person/person/zielesny/" target="_blank"
            rel="noopener noreferrer" class="link">Prof. Achim Zielesny</a>
          and
          <a href="https://www.linkedin.com/in/steinbeck/" target="_blank" rel="noopener noreferrer" class="link">Prof.
            Christoph Steinbeck</a>.
        </p>
      </section>

      <section class="section citation">
        <h2>How to cite us?</h2>
        <div class="citation-box">
          <p>For STOUT V1:</p>
          <p>
            Rajan, K., Zielesny, A. & Steinbeck, C. STOUT: SMILES to IUPAC names
            using neural machine translation. J Cheminform 13, 34 (2021).
            <a href="https://doi.org/10.1186/s13321-021-00512-4" target="_blank" rel="noopener noreferrer"
              class="link">https://doi.org/10.1186/s13321-021-00512-4</a>
          </p>
        </div>
        <div class="citation-box">
          <p>For STOUT V2:</p>
          <p>
            Rajan K, Zielesny A, Steinbeck C. STOUT V2.0: SMILES to IUPAC name
            conversion using transformer models. ChemRxiv. 2024;
            <a href="https://doi.org/10.26434/chemrxiv-2024-089vs" target="_blank" rel="noopener noreferrer"
              class="link">doi:10.26434/chemrxiv-2024-089vs</a>
          </p>
        </div>
      </section>

      <section class="section contact">
        <h2>Contact Us</h2>
        <div class="contact-info">
          <div class="map">
            <iframe
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2503.2949726059553!2d11.581905350629135!3d50.93352470346138!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47a6a898c3634fbb%3A0xdf22378d9f537b71!2sLessingstra%C3%9Fe%208%2C%2007743%20Jena%2C%20Germany!5e0!3m2!1sen!2s!4v1681045800175!5m2!1sen!2s"
              width="100%" height="300" style="border: 0" allowfullscreen="" loading="lazy" title="Location map" />
          </div>
          <div class="contact-details">
            <div class="address">
              <h3>Address</h3>
              <p>
                Institute for Inorganic and Analytical Chemistry, Friedrich
                Schiller University, Lessingstraße 8, Jena 07743, Germany
              </p>
            </div>
            <div class="authors">
              <h3>Authors</h3>
              <ul>
                <li>
                  Prof. Dr. Christoph Steinbeck:
                  <a href="mailto:christoph.steinbeck@uni-jena.de" class="link">christoph.steinbeck@uni-jena.de</a>
                </li>
                <li>
                  Prof. Dr. Achim Zielesny:
                  <a href="mailto:achim.zielesny@w-hs.de" class="link">achim.zielesny@w-hs.de</a>
                </li>
                <li>
                  Dr. Kohulan Rajan:
                  <a href="mailto:kohulan.rajan@uni-jena.de" class="link">kohulan.rajan@uni-jena.de</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section class="section acknowledgement">
        <h2>Acknowledgement</h2>
        <p>
          Research supported with Cloud TPUs from Google's TPU Research Cloud
          (TRC)
        </p>
        <img src="@/assets/tpu-research-cloud-logo.png" alt="TPU Research Cloud Logo" width="250" class="tpu-logo" />
        <p>
          We greatly acknowledge OpenEye for granting us an academic license to
          their Lexichem software, without which this work would not have been
          possible.
        </p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutPage',
}
</script>

<style scoped>
.about {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Bahnschrift', sans-serif;
  color: #0a2472;
  background-color: #f0f7ff;
  min-height: 100vh;
}

.title {
  font-size: 3rem;
  font-weight: bold;
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

.citation-box {
  background-color: #dbeafe;
  padding: 20px;
  border-radius: 12px;
  font-style: italic;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  /* Add space between citation boxes */
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

.map {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(10, 36, 114, 0.1);
  transition: all 0.3s ease;
}

.map:hover {
  box-shadow: 0 8px 16px rgba(10, 36, 114, 0.2);
}

.contact-details {
  display: grid;
  gap: 20px;
}

h3 {
  color: #2563eb;
  margin-bottom: 10px;
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

@media (min-width: 768px) {
  .content-wrapper {
    grid-template-columns: repeat(2, 1fr);
  }

  .developers,
  .acknowledgement {
    grid-column: span 2;
  }

  .contact-info {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 767px) {
  .about {
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

.team-member p {
  margin-bottom: 15px;
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

@media (max-width: 767px) {
  .team-grid {
    grid-template-columns: 1fr;
  }
}
</style>
