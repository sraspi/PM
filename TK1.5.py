import sys 
import time 
import datetime 
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np
import bme280
import bme280_77
import psutil

temperature1,pressure1,humidity1 = bme280.readBME280All()
temperature2,pressure2,humidity2 = bme280_77.readBME280All()


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
t_end = time.time()
t_start = time.time()
timeout = 0



timestr = time.strftime("%Y%m%d_%H%M%S")
t_end = time.time()
data = "/home/pi/PM/" + "TK_" + timestr+ ".txt"
f = open(data,  "w")
f.write("Datum/Zeit,         Temp1,          Temp2,          Druck1,         Druck2,           timeout[s],      cpu[%]" + '\n')
f.close()



### Prepare the plot

# Clean up and exit on matplotlib window close
def on_close(event):
    #print("Cleaning up...")
    GPIO.cleanup()
    #print("Bye :)")
    sys.exit(0)


plt.ion() # Interactive mode otherwise plot won't update in real time
fig = plt.figure(figsize=(7, 9))
fig.canvas.manager.set_window_title("TK 1.5")
#fig.canvas.manager.full_screen_toggle()
fig.canvas.mpl_connect("close_event", on_close) # Connect the plot window close event to function on_close
ax = fig.add_subplot(111)
ax2 = ax.twinx() # Get a second y axis

(A0_line,) = ax.plot(x, y, label="A0", color="#FFFF00") #00549F is the RWTH blue color
ax.set_ylabel("Temperatur [°C]", color="#CC071E")

(A1_line,) = ax.plot(x, y2, label="A1", color="#CC071E", linestyle="--") # #auf 2.y-Achse  CC071E is the RWTH red (both colors as defined in the official RWTH guide)
#ax.set_ylabel("counts", color="#000000") #auf 2.y-Achse 


(A2_line,) = ax2.plot(x, y3, label="A2", color="#00549F") #00FFFF
ax2.set_ylabel("Druck [mbar]", color="#00549F")

(A3_line,) = ax2.plot(x, y4, label="A3", color="#00FF00") #auf 2.y-Achse  00549F is the RWTH blue color
#ax2.set_ylabel("pressure [mbar]", color="#000000") #auf 2.y-Achse 

cpu = psutil.cpu_percent(1)
plt.title("BMP280  " + str(timestr) + "  Temp1: " + str(temperature1) + " Temp2 " +str(temperature2) + " Druck1:" + str(round(pressure1,0)) + " Druck2:" + str(round(pressure2,0)), fontsize=10) # To display 0 initially. Will be updated 
plt.xlabel("Zeit", color="#000000")

           

#Start = time.time()
try:
    while True :
        t_start = time.time()
        temperature1,pressure1,humidity1 = bme280.readBME280All()
        temperature2,pressure2,humidity2 = bme280_77.readBME280All()
        cpu = psutil.cpu_percent(1)
        timestr = time.strftime("%Y%m%d_%H%M%S")
        f = open(data,  "a")
        f.write(timestr + ",   " + str(A0) + ",       " + str(A1) + ",      " + str(A2) + ",    "   +  str(A3)  + ",    " + str(timeout) + ",    " + str(cpu) + '\n')
        f.close()
        
        if (timeout < 60):
            time.sleep(0.05)
            z = datetime.datetime.now()
            delta = z - x[-1]  # Last element in x is the timestamp of the last measurement!
            #A0 = adc.read_adc(0, 1)
            #A1 = round((adc.read_adc(1, 1)/2),0)
            #A2 = round((adc.read_adc(2, 1)/3),0)
            #A3 = round((adc.read_adc(2, 1)/4),0)
            A0 = temperature1
            A1 = temperature2
            A2 = pressure1
            A3 = pressure2
            x.append(z)
            y.append(A0)
            y2.append(A1)
            y3.append(A2)
            y4.append(A3)
            
            # ..update plot..
            time.sleep(0.05)
            plt.title("BMP280  " + str(timestr) + "  Temp1: " + str(temperature1) + " Temp2 " +str(temperature2) + " Druck1:" + str(round(pressure1,0)) + " Druck2:" + str(round(pressure2,0)), fontsize=10) 
            time.sleep(0.05)
            time.sleep(0.05)
            A0_line.set_xdata(x)
            time.sleep(0.05)
            A0_line.set_ydata(y)
            time.sleep(0.05)
            A1_line.set_xdata(x)
            time.sleep(0.05)
            A1_line.set_ydata(y2)
            time.sleep(0.05)
            A2_line.set_xdata(x)
            time.sleep(0.05)
            A2_line.set_ydata(y3)
            time.sleep(0.05)
            A3_line.set_xdata(x)
            time.sleep(0.05)
            A3_line.set_ydata(y4)
            
            
            time.sleep(0.05)
            ax.relim()  # Rescale data limit for first line
            time.sleep(0.05)
            ax.autoscale_view()  # Rescale view limit for first line
            #ax2.relim()  # Rescale data limit for second line
            #ax2.autoscale_view()  # Rescale view limit for second line
            time.sleep(0.05)
            ax.set_ylim(23, 28)

            time.sleep(0.05)
            plt.ylim(970,1030)
            time.sleep(0.05)
            #plt.xlabel("Zeit", fontsize=10, color="#000000")
            time.sleep(0.05)
            fig.canvas.draw()
            time.sleep(0.05)
            fig.canvas.flush_events()

            
            t_end = time.time()
            timeout = (t_end-t_start)
            #print(timeout)
            
        else:   
            timestr = time.strftime("%Y%m%d_%H%M%S")
            f = open(data,  "a")
            f.write(timestr + " error by diagramm "  + '\n')
            f.close()
            t_end = time.time()
        
        
               
        time.sleep(30)
           
            
            


except KeyboardInterrupt:
    print("keyboardInterrupt")
    GPIO.cleanup()
    print("\nBye")
    sys.exit()

