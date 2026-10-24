import re,sys,json,glob,os
root=sys.argv[1]
design=open(sys.argv[2]).read()
polys=re.findall(r'clip-path:polygon\(([^)]*)\)',design)
t=open(root+'/build/template.html').read()
t=t.replace('__TEAR1__',polys[0]).replace('__TEAR2__',polys[1])
def read_pack(path):
    # content pack: @unit / @lang / @topic / @words|@rituals sections, '#' lines are comments
    pk={'id':os.path.splitext(os.path.basename(path))[0],'unit':None,'lang':None,'topics':[]}
    cur=None
    for line in open(path,encoding='utf-8').read().splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        if s.startswith('@unit '): pk['unit']=s[6:].strip()
        elif s.startswith('@lang '): pk['lang']=s[6:].strip()
        elif s.startswith('@topic '):
            cur={'name':s[7:].strip(),'type':'words','lines':[]}; pk['topics'].append(cur)
        elif s in ('@words','@rituals'):
            assert cur,path+': section before @topic'; cur['type']=s[1:]
        else:
            assert cur,path+': text before @topic: '+s; cur['lines'].append(s)
    assert pk['unit'] and pk['lang'],path+': @unit and @lang are required'
    for tp in pk['topics']:
        assert tp['lines'],path+': empty topic '+tp['name']
        tp['text']='\n'.join(tp.pop('lines'))
    return pk
def packs_for(name):
    ps=[read_pack(p) for p in sorted(glob.glob(f'{root}/content/{name}/*.txt'))]
    return json.dumps(ps,ensure_ascii=False).replace('</','<\\/')
for name,hero,langs in [('harry','assets/harry.jpg',"['Angielski','Niemiecki']"),('hermione','assets/hermione.jpg',"['Angielski']")]:
    open(f'{root}/{name}.html','w').write(t.replace('__HERO__',hero).replace('__KEY__','spellbook_'+name).replace('__LANGS__',langs).replace('__PACKS__',packs_for(name)).replace('__NAME__',name).replace('<title>Spellbook</title>',f"<title>{name.title()}'s Spellbook</title>"))
# artifact variants: body content only, no document wrapper
for name in ['harry','hermione']:
    h=open(f'{root}/{name}.html').read()
    h=re.sub(r'<link rel="(manifest|icon|apple-touch-icon)"[^\n]*\n|<meta name="(apple-)?mobile-web-app-[^\n]*\n|<meta name="apple-mobile[^\n]*\n|if\(\'serviceWorker\'[^\n]*\n','',h)
    h=h.replace('<!doctype html>\n','')
    h=re.sub(r'<html[^>]*>\n<head>\n','',h).replace('</head>\n<body>\n','').replace('</body>\n</html>\n','')
    h=h.replace('<meta charset="utf-8">\n','').replace('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n','')
    open(f'{root}/build/{name}.artifact.html','w').write(h)
