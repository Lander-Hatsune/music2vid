import moviepy.editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from scipy.signal import savgol_filter
from scipy import interpolate

BAND_W = 512
INTERP_L = 100

class Visualizer:

    def __init__(self, audio):
        self.audio = audio.to_soundarray()
        self.audio = np.hypot(self.audio[:, 0], self.audio[:, 1])
        self.fps = audio.fps
        half_hann = np.hanning(2 * INTERP_L // 3)[0:INTERP_L // 3]
        self.window = np.concatenate((half_hann,
                                      np.ones(INTERP_L - 2 * len(half_hann)),
                                      half_hann[::-1]))
        self.x = np.linspace(0, 10, BAND_W)
        self.x_s = np.linspace(0, 10, INTERP_L)

        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1])

        DPI = self.fig.get_dpi()
        self.fig.set_size_inches(1920.0 / float(DPI), 200.0 / float(DPI))

    def _draw(self, spec, c):

        y = savgol_filter(spec, BAND_W // 2, 3)
        spl = interpolate.splrep(self.x, y)
        y_s = interpolate.splev(self.x_s, spl) * self.window
        
        self.ax.clear()
        self.ax.set_axis_off()
        self.ax.set_ylim(bottom=-1.5, top=1.5)
        self.ax.set_xlim(left=0, right=10)
        self.ax.add_patch(Rectangle((0, -1.5), 10, 3, color='k'))
        self.ax.fill_between(self.x_s, y_s, color=c)
        self.ax.fill_between(self.x_s, -y_s, color=c)

        ret = mplfig_to_npimage(self.fig).copy()
        return ret

    def visualize(self, f):

        if (f + 0.1) * self.fps > len(self.audio) or (f - 0.1) < 0:
            return self._draw(np.zeros(BAND_W), c='k')

        frame = self.audio[int((f - 0.1) * self.fps):int((f + 0.1) * self.fps)]
        spec = np.abs(np.fft.fftshift(frame))

        checkpoint = len(spec) // 6

        r_spec = spec[1:BAND_W + 1]
        g_spec = spec[checkpoint * 1:checkpoint * 1 + BAND_W]
        b_spec = spec[checkpoint * 2:checkpoint * 2 + BAND_W]

        fig_r = self._draw(r_spec, c='#F00')
        fig_g = self._draw(g_spec, c='#0F0')
        fig_b = self._draw(b_spec, c='#00F')

        return np.maximum(np.maximum(fig_r, fig_g), fig_b)
        

        

        
