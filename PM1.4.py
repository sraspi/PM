import sys 
import time 
import datetime 
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np

from ADS1x15 import ADS1115
adc = ADS1115()

start = datetime.datetime.now()
x = [start]
y = [0]
y2 = [0]
y3 = [0]
y4 = [0]
A0 = 0
A1 = 0
A2 = 0
A3 = 0

timestr = time.strftime("%Y%m%d_%H%M%S")
data = "/home/pi/stta/" + "PM_" + timestr+ ".txt"
f = open(data,  "w")
f.write("Datum/Zeit,         A0,          A1,          A2,         A3" + '\n')
f.close()



### Prepare the plot

# Clean up and exit on matplotlib window close
def on_close(event):
    print("Cleaning up...")
    GPIO.cleanup()
    print("Bye :)")
    sys.exit(0)


plt.ion() # Interactive mode otherwise plot won't update in real time
fig = plt.figure(figsize=(15, 15))
fig.canvas.manager.set_window_title("Powermeter 1.4")
#fig.canvas.manager.full_screen_toggle()
fig.canvas.mpl_connect("close_event", on_close) # Connect the plot window close event to function on_close
ax = fig.add_subplot(111)
#ax2 = ax.twinx() # Get a second y axis

(A0_line,) = ax.plot(x, y, label="A0", color="#FFFF00") #00549F is the RWTH blue color
ax.set_ylabel("counts", color="000000")

(A1_line,) = ax.plot(x, y2, label="A1", color="#CC071E", linestyle="--") # #auf 2.y-Achse  CC071E is the RWTH red (both colors as defined in the official RWTH guide)
ax.set_ylabel("counts", color="#000000") #auf 2.y-Achse 


(A2_line,) = ax.plot(x, y3, label="A2", color="#00549F") #00FFFF
ax.set_ylabel("counts", color="#000000")

(A3_line,) = ax.plot(x, y4, label="A3", color="#00FF00") #auf 2.y-Achse  00549F is the RWTH blue color
ax.set_ylabel("counts", color="#000000") #auf 2.y-Achse 

# plt.ylim(0, 150) commented out because it overrides dynamic axes scaling
plt.title("ADS1115 " + " A0:" + str(A0) + "A1" +str(A1) + " A2:" + str(A2) + " A3:" + str(A3), fontsize=10) # To display 0 initially. Will be updated 
plt.xlabel("Zeit", color="#000000")

           

Start = time.time()
try:
    while True:     
       
        z = datetime.datetime.now()
        delta = z - x[-1]  # Last element in x is the timestamp of the last measurement!
        A0 = adc.read_adc(0, 1)
        A1 = round((adc.read_adc(1, 1)/2),0)
        A2 = round((adc.read_adc(2, 1)/3),0)
        A3 = round((adc.read_adc(2, 1)/4),0)
        x.append(z)
        y.append(A0)
        y2.append(A1)
        y3.append(A2)
        y4.append(A3)
        # ..update plot..
        plt.title("ADS1115 " + "    A0:" + str(A0) + "   A1:" +str(A1) + "     A2:" + str(A2) + "     A3:" + str(A3), fontsize=10)
        
        A0_line.set_xdata(x)
        A0_line.set_ydata(y)
        A1_line.set_xdata(x)
        A1_line.set_ydata(y2)
        A2_line.set_xdata(x)
        A2_line.set_ydata(y3)
        A3_line.set_xdata(x)
        A3_line.set_ydata(y4)
        ax.relim()  # Rescale data limit for first line
        ax.autoscale_view()  # Rescale view limit for first line
        #ax2.relim()  # Rescale data limit for second line
        #ax2.autoscale_view()  # Rescale view limit for second line
        plt.xlabel("Zeit", fontsize=10, color="#000000")
        fig.canvas.draw()
        fig.canvas.flush_events()

        
        timestr = time.strftime("%Y%m%d_%H%M%S")
        f = open(data,  "a")
        f.write(timestr + ",   " + str(A0) + ",       " + str(A1) + ",      " + str(A2) + ",    "   +  str(A3)  + '\n')
        f.close()
        time.sleep(0.999)
            
            


except KeyboardInterrupt:
    print("keyboardInterrupt")
    GPIO.cleanup()
    print("\nBye")
    sys.exit()

