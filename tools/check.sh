#!/bin/zsh
id=$1
o=$(curl -s -w "\n%{http_code}" "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=$id&format=json")
code=${o##*$'\n'}; body=${o%$'\n'*}
w=$(curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36" -H "Accept-Language: zh-TW" "https://www.youtube.com/watch?v=$id")
pe=$(print -r -- "$w" | grep -o '"playableInEmbed":[a-z]*' | head -1)
ps=$(print -r -- "$w" | grep -o '"playabilityStatus":{"status":"[A-Z_]*"' | head -1 | sed 's/.*"status":"//;s/"//')
meta=$(print -r -- "$body" | python3 -c 'import sys,json
try:
 d=json.load(sys.stdin);print(d["author_name"]+"\t"+d["title"])
except Exception: print("-\t-")')
print -r -- "$id	$code	$pe	$ps	$meta"
