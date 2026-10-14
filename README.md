<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)"
    srcset="assets/banner-light.svg">
  <img src="assets/banner-light.svg" width="100%"
    alt="Pixel art banner: kevelmun, build ship lead, mountains, code terminal">
</picture>

<h1>Kevin Elihan Muñoz Calva</h1>

<p><b>Software engineer who builds products end to end:<br>
mobile app, backend, infrastructure and AI tools.</b></p>

<p>Co-founder and tech lead of <a href="https://sotita.com">Sotita</a> ·
Master's in Project Management at UPV · From Ecuador</p>

<p><b>Open to opportunities</b> in software engineering and project
management.</p>

<a href="https://www.linkedin.com/in/kevelmun"><img
  src="https://img.shields.io/badge/LinkedIn-kevelmun-0A66C2?style=for-the-badge"
  alt="LinkedIn: kevelmun"></a>
<a href="mailto:3lihan.m.c@gmail.com"><img
  src="https://img.shields.io/badge/Email-3lihan.m.c%40gmail.com-4C5BD4?style=for-the-badge"
  alt="Email: 3lihan.m.c@gmail.com"></a>
<a href="https://kevelmun.dev"><img
  src="https://img.shields.io/badge/Web-kevelmun.dev-1B2540?style=for-the-badge"
  alt="Website: kevelmun.dev"></a>

<sub><a href="README.es.md">Leer en español</a></sub>

</div>

## <img src="assets/icons/now.svg" width="24" alt=""> Now

- **Sotita** is in beta with testers.
  <!-- TODO: métrica (número de beta testers, descargas o usuarios activos) -->
- **CV Adapter** is getting ready to be open source.
- **Master's in Project Management**: learning to plan and lead the kind of
  projects I already build.

## <img src="assets/icons/projects.svg" width="24" alt=""> Featured projects

<table>
<tr>
<td width="50%" valign="top">
  <picture>
    <source media="(prefers-color-scheme: dark)"
      srcset="assets/projects/sotita-dark.svg">
    <source media="(prefers-color-scheme: light)"
      srcset="assets/projects/sotita-light.svg">
    <img src="assets/projects/sotita-light.svg" width="100%"
      alt="Pixel art: a phone with a finance dashboard, coins and a cloud">
  </picture>
  <h3><a href="https://sotita.com">Sotita</a></h3>
  <sub>Personal finance app · co-founder and tech lead · in beta ·
  private code</sub>
  <p><b>Problem:</b> recording an expense should not depend on having a
  connection.</p>
  <p><b>Solution:</b> an offline-first Flutter app. The finance core runs on
  a local SQLite database and syncs with a self-hosted Supabase backend
  through PowerSync. A Cloudflare Worker runs scheduled jobs (recurring
  transactions, credit card installments, budget alerts) and sends push
  notifications. Dev, staging and production run on Docker with Dokploy;
  secrets live in Infisical.</p>
  <p><code>Flutter</code> <code>Dart</code> <code>Riverpod</code>
  <code>Drift</code> <code>Supabase</code> <code>PostgreSQL</code>
  <code>PowerSync</code> <code>Cloudflare Workers</code>
  <code>TypeScript</code> <code>Astro</code> <code>Docker</code>
  <code>Dokploy</code> <code>Infisical</code></p>
</td>
<td width="50%" valign="top">
  <picture>
    <source media="(prefers-color-scheme: dark)"
      srcset="assets/projects/cv-adapter-dark.svg">
    <source media="(prefers-color-scheme: light)"
      srcset="assets/projects/cv-adapter-light.svg">
    <img src="assets/projects/cv-adapter-light.svg" width="100%"
      alt="Pixel art: a CV page with highlighted keywords and a check badge">
  </picture>
  <h3>CV Adapter</h3>
  <!-- TODO: enlace al repo público de CV Adapter -->
  <sub>AI tool that tailors my CV to each job · personal tool · runs
  locally · code coming soon</sub>
  <p><b>Problem:</b> tailoring a CV to every job post takes time, and AI
  tools tend to invent experience.</p>
  <p><b>Solution:</b> all my experience lives in one structured file. For
  each job post, Claude picks what is relevant and rewrites it in the
  post's words. A validator checks every line against real achievements,
  numbers and skills; if a check fails, the model gets the errors and
  repairs the CV. The app renders a one-column DOCX and PDF, then re-reads
  the PDF like an ATS and reports keyword coverage.</p>
  <p><code>Python</code> <code>FastAPI</code> <code>vanilla JavaScript</code>
  <code>Claude API (forced tool use)</code> <code>JSON Schema</code>
  <code>python-docx</code> <code>ReportLab</code> <code>Docker</code></p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
  <picture>
    <source media="(prefers-color-scheme: dark)"
      srcset="assets/projects/spring-validator-dark.svg">
    <source media="(prefers-color-scheme: light)"
      srcset="assets/projects/spring-validator-light.svg">
    <img src="assets/projects/spring-validator-light.svg" width="100%"
      alt="Pixel art: a code editor with lint markers next to a green leaf">
  </picture>
  <h3><a href="https://github.com/kevelmun/spring-boot-validator">Spring
  Boot Syntax Validator</a></h3>
  <sub>Side project · public code</sub>
  <p><b>Problem:</b> moving from Laravel or Express to Spring Boot means
  learning many conventions at once, with nobody checking your code.</p>
  <p><b>Solution:</b> 15 exercises with three layers of feedback:
  structural checks on the real syntax tree (JavaParser), real compilation
  with an embedded <code>javac</code>, and a linter for common Spring
  mistakes.</p>
  <p><code>Java 21</code> <code>Spring Boot</code> <code>JavaParser</code>
  <code>React</code> <code>Vite</code> <code>Tailwind CSS</code>
  <code>CodeMirror</code> <code>Docker</code></p>
