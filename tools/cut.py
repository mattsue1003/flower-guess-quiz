import numpy as np
from PIL import Image,ImageFilter
from scipy import ndimage as nd
# key: (crop fractions l,t,r,b)
jobs={'peony':(0.05,0.05,0.98,0.80),'camellia':(0.0,0.0,1.0,1.0),'fav2':(0.02,0.0,0.98,0.80),'lotusi':(0.0,0.25,0.8,1.0),'rosag':(0.0,0.03,0.85,0.88),'fav3':(0.02,0.0,0.98,0.80)}
for k,(l,t,r,b) in jobs.items():
    im=Image.open(f'work/deco/{k}.src').convert('RGB'); W,H=im.size
    im=im.crop((int(l*W),int(t*H),int(r*W),int(b*H)))
    a=np.asarray(im).astype(float)/255
    mx=a.max(2); mn=a.min(2); sat=(mx-mn)/(mx+1e-6)
    # paper: sample border median
    bd=np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3),a[:,:8].reshape(-1,3),a[:,-8:].reshape(-1,3)])
    paper=np.median(bd,0)
    dist=np.sqrt(((a-paper)**2).sum(2))
    psat=(paper.max()-paper.min())/paper.max()
    m=(dist>(0.24 if k.startswith('fav') else 0.15))|(sat>psat+0.22)
    m=nd.binary_closing(m,iterations=2)
    holes=nd.binary_fill_holes(m)&~m; hl,hn=nd.label(holes); hs=nd.sum(holes,hl,range(1,hn+1)); m=m|np.isin(hl,1+np.where(hs<400)[0])
    m=nd.binary_opening(m,iterations=2)
    lab,n=nd.label(m); sizes=nd.sum(m,lab,range(1,n+1))
    keep=np.isin(lab,1+np.where(sizes>sizes.max()*0.04)[0])
    alpha=Image.fromarray((keep*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    out=im.convert('RGBA'); out.putalpha(alpha)
    bb=out.getbbox(); out=out.crop(bb); out.thumbnail((700,700))
    out.save(f'assets/deco/{k}.png',optimize=True)
    print(k,out.size)
