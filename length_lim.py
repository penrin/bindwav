import numpy as np
import matplotlib.pyplot as plt


def calc_lengthlim(ws, fs, ch):
    if ch > min(2 ** 16 - 1, np.floor(2 ** 32 / ws / fs)):
        return -1
    else:
        return np.floor((2 ** 32 - 1) / ws / ch)


ws, fs = 3, 48000
ch = [1, 2, 24, 96, 288, 1024, min(2 ** 16 - 1, np.floor(2 ** 32 / 3 / 48000))]
L = np.empty(len(ch), dtype=np.int)
for i in range(len(ch)):
    L[i] = calc_lengthlim(ws, fs, ch[i])
    print(ch[i], L[i] / fs)

plt.plot(ch, L / fs, '.-')
plt.xscale('log')
plt.yscale('log')

plt.xlabel('Number of channels')
plt.ylabel('Time (sec)')
plt.xlim(1, 2 ** 17)
plt.grid(which='both', lw=0.5)
plt.show()




