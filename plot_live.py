import numpy
from numpy.fft import fft
import matplotlib.pyplot as plt
import rtlsdr
from scikits.audiolab import Format, Sndfile
from scikits.samplerate import resample

sdr = rtlsdr.RtlSdr()
sdr.sample_rate = 1024000    # sampling rate
sdr.center_freq = 88.5e6   # 162MhZ center frequency
sdr.gain = 36


filename = "test2.wav"
format = Format('wav')
f = Sndfile(filename, 'w', format, 1, 48000)
y = sdr.read_samples(1024000)
ry = numpy.real(y)
rsy = resample(ry, 48000/1024000., "sinc_fastest")
print len(rsy)
f.write_frames(rsy)
f.close()

# d = numpy.empty([1024000*10],dtype='complex')
# for i in range(10):
#     y = sdr.read_samples(1024000)
#     d[i*1024000:(i+1)*1024000] = y

# d = numpy.array(y)
# f = fft(d)
# print f
# plt.plot(f)
# plt.show()

