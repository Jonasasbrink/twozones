import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import requests

# ThingSpeak API detaljer
api_key = "XXX"
channel_url = "https://api.thingspeak.com/update"

# DHT11 sensor inställningar
dht_sensor = adafruit_dht.DHT11(board.D4)  # GPIO 4 (PIN 7)

# Regnsensor inställningar
RAIN_PIN = 17  # GPIO 17 (PIN 11)

# Ställ in GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_PIN, GPIO.IN)

# Funktion för att läsa från DHT11
def read_dht11():
    try:
        temperature = dht_sensor.temperature
        return temperature
    except RuntimeError as e:
        print(f"Fel vid läsning av DHT11: {e}")
        return None

# Funktion för att läsa från regnsensorn
def read_rain_sensor():
    return 1 - GPIO.input(RAIN_PIN)  # 0 = Torrt, 1 = Regn upptäckt

# Skicka data till ThingSpeak och verifiera att den kom fram
def send_to_thingspeak(temperature, rain_status):
    payload = {
        "api_key": api_key,
        "field1": temperature,  # Temperatur
        "field2": rain_status   # Regnsensorstatus (0 = Torrt, 1 = Regn)
    }

    try:
        response = requests.post(channel_url, params=payload)
        if response.status_code == 200:
            if response.text.strip() == "0":
                print("Fel: ThingSpeak tog inte emot datan. Kontrollera API-nyc>
            else:
                print(f"Data skickad till ThingSpeak: Temp={temperature}°C, Rai>
        else:
            print(f"Fel vid sändning till ThingSpeak: HTTP {response.status_cod>
    except Exception as e:
        print(f"Fel vid HTTP-anrop: {e}")

# Huvudprogrammet
if __name__ == "__main__":
    try:
        while True:
            temperature = read_dht11()
            if temperature is not None:
                rain_status = read_rain_sensor()
                send_to_thingspeak(temperature, rain_status)

            # Väntar i 20 sekunder innan nästa uppdatering
            print("Väntar i 20 sekunder innan nästa uppdatering...")
            time.sleep(20)
    except KeyboardInterrupt:
        print("Programmet avbröts.")
    finally:
        GPIO.cleanup()  # Rensa upp GPIO-inställningar

