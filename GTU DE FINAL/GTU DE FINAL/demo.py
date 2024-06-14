import serial
import re

# Define the serial port and baud rate
# Change 'COM3' to your Arduino's serial port
ser = serial.Serial('COM3', 9600)

try:
    while True:
        # Read data from the serial port as bytes
        data = ser.readline().decode().strip()

        # Extract distance values using regular expressions
        distances = re.findall(r'Distance\d+: (\d+\.\d+)', data)

        # Assign each distance value to a separate variable
        Left_hand, right_hand, left_leg, right_leg, front_side, back_side = map(float, distances)

        # Here you can process the distances as needed

        # Optional: Add a delay to control the rate of data collection
        # time.sleep(0.1)

except KeyboardInterrupt:
    # Close the serial connection when the program is interrupted
    ser.close()
    print("Serial connection closed.")
