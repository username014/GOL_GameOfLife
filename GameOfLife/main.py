import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

class Rules:
    B1 = 0.278
    B2 = 0.365
    D1 = 0.267
    D2 = 0.445
    N = 0.028
    M = 0.147
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    @staticmethod
    def sigma(x, a, alpha):
        return 1.0 / (1.0 + np.exp(-4.0 / alpha * (x - a)))
    def sigma2(self, x, a, b):
        return self.sigma(x, a, self.N) * (1.0 - self.sigma(x, b, self.N))
    @staticmethod
    def lerp(a, b, t):
        return (1.0 - t) * a + t * b
    def s(self, n, m):
        alive = self.sigma(m, 0.5, self.M)
        return self.sigma2(n, self.lerp(self.B1, self.D1, alive), self.lerp(self.B2, self.D2, alive))


def logistic2d(size, radius, roll=True, logres=None):
    y, x = size
    # Get coordinate values of each point
    yy, xx = np.mgrid[:y, :x]
    # Distance between each point and the center
    radiuses = np.sqrt((xx - x/2)**2 + (yy - y/2)**2)
    # Scale factor for the transition width
    if logres is None:
        logres = math.log(min(*size), 2)
    with np.errstate(over="ignore"):
        # With big radiuses, the exp overflows,
        # but 1 / (1 + inf) == 0, so it's fine
        logistic = 1 / (1 + np.exp(logres * (radiuses - radius)))
    if roll:
        logistic = np.roll(logistic, y//2, axis=0)
        logistic = np.roll(logistic, x//2, axis=1)
    return logistic


class Multipliers:
    INNER_RADIUS = 7.0
    OUTER_RADIUS = INNER_RADIUS * 3.0
    def __init__(self, size, inner_radius=INNER_RADIUS, outer_radius=OUTER_RADIUS):
        inner = logistic2d(size, inner_radius)
        outer = logistic2d(size, outer_radius)
        annulus = outer - inner
        inner /= np.sum(inner)
        annulus /= np.sum(annulus)
        self.M = np.fft.fft2(inner)
        self.N = np.fft.fft2(annulus)


class SmoothLife:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.multipliers = Multipliers((height, width))
        self.rules = Rules()
        self.clear()

    def clear(self):
        self.field = np.zeros((self.height, self.width))

    def step(self):
        field_ = np.fft.fft2(self.field)
        M_buffer_ = field_ * self.multipliers.M
        N_buffer_ = field_ * self.multipliers.N
        M_buffer = np.real(np.fft.ifft2(M_buffer_))
        N_buffer = np.real(np.fft.ifft2(N_buffer_))
        s = self.rules.s(N_buffer, M_buffer)
        nextfield = s
        self.field = np.clip(nextfield, 0, 1)
        return self.field

    def _step(self, mode, f, s, m, dt):
        if mode == 0:
            return s
        elif mode == 1:
            return f + dt*(2*s - 1)
        elif mode == 2:
            return f + dt*(s - f)
        elif mode == 3:
            return m + dt*(2*s - 1)
        elif mode == 4:
            return m + dt*(s - m)

    def add_speckles(self, count=None, intensity=1):
        if count is None:
            count = 200 * (self.width * self.height) / (128 * 128)
            count *= (7.0 / self.multipliers.INNER_RADIUS) ** 2
            count = int(count)
        for i in range(count):
            radius = int(self.multipliers.INNER_RADIUS)
            r = np.random.randint(0, self.height - radius)
            c = np.random.randint(0, self.width - radius)
            self.field[r:r+radius, c:c+radius] = intensity



def show_animation():
    w = 1 << 9
    h = 1 << 9
    sl = SmoothLife(h, w)
    sl.add_speckles()
    sl.step()
    fig = plt.figure()
    #цвета, которые можно использовать:'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'
    im = plt.imshow(sl.field, animated=True, cmap=plt.get_cmap("gnuplot"), aspect="equal")
    def animate(*args):
        im.set_array(sl.step())
        return (im, )
    ani = animation.FuncAnimation(fig, animate, interval=1, blit=True)
    plt.show()

def save_animation():
    w = 1 << 8
    h = 1 << 8
    sl = SmoothLife(h, w)
    sl.add_speckles()
    from skvideo.io import FFmpegWriter
    from matplotlib import cm
    fps = 60
    frames = 100
    w = FFmpegWriter("smoothlife.mp4", inputdict={"-r": str(fps)})
    for i in range(frames):
        frame = cm.gnuplot(sl.field)
        frame *= 255
        frame = frame.astype("uint8")
        w.writeFrame(frame)
        sl.step()
    w.close()

if __name__ == '__main__':
    show_animation()