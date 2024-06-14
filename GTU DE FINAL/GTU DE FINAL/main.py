import serial
import time

# Define the serial port and baud rate
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to your Arduino's serial port

# Open the serial connection
ser.open()

try:
    while True:
        # Read data from the serial port
        data = ser.readline().decode().strip()
        
        # Print the received data
        print("Received:", data)
        
        # Here you can process the data as needed, e.g., save it to a file
        
        # Optional: Add a delay to control the rate of data collection
        # time.sleep(0.1)
        
except KeyboardInterrupt:
    # Close the serial connection when the program is interrupted
    ser.close()
    print("Serial connection closed.")