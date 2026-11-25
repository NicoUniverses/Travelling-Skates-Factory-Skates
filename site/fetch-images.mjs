// Build step: download the site images once into assets/img so the site is served entirely from Vercel.
import { readFile, writeFile, mkdir, access } from 'node:fs/promises';
const list = JSON.parse(await readFile('images.json'));
await mkdir('assets/img/', { recursive: true });
let ok = 0, fail = 0;
const queue = [...list];
async function worker() {
  while (queue.length) {
    const [name, url] = queue.shift();
    const dest = 'assets/img/' + name;
    try { await access(dest); ok++; continue; } catch {}
    for (let t = 0; t < 3; t++) {
      try {
        const r = await fetch(url, { headers: { accept: 'image/jpeg,image/png,*/*;q=0.5' } });
        if (!r.ok) throw new Error('HTTP ' + r.status);
        await writeFile(dest, Buffer.from(await r.arrayBuffer()));
        ok++; break;
      } catch (e) { if (t === 2) { fail++; console.error('FAILED', name, e.message); } }
    }
  }
}
await Promise.all(Array.from({ length: 8 }, worker));
console.log(`images: ${ok} ok, ${fail} failed`);
if (fail) process.exit(1);
// remove build-only files from the published output
const { unlink } = await import('node:fs/promises');
try { await unlink('images.json'); } catch {}
