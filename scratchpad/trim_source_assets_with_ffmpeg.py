import glob
import os
from subprocess import call

src_folder = r"\\diskstation\web\mott_ingest\aenetworks"
target_folder = r"C:\Users\earabmt\Downloads\A+E\trimmed_assets"
output_prefix = ""
output_postfix = "_trimmed"
search_term = "*.mxf"
simulation = False

if not os.path.exists(src_folder):
    print(f'Src folder does not exist!: {target_folder}')
    print('Exiting')
    exit()

if not os.path.exists(target_folder):
    print(f'Attempting to make target folder: {target_folder}')
    os.makedirs(target_folder)
print(f'target folder exists: {target_folder}')

for fp in glob.glob(os.path.join(src_folder, search_term)):
    print(f'source: {fp}')
    _, fn = os.path.split(fp)
    bn, ext = os.path.splitext(fn)
    target_fn = output_prefix + bn + output_postfix + ext
    target_fp = os.path.join(target_folder, target_fn)
    print(f'target: {target_fp}')
    cmd = f'ffmpeg -i "{fp}" -ss 00:00:00 -to 00:01:00 -c:v copy -c:a copy -map 0 "{target_fp}"'
    print(f'cmd: {cmd}')
    if not simulation:
        call(cmd)


"""
TRIM
cmd = f'ffmpeg -i "{fp}" -ss 00:00:00 -to 00:01:00 -c:v copy -c:a copy -map 0 "{target_fp}"'



"""