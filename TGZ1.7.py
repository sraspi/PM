import sys 
import time 
import datetime 
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import psutil




pin = 17  
count = 0
gas_volume = 0
r = 0
start = datetime.datetime.now()
x = [start]
y = [0]
y2 = [0]
V_diff = 0
V1 = 0
V2 = 0

GPIO.setmode(GPIO.BCM)  
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


timestr = time.strftime("%Y%m%d_%H%M%S")
data = "/home/pi/stta/" + "TGZ_" + timestr+ ".txt"
f = open(data,  "w")
f.write("Datum/Zeit,          Gasvolumen[L],        Gasdurchflussrate[L/min],       cpu[%]" + '\n')
f.close()


### Prepare the plot
# Clean up and exit on matplotlib window close
def on_close(event):
    f.close()  # Save file one last time
    print("Cleaning up...")
    GPIO.cleanup()
    print("Bye :)")
    sys.exit(0)


plt.ion() # Interactive mode otherwise plot won't update in real time
fig = plt.figure(figsize=(8, 6))
fig.canvas.manager.set_window_title("Trommelgaszaehler")
#fig.canvas.manager.full_screen_toggle()
fig.canvas.mpl_connect("close_event", on_close) # Connect the plot window close event to function on_close
ax = fig.add_subplot(111)
ax2 = ax.twinx() # Get a second y axis
(vol_line,) = ax.plot(x, y, label="Gasvolumen", color="#00549F") #00549F is the RWTH blue color
ax.set_ylabel("Gasvolumen in L", color="#00549F")
(rate_line,) = ax2.plot(x, y2, label="Gasdurchflussrate", color="#CC071E", linestyle="--") #CC071E is the RWTH red (both colors as defined in the official RWTH guide)
ax2.set_ylabel("Gasdurchflussrate in L/min", color="#CC071E")
# plt.ylim(0, 150) commented out because it overrides dynamic axes scaling
plt.title("Gasvolumen: " + str(gas_volume) + "L", fontsize=25) # To display 0ml initially. Will be updated in an event-driven manner (see on_trigger)
plt.xlabel("Zeit", fontsize=25)



def on_trigger(triggered_pin):
    global count
    count = count + 1
    
GPIO.add_event_detect(pin, GPIO.RISING, callback=on_trigger)

try:
    while True:
          
        z = datetime.datetime.now()
        delta = z - x[-1]  # Last element in x is the timestamp of the last measurement!
        # Put new values into their respective lists..        
        x.append(z)
        gas_volume = count*2.5/1000
        y.append(gas_volume)
        V2 = gas_volume
        V_diff = V2 - V1
        r = V_diff / delta.total_seconds()*60
        y2.append(r)
        
        plt.title("Gasvolumen: " + str(gas_volume) + "L", fontsize=25)#Diagrammtitel
        vol_line.set_xdata(x)
        vol_line.set_ydata(y)
        rate_line.set_xdata(x)
        rate_line.set_ydata(y2)
        ax.relim()  # Rescale data limit for first line
        ax.autoscale_view()  # Rescale view limit for first line
        ax2.relim()  # Rescale data limit for second line
        ax2.autoscale_view()  # Rescale view limit for second line

        fig.canvas.draw()
        fig.canvas.flush_events()
        
        cpu = psutil.cpu_percent(10)
        Zeit = time.strftime("%Y-%m-%d %H:%M:%S")
        f = open(data, "a")
        f.write(Zeit + ",       " + str(gas_volume) + ",                " + str(r) +  ",       " + str(cpu) + "\n")
        f.close()
        
        V1 = V2
        time.sleep(60)
        


except KeyboardInterrupt:
    print("keyboardInterrupt")
    timestr = time.strftime("%Y%m%d_%H%M%S")
    f = open(data, "a")
    f.write("KeyboardInterrupt at: " + timestr + "\n")
    f.close()
    GPIO.cleanup()
    print("\nBye")
    sys.exit()

