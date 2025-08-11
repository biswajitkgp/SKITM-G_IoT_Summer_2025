# ------------------- LIBRARIES -------------------
from machine import Pin, ADC, I2C
from time import sleep, time
import dht
import network
import urequests
import ujson
import gc # Garbage Collection library

# Import the I2C LCD library (must be in the /lib folder)
from i2c_lcd import I2cLcd

# ------------------- CONFIGURATION -------------------
# --- WiFi Details ---
WIFI_SSID = "Airtel_Ellipse Nelvana"
WIFI_PASSWORD = "hare_krishna"

# --- Google AI Studio API ---
# This is the key from your original script.
API_KEY = "AIzaSyB0kX6Wd9i_maDHaswqwa4QNlsDzj_aOAY"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# --- Hardware Pin Assignments ---
DHT_PIN = 14
LDR_PIN = 34
BUTTON_PIN = 16
I2C_SDA_PIN = 21
I2C_SCL_PIN = 22
LED_R_PIN = 17
LED_G_PIN = 18
LED_B_PIN = 5
BUZZER_PIN = 15

# --- LCD I2C Configuration ---
I2C_ADDR = 0x27 
LCD_NUM_ROWS = 4
LCD_NUM_COLS = 20

# --- Data Collection ---
DATA_HISTORY_SIZE = 100

# ------------------- GLOBAL VARIABLES -------------------
forecast_request_pending = False
sensor_data_history = []
last_temp = 0.0
last_hum = 0.0
## CHANGE: Added a variable to track the time of the last interrupt for debouncing.
last_interrupt_time = 0

# ------------------- HARDWARE INITIALIZATION -------------------
dht_sensor = dht.DHT22(Pin(DHT_PIN))
ldr = ADC(Pin(LDR_PIN))
ldr.atten(ADC.ATTN_11DB)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
led_r = Pin(LED_R_PIN, Pin.OUT)
led_g = Pin(LED_G_PIN, Pin.OUT)
led_b = Pin(LED_B_PIN, Pin.OUT)
buzzer = Pin(BUZZER_PIN, Pin.OUT)
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, LCD_NUM_ROWS, LCD_NUM_COLS)

# ------------------- HELPER FUNCTIONS -------------------

def set_led_color(r, g, b):
    """Control the RGB LED. 1 for ON, 0 for OFF."""
    led_r.value(r); led_g.value(g); led_b.value(b)

def short_beep(duration_ms=50):
    """Make a short beep sound."""
    buzzer.on(); sleep(duration_ms / 1000); buzzer.off()
    
def display_wrapped_text(text, start_line=1):
    """
    Displays word-wrapped text on the LCD. Handles long messages by splitting
    them into pages and showing them sequentially.
    """
    words = text.split(' ')
    all_lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > LCD_NUM_COLS:
            all_lines.append(current_line)
            current_line = word + " "
        else:
            current_line += word + " "
    all_lines.append(current_line)

    lines_per_page = LCD_NUM_ROWS - start_line
    num_pages = (len(all_lines) + lines_per_page - 1) // lines_per_page

    try:
        for page in range(num_pages):
            for i in range(start_line, LCD_NUM_ROWS):
                lcd.move_to(0, i)
                lcd.putstr(" " * LCD_NUM_COLS)
            
            start_index = page * lines_per_page
            end_index = start_index + lines_per_page
            page_lines = all_lines[start_index:end_index]

            for i, line in enumerate(page_lines):
                lcd.move_to(0, start_line + i)
                lcd.putstr(line)
            
            if num_pages > 1:
                sleep(4)
    except OSError as e:
        print(f"Error writing wrapped text to LCD: {e}")


def connect_wifi():
    """Connects the ESP32 to the WiFi network and provides feedback."""
    lcd.clear(); lcd.putstr("Connecting to WiFi")
    set_led_color(1, 1, 0)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        for _ in range(15):
            if wlan.isconnected(): break
            sleep(1)
    if wlan.isconnected():
        print(f"WiFi Connected. IP: {wlan.ifconfig()[0]}")
        lcd.clear(); lcd.putstr("WiFi Connected!")
        set_led_color(0, 0, 1); short_beep(); sleep(2)
        return True
    else:
        print("WiFi connection failed.")
        lcd.clear(); lcd.putstr("WiFi Failed!"); set_led_color(1, 0, 0)
        return False

