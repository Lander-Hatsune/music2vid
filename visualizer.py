import moviepy.editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


class Visualizer:

    def __init__(self, audio):
        self.audio = audio.to_soundarray()[:, 0]
        self.fps = audio.fps
        self.window = np.hamming(self.fps // 24)
        self.x = np.linspace(0, 10, 50)

        plt.box(False)

        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1])

        DPI = self.fig.get_dpi()
        self.fig.set_size_inches(1000.0 / float(DPI), 200.0 / float(DPI))

    def visualize(self, f):

        if (f + 1 / 24) * self.fps > len(self.audio):
            return mplfig_to_npimage(self.fig)

        frame = self.audio[int(f * self.fps):int((f + 1 / 24) * self.fps)]
        spec = np.abs(np.fft.fftshift(frame))

        checkpoint = len(spec) // 8

        r_spec = spec[checkpoint:checkpoint + 50]
        g_spec = spec[checkpoint * 2:checkpoint * 2 + 50]
        b_spec = spec[checkpoint * 3:checkpoint * 3 + 50]


        self.ax.clear()
        self.ax.set_axis_off()
        self.ax.set_ylim(bottom=0, top=1)
        self.ax.set_xlim(left=0, right=10)
        self.ax.add_patch(Rectangle((0, 0), 10, 1, color='k'))
        self.ax.fill_between(self.x, r_spec, color='#1a8bd9', alpha=0.2)
        self.ax.fill_between(self.x, g_spec, color='#cf277f', alpha=0.2)
        self.ax.fill_between(self.x, b_spec, color='#25c9c0', alpha=0.2)

        return mplfig_to_npimage(self.fig)
        

        

        
