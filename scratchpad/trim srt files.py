import glob
import os
import srt

src_folder = r"\\192.168.1.210\web\mott_ingest\aenetworks\subs\offset4"
target_folder = r"\\192.168.1.210\web\mott_ingest\aenetworks\subs\trimmed"
output_prefix = ""
output_postfix = ""
search_term = "*.srt"
max_end_in_secs = 60
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
    with open(fp, 'r', encoding='utf8') as f:
        subtitle_generator = srt.parse(f.read())
    subtitles = list(subtitle_generator)
    filtered_subtitles = [
        sub for sub in subtitles
        if sub.end.total_seconds() <= max_end_in_secs
    ]
    for sub in filtered_subtitles:
        print(sub)
    if not simulation:
        with open(target_fp, 'w', encoding='utf8') as tf:
            tf.writelines(srt.compose(filtered_subtitles))





"""
TRIM
cmd = f'ffmpeg -i "{fp}" -ss 00:00:00 -to 00:01:00 -c:v copy -c:a copy -map 0 "{target_fp}"'



"""