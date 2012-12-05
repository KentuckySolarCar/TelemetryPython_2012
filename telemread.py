from time import sleep, ctime, time

#this code is poorly written, and no one should use
#it for anything
#John is a mad individual.
###################################################
# 
###################################################
def parse(line,voltage):
    ready = 0
    templist = []
    varid = ""
    value = 0
    
    line = line.replace(" ","")
    line = line.replace("\r","")
    templist = line.split(":")
    
    varid = templist[0]
    if len(templist) > 1:
        value = int(templist[1])
        if varid[0] == "V":
            voltage[ int(varid[2])-1 ] = value
        if varid[0] == "T":
            temperature[ int(varid[2]) ] = value
            
    return ready
####################################################

def csvwrite(voltage,t):
    outfile = open("BattVolts.csv","a")
    line = str(t)
    for i in range(0,global.batnum):
        line = line  + "," + str(voltage[i])
    print(line,file=outfile)
    outfile.close()
    
###################################################
global.batnum = 0
def main():
    #initialize serial communication
    ser = Serial()
    cin = input("COM port: ")
    if cin == "":
        ser.port = 'COM4'
    else:
        ser.port = cin
    cin = input("Baudrate: ")
    if cin == "":
        ser.port = '19200'
    else:
        ser.port = cin
    print(ser)
    ser.open()
    global.batnum = eval(input("Number of batteries: "))
    
    #vars
    flag = False
    line = ""
    voltage = []
    for i in range(0,global.batnum):
        voltage.append(0)
  
    #header to csv file
    outfile = open("BattVolts.csv","w")
    header = "Timestamp"
    for i in range(0,global.batnum):
        header = header  + ", V" + str(i)
    print(header,file=outfile)
    outfile.close()
    
    input("PRESS <Enter> TO BEGIN MONITORING")
    reftime = time()
    print("PRESS <CTRL> + C TO EXIT")
    
    while not flag:
        try:
            #read one character at a time from the serial port and build a line
            #once the line ends, parse the data and update the variables
            byte = ser.read()
            if len(byte) > 0:
                char = chr(byte[0])
                char = char.replace("\r","")
                if char == "\n":
                    #print(line)
                    if len(line) > 0:
                        ready = parse(line,voltage)
                    line = ""
                else:
                    line = line + char
            

            #Write to the CSV file whenever parse sees the highest bat number
            if(ready):
                print("Voltage logged on ",ctime(),voltage)
                csvwrite(voltage,time())
            
        except:
            flag = True

    ser.close()
    input("press <enter> to exit")
main()
