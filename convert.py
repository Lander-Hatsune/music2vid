import argparse
import os
import moviepy.editor as mpy
import moviepy.audio.fx.all as afx
import filetype
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

    os.system('mkdir output')

    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        name = os.path.splitext(filename)[0]
        mimetype = filetype.guess(path).mime[:5]

        if mimetype == 'audio':
            music = mpy.AudioFileClip(path)
        elif mimetype == 'video':
            music = mpy.VideoFileClip(path).audio
        else:
            print(f'{filename} isn\'t a video/audio file')
            continue

        visualizer = Visualizer(music)

        text = (mpy.TextClip(name,
                             fontsize=80,
                             font='Microsoft-YaHei-UI-Bold',
                             color='white')
                .set_position(('center', 'center')))


        visualized = (mpy.VideoClip(visualizer.visualize)
                     .set_position(('center', 'bottom')))
        
        vid = (mpy.CompositeVideoClip([text, visualized], size=(1920, 1080))
               .set_duration(music.duration))
        
        vid = vid.set_audio(music).afx(afx.audio_normalize)

        vid.write_videofile(f'output/{name}-[仅音乐].mp4', fps=24)
        vid.close()