def get_weather_forecast():
    """Manages the full process of getting a forecast from the AI."""
    set_led_color(0, 0, 1); lcd.clear(); lcd.putstr("Fetching Forecast...")
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected(): return "WiFi Disconnected"
    
    gc.collect()
    
    data_string = ", ".join([f"({t},{h},{l})" for t, h, l in sensor_data_history])
    prompt = (
        "You are a weather forecaster. Based on this data "
        f"(Temp C, Hum %, Light 0-4095): {data_string}. "
        "Give a very short forecast (max 12 words) for the next 1-3 hours. No markdown or asterisks."
    )
    headers = {'Content-Type': 'application/json', 'X-goog-api-key': API_KEY}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = None
    try:
        response = urequests.post(API_URL, headers=headers, data=ujson.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            forecast = result['candidates'][0]['content']['parts'][0]['text']
            set_led_color(0, 1, 0); short_beep(100)
            return forecast.strip().replace('\n', ' ').replace('*', '')
        else:
            set_led_color(1, 0, 0)
            return f"API Error {response.status_code}"
    except Exception as e:
        print(f"Error during API call: {e}")
        set_led_color(1, 0, 0)
        return "Network/Mem Error"
    finally:
        if response: response.close()
        gc.collect()

## CHANGE: Added a time-based check to debounce the interrupt.
def button_interrupt_handler(pin):
    """Interrupt service routine with debouncing to prevent false triggers."""
    global forecast_request_pending, last_interrupt_time
    current_time = time()
    # Ignore interrupt if it's too close to the last one (500ms debounce)
    if (current_time - last_interrupt_time) > 0.5:
        forecast_request_pending = True
        last_interrupt_time = current_time

# ------------------- MAIN PROGRAM -------------------

# 1. Initial Setup
set_led_color(0, 0, 0); buzzer.off()
lcd.clear(); lcd.putstr("Weather Station"); lcd.move_to(0, 1); lcd.putstr("Booting Up..."); sleep(2)

# 2. Connect to WiFi
if not connect_wifi():
    while True: set_led_color(1, 0, 0); sleep(0.5); set_led_color(0, 0, 0); sleep(0.5)

# 3. Attach Interrupt and Display Ready Message
button.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt_handler)
lcd.clear(); lcd.putstr("System Ready."); sleep(2)

print("Starting main loop...")
# 4. Main Loop
while True:
    # --- Read the DHT22 Sensor ---
    read_success = False
    for i in range(3):
        try:
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            hum = dht_sensor.humidity()
            read_success = True
            break
        except OSError:
            sleep(0.5)
    
    if not read_success:
        print("Warning: Using last known sensor values.")
        temp, hum = last_temp, last_hum
        set_led_color(1, 1, 0)
    else:
        last_temp, last_hum = temp, hum
        set_led_color(0, 1, 0)

    # --- Read the LDR sensor ---
    light = ldr.read()

    # --- Check for AI Forecast Request ---
    if forecast_request_pending:
        forecast_request_pending = False
        short_beep()
        if len(sensor_data_history) < 10:
            display_wrapped_text("Not enough data yet. Please wait.", 1)
            sleep(3)
        else:
            forecast_text = get_weather_forecast()
            lcd.clear(); lcd.putstr("AI Forecast:")
            display_wrapped_text(forecast_text, 1)
        lcd.clear()

    # --- Store Data for AI and Display Live Values ---
    if read_success:
        sensor_data_history.append((temp, hum, light))
        if len(sensor_data_history) > DATA_HISTORY_SIZE:
            sensor_data_history.pop(0)

    try:
        if not forecast_request_pending:
            lcd.move_to(0, 0); lcd.putstr(f"Temp: {temp:.1f}C/{temp * 1.8 + 32:.1f}F")
            lcd.move_to(0, 1); lcd.putstr(f"Humidity: {hum:.1f}%      ")
            lcd.move_to(0, 2); lcd.putstr(f"Light: {light}         ")
            lcd.move_to(0, 3); lcd.putstr("Press button for AI ")
    except OSError as e:
        print(f"LCD Update Failed: {e}. Check I2C connection.")

    # Loop delay for 1-second interval
    sleep(1)
