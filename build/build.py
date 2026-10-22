import re,sys
root=sys.argv[1]
design=open(sys.argv[2]).read()
polys=re.findall(r'clip-path:polygon\(([^)]*)\)',design)
t=open(root+'/build/template.html').read()
t=t.replace('__TEAR1__',polys[0]).replace('__TEAR2__',polys[1])
for name,hero in [('harry','assets/harry.jpg'),('hermione','assets/hermione.jpg')]:
    open(f'{root}/{name}.html','w').write(t.replace('__HERO__',hero).replace('__KEY__','spellbook_'+name).replace('<title>Spellbook</title>',f'<title>Spellbook — {name.title()}</title>'))
