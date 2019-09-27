import wave
import numpy as np

inputFile = '/Users/giulio/Downloads/OSR_us_000_0061_8k.wav'
wr = wave.open(inputFile, 'r')
ww = wave.open(inputFile.replace('.wav', '_pitch.wav'), 'w')
ww.setparams(wr.getparams())

fr = 20
sz = wr.getframerate() // fr  # Read and process 1/fr second at a time.
# A larger number for fr means less reverb.
c = int(wr.getnframes() / sz)  # count of the whole file
print "Splitting file into %d parts" % c
shift = 100 // fr  # shifting 100 Hz
print "Applying shift of %d Hz" % shift
for num in range(c):
    da = np.fromstring(wr.readframes(sz), dtype=np.int16)
    left, right = da[0::2], da[1::2]

    # Compute FFT
    lf, rf = np.fft.rfft(left), np.fft.rfft(right)

    # Increase pitch
    lf, rf = np.roll(lf, shift), np.roll(rf, shift)

    # Set low frequencies to 0 after rolling
    lf[0:shift], rf[0:shift] = 0, 0

    # Compute IFFT to convert signal back into amplitude
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)

    # Combine channels
    ns = np.column_stack((nl, nr)).ravel().astype(np.int16)

    # Write output
    ww.writeframes(ns.tostring())

# Close files
wr.close()
ww.close()
