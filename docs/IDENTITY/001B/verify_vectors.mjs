// Independent JavaScript encoder for offline synthetic vectors; no Android codec or runtime.
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const vectors=JSON.parse(readFileSync(new URL('./vectors.json',import.meta.url),'utf8')).vectors;
function encode(v) {
  if(v===null)return 'null';
  if(typeof v==='boolean')return v?'true':'false';
  if(typeof v==='number') { if(!Number.isSafeInteger(v)||v<0)throw Error('integer');return String(v); }
  if(typeof v==='string') {
    for(const c of v) { const n=c.codePointAt(0);if(n>=0xd800&&n<=0xdfff)throw Error('surrogate'); }
    return JSON.stringify(v);
  }
  if(Array.isArray(v))return '['+v.map(encode).join(',')+']';
  if(v&&typeof v==='object')return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+encode(v[k])).join(',')+'}';
  throw Error('unsupported');
}
for(const v of vectors) {
  const bytes=Buffer.from(encode(v.value),'utf8');
  const digest=createHash('sha256').update(Buffer.from('jarvis.identity/1:001B.1\0','utf8')).update(bytes).digest('hex');
  if(bytes.toString('hex')!==v.canonical_hex||digest!==v.sha256)throw Error('vector mismatch: '+v.name);
}
console.log(JSON.stringify({javascript_vectors: vectors.length,result:'OK',android_codec_tested:false}));
