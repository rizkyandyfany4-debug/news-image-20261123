// News Image 23 November 2026 entry (Node 22, standard library only).
// The whole program does one thing: it copies entry.png from the repository
// root to /output/entry.png, where the gate reads the front page this entry
// hands in. The image itself is the entry: a newspaper-style front page
// summing up the world news of Monday 23 November 2026, rendered by the
// agent session that wrote this file.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

// The front page must be a real PNG, at most 1024x1024 and at most 1 MiB.
// Check that before copying, so a bad entry.png fails loudly here instead
// of reaching the gate.
import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const MAX_BYTES = 1024 * 1024;
const MAX_DIM = 1024;

const source = join(BOT_DIR, 'entry.png');

let buf: Buffer;
try {
  buf = readFileSync(source);
} catch (err) {
  console.error(`entry.png could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 33 || !buf.subarray(0, 8).equals(PNG_MAGIC)) {
  console.error('entry.png is not a PNG file; refusing to copy.');
  process.exit(1);
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > MAX_DIM || height > MAX_DIM) {
  console.error(`entry.png is ${width}x${height}, over the ${MAX_DIM}x${MAX_DIM} cap; refusing to copy.`);
  process.exit(1);
}
if (buf.length > MAX_BYTES) {
  console.error(`entry.png is ${buf.length} bytes, over the 1 MiB cap; refusing to copy.`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(source, join(OUTPUT_DIR, 'entry.png'));
} catch (err) {
  console.error(`entry.png could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
