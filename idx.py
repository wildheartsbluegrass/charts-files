import os,time,html
from urllib.parse import quote
SKIP={'.DS_Store','.git','icons','index.html','idx.py','conv.sh'}
def size(n):
    for u,d in (('G',1<<30),('M',1<<20),('K',1<<10)):
        if n>=d: v=n/d; return f"{v:.1f}{u}" if v<10 and u!='M' or (u=='M' and v<10) else f"{round(v)}{u}"
    return str(n)
def build(path,title,depth):
    ic="../"*depth+"icons/"
    ents=sorted((e for e in os.listdir(path) if e not in SKIP and not e.startswith('.')),key=lambda s:(not os.path.isdir(os.path.join(path,s)),s.lower()))
    rows=[]
    for e in ents:
        p=os.path.join(path,e);d=os.path.isdir(p);st=os.stat(p)
        name=e+("/" if d else "");href=quote(e)+("/" if d else "")
        icon,alt=("blank.gif","[DIR]") if d else (("layout.gif","[VID]") if e.lower().endswith(".mp4") else ("blank.gif","[   ]"))
        rows.append(f'<tr><td valign="top"><img src="{ic}{icon}" alt="{alt}"></td><td><a href="{href}">{html.escape(name)}</a></td><td align="right">{time.strftime("%Y-%m-%d %H:%M",time.localtime(st.st_mtime))}  </td><td align="right">{"  - " if d else size(st.st_size)}</td><td>&nbsp;</td></tr>')
    out=f'''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Index of {html.escape(title)}</title>
 </head>
 <body>
<h1>Index of {html.escape(title)}</h1>
  <table>
   <tbody><tr><th valign="top"><img src="{ic}blank.gif" alt="[ICO]"></th><th>Name</th><th>Last modified</th><th>Size</th><th>Description</th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="{ic}back.gif" alt="[PARENTDIR]"></td><td><a href="../">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
{chr(10).join(rows)}
   <tr><th colspan="5"><hr></th></tr>
</tbody></table>
</body></html>
'''
    open(os.path.join(path,"index.html"),"w").write(out)
    for e in ents:
        if os.path.isdir(os.path.join(path,e)): build(os.path.join(path,e),title+"/"+e,depth+1)
# Regenerates index.html in this folder and every subfolder.
build(os.path.dirname(os.path.abspath(__file__)),"/Wildhearts Bluegrass/Charts",0)
