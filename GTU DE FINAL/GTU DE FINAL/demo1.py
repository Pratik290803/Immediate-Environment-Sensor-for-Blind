import serial
import re

# Define the serial port and baud rate
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to your Arduino's serial port

try:
    while True:
        # Read data from the serial port as bytes
        data = ser.readline().decode().strip()
        
        # Extract distance values using regular expressions
        distances = re.findall(r'Distance\d+: (\d+\.\d+)', data)
        
        # Print the extracted distance values
        print("Distances:", distances)
        
        # Here you can process the distance values as needed
        
        # Optional: Add a delay to control the rate of data collection
        # time.sleep(0.1)
        
except KeyboardInterrupt:
    # Close the serial connection when the program is interrupted
    ser.close()
    print("Serial connection closed.")