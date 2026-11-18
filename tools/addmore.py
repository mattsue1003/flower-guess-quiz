# 依挑選結果下載額外照片並寫入 data/media.js 的 more 欄位
import json, sys, os, subprocess, re
UA = "FlowerQuizBuilder/1.0 (educational teaching page; https://mattsue1003.github.io/)"
PICK = dict(mume=[1,4], sakura=[2,5], azalea=[8,0], tung=[7,4], lotus=[3,10], sunflower=[1,9], rose=[11,2],
 orchid=[6,11], chrys=[3,8], osmanthus=[4,8], jasmine=[4,8], yulan=[1,8], bougain=[0,10], morning=[0,10],
 tanhua=[0,10], hydrangea=[0,1], phoenix=[6,1], cassia=[1,8], lily=[4,6], lavender=[4,3], cosmos=[4,3],
 kapok=[7,6], daylily=[1,9], calla=[5,10], tulip=[7,9], carnation=[5,11], hibiscus=[3,8], camellia=[5,7],
 plumeria=[2,10], narcissus=[1,11], murraya=[4,6], peach=[0,8], chinaberry=[2,6], gingerlily=[9,4],
 waterlily=[7,0], flamevine=[4,10], roselle=[11,0], poinsettia=[3,11], trumpettree=[4,1], wisteria=[4,9])
c = json.load(open(sys.argv[1]))
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(root, "data/media.js"), encoding="utf-8").read()
head, body = src.split("window.MEDIA=", 1)
mjson, rest = body.split("\n};", 1)
M = json.loads(mjson + "\n}")
for k, idx in PICK.items():
    more = []
    for n, i in enumerate(idx, start=2):
        p = c[k][i]; f = os.path.join(root, f"assets/img/{k}-{n}.jpg")
        if not os.path.exists(f) or os.path.getsize(f) < 5000:
            subprocess.run(["curl", "-s", "-L", "-A", UA, "-o", f, p["thumb"]], check=True)
        more.append(dict(author=p["author"], lic=p["lic"], licurl=p["licurl"], page=p["page"]))
    M[k]["more"] = more
open(os.path.join(root, "data/media.js"), "w", encoding="utf-8").write(head + "window.MEDIA=" + json.dumps(M, ensure_ascii=False, indent=1) + ";" + rest.lstrip(";"))
print("done", len(PICK))
