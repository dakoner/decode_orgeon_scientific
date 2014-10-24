import numpy
from numpy.fft import fft
import matplotlib.pyplot as plt
from matplotlib import collections
import rtlsdr
from scikits.audiolab import Format, Sndfile
#from scikits.samplerate import resample


# sdr = rtlsdr.RtlSdr()
# sdr.sample_rate = 1024000    # sampling rate
# sdr.center_freq = 88.5e6   # 162MhZ center frequency
# sdr.gain = 36

# filename = "test2.wav"
# format = Format('wav')
# f = Sndfile(filename, 'w', format, 1, 48000)

# y = sdr.read_samples(1024000)
# ry = numpy.real(y)
# rsy = resample(ry, 48000/1024000., "sinc_fastest")
# f.write_frames(rsy)
# f.close()

# d = numpy.empty([1024000*10],dtype='complex')
# for i in range(10):
#     y = sdr.read_samples(1024000)
#     d[i*1024000:(i+1)*1024000] = y

# d = numpy.array(y)
# f = fft(d)
# print f
# plt.plot(f)
# plt.show()

# filename = "test2.wav"
# format = Format('wav')
# f = Sndfile(filename, 'w', format, 1, 48000)
# y = sdr.read_samples(1024000)


filename = 'trim.wav'
format = Format('wav')
f = Sndfile(filename, 'r')
y = f.read_frames(f.nframes)
x = numpy.arange(0, len(y))
signs = numpy.array(y > 0.05, int)
differences = numpy.diff(signs)
changes = numpy.nonzero(differences)[0]
changes_delta_t = numpy.diff(changes)
changes_long = numpy.where(changes_delta_t > 30, 0, 1)
print changes_long
halfclock = numpy.mean(numpy.diff(changes[1:24]))
print halfclock


f, ax = plt.subplots()
ax.plot(x, y, '-')

# cl = numpy.zeros((len(changes), 2, 2))
# for i in range(len(changes)):
#     cl[i] = [[changes[i], 0], [changes[i], 1]]
#ax.plot(x, signs, '-')
# ax.plt(x[:-1], differences, '-')
ax.scatter(changes, numpy.zeros(len(changes)))

i = 0
cl = []
c = changes[1] - halfclock * 2 - halfclock / 2
bitvalues = []
while True:
  print c
  v = y[round(c + halfclock * 2)]
  print y[round(c + halfclock * 2)]
  bitvalues.append(bool(v > 0.05))
  cl.append([[c, 0], [c + halfclock, 0]])
  cl.append([[c + halfclock, 0], [c + halfclock, 0.07]])
  cl.append([[c + halfclock, 0.07], [c + halfclock * 2, 0.07]])
  cl.append([[c + halfclock * 2, 0.07], [c + halfclock * 2, 0]])
  c += halfclock * 2
  if c + halfclock * 2 > len(y):
    break

s = []
for b in bitvalues:
  if b:
    s.append(1)
  else:
    s.append(0)

print ''.join(map(str, s))

lc = collections.LineCollection(cl)
ax.add_collection(lc)
ax.autoscale()
# plt.show()
