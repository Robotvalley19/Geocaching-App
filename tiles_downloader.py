"""
Offline Tile Downloader for OpenStreetMap
⚠️ Tiles are NOT included in this repository.
Use only responsibly. Respect tile server usage policies.
"""

import os, time, argparse, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

USER_AGENT = "MyGeocacheOfflineDownloader/1.0"

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--minz", type=int, default=0)
    p.add_argument("--maxz", type=int, default=8)
    p.add_argument("--out", default="./static/tiles")
    p.add_argument("--threads", type=int, default=8)
    p.add_argument("--delay", type=float, default=0.1)
    p.add_argument("--server", default="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
    return p.parse_args()

def ensure_dirs(path): os.makedirs(path, exist_ok=True)
def tile_url(server_tpl,z,x,y): return server_tpl.format(z=z,x=x,y=y)
def download_tile(session,server_tpl,z,x,y,out_dir,delay):
    url = tile_url(server_tpl,z,x,y)
    outfile = os.path.join(out_dir,str(z),str(x),f"{y}.png")
    ensure_dirs(os.path.dirname(outfile))
    if os.path.isfile(outfile): return True
    try:
        r = session.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
        if r.status_code==200:
            with open(outfile,"wb") as f: f.write(r.content)
            if delay: time.sleep(delay)
            return True
    except: return False
    return False

def main():
    args = parse_args()
    total = sum((1<<z)**2 for z in range(args.minz,args.maxz+1))
    if total>1_000_000: print("WARNING: >1,000,000 tiles"); time.sleep(3)
    session = requests.Session(); session.headers.update({"User-Agent":USER_AGENT})
    for z in range(args.minz,args.maxz+1):
        n=1<<z; zoom_tiles=[(z,x,y) for x in range(n) for y in range(n)]
        print(f"Zoom {z}: {len(zoom_tiles)} tiles")
        with ThreadPoolExecutor(max_workers=args.threads) as exe:
            futures={exe.submit(download_tile,session,args.server,z,x,y,args.out,args.delay):(z,x,y) for z,x,y in zoom_tiles}
            pbar=tqdm(total=len(zoom_tiles), desc=f"z={z}", unit="tile")
            for fut in as_completed(futures): fut.result(); pbar.update(1)
            pbar.close()

if __name__=="__main__": main()