</td>
<td width="50%" valign="top">
  <picture>
    <source media="(prefers-color-scheme: dark)"
      srcset="assets/projects/stereothermal-dark.svg">
    <source media="(prefers-color-scheme: light)"
      srcset="assets/projects/stereothermal-light.svg">
    <img src="assets/projects/stereothermal-light.svg" width="100%"
      alt="Pixel art: two stereo cameras and a thermal camera, a heat map">
  </picture>
  <h3><a href="https://github.com/kevelmun/StereoThermal">StereoThermal</a></h3>
  <sub>Research project · computer vision</sub>
  <p><b>Problem:</b> combining color and thermal images needs frames taken
  at the same moment and aligned with each other.</p>
  <p><b>Solution:</b> synchronized capture from two stereo cameras and one
  thermal camera, plus image registration with LightGlue.</p>
  <p><code>Python</code> <code>OpenCV</code> <code>LightGlue</code>
  <code>Jupyter</code></p>
</td>
</tr>
</table>

## <img src="assets/icons/stack.svg" width="24" alt=""> Tech stack

<picture>
  <source media="(prefers-color-scheme: dark)"
    srcset="https://skillicons.dev/icons?i=flutter%2Cdart%2Csupabase%2Cpostgres%2Cts%2Cpython%2Cfastapi%2Cphp%2Claravel%2Cdocker%2Ccloudflare%2Creact&theme=dark">
  <source media="(prefers-color-scheme: light)"
    srcset="https://skillicons.dev/icons?i=flutter%2Cdart%2Csupabase%2Cpostgres%2Cts%2Cpython%2Cfastapi%2Cphp%2Claravel%2Cdocker%2Ccloudflare%2Creact&theme=light">
  <img src="https://skillicons.dev/icons?i=flutter,dart,supabase,postgres,ts,python,fastapi,php,laravel,docker,cloudflare,react&theme=light"
    alt="Core stack icons; the full list is written below">
</picture>

<table>
<tr>
  <td><b>Mobile</b></td>
  <td><code>Flutter</code> <code>Dart</code> <code>Riverpod</code>
  <code>Drift</code> · also <code>Ionic</code></td>
</tr>
<tr>
  <td><b>Backend and data</b></td>
  <td><code>TypeScript</code> <code>Python</code> <code>FastAPI</code>
  <code>PHP</code> <code>Laravel</code> <code>Java</code>
  <code>Spring Boot</code> <code>PostgreSQL</code> <code>Supabase</code>
  <code>PowerSync</code> <code>SQLite</code></td>
</tr>
<tr>
  <td><b>Frontend</b></td>
  <td><code>React</code> <code>Astro</code> <code>Tailwind CSS</code>
  <code>vanilla JavaScript</code> · also <code>Angular</code></td>
</tr>
<tr>
  <td><b>Infrastructure</b></td>
  <td><code>Docker</code> <code>Dokploy</code>
  <code>Cloudflare Workers</code> <code>Infisical</code> <code>Caddy</code>
  <code>Nginx</code></td>
</tr>
<tr>
  <td><b>AI and computer vision</b></td>
  <td><code>Claude API</code> <code>Ollama</code> <code>Azure Speech</code>
  <code>OpenCV</code> <code>Open3D</code> <code>LightGlue</code></td>
</tr>
<tr>
  <td><b>Games</b></td>
  <td><code>Godot</code> <code>Unity</code></td>
</tr>
</table>

## <img src="assets/icons/beyond.svg" width="24" alt=""> Beyond code

- **How I work:** at Sotita, every feature starts as a numbered spec with its
  decisions written down, then ships as a small vertical slice.
- **Problems I have not solved yet are the fun part.** Example: the Spring
  Boot validator compiles code that uses Lombok without Lombok's annotation
  processor. It generates the missing methods in the syntax tree instead.
- **More research:** turning 3D point clouds into image datasets for fruit
  ripeness ([Fruit-Ripeness](https://github.com/kevelmun/Fruit-Ripeness)) and
  a voice assistant with Azure Speech and Ollama
  ([VoiceChat-AzureOllamaAgent](https://github.com/kevelmun/VoiceChat-AzureOllamaAgent)).
- **Games:** [Scape from the Dark](https://kevelmun.itch.io/scape-from-the-dark),
  a university team game made in Godot.

## <img src="assets/icons/contact.svg" width="24" alt=""> Contact

The fastest way to reach me is email:
[3lihan.m.c@gmail.com](mailto:3lihan.m.c@gmail.com). You can also find me on
[LinkedIn](https://www.linkedin.com/in/kevelmun) and at
[kevelmun.dev](https://kevelmun.dev).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <source media="(prefers-color-scheme: light)"
    srcset="assets/footer-light.svg">
  <img src="assets/footer-light.svg" width="100%" alt="">
</picture>
