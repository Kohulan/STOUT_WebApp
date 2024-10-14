<template>
  <nav class="nav-container">
    <div class="nav-content">
      <div class="nav-left">
        <button @click="toggleMenu" class="hamburger-menu">
          <span></span>
          <span></span>
          <span></span>
        </button>
        <router-link to="/" class="logo-link">
          <img src="@/assets/STOUT.svg" alt="STOUT Logo" class="logo" />
        </router-link>
      </div>
      <div :class="['nav-links', { 'nav-active': isMenuOpen }]">
        <router-link v-for="page in pages" :key="page" :to="getRouteForPage(page)"
          :class="{ active: $route.name === page }" @click="closeMenu">
          {{ page }}
        </router-link>
      </div>
      <a href="https://github.com/Kohulan/STOUT_WebApp" target="_blank" rel="noopener noreferrer" class="github-link">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" class="github-icon" aria-hidden="true">
          <path fill-rule="evenodd"
            d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
        </svg>
        <span class="github-text">GitHub</span>
      </a>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavigationBar',
  data() {
    return {
      pages: [
        'Home',
        'SMILES to IUPAC',
        'Structure to IUPAC',
        'IUPAC to SMILES',
        'DECIMER It!',
        'Health Check',
        'About'
      ],
      isMenuOpen: false
    }
  },
  methods: {
    getRouteForPage(page) {
      const routeMap = {
        'Home': '/',
        'SMILES to IUPAC': '/smiles-to-iupac',
        'Structure to IUPAC': '/structure-to-iupac',
        'IUPAC to SMILES': '/iupac-to-smiles',
        'DECIMER It!': '/decimer-it',
        'Health Check': '/health-check',
        'About': '/about'
      }
      return routeMap[page] || '/'
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    closeMenu() {
      this.isMenuOpen = false;
    }
  }
}
</script>

<style scoped>
body,
html {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Bahnschrift', sans-serif;
}

.nav-container {
  background-color: #005f73;
  position: fixed;
  font-family: 'Bahnschrift', sans-serif;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  margin: 0;
  padding: 1px;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
}

.nav-left {
  display: flex;
  align-items: center;
}

.logo-link {
  display: flex;
  align-items: center;
}

.logo {
  max-height: 40px;
  width: auto;
}

.nav-links {
  display: flex;
  align-items: center;
  height: 100%;
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 0 15px;
  font-size: 0.9rem;
  transition: background-color 0.3s, color 0.3s;
  height: 100%;
  display: flex;
  align-items: center;
}

.nav-links a:hover,
.nav-links a.active {
  background-color: #0a9396;
}

.github-link {
  display: flex;
  align-items: center;
  background-color: #94d2bd;
  color: #001219;
  text-decoration: none;
  padding: 8px 15px;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: bold;
  transition: background-color 0.3s;
}

.github-link:hover {
  background-color: #e9d8a6;
}

.github-icon {
  width: 20px;
  height: 20px;
  margin-right: 8px;
  fill: #001219;
}

.github-link:hover .github-icon {
  fill: #001219;
}

.hamburger-menu {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 30px;
  height: 25px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-right: 15px;
}

.hamburger-menu span {
  width: 30px;
  height: 3px;
  background: white;
  border-radius: 10px;
  transition: all 0.3s linear;
  position: relative;
  transform-origin: 1px;
}

@media (max-width: 1024px) {
  .nav-content {
    justify-content: space-between;
    padding: 0 15px;
  }

  .hamburger-menu {
    display: flex;
  }

  .nav-links {
    position: absolute;
    top: 60px;
    left: 0;
    flex-direction: column;
    background-color: #005f73;
    /* Ensure this matches the nav background */
    width: 100%;
    align-items: flex-start;
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    /* Add shadow for depth */
  }

  .nav-links.nav-active {
    transform: translateX(0);
  }

  .nav-links a {
    width: 100%;
    padding: 15px;
    border-bottom: 1px solid #0a9396;
    color: white;
    /* Ensure text color contrasts with background */
    background-color: #005f73;
    /* Match nav background */
  }

  .nav-links a:hover,
  .nav-links a.active {
    background-color: #0a9396;
    /* Slightly lighter for hover/active state */
  }

  .github-link {
    margin-left: auto;
  }

  .github-text {
    display: none;
  }
}

/* Additional styles to ensure menu visibility */
.nav-container {
  background-color: #005f73;
}

.nav-links {
  background-color: #005f73;
}

.nav-links a {
  color: white;
  background-color: #005f73;
}

.nav-links a:hover,
.nav-links a.active {
  background-color: #0a9396;
}
</style>