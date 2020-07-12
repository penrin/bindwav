bindwav
=======

bind multiple wave files into one file


Requirments
-----------

* python3
* numpy



Usage
-----

```
$ python bindwav ABC 24
```
binds multiple wav files `ABC_01.wav, ABC_02.wav, ..., ABC_24.wav` into one file `ABC_bind24ch.wav`.
Multiple file needs to be monaural and named by serial numbers starting from 1.

'0' digits filled to the left is adjusted by option `--digit`, so `--digit 1` don't fill zeros. If 0 or less is put in this option, the digit is automatically determined.


Data size limit
---------------

The write data size is limited to 2^32-1 bytes (excluding 44 bytes for file header).
And, the number of channels, sample length, etc. are limited according to the description space of the _fmt chunk_.
(This program does not support the wave extension format.)

As long as the common sample width and sample rate are used, the number of channels and sample length must satisfy the following conditions:

1. `ch < 2^16`
2. `ws * fs * ch < 2^32`
3. `ws * length * ch < 2^32`

here

* `ch`: number of channels
* `ws`: sample width (bytes)
* `fs`: sample rate (Hz)
* `length`: sample length per 1 channel


conditions 1 and 2 come from the _fmt chunk_, and
3 comes from _data chunk_.

If `ws` and `fs` are given, the upper limit of `ch` is determined by `min(2^16 - 1, floor(2^32 / ws / fs))`. 
Then, the upper limit of `length` is determined by `floor(2^32 / ws / ch)`.



`ch` upper limit example:

| fs (Hz) | 8 bit | 16 bit | 24 bit | 32 bit |
| ---: | ---: | ---: | ---: | ---: | 
| 8000 | 65535 | 65535 | 65535 | 65535 |
| 32000 | 65535 | 65535 | 44739 | 33554 |
| 44100 | 65535 | 48695 | 32463 | 24347 |
| 48000 | 65535 | 44739 | 29826 | 22369 |
| 64000 | 65535 | 33554 | 22369 | 16777 |
| 88200 | 48695 | 24347 | 16231 | 12173 |
| 96000 | 44739 | 22369 | 14913 | 11184 |
| 128000 | 33554 | 16777 | 11184 | 8388 |
| 176400 | 24347 | 12173 | 8115 | 6086 |
| 192000 | 22369 | 11184 | 7456 | 5592 |


`length` upper limit example:

<img width="420" alt="length_lim" src="https://user-images.githubusercontent.com/8520833/87246854-d5387780-c48a-11ea-9dee-a109d358763d.png">
