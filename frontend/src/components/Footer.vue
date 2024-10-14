<template>
  <footer class="footer">
    <div class="footer-content">
      <p class="disclaimer">
         ⚠️ Disclaimer: STOUT is an AI language model and may produce errors. For accuracy, we recommend using a deterministic name generator like LexiChem.
      </p>
      <p class="copyright">
        &copy; 2024 <strong>stout.decimer.ai</strong> is created and maintained by the 
        <a href="https://cheminf.uni-jena.de" target="_blank">Steinbeck Group</a>
      </p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterInformation'
}
</script>

<style scoped>
.footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background: linear-gradient(135deg, #006D77, #008891);
  color: #ffffff;
  text-align: center;
  padding: 8px 0;
  font-family: 'Bahnschrift', sans-serif;
  font-size: 0.9rem;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
  z-index: 999;
}

.footer-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}

.disclaimer {
  font-weight: 500;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon {
  margin-right: 8px;
  font-size: 1.2rem;
}

.copyright {
  font-size: 0.8rem;
  opacity: 0.9;
}

.footer a {
  color: #3AAFBF;
  text-decoration: none;
  transition: color 0.2s ease, text-shadow 0.2s ease;
}

.footer a:hover {
  color: #F0F4F8;
  text-decoration: none;
  text-shadow: 0 0 8px rgba(240, 244, 248, 0.5);
}

@media (max-width: 600px) {
  .footer {
    font-size: 0.8rem;
  }
  
  .icon {
    font-size: 1rem;
  }
  
  .copyright {
    font-size: 0.7rem;
  }
}
</style>