# travellingskates.com — sitio

Sitio estático de Travelling Skates S.A., desplegado en Vercel (proyecto `travellingskates`, dominio travellingskates.com).

- `data/raw.json` — contenido del sitio original (textos, galerías, enlaces).
- `build.py` — genera todas las páginas en `out/` respetando el diseño original.
- `historia.py` — página **Historia** (historia, procesos de ruedas y planchas, productos, videos, reconocimientos y prensa).
- `assets/historia/` — imágenes optimizadas del material de este repo (renders, planos, producción, prensa).
- `base.css`, `site.js` — estilos y comportamiento (galerías, lightbox, videos).
- `fetch-images.mjs` — en el build descarga las imágenes del catálogo original a `out/assets/img/`.

Build local: `python3 build.py out && cp -r assets/historia out/assets/`
