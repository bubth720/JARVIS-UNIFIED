"""Offline HTML, Markdown and machine receipts from actual persisted observations."""
import html,json
from pathlib import Path
from .evidence import write

def render(receipt, output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    write(out/'report.json',receipt)
    rows=receipt.get('modules',[]);results=receipt.get('commands',[])
    md=['# JARVIS INTEGRATION LAB — '+receipt.get('status','UNKNOWN'),'',
        'Campagne : `'+receipt['id']+'` ; mode '+receipt['profile']+'.',
        'LAB commit : `'+receipt['lab_commit']+'` ; tree `'+receipt['lab_tree']+'`.',
        'Les tests hôte, schémas et APK compilées ne prouvent ni Android ni une intégration runtime.','',
        '| Module | Source | État | Blocage |','|---|---|---|---|']
    md += ['| '+r['module']+' | `'+r['commit']+'` | '+r['status']+' | '+str(r.get('reason') or '')+' |' for r in rows]
    md += ['', '## Commandes exécutées', '', '| ID | Module / type | État | Invocations / uniques | Durée hôte (s) |', '|---|---|---|---|---|']
    for r in results:
        md.append('| '+r['id']+' | '+r['module']+' / '+r['kind']+' | '+r['status']+' | '+str(r.get('test_invocations'))+' / '+str(r.get('unique_test_cases'))+' | '+str(round(r.get('duration_ns',0)/1e9,3))+' |')
    md += ['', '## Android', '', json.dumps(receipt.get('android'),ensure_ascii=False), '',
           '## APK', '', 'Toutes les APK restent NON QUALIFIÉES tant que la réception Android du même build ne passe pas.', '',
           '## Décisions', '', 'CORE/LLM, racine LAB_CLOUD, JNI, modèles, appareils personnels et fusion : non autorisés par ce laboratoire.', '',
           '## Non exécuté', '', 'Génération réelle LLM, matériel personnel, nouvelles connexions runtime : NOT_RUN.', '',
           'Rapports complets : report.json, logs/, APK et manifeste SHA256. Durées de build : horloge monotone hôte, pas latence Android.', '',
           'Artefacts Actions conservés 90 jours ; télécharger evidence.zip avant expiration. Ce dashboard ne déclenche aucun build.']
    (out/'REPORT.md').write_text('\n'.join(md)+'\n')
    e=lambda v:html.escape(str(v),quote=True)
    def table(headers,data):
        return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(c)+'</td>' for c in row)+'</tr>' for row in data)+'</tbody></table></div>'
    sections=[]
    def section(i,title,body):sections.append('<section id="'+i+'"><h2>'+title+'</h2>'+body+'</section>')
    section('modules','Modules',table(['Module','Branche','Commit','État','Blocage'],[(r['module'],r['branch'],r['commit'],r['status'],r.get('reason','')) for r in rows]))
    section('dependencies','Dépendances et licences', ''.join('<details><summary>'+e(r['module'])+'</summary><pre>'+e(json.dumps(r.get('dependencies',{}),ensure_ascii=False,indent=2))+'</pre></details>' for r in rows))
    section('tests','Tests réels',table(['Commande','Type','État','Invocations','Cas uniques','Log'],[(r['id'],r['kind'],r['status'],r.get('test_invocations'),r.get('unique_test_cases'),r.get('log')) for r in results])+'<p>Ne pas additionner les variantes comme de nouveaux cas uniques. STATIC/NATIVE helper/SIMULATION ne prouvent aucune génération réelle.</p>')
    section('compat','Compatibilité',table(['De','Vers','État','Divergences','Inconnues'],[(r['from'],r['to'],r['status'],', '.join(r['mismatches']),', '.join(r['unknown'])) for r in receipt.get('compatibility',[])]))
    section('contracts','Contrats',table(['De','Vers','État runtime','Schémas','Motif'],[(r['from'],r['to'],r['status'],r['schema_equality'],r['reason']) for r in receipt.get('contracts',{}).get('links',[])]))
    section('android','Android', '<pre>'+e(json.dumps(receipt.get('android'),ensure_ascii=False,indent=2))+'</pre><p>APK de laboratoire : '+e(receipt.get('apks',{}).get('status','NOT_RUN'))+' — non qualifiées.</p><ul>'+''.join('<li><a href="'+e(a['path'])+'">'+e(a['path'])+'</a> · SHA256 '+e(a['sha256'])+'</li>' for a in receipt.get('apks',{}).get('artifacts',[]))+'</ul>')
    failed=[(r['module'],r['id'],r.get('reason'),r['status']) for r in results if r['status']!='PASS']
    section('regressions','Régressions',table(['Module','Commande','Cause','État'],failed)+'<p>Historique conservé : garde AndroidManifest LLM FAIL ; M51-R1 Android BLOCKED. Références et liens dans config/history.json, sans réécriture rétroactive.</p>')
    section('history','Historique', '<p>Cette campagne : '+e(receipt['id'])+'. Comparaison explicite : lab.py compare --before … --after … ; aucune équivalence de plateforme ou de cache présumée.</p>')
    section('decisions','Décisions', '<p>Mandats CORE/LLM, clés, JNI, nouveaux modèles, intégrations sensibles et appareils personnels : gates fermées. Aucune fusion ou installation par la consultation de cette page.</p>')
    data=json.dumps(receipt,ensure_ascii=False).replace('<','\\u003c').replace('&','\\u0026')
    css='body{margin:0;background:#101827;color:#e7edf8;font:16px system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:24px}h1{font-size:clamp(24px,5vw,40px)}nav{display:flex;flex-wrap:wrap;gap:14px}a{color:#75d8ff}section{margin:28px 0;padding:18px;background:#1a263b;border-radius:12px}.scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:10px;text-align:left;border-bottom:1px solid #35435c;vertical-align:top}pre{white-space:pre-wrap;overflow-wrap:anywhere}header p{color:#bac9e0}.state{display:inline-block;padding:8px 14px;background:#534126;border-radius:8px}'
    page='<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; script-src \'none\'; img-src data:; base-uri \'none\'; form-action \'none\'"><title>JARVIS Integration Lab</title><style>'+css+'</style><main><header><p>JARVIS · LAB-01 · outil de développement</p><h1>Integration Lab</h1><strong class="state">'+e(receipt.get('status'))+'</strong><p>'+e(receipt['id'])+' · '+e(receipt['profile'])+' · '+e(receipt['lab_commit'])+'</p><p>'+str(len(rows))+' modules inspectés · '+str(sum(r['status']=='PASS' for r in results))+' commandes réussies · '+str(sum(r['status']=='FAIL' for r in results))+' échouées · '+str(len(receipt.get('apks',{}).get('artifacts',[])))+' APK construites (non qualifiées)</p><nav>'+''.join('<a href="#'+i+'">'+name+'</a>' for i,name in [('modules','Modules'),('tests','Tests'),('compat','Compatibilité'),('contracts','Contrats'),('android','Android'),('regressions','Régressions'),('history','Historique'),('decisions','Décisions')])+'</nav></header>'+''.join(sections)+'<footer><p>Vue autonome hors ligne. Aucune commande, installation ou connexion réseau à la consultation.</p></footer></main><script type="application/json" id="receipt">'+data+'</script></html>'
    (out/'dashboard.html').write_text(page)
    return {'json':'report.json','markdown':'REPORT.md','dashboard':'dashboard.html'}

def compare(before,after):
    changed=[]
    a={r['module']:r for r in before.get('modules',[])};b={r['module']:r for r in after.get('modules',[])}
    for m in sorted(set(a)|set(b)):
        x,y=a.get(m,{}),b.get(m,{})
        changed.append({'module':m,'before':x.get('commit'),'after':y.get('commit'),'before_status':x.get('status','UNKNOWN'),'after_status':y.get('status','UNKNOWN'),'recommendation':'OPTIMISER' if y.get('status')=='FAIL' else 'CONSERVER'})
    comparable=before.get('environment')==after.get('environment') and before.get('profile')==after.get('profile') and before.get('build_cache_state')==after.get('build_cache_state') and before.get('build_cache_state') not in (None,'UNKNOWN')
    return {'status':'PARTIAL' if not comparable else 'PASS','modules':changed,'performance_comparable':comparable,
            'performance_delta':None,'memory_delta':None,'note':'No replacement or connection recommended without runtime, quality, authority and resource evidence.'}
