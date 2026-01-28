<script>
  import Router from 'svelte-spa-router'
  import Home from './pages/Home.svelte'
  import Movilidad from './pages/Movilidad.svelte'
  import Calistenia from './pages/Calistenia.svelte'
  import Peliculas from './pages/Peliculas.svelte'

  const routes = {
    '/': Home,
    '/movilidad': Movilidad,
    '/calistenia': Calistenia,
    '/peliculas': Peliculas
  }
</script>

<header class="topbar">
  <a class="brand" href="/">Clawdbot Portal</a>
  <nav>
    <a href="/movilidad">Movilidad</a>
    <a href="/calistenia">Calistenia</a>
    <a href="/peliculas">Películas</a>
  </nav>
</header>

<main>
  <Router {routes} />
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "Noto Sans", sans-serif;
    background: #0b1020;
    color: #e5e7eb;
  }
  a { color: inherit; }
  .topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: #0f172a;
    border-bottom: 1px solid #1f2937;
  }
  .brand {
    font-weight: 700;
    text-decoration: none;
    color: #e5e7eb;
  }
  nav a {
    margin-left: 1rem;
    text-decoration: none;
    color: #cbd5f5;
  }
  nav a:hover { color: #fff; }
  main { min-height: calc(100vh - 64px); }
</style>
