import numpy
from scikits.audiolab import Format, Sndfile


def logic_to_nibble(data):
  logic = {True: '1',
           False: '0'}
  nibble = int(''.join(map(lambda x: logic[x], data[0:4][::-1])), 2)
  # print data, ''.join(map(lambda x: logic[x], data[0:4][::-1]))
  return nibble

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

assert bitvalues[:24] == [
    True, True, True, True, True, True, True, True, True, True, True, True,
    True, True, True, True, True, True, True, True, True, True, True, True]

assert bitvalues[24:28] == [False, True, False, True]
payload = bitvalues[28:]
val = 0

sensor = []
nibble = logic_to_nibble(payload[0:4])
sensor.append(nibble)
nibble = logic_to_nibble(payload[4:8])
sensor.append(nibble)
nibble = logic_to_nibble(payload[8:12])
sensor.append(nibble)
nibble = logic_to_nibble(payload[12:16])
sensor.append(nibble)
print sensor

channel = logic_to_nibble(payload[16:20])
print channel

rolling_code = []
nibble = logic_to_nibble(payload[20:24])
rolling_code.append(nibble)
nibble = logic_to_nibble(payload[24:28])
rolling_code.append(nibble)
print rolling_code

battery = logic_to_nibble(payload[28:32])
print battery

anemometer_direction = logic_to_nibble(payload[32:36])
print anemometer_direction

anemometer_unknown = logic_to_nibble(payload[36:40])
print anemometer_unknown

anemometer_unknown2 = logic_to_nibble(payload[40:44])
print anemometer_unknown2

anemometer_current_speed = []
anemometer_current_speed.append(logic_to_nibble(payload[44:48]))
anemometer_current_speed.append(logic_to_nibble(payload[48:52]))
anemometer_current_speed.append(logic_to_nibble(payload[52:56]))
print anemometer_current_speed

anemometer_average_speed = []
anemometer_average_speed.append(logic_to_nibble(payload[56:60]))
anemometer_average_speed.append(logic_to_nibble(payload[60:64]))
anemometer_average_speed.append(logic_to_nibble(payload[64:68]))
print anemometer_average_speed

checksum1 = logic_to_nibble(payload[-16:-12])
print checksum1
checksum2 = logic_to_nibble(payload[-12:-8])
print checksum2

postamble1 = logic_to_nibble(payload[-8:-4])
print postamble1
postamble2 = logic_to_nibble(payload[-4:])
print postamble2


