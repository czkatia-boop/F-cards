import re,sys
root=sys.argv[1]
design=open(sys.argv[2]).read()
polys=re.findall(r'clip-path:polygon\(([^)]*)\)',design)
t=open(root+'/build/template.html').read()
t=t.replace('__TEAR1__',polys[0]).replace('__TEAR2__',polys[1])
for name,hero,langs in [('harry','assets/harry.jpg',"['Angielski','Niemiecki']"),('hermione','assets/hermione.jpg',"['Angielski']")]:
    open(f'{root}/{name}.html','w').write(t.replace('__HERO__',hero).replace('__KEY__','spellbook_'+name).replace('__LANGS__',langs).replace('__NAME__',name).replace('<title>Spellbook</title>',f"<title>{name.title()}'s Spellbook</title>"))
# artifact variants: body content only, no document wrapper
for name in ['harry','hermione']:
    h=open(f'{root}/{name}.html').read()
    h=re.sub(r'<link rel="(manifest|icon|apple-touch-icon)"[^\n]*\n|<meta name="(apple-)?mobile-web-app-[^\n]*\n|<meta name="apple-mobile[^\n]*\n|if\(\'serviceWorker\'[^\n]*\n','',h)
    h=h.replace('<!doctype html>\n','')
    h=re.sub(r'<html[^>]*>\n<head>\n','',h).replace('</head>\n<body>\n','').replace('</body>\n</html>\n','')
    h=h.replace('<meta charset="utf-8">\n','').replace('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n','')
    open(f'{root}/build/{name}.artifact.html','w').write(h)
