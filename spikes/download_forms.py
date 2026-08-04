import os
import subprocess

forms = ['i-130', 'i-485', 'i-765', 'i-129', 'n-400', 'g-28']
os.makedirs('forms', exist_ok=True)

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

for f in forms:
    url = f'https://www.uscis.gov/sites/default/files/document/forms/{f}.pdf'
    out_path = os.path.join('forms', f'{f}.pdf')
    print(f'Downloading {f}.pdf...')
    cmd = ['curl.exe', '-s', '-A', ua, '-o', out_path, url]
    subprocess.run(cmd, check=True)
    size = os.path.getsize(out_path)
    print(f'Saved {out_path} ({size:,} bytes)')

print("All downloads complete!")
