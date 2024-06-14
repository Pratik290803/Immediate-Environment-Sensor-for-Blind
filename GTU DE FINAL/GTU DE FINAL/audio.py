import serial
import time
from gtts import gTTS
import pygame
from io import BytesIO
import speech_recognition as sr

# Initialize pygame mixer
pygame.mixer.init()

# Define the serial port and baud rate
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to your Arduino's serial port

# Function to convert text to speech and play audio
def play_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_data = BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    pygame.mixer.music.load(audio_data)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Function to recognize voice command
def recognize_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print("User said:", command)
        return command
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

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
            # Recognize voice command to start collecting data
            command = recognize_command()
            if command and "start data collection" in command:
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
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    main()
