import numpy as np
from doppler import Doppler
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Physical Values
v_sound = 330.0  # Speed of sound
x_source, y_source = (0, 0)  # Source Coordinates
x_observer, y_observer = (10, 0)  # Observer Coordinates
vx_source, vy_source = (100, 100)  # Source Velocity
vx_observer, vy_observer = (0, 0)  # Observer Velocity
frequency = 100  # Frequency of Sound Wave (integer)

# Program values
max_waves = frequency/5
time_limit = 1  # (integer)
plot = True
program_speed = 1 if plot else 2  # 1 or 2


class Wave:
    def __init__(self, x: float, y: float):
        self.r: float = 0
        self.x = x
        self.y = y
        self.wave = plt.Circle((self.x, self.y), self.r,
                               facecolor='blue', edgecolor='k')

    def update(self, r: float):
        self.r = r
        self.wave = plt.Circle((self.x, self.y), r,
                               facecolor='none', edgecolor='k')


def generateAudio(frequencies: np.ndarray, sample_rate=44100):
    t = np.linspace(0., 1., sample_rate)
    amplitude = np.iinfo(np.int16).max
    data = np.array([])
    for freq in frequencies:
        data = np.append(data, amplitude*np.sin(2.*np.pi*freq*t))
    write("doppler_effect.wav", sample_rate, data.astype(np.int16))


if(plot):
    plt.ion()
    fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(10, 6))
    ax: list[list[plt.Axes]]
    ax[1][1].axhline(y=frequency, color="purple", linestyle="--")
max_x = np.max([x_source + vx_source*time_limit,
               x_observer + vx_observer*time_limit])*1.2
max_y = np.max([y_source + vy_source*time_limit,
               y_observer + vy_observer*time_limit])*1.2
x_diff, y_diff = (np.abs(x_observer-x_source), np.abs(x_observer-x_source))
max_diff = np.max([x_diff, y_diff])*1.2
max_coordinate = np.max([max_x, max_y])
waves: list[Wave] = []
dt = 1/frequency
w = 2*np.pi*frequency
k = 0

apparent_frequencies = np.array([])


for time_frame in np.linspace(0, time_limit, int(np.floor((10 * frequency * time_limit)/program_speed))):
    t = time_frame * program_speed
    k += 1 * program_speed
    x1, y1 = (x_source + vx_source*t, y_source + vy_source*t)
    x2, y2 = (x_observer + vx_observer*t, y_observer + vy_observer * t)

    doppler = Doppler(source_frequency=frequency,
                      v_observer=[vx_observer, vy_observer],
                      v_source=[vx_source, vy_source],
                      source_coordinate=[x1, y1],
                      observer_coordinates=[x2, y2],
                      v_sound=v_sound)

    w_apparent = doppler.apparent_frequency()
    apparent_frequencies = np.append(apparent_frequencies, (w_apparent))

    if(plot):
        ax[0][1].cla()
        ax[0][0].set_title('Sound Wave as sent by source')
        ax[1][0].set_title('Sound Wave as perceived by observer')
        ax[1][1].set_title('Apparent frequency')
        ax[0][1].set_title('Physical Situation')
        for i in [ax[1][0], ax[1][1]]:
            i.set_xlabel('Time (s)')
        for i in waves:
            i.update(i.r + v_sound*dt*program_speed/10)
            ax[0][1].add_artist(i.wave)
        if k >= 10:
            new_Wave = Wave(x1, y1)
            ax[0][1].add_artist(new_Wave.wave)
            waves.append(new_Wave)
            k = 0
        if len(waves) > max_waves:
            waves.pop(0)
        ax[0][1].plot(x1, y1, 'ro')
        ax[0][1].plot(x2, y2, 'bo')
        ax[0][1].set_xlim(-max_diff,  max_diff)
        ax[0][1].set_ylim(-max_diff,  max_diff)

        if t > dt*10:
            for i in [ax[0][0], ax[1][0], ax[1][1]]:
                i.set_xlim(t-dt*10, t)
        else:
            for i in [ax[0][0], ax[1][0], ax[1][1]]:
                i.set_xlim(0, dt*10)
        ax[1][1].plot(t, w_apparent, 'go')
        ax[0][0].plot(t, np.sin(w*t), 'ro')
        ax[1][0].plot(t, np.sin(w_apparent*t), 'bo')
        fig.tight_layout()
        for i in ax:
            for m in i:
                plt.setp(m.get_xticklabels(), rotation=30,
                         horizontalalignment='right')
        fig.suptitle(f'time (t) = {t:.3f}s', fontsize=10)
        fig.canvas.draw()
        fig.canvas.flush_events()

print("Finished simulating! Now generating Audio File...")
generateAudio(apparent_frequencies)
print("Done!")
