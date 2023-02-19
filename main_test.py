import time 
import ctypes, os 
import max30100
import numpy as np

#Constants:
CLOCK_MONOTONIC_RAW = 4 # see <linux/time.h> here: https://github.com/torvalds/linux/blob/master/include/uapi/linux/time.h

#prepare ctype timespec structure of {long, long}
class timespec(ctypes.Structure):
    _fields_ =\
    [
        ('tv_sec', ctypes.c_long),
        ('tv_nsec', ctypes.c_long)
    ]

#Configure Python access to the clock_gettime C library, via ctypes:
#Documentation:
#-ctypes.CDLL: https://docs.python.org/3.2/library/ctypes.html
#-librt.so.1 with clock_gettime: https://docs.oracle.com/cd/E36784_01/html/E36873/librt-3lib.html #-
#-Linux clock_gettime(): http://linux.die.net/man/3/clock_gettime
librt = ctypes.CDLL('librt.so.1', use_errno=True)
clock_gettime = librt.clock_gettime
#specify input arguments and types to the C clock_gettime() function
# (int clock_ID, timespec* t)
clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]

def monotonic_time():
    "return a timestamp in seconds (sec)"
    t = timespec()
    #(Note that clock_gettime() returns 0 for success, or -1 for failure, in
    # which case errno is set appropriately)
    #-see here: http://linux.die.net/man/3/clock_gettime
    if clock_gettime(CLOCK_MONOTONIC_RAW , ctypes.pointer(t)) != 0:
        #if clock_gettime() returns an error
        errno_ = ctypes.get_errno()
        raise OSError(errno_, os.strerror(errno_))
    return t.tv_sec + t.tv_nsec*1e-9 #sec 

def micros():
    "return a timestamp in microseconds (us)"
    return monotonic_time()*1e6 #us 

def millis():
    "return a timestamp in milliseconds (ms)"
    return monotonic_time()*1e3 #ms 
    



t = time.time()

t_vec,ir_vec,red_vec = [],[],[]

start=millis()
now=millis()

mx30 = max30100.MAX30100()
mx30.enable_spo2()

while (now-start)<=9000:
    mx30.read_sensor()
    # The latest values are now available via .ir and .red
    print(str(mx30.ir)+":"+str( mx30.red))
    t=micros()
    now=millis()
    t_vec.append(t)
    ir_vec.append(mx30.ir)
    red_vec.append(mx30.red)

s1 = 0 # change this for different range of data
s2 = len(t_vec) # change this for ending range of data
t_vec = np.array(t_vec[s1:s2])
ir_vec = ir_vec[s1:s2]
red_vec = red_vec[s1:s2]

# sample rate and heart rate ranges
samp_rate = 1/np.mean(np.diff(t_vec)) # average sample rate for determining peaks
heart_rate_range = [0,250] # BPM
heart_rate_range_hz = np.divide(heart_rate_range,60.0)
max_time_bw_samps = 1/heart_rate_range_hz[1] # max seconds between beats
max_pts_bw_samps = max_time_bw_samps*samp_rate # max points between beats

## FFT and plotting frequency spectrum of data
f_vec = np.arange(0,int(len(t_vec)/2))*(samp_rate/(len(t_vec)))
f_vec = f_vec*60
fft_var = np.fft.fft(red_vec)
fft_var = np.append(np.abs(fft_var[0]),2.0*np.abs(fft_var[1:int(len(fft_var)/2)]),
                    np.abs(fft_var[int(len(fft_var)/2)]))

bpm_max_loc = np.argmin(np.abs(f_vec-heart_rate_range[1]))
f_step = 1
f_max_loc = np.argmax(fft_var[f_step:bpm_max_loc])+f_step
print('BPM: {0:2.1f}'.format(f_vec[f_max_loc]))