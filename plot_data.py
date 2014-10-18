import matplotlib.pyplot as plt
from scikits import audiolab

t = audiolab.Sndfile("trim.wav")
f = t.read_frames(t.nframes)
plt.plot(f)
plt.show()
