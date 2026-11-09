"""Atomic receipts and allowlisted evidence export; no source folders or model weights."""
import hashlib,json,os,re,zipfile
from pathlib import Path,PurePosixPath
from .integrity import sha

def write(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_name(path.name+'.tmp')
    temp.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n');os.replace(temp,path)

def allowed(name):
    p=PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name or not name:return False
    if any(s in {'sources','workspace','.git'} for s in p.parts):return False
    if p.suffix=='.apk':return name in {'apks/M51-'+v+x+'.apk' for v in ['baseline','candidate'] for x in ['','-tests']}
    return p.suffix in {'.json','.md','.html','.txt','.log','.xml','.png','.svg'}

def files(output):
    root=Path(output);items=[]
    for f in sorted(root.rglob('*')):
        name=f.relative_to(root).as_posix()
        if f.is_symlink():raise ValueError('SYMLINK_EVIDENCE_REFUSED')
        if not f.is_file() or name in {'evidence.zip','evidence.zip.sha256','SHA256SUMS'} or any(x in f.relative_to(root).parts for x in ['workspace','sources']):continue
        if not allowed(name):raise ValueError('UNAUTHORIZED_EXPORT:'+name)
        if f.stat().st_size>32*1024*1024:raise ValueError('OVERSIZE_EVIDENCE:'+name)
        items.append((name,f))
    return items

def export(output):
    root=Path(output);items=files(root)
    sums=''.join(sha(p)+'  '+name+'\n' for name,p in items)
    (root/'SHA256SUMS').write_text(sums)
    zpath=root/'evidence.zip'
    with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
        for name,p in items:
            entry=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o100644<<16
            z.writestr(entry,p.read_bytes())
        z.writestr('SHA256SUMS',sums)
    digest=sha(zpath);(root/'evidence.zip.sha256').write_text(digest+'  evidence.zip\n')
    verify_archive(zpath)
    return {'path':'evidence.zip','sha256':digest,'files':len(items),'bytes':zpath.stat().st_size}

def verify_archive(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or len(names)>5000 or 'SHA256SUMS' not in names:raise ValueError('INVALID_ARCHIVE_INDEX')
        if sum(i.file_size for i in z.infolist())>256*1024*1024:raise ValueError('OVERSIZE_ARCHIVE')
        indexed={}
        for line in z.read('SHA256SUMS').decode().splitlines():
            digest,name=line.split('  ',1)
            if name in indexed or not re.fullmatch('[0-9a-f]{64}',digest) or not allowed(name):raise ValueError('UNSAFE_ARCHIVE_MEMBER')
            indexed[name]=digest
        if set(names)!=(set(indexed)|{'SHA256SUMS'}):raise ValueError('UNINDEXED_ARCHIVE_MEMBER')
        for name,digest in indexed.items():
            if hashlib.sha256(z.read(name)).hexdigest()!=digest:raise ValueError('ARCHIVE_DIGEST_MISMATCH')
    return {'status':'PASS','files':len(indexed),'sha256':sha(path)}
