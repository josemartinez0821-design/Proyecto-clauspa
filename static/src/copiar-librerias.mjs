// Copia Alpine.js y Swiper de node_modules a static/vendor, para que el servidor no necesite Node.
// Se corre con: npm run librerias
import { copyFileSync, mkdirSync } from "node:fs";

const archivos = [
  ["node_modules/alpinejs/dist/cdn.min.js", "static/vendor/alpine.min.js"],
  ["node_modules/swiper/swiper-bundle.min.js", "static/vendor/swiper-bundle.min.js"],
  ["node_modules/swiper/swiper-bundle.min.css", "static/vendor/swiper-bundle.min.css"],
];

mkdirSync("static/vendor", { recursive: true });
for (const [origen, destino] of archivos) {
  copyFileSync(origen, destino);
  console.log(`${origen} → ${destino}`);
}
