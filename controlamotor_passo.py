import machine
from machine import Pin
from machine import Timer
from network import WLAN
from umqtt.simple import MQTTClient
from ujson import loads

# Configurações da rede Wi-Fi
WIFI_SSID = 'NOME_DA_REDE_WIFI'
WIFI_PASSWORD = 'SENHA_DA_REDE_WIFI'

# Configurações dos motores de passo
MOTOR1_STEP_PIN = 26
MOTOR1_DIR_PIN = 27
MOTOR2_STEP_PIN = 32
MOTOR2_DIR_PIN = 33
MOTOR3_STEP_PIN = 34
MOTOR3_DIR_PIN = 35
MOTOR4_STEP_PIN = 36
MOTOR4_DIR_PIN = 39

# Configuração do MQTT
MQTT_SERVER = 'IP_DO_SERVIDOR_MQTT'
MQTT_PORT = 1883
MQTT_TOPIC = 'COORDENADAS_TOPIC'

# Inicialização do Wi-Fi
wlan = WLAN(mode=WLAN.STA)
wlan.connect(ssid=WIFI_SSID, auth=(WIFI_SSID, WIFI_PASSWORD))
while not wlan.isconnected():
    machine.idle()

# Inicialização dos motores de passo
motor1 = machine.Pin(MOTOR1_STEP_PIN, mode=machine.Pin.OUT)
dir1 = machine.Pin(MOTOR1_DIR_PIN, mode=machine.Pin.OUT)
motor2 = machine.Pin(MOTOR2_STEP_PIN, mode=machine.Pin.OUT)
dir2 = machine.Pin(MOTOR2_DIR_PIN, mode=machine.Pin.OUT)
motor3 = machine.Pin(MOTOR3_STEP_PIN, mode=machine.Pin.OUT)
dir3 = machine.Pin(MOTOR3_DIR_PIN, mode=machine.Pin.OUT)
motor4 = machine.Pin(MOTOR4_STEP_PIN, mode=machine.Pin.OUT)
dir4 = machine.Pin(MOTOR4_DIR_PIN, mode=machine.Pin.OUT)

# Configuração dos timers para controlar os motores de passo
timer1 = Timer(0)
timer2 = Timer(1)
timer3 = Timer(2)
timer4 = Timer(3)

# Variáveis para armazenar as coordenadas
coord1 = 0
coord2 = 0
coord3 = 0
coord4 = 0

# Função de callback para processar as mensagens MQTT recebidas
def mqtt_callback(topic, msg):
    global coord1, coord2, coord3, coord4
    data = loads(msg)
    coord1 = data['motor1']
    coord2 = data['motor2']
    coord3 = data['motor3']
    coord4 = data['motor4']

# Configuração do cliente MQTT
mqtt_client = MQTTClient("ESP32", MQTT_SERVER, port=MQTT_PORT)
mqtt_client.set_callback(mqtt_callback)
mqtt_client.connect()
mqtt_client.subscribe(MQTT_TOPIC)

# Função para mover o motor de passo para uma coordenada específica
def move_motor(timer, step_pin, dir_pin, coord):
    if coord != 0:
        dir_pin.value(1 if coord > 0 else 0)
        for _ in range(abs(coord)):
            step_pin.value(1)
            machine.delay(1)
            step_pin.value(0)
            machine.delay(1)

# Função para atualizar os motores de passo
def update_motors(timer):
    move_motor(timer1, motor1, dir1, coord1)
    move_motor(timer2, motor2, dir2, coord2)
    move_motor(timer3, motor3, dir3, coord3)
    move_motor(timer4, motor4, dir4, coord4)

# Configuração dos timers para atualizar os motores a cada 5 minutos
timer1.init(period=5*60*1000, mode=Timer.PERIODIC, callback=update_motors)
timer2.init(period=5*60*1000, mode=Timer.PERIODIC, callback=update_motors)
timer3.init(period=5*60*1000, mode=Timer.PERIODIC, callback=update_motors)
timer4.init(period=5*60*1000, mode=Timer.PERIODIC, callback=update_motors)

# Loop principal para processar as mensagens MQTT
while True:
    mqtt_client.wait_msg()
