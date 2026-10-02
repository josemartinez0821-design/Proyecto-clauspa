// Copia Alpine.js, Swiper y las letras de node_modules a static/, para que el servidor no necesite Node.
// Se corre con: npm run librerias
import { copyFileSync, mkdirSync } from "node:fs";

const letras = [
  "jost/files/jost-latin-400-normal.woff2",
  "jost/files/jost-latin-500-normal.woff2",
  "cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2",
  "cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2",
  "great-vibes/files/great-vibes-latin-400-normal.woff2",
];

const archivos = [
  ["node_modules/alpinejs/dist/cdn.min.js", "static/vendor/alpine.min.js"],
  ["node_modules/swiper/swiper-bundle.min.js", "static/vendor/swiper-bundle.min.js"],
  ["node_modules/swiper/swiper-bundle.min.css", "static/vendor/swiper-bundle.min.css"],
  ...letras.map((ruta) => [`node_modules/@fontsource/${ruta}`, `static/fonts/${ruta.split("/").pop()}`]),
];

mkdirSync("static/vendor", { recursive: true });
mkdirSync("static/fonts", { recursive: true });
for (const [origen, destino] of archivos) {
  copyFileSync(origen, destino);
  console.log(`${origen} → ${destino}`);
}
