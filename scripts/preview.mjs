// Read-only final-deliverable preview. No directory listing or repo file access.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'deliver/ashab-51');
const routes = new Map([
  ['/', [path.join(root, 'preview/index.html'), 'text/html; charset=utf-8']],
  ['/media/reel.mp4', [path.join(output, 'maalsadiqeen-51.mp4'), 'video/mp4']],
  ['/media/cover.jpg', [path.join(output, 'maalsadiqeen-51-cover.jpg'), 'image/jpeg']],
  ['/media/caption.txt', [path.join(output, 'caption-ar.txt'), 'text/plain; charset=utf-8']],
  ['/media/comment.txt', [path.join(output, 'pinned-comment-ar.txt'), 'text/plain; charset=utf-8']],
  ['/media/beat-sheet.md', [path.join(output, 'beat-sheet-fa.md'), 'text/markdown; charset=utf-8']],
  ['/media/qa.md', [path.join(output, 'qa-report.md'), 'text/markdown; charset=utf-8']],
  ['/assets/logo.png', [path.join(root, 'maalsadiqeen-reel/assets/brand/logo.png'), 'image/png']],
  ['/assets/naskh.ttf', [path.join(root, 'maalsadiqeen-reel/assets/fonts/NotoNaskhArabic-Regular.ttf'), 'font/ttf']],
  ['/assets/kufi.ttf', [path.join(root, 'maalsadiqeen-reel/assets/fonts/NotoKufiArabic-Bold.ttf'), 'font/ttf']],
]);

const server = http.createServer((req, res) => {
  if (!['GET', 'HEAD'].includes(req.method)) {
    res.writeHead(405, { Allow: 'GET, HEAD' }).end(); return;
  }
  const url = new URL(req.url, 'http://preview.invalid');
  const route = routes.get(url.pathname);
  if (!route) { res.writeHead(404).end('Not found'); return; }
  const [file, type] = route;
  let stat;
  try { stat = fs.statSync(file); } catch { res.writeHead(404).end('Deliverable not built yet'); return; }
  const headers = { 'Content-Type': type, 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-cache', 'X-Content-Type-Options': 'nosniff' };
  if (url.searchParams.has('download')) {
    headers['Content-Disposition'] = `attachment; filename="${path.basename(file)}"`;
  }
  let start = 0, end = stat.size - 1, status = 200;
  if (req.headers.range) {
    const match = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
    if (!match || (!match[1] && !match[2])) {
      res.writeHead(416, { 'Content-Range': `bytes */${stat.size}` }).end(); return;
    }
    if (!match[1]) start = Math.max(0, stat.size - Number(match[2]));
    else {
      start = Number(match[1]);
      if (match[2]) end = Math.min(Number(match[2]), stat.size - 1);
    }
    if (start > end || start >= stat.size || !Number.isSafeInteger(start) || !Number.isSafeInteger(end)) {
      res.writeHead(416, { 'Content-Range': `bytes */${stat.size}` }).end(); return;
    }
    status = 206;
    headers['Content-Range'] = `bytes ${start}-${end}/${stat.size}`;
  }
  headers['Content-Length'] = Math.max(0, end - start + 1);
  res.writeHead(status, headers);
  if (req.method === 'HEAD' || !stat.size) { res.end(); return; }
  const stream = fs.createReadStream(file, { start, end });
  stream.on('error', () => res.destroy());
  res.on('close', () => stream.destroy());
  stream.pipe(res);
});
const port = Number(process.env.PORT || 3000);
server.listen(port, '0.0.0.0', () => console.log(`مع الصادقين · Final reel preview · 0.0.0.0:${port}`));
process.on('SIGTERM', () => server.close(() => process.exit(0)));
