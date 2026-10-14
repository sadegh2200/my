// Offline-friendly browser setup: all binary bytes come from the pinned npm
// package, not an unapproved Chrome download host. Outputs are ignored cache.
import { createReadStream, createWriteStream } from 'node:fs';
import { access, chmod, mkdir, writeFile } from 'node:fs/promises';
import { createBrotliDecompress } from 'node:zlib';
import { pipeline } from 'node:stream/promises';
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const bin = path.resolve(path.dirname(require.resolve('@sparticuz/chromium')), '../bin');
const cache = path.join(root, '.cache/browser');
await mkdir(path.join(cache, 'fonts'), { recursive: true });
const exists = async p => { try { await access(p); return true; } catch { return false; } };

async function unpack(archive, to, marker) {
  if (await exists(marker)) return;
  const proc = spawn('tar', ['xf', '-', '-C', to], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((resolve, reject) => {
    proc.on('error', reject);
    proc.on('close', code => code === 0 ? resolve() : reject(new Error(`tar exit ${code}`)));
  });
  await pipeline(createReadStream(path.join(bin, archive)), createBrotliDecompress(), proc.stdin);
  await done;
}
const executable = path.join(cache, 'chromium');
if (!(await exists(executable))) {
  await pipeline(createReadStream(path.join(bin, 'chromium.br')), createBrotliDecompress(), createWriteStream(executable));
}
await chmod(executable, 0o755);
await unpack('al2023.tar.br', cache, path.join(cache, 'lib/libnss3.so'));
await unpack('swiftshader.tar.br', cache, path.join(cache, 'libEGL.so'));
await unpack('fonts.tar.br', path.join(cache, 'fonts'), path.join(cache, 'fonts/fonts.conf'));
await writeFile(path.join(root, '.cache/browser-path.txt'), executable + '\n');
console.log(`Browser ready: ${executable}`);
