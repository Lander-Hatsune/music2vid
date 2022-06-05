VERSION = 'v4.2'

import argparse
import os
from itertools import compress
import io
import stagger
from termcolor import colored
from PIL import Image
import numpy as np
import moviepy.editor as mpy
import moviepy.audio.fx.all as afx
from visualizer import Visualizer

MEDIA_EXT = ['.mp4', '.3gp', '.m4v', '.mkv', '.webm',
             '.mov', '.avi', '.wmv', '.mpg', '.flv',
             '.aac', '.mid', '.mp3', '.m4a', '.ogg', 
             '.flac', '.wav', '.amr', '.aiff']

IMG_EXT = ['.dwg', '.xcf', '.jpg', '.jpx', '.png', 
           '.apng', '.gif', '.webp', '.cr2', '.tif', 
           '.bmp', '.jxr', '.psd', '.ico', '.heic']


class Log:
    info = lambda s: print(colored('[INFO] ' + str(s)))
    err = lambda s: print(colored('[ERROR] ' + str(s), 'red'))
    done = lambda s: print(colored('[DONE] ' + str(s), 'green'))
    warn = lambda s: print(colored('[WARN] ' + str(s), 'yellow'))
    debug = lambda s: print(colored('[DEBUG]' + str(s), 'blue'))

def selExt(filenames, exts):
    mask = []
    for filename in filenames:
        mask.append(os.path.splitext(filename)[1] in exts)
    return compress(filenames, mask)
            

def parseArgs():
    parser = argparse.ArgumentParser(
        description='Convert/extract music to visualize as video')
    parser.add_argument('dir', type=str,
                        help='Dir of music/mv files to be converted/extracted')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parseArgs()
    dir = args.dir

    os.system('mkdir -p output')
    os.system('mkdir -p input/converted')
    os.system('mkdir -p input/failed')

    _, _, files = next(os.walk(dir))
    for filename in selExt(files, MEDIA_EXT):
        path = os.path.join(dir, filename)
        name, _ = os.path.splitext(filename)

        Log.info(f"Converting {filename}")

        try:
            music = mpy.AudioFileClip(path).audio_normalize()
        except Exception as e:
            Log.err(f'{e} occured when reading {filename}')
            os.system(f'mv "{path}" input/failed')
            continue

        visualizer = Visualizer(music)

        try:
            Log.info('Trying to parse album pic from file')
            tag = stagger.read_tag(path)
            album_pic = np.array(Image.open(io.BytesIO(
                tag[stagger.id3.APIC][0].data)))
            Log.done('Album pic parsed from file')
        except Exception as e:
            Log.warn(f'{e} occured when parsing album pic')
            album_pic = None

            Log.info('Trying to find album pic in input dir')
            for pic_filename in selExt(files, IMG_EXT):
                pic_path = os.path.join(dir, pic_filename)
                print(os.path.splitext(pic_filename)[0],
                      os.path.splitext(filename)[0])
                if os.path.splitext(pic_filename)[0] == \
                   os.path.splitext(filename)[0]:
                    album_pic = np.array(Image.open(pic_path))
                    os.system(f'mv "{pic_path}" input/converted')
                    Log.done('Album pic found in input dir')
                    break
            if album_pic is None:
                Log.warn('No album pic found in input dir')
            
        pic = (mpy.ImageClip(album_pic)
               .resize((600, 600))
               .set_position(('center', 120))
               .fadein(1)) if album_pic is not None else None

        text = (mpy.TextClip(name,
                             fontsize=50,
                             font='Microsoft-YaHei-UI-Bold',
                             color='white',
                             size=(1080, 120))
                .set_position(('center', 720 if pic is not None else 'center'))
                .fadein(1))

        visualized = (mpy.VideoClip(visualizer.visualize)
                     .set_position(('center', 'bottom')))

        composite = [pic, text, visualized] if pic is not None else \
            [text, visualized]
        
        vid = (mpy.CompositeVideoClip(composite, size=(1920, 1080))
               .set_duration(music.duration))
        
        vid = vid.set_audio(music)

        vid.write_videofile(f'output/{name} - [仅音乐{VERSION}].mp4', fps=24)
        vid.close()
        Log.done(f"{name} converted")

        os.system(f'mv "{path}" input/converted')


