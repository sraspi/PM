import sys 
import time 
import datetime 
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import threading

start = datetime.datetime.now()
count = 0
gas_volume = 0
r = 0
x = [start]
y = [0]
y2 = [0]
V_start = 0
V_end = 0
V_diff = 0

timestr = time.strftime("%Y%m%d_%H%M%S")
data = "/home/pi/stta/" + "TGZ_" + timestr+ ".txt"
f = open(data,  "w")
f.write("Datum/Zeit,          Gasvolumen[L],        Gasdurchflussrate[L/min]" + '\n')
f.close()

Start = time.time()

def TGZ_sim1():
    while True:
        try:
            global count
            count = (count + 1)
            time.sleep(0.1)
       
        except KeyboardInterrupt:
            print("keyboardInterrupt")
            timestr = time.strftime("%Y%m%d_%H%M%S")
            f = open(data, "a")
            f.write("KeyboardInterrupt at: " + timestr + "\n")
            f.close()
            GPIO.cleanup()
            print("\nBye")
            sys.exit()
        

t = threading.Thread(target=TGZ_sim1)
t.start()

### Prepare the plot
# Clean up and exit on matplotlib window close
def on_close(event):
    f.close()  # Save file one last time
    print("Cleaning up...")
    GPIO.cleanup()
    print("Bye :)")
    sys.exit(0)


plt.ion() # Interactive mode otherwise plot won't update in real time
fig = plt.figure(figsize=(10, 10))
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
plt.xlabel("Vergangene Zeit seit Versuchstart", fontsize=25)



def on_trigger(triggered_pin):
    global gas_volume
    gas_volume = count * 2.5
    z = datetime.datetime.now()
    delta = z - x[-1]  # Last element in x is the timestamp of the last measurement!
    # Put new values into their respective lists..
    x.append(z)
    y.append(gas_volume)
    w.append(a)
    r = 2.5 / delta.total_seconds()
    y2.append(r)





    # ..update plot..
    while True:
        plt.title("Gasvolumen" + str(gas_volume) + "L", fontsize=25)
        vol_line.set_xdata(x)
        vol_line.set_ydata(y)
        rate_line.set_xdata(x)
        rate_line.set_ydata(y2)
        ax.relim()  # Rescale data limit for first line
        ax.autoscale_view()  # Rescale view limit for first line
        ax2.relim()  # Rescale data limit for second line
        ax2.autoscale_view()  # Rescale view limit for second line
           


try:
    while True:
            
        End = time.time()
        diff = (End - Start)/60  # Zeit in Stunden seit Versuchsstart
        time.sleep(0.01)
        
        
        if diff>0.1:
            
            z = datetime.datetime.now()
            delta = z - x[-1]  # Last element in x is the timestamp of the last measurement!
            # Put new values into their respective lists..
            gas_volume = count*2.5/1000
            V_end = gas_volume
            V_diff = V_end-V_start
            x.append(z)
            y.append(gas_volume)
            r = V_diff/delta.total_seconds()*60 #[L/min)
            print(r)
            y2.append(r)
            # ..update plot..
           
            f = open(data, "a")
            f.write(timestr + ",       " + str(gas_volume) + ",                " + str(r) + "\n")
            f.close()
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
            timestr = time.strftime("%Y%m%d_%H%M%S")         
            Start = time.time()
            V_start = gas_volume
            


except KeyboardInterrupt:
    print("keyboardInterrupt")
    timestr = time.strftime("%Y%m%d_%H%M%S")
    f = open(data, "a")
    f.write("KeyboardInterrupt at: " + timestr + "\n")
    f.close()
    GPIO.cleanup()
    print("\nBye")
    sys.exit()

