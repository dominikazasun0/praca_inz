import numpy as np
import adi
import matplotlib.pyplot as plt

sample_rate = 1e6 # Hz
center_freq = 915e6 # Hz
num_samps = 10000 # number of samples per call to rx()

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Config Tx
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -25 # Increase to increase tx power, valid range is -90 to 0 dB

# Config Rx
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 0.0 # dB, increase to increase the receive gain, but be careful not to saturate the ADC

# Create transmit waveform (QPSK, 16 samples per symbol)
N = 1 # number of samples to transmit at once
t = np.arange(N)/sample_rate
samples = 0.5*np.exp(2.0j*np.pi*1e3*t) # Simulate a sinusoid of 100 kHz, so it should show up at 915.1 MHz at the receiver
samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
# Start the transmitter
sdr.tx_cyclic_buffer = True # Enable cyclic buffers
sdr.tx(samples) # start transmitting

# Clear buffer just to be safe
for i in range (0, 10):
    raw_data = sdr.rx()

# Receive samples
rx_samples = sdr.rx()
while 1:
    print(rx_samples.real)

# Stop transmitting
#sdr.tx_destroy_buffer()

# Calculate power spectral density (frequency domain version of signal)
#psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2
#psd_dB = 10*np.log10(psd)
#f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))

# Plot time domain
#plt.figure(0)
#plt.plot(np.real(rx_samples[::100]))
#plt.plot(np.imag(rx_samples[::100]))
#plt.xlabel("Time")

# Plot freq domain
#plt.figure(1)
#plt.plot(f/1e6, psd_dB)
#plt.xlabel("Frequency [MHz]")
#plt.ylabel("PSD")
#plt.show()