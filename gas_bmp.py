import RPi.GPIO as GPIO
import Adafruit_BMP.BMP085 as BMP085
import time
import requests

# --- Konfiguration ---
MQ2_SENSOR_PIN = 14  # GPIO-pin för den digitala utgången från MQ-2-sensorn
THINGSPEAK_API_KEY = "XXX"
THINGSPEAK_URL = "https://api.thingspeak.com/update"
INTERVAL = 15  # Minsta uppdateringsintervall (ThingSpeak tillåter 15 sekunder)

# Initiera GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(MQ2_SENSOR_PIN, GPIO.IN)  # Ställ in den digitala pinnen som input

# Initiera BMP180-sensor
sensor = BMP085.BMP085(busnum=1)

def read_mq2_sensor():
    # Läs det digitala värdet från MQ-2 sensorn
    return GPIO.input(MQ2_SENSOR_PIN) == GPIO.LOW  # Returnera True om gas upptäcks

def upload_to_thingspeak(pressure, gas_detected):
    try:
        payload = {
            'api_key': THINGSPEAK_API_KEY,
            'field1': pressure,
            'field2': int(gas_detected)  # Skicka 1 om gas upptäcks, annars 0
        }
        response = requests.get(THINGSPEAK_URL, params=payload)
        print(f"Data skickad: Lufttryck={pressure} Pa, Gas upptäckt={gas_detected}, Svar: {response.text}")
    except Exception as e:
        print(f"Fel vid uppladdning: {e}")

try:
    while True:
        # Läs sensordata
        gas_detected = read_mq2_sensor()
        pressure = sensor.read_pressure()  # Läs endast lufttrycket från BMP180-sensorn

        # Utskrift till terminalen
        print(f"Lufttryck: {pressure} Pa, Gas upptäckt: {gas_detected}")

        # Skicka data till ThingSpeak
        upload_to_thingspeak(pressure, gas_detected)

        time.sleep(INTERVAL)
except KeyboardInterrupt:
    print("Avslutar...")
    GPIO.cleanup()
