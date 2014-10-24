import numpy
from scikits.audiolab import Format, Sndfile


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


c = changes[1] - halfclock * 2 - halfclock / 2
bitvalues = []
while True:
  v = y[round(c + halfclock * 2)]
  bitvalues.append(bool(v > 0.05))
  c += halfclock * 2
  if c + halfclock * 2 > len(y):
    break

s = []
for b in bitvalues:
  if b:
    s.append(1)
  else:
    s.append(0)

print len(bitvalues[:24])
print bitvalues[:24]
assert bitvalues[:24] == [
    True, True, True, True, True, True, True, True, True, True, True, True,
    True, True, True, True, True, True, True, True, True, True, True, True]

assert bitvalues[24:28] == [False, True, False, True]
payload = bitvalues[28:]
val = 0
print payload[:16]
logic = {True: '1',
         False: '0'}
sensor = []
print ''.join(map(lambda x: logic[x], payload[0:4][::-1]))
nibble = int(''.join(map(lambda x: logic[x], payload[0:4][::-1])), 2)
sensor.append(nibble)
nibble = int(''.join(map(lambda x: logic[x], payload[4:8][::-1])), 2)
sensor.append(nibble)
nibble = int(''.join(map(lambda x: logic[x], payload[8:12][::-1])), 2)
sensor.append(nibble)
nibble = int(''.join(map(lambda x: logic[x], payload[12:16][::-1])), 2)
sensor.append(nibble)
print sensor
# print hex(val)
print ''.join(map(str, s))
