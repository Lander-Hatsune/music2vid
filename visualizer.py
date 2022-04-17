import moviepy.editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import splrep, splev
from randcolor import get3Colors

BAND_0 = np.arange(16, 160) # 40 ~ 400
BAND_1 = np.arange(160, 600) # 150 ~ 1500
BAND_2 = np.arange(600, 1600) # 400 ~ 4000

class Visualizer:

    def __init__(self, audio):
        self.audio = audio.to_soundarray()
        self.audio = np.hypot(self.audio[:, 0], self.audio[:, 1])
        self.colors = get3Colors(int(sum(self.audio)))
        self.fps = audio.fps

        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        DPI = self.fig.get_dpi()
        self.fig.set_size_inches(1920.0 / float(DPI), 240.0 / float(DPI))

    def _prepare(self):
        self.ax.clear()
        self.ax.set_axis_off()
        self.ax.set_ylim(bottom=-1.2, top=1.2)
        self.ax.set_xlim(left=0, right=1)
        self.ax.add_patch(Rectangle((0, -1.2), 1, 1.2 * 2, color='k'))

    def _draw(self, spec, c):
        self._prepare()

        spec = spec[::len(spec) // 128] # at most 128 knots
        spec = spec / (np.max(spec) + 0.00001) # no nan
        spec = spec * np.hanning(len(spec))
        spec = savgol_filter(spec, len(spec) // 3, 5)
        spec = savgol_filter(spec, len(spec) // 3, 5)
        x = np.linspace(0, 1, len(spec))
        self.ax.fill_between(x, spec, color=c)
        self.ax.fill_between(x, -spec, color=c)

        ret = mplfig_to_npimage(self.fig).copy()
        return ret

    def visualize(self, f):

        if (f + 0.1) * self.fps > len(self.audio) or (f - 0.3) < 0:
            return self._draw(np.zeros(len(BAND_0)), c='k')

        frame = self.audio[int((f - 0.3) * self.fps):int((f + 0.1) * self.fps)]
        spec = np.abs(np.fft.rfft(frame))

        fig_0 = self._draw(spec[BAND_0], c=self.colors[0])
        fig_1 = self._draw(spec[BAND_1], c=self.colors[1])
        fig_2 = self._draw(spec[BAND_2], c=self.colors[2])

        return np.maximum(np.maximum(fig_0, fig_1), fig_2)
