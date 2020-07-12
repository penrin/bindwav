import sys
import os
import wave
import math
import numpy as np


class ProgressBar():

    def __init__(self, end, bar_length=40, slug='=', space=' '):
        self.bar_length = bar_length
        self.slug = slug
        self.space = space
        
        self.end = end
        self.count = 0
        self.bar()
    
    def bar(self, tail=''):
        percent = self.count / self.end
        self.count += 1
        
        len_slugs = int(percent * self.bar_length)
        slugs = self.slug * len_slugs
        spaces = self.space * (self.bar_length - len_slugs)
        txt = '\r[{bar}] {percent:.1%} {tail}'.format(
                bar=(slugs + spaces), percent=percent, tail=tail)
        if percent == 1:
            txt += '\n'
        sys.stdout.write(txt)
        sys.stdout.flush()
        

def bind(head, N, ndigits=0, chunksize=2**14):

    # file name
    if not ndigits > 0:
        ndigits = len(str(N))

    filenames = []
    for ch in range(1, N + 1):
        fname = head + '_' + str(ch).zfill(ndigits) + '.wav'
        filenames.append(fname)

    # open read files ... close() is called automatically on garbage collection
    wr = [wave.open(fname, 'r') for fname in filenames]
    
    # check params
    for i in range(N):
        if wr[i].getnchannels() != 1:
            raise Exception('Not mono: \'%s\'' % filenames[i])

    sampwidth = wr[0].getsampwidth()
    for i in range(1, N):
        if wr[i].getsampwidth() != sampwidth:
            raise Exception('sample width mismatching')

    framerate = wr[0].getframerate()
    for i in range(1, N):
        if wr[i].getframerate() != framerate:
            raise Exception('sample rate mismatching')

    nframes = wr[0].getnframes()
    for i in range(1, N):
        if wr[i].getnframes() != nframes:
            raise Exception('sample size mismatching')

    # check writability as wave
    if not N < 2 ** 16: # fmt channel
        raise Exception('not writable: nchannels is too much')
    if not sampwidth * framerate * N < 2 ** 32: # fmt bytes per sec
        raise Exception('not writable: bytes per sec is too much')
    if not sampwidth * nframes * N < 2 ** 32: # data chunk size
        raise Exception('not writable: too long')


    # open write file ... close() is called automatically on garbage collection
    fname = head + '_bind%dch.wav' % N
    cnt = 1
    while os.path.exists(fname):
        fname = head + '_bind%dch_%d.wav' % (N, cnt)
        cnt += 1

    ww = wave.open(fname, 'wb')
    ww.setparams((N, sampwidth, framerate, 0, 'NONE', 'not compressed'))
    
    
    # bind
    buff = np.empty([chunksize, N, sampwidth], dtype=np.uint8, order='C')
    
    pg = ProgressBar(math.ceil(nframes / chunksize))
    pos = 0
    while pos < nframes:
        
        if nframes - pos < chunksize:
            buff = buff[:nframes - pos, :, :]
            pos = nframes
        else:
            pos += chunksize

        for i in range(N):
            frame = wr[i].readframes(chunksize)
            data = np.frombuffer(frame, dtype=np.uint8)
            buff[:, i, :] = data.reshape(-1, sampwidth)
        ww.writeframes(buff.tostring())
        pg.bar()
    
    return


if __name__ == '__main__':
    
    head = 'test'
    N = 4
    ndigits = 0
    chunksize = 2 ** 14
    try:
        bind(head, N, ndigits, chunksize)
    except Exception as e:
        print(e)

