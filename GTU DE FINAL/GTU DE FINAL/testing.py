import serial
import time
from gtts import gTTS
import pyaudio
import io
import speech_recognition as sr
import keyboard

# Define the serial port and baud rate
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to your Arduino's serial port

# Function to convert text to speech and play audio
def play_audio(text):
    try:
        # Create audio data in memory
        audio_data = io.BytesIO()
        tts = gTTS(text=text, lang='en')
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(format=p.get_format_from_width(2),
                        channels=1,
                        rate=22050,
                        output=True)

        # Read data
        data = audio_data.read(1024)

        # Play stream
        while data:
            stream.write(data)
            data = audio_data.read(1024)

        # Stop stream
        stream.stop_stream()
        stream.close()

        # Close PyAudio
        p.terminate()
    except Exception as e:
        print("Error playing audio:", e)

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
            print("Press 'O' to trigger audio playback.")
            keyboard.wait('O')
            print("Starting data collection...")
            play_audio("Starting data collection...")  # Provide feedback
            time.sleep(2)  # Give time for feedback audio to complete

            # Start collecting data from Arduino
            arduino_data = []
            for _ in range(10):  # Collect data for 10 seconds
                distances = get_distances_from_arduino()
                if distances:
                    arduino_data.append(distances)
                time.sleep(1)  # Collect data every second

            print("Data collection complete.")
            play_audio("Data collection complete.")  # Provide feedback

            # Analyze collected data to detect obstacle
            obstacle_detected = False
            for distances in arduino_data:
                obstacle_sensors = detect_obstacle(distances)
                if obstacle_sensors:
                    obstacle_info = ", ".join(obstacle_sensors)
                    print(f"Obstacle detected: {obstacle_info}")
                    play_audio(f"Obstacle detected at {obstacle_info}.")  # Provide feedback
                    obstacle_detected = True
                    break

            if not obstacle_detected:
                print("No obstacle detected.")
                play_audio("No obstacle detected.")  # Provide feedback

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
