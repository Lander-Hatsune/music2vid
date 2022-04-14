import argparse
import os
import io
import stagger
from PIL import Image
import numpy as np
import moviepy.editor as mpy
import moviepy.audio.fx.all as afx
from visualizer import Visualizer

def parseArgs():
    parser = argparse.ArgumentParser(
        description='Convert/extract music to plain vid')
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

    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        if not os.path.isfile(path):
            continue
        
        name, ext = os.path.splitext(filename)

        try:
            music = mpy.AudioFileClip(path).audio_normalize()
            album_pic = np.array(Image.open(io.BytesIO(
                stagger.read_tag(path)[stagger.id3.APIC][0].data))) \
                if ext == '.mp3' else None
        except Exception as e:
            print(filename, e)
            os.system(f'mv "{path}" input/failed')
            continue

        visualizer = Visualizer(music)

        text = (mpy.TextClip(name,
                             fontsize=50,
                             font='Microsoft-YaHei-UI-Bold',
                             color='white',
                             size=(1080, 120))
                .set_position(('center', 720))
                .fadein(0.5))


        pic = (mpy.ImageClip(album_pic)
               .resize((600, 600))
               .set_position(('center', 120))
               .fadein(0.5)) if album_pic is not None else None

        visualized = (mpy.VideoClip(visualizer.visualize)
                     .set_position(('center', 'bottom')))
        
        vid = (mpy.CompositeVideoClip([pic, text, visualized], size=(1920, 1080))
               .set_duration(music.duration))
        
        vid = vid.set_audio(music)

        vid.write_videofile(f'output/{name} - [仅音乐].mp4', fps=24)
        vid.close()

        os.system(f'mv "{path}" input/converted')


