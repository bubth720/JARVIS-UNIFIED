"""Publish bounded UTF-8 text reports only, never any private data or executable/model payload."""
import hashlib,json
from pathlib import Path
from tooling.v1.validate import ROOT

def main():
 source=ROOT/'.audit-cache/m51-ci/raw';target=ROOT/'.audit-cache/m51-ci/public'
 target.mkdir(parents=True,exist_ok=False);names=[]
 for p in sorted(source.iterdir()):
  if not p.is_file():continue
  assert not p.is_symlink() and p.suffix.lower() in {'.json','.log','.txt','.svg'} and p.stat().st_size<=2*1024**2
  raw=p.read_bytes();assert not raw.startswith(b'GGUF');raw.decode('utf-8')
  (target/p.name).write_bytes(raw);names.append(p.name)
 (target/'publication.json').write_text(json.dumps({'status':'PASS','text_only':True,'model_or_voice_assets':False,'files':names},indent=2)+'\n')
 files=sorted(target.iterdir());(target/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in files))
 print('TEXT_ONLY',len(files),'reports')
if __name__=='__main__':main()
