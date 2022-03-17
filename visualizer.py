import moviepy.editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from scipy import interpolate

BAND_W = 100
INTERP_L = 100

class Visualizer:

    def __init__(self, audio):
        self.audio = audio.to_soundarray()
        self.audio = (self.audio[:, 0] + self.audio[:, 1]) # 2 channels
        self.fps = audio.fps
        self.window = np.hanning(BAND_W)
        self.x = np.linspace(0, 10, BAND_W)
        self.x_s = np.linspace(0, 10, INTERP_L)
        self.prev_y_s = np.zeros(INTERP_L)

        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1])

        DPI = self.fig.get_dpi()
        self.fig.set_size_inches(1920.0 / float(DPI), 200.0 / float(DPI))

    def _draw(self, spec, c):

        spl = interpolate.splrep(self.x, spec * self.window, s=1)
        y_s = np.tanh(interpolate.splev(self.x_s, spl))

        self.ax.clear()
        self.ax.set_axis_off()
        self.ax.set_ylim(bottom=-1, top=1)
        self.ax.set_xlim(left=0, right=10)
        self.ax.add_patch(Rectangle((0, -1), 10, 2, color='k'))
        self.ax.fill_between(self.x_s, y_s, color=c)
        self.ax.fill_between(self.x_s, -y_s, color=c)
        ret = mplfig_to_npimage(self.fig).copy()
        return ret

    def visualize(self, f):

        if (f + 1) * self.fps > len(self.audio) or (f - 1) < 0:
            return self._draw(np.zeros(BAND_W), c='k')

        frame = self.audio[int((f - 1) * self.fps):int((f + 1) * self.fps)]
        spec = np.abs(np.fft.fftshift(frame))

        checkpoint = len(spec) // 8

        r_spec = spec[checkpoint:checkpoint + BAND_W]
        g_spec = spec[checkpoint * 2:checkpoint * 2 + BAND_W]
        b_spec = spec[checkpoint * 3:checkpoint * 3 + BAND_W]

        fig_r = self._draw(r_spec, c='#F00')
        fig_g = self._draw(g_spec, c='#0F0')
        fig_b = self._draw(b_spec, c='#00F')

        return np.maximum(np.maximum(fig_r, fig_g), fig_b)
        

        

        
