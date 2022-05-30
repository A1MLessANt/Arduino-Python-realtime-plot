import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import serial


#initialize serial port
ser = serial.Serial()
# ser.port = '/dev/ttyACM0' #Arduino serial port
ser.port = 'COM14'
ser.baudrate = 9600
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n") #print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] #store trials here (n)
ys = [] #store relative frequency here
rs = [] #for theoretical probability

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    
    line=ser.readline() .decode('ascii')  
    line_split= line.split(",")
    volt = float(line_split[0])
    distance = float(line_split[1])
    time_ms = int(line_split[2])
    time = time_ms/1000
    
    #saving data in a text string for textbox visualization
    textstr = '\n'.join((
    r'$\mathrm{Volt}=%.2f$' % (volt, ),
    r'$\mathrm{Dist}=%.2f$' % (distance, ),
    r'$\mathrm{Time}=%.2f$' % (time, )))
    
    
	# Add x and y to lists
    xs.append(time)
    ys.append(volt)
    rs.append(distance)

    # Limit x and y lists to 20 items
    #xs = xs[-20:]
    #ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label="Volt")
    ax.plot(xs, rs, label="Distance in mm")
    
    #style and positions of textbox
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.title('Realtime Plotting of Feedback Control System')
    #plt.ylabel('Relative frequency')
    plt.xlabel('Time(s)')
    plt.legend()
    plt.axis([1, None, -0.5, 15]) #Use for arbitrary number of trials
    #plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
