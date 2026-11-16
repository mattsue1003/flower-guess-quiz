import json,sys,re,subprocess,html
UA="FlowerQuizBuilder/1.0 (educational teaching page; https://mattsue1003.github.io/)"
files=sys.argv[1].split("|")
args=["curl","-s","-A",UA,"-G","https://commons.wikimedia.org/w/api.php","--data-urlencode","titles="+"|".join("File:"+f for f in files),"-d","action=query","-d","prop=imageinfo","-d","iiprop=url|extmetadata|size","-d","iiurlwidth=1000","-d","format=json"]
d=json.loads(subprocess.run(args,capture_output=True,text=True).stdout)
out={}
for p in d["query"]["pages"].values():
    ii=p.get("imageinfo",[{}])[0]; m=ii.get("extmetadata",{})
    g=lambda k:re.sub("<[^>]+>","",html.unescape(m.get(k,{}).get("value",""))).strip()
    out[p["title"][5:].replace(" ","_")]=dict(thumb=ii.get("thumburl"),w=ii.get("width"),h=ii.get("height"),author=g("Artist"),lic=g("LicenseShortName"),licurl=m.get("LicenseUrl",{}).get("value",""),page=ii.get("descriptionurl"))
print(json.dumps(out,ensure_ascii=False,indent=1))
