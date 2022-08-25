#%%
import scipy.signal as sig
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

def toHz(value):
    from numpy import pi
    return value/2/pi

f_cut = 1000
w_cut = 2*np.pi*f_cut

num_L1 = np.array([w_cut])
den_L1 = np.array([1., w_cut])
s_L1 = sig.lti(num_L1, den_L1)
w_L1, m_L1, P_L1 = sig.bode(s_L1)

num_H1 = np.array([1., 0.])
den_H1 = np.array([1., w_cut])
s_H1 = sig.lti(num_H1, den_H1)
w_H1, m_H1, P_H1 = sig.bode(s_H1)

plt.figure(figsize=(12,5))
plt.semilogx(toHz(w_L1), m_L1, lw=2, label='1st LPF')
plt.semilogx(toHz(w_H1), m_H1, lw=2, label='1st HPF')
plt.axvline(f_cut, color='k', lw=1)
plt.xlim(50, 15000)
plt.ylim(-25, 2)
plt.ylabel('Amplitude [dB]')
plt.xticks([100, 1000, 10000], ('','$f_{cut}$[Hz]',''), fontsize = 20)
plt.legend()
plt.grid()

plt.figure(figsize=(12,5))
plt.semilogx(toHz(w_L1), P_L1, lw=2, label='1st LPF')
plt.semilogx(toHz(w_H1), P_H1, lw=2, label='1st HPF')
plt.axvline(f_cut, color='k', lw=1)
plt.xlim(50, 15000)
plt.ylabel('Phase [degree]')
plt.legend()
plt.xticks([100, 1000, 10000], ('','$f_{cut}$[Hz]',''), fontsize = 20)
plt.grid()

plt.show()


#%%
# Create Test Signal
Fs = 10*10**3               # 10kHz
Ts = 1/Fs                   # sample Time
endTime = 1
t = np.arange(0.0, endTime, Ts)

inputSig = 3.*np.sin(2.*np.pi*t)

sampleFreq = np.arange(10,500,50)

for freq in sampleFreq:
    inputSig = inputSig + 2*np.sin(2*np.pi*freq*t)
    
plt.figure(figsize=(12,5))
plt.plot(t, inputSig)
plt.xlabel('Time(s)')
plt.title('Test Signal in Continuous')
plt.grid(True)
plt.show()

