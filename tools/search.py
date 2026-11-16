import json,sys,re,subprocess,html
UA="FlowerQuizBuilder/1.0 (educational teaching page; https://mattsue1003.github.io/)"
q=sys.argv[1]; n=sys.argv[2] if len(sys.argv)>2 else "8"
args=["curl","-s","-A",UA,"-G","https://commons.wikimedia.org/w/api.php","--data-urlencode","gsrsearch="+q+" filetype:bitmap","-d","action=query","-d","generator=search","-d","gsrnamespace=6","-d","gsrlimit="+n,"-d","prop=imageinfo","-d","iiprop=url|extmetadata|size","-d","iiurlwidth=400","-d","format=json"]
d=json.loads(subprocess.run(args,capture_output=True,text=True).stdout)
for p in sorted(d.get("query",{}).get("pages",{}).values(),key=lambda p:p.get("index",0)):
    ii=p["imageinfo"][0]; m=ii.get("extmetadata",{})
    g=lambda k:re.sub("<[^>]+>","",html.unescape(m.get(k,{}).get("value",""))).strip()
    print(p["title"][5:], ii["width"],"x",ii["height"], g("LicenseShortName"),"|",g("Artist")[:30],"|",ii["thumburl"])
