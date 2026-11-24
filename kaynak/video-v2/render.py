import asyncio, base64, subprocess, time, os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1920,'height':1080})
        await pg.goto('http://localhost:8777/anim.html')
        info=await pg.evaluate('window.READY'); total=info['TOTAL']; N=int(total*30)
        ff=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-',
            '-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-movflags','+faststart','tmp_nabiz_v2.mp4'],stdin=subprocess.PIPE)
        t0=time.time()
        for f in range(N):
            d=await pg.evaluate(f'render({f})')
            ff.stdin.write(base64.b64decode(d[23:]))
            if f%600==0: print(f,N,round(time.time()-t0),flush=True)
        ff.stdin.close(); rc=ff.wait(); await b.close()
        if rc==0: os.rename('tmp_nabiz_v2.mp4','Periapsis_NABIZ_Video_v2.mp4'); print('done',round(time.time()-t0))
asyncio.run(main())
