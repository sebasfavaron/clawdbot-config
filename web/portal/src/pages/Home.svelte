<script>
  const links = [
    { href: '/movilidad', label: 'Movilidad' },
    { href: '/calistenia', label: 'Calistenia' },
    { href: '/peliculas', label: 'Películas' }
  ];
</script>

<section class="page">
  <h1>Portal de Entrenamiento</h1>
  <p>Bienvenido. Elegí una sección:</p>
  <div class="grid">
    {#each links as link}
      <a class="card" href={link.href}>{link.label}</a>
    {/each}
  </div>
</section>

<style>
  .page { padding: 2rem; }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-top: 1.5rem;
  }
  .card {
    display: block;
    padding: 1.25rem;
    border-radius: 12px;
    background: #111827;
    color: #fff;
    text-decoration: none;
    border: 1px solid #1f2937;
    transition: transform .1s ease, box-shadow .1s ease;
  }
  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,.2);
  }
</style>
