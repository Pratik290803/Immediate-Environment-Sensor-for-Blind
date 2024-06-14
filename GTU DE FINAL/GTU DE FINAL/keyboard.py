import serial
import time
import keyboard

# Define the serial port and baud rate
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to your Arduino's serial port

# Function to get distances from Arduino
def get_distances_from_arduino():
    try:
        data = ser.readline().decode().strip()
        distances = [float(distance.split(":")[1]) for distance in data.split("\t\t")]
        return distances
    except Exception as e:
        print("Error reading data from Arduino:", e)
        return None

# Function to determine which sensor detected the obstacle
def detect_obstacle(distances):
    obstacle_sensors = []
    sensor_names = ['left hand', 'right hand', 'left leg', 'right leg', 'front side', 'back side']
    for i, distance in enumerate(distances):
        if distance < 50:  # Adjust threshold as needed
            obstacle_sensors.append(sensor_names[i])
    return obstacle_sensors

# Main function
def main():
    try:
        while True:
            # Wait for the 'O' key press event
            print("Press 'O' to trigger data collection.")
            keyboard.wait('O')
            print("Starting data collection...")
            time.sleep(2)  # Simulate data collection process
            print("Data collection complete.")

            # Start collecting data from Arduino
            arduino_data = []
            for _ in range(10):  # Collect data for 10 seconds
                distances = get_distances_from_arduino()
                if distances:
                    arduino_data.append(distances)
                time.sleep(1)  # Collect data every second

            # Analyze collected data to detect obstacle
            obstacle_detected = False
            for distances in arduino_data:
                obstacle_sensors = detect_obstacle(distances)
                if obstacle_sensors:
                    obstacle_info = ", ".join(obstacle_sensors)
                    print(f"Obstacle detected: {obstacle_info}")
                    obstacle_detected = True
                    break

            if not obstacle_detected:
                print("No obstacle detected.")

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
