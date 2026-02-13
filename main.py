from machine import Pin, I2C, time_pulse_us
from time import sleep, sleep_us
from ssd1306 import SSD1306_I2C

# Configuração do I2C para o display OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c)

# Configuração do sensor ultrassônico
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

# LEDs RGB (3 LEDs RGB) - pinos atualizados para evitar conflitos
r_pins = [Pin(2, Pin.OUT), Pin(15, Pin.OUT), Pin(19, Pin.OUT)]
g_pins = [Pin(4, Pin.OUT), Pin(16, Pin.OUT), Pin(17, Pin.OUT)]
b_pins = [Pin(13, Pin.OUT), Pin(14, Pin.OUT), Pin(27, Pin.OUT)]

# Lista de cores (R, G, B)
cores = [
    (1, 0, 0),  # Vermelho
    (0, 1, 0),  # Verde
    (0, 0, 1),  # Azul
    (1, 1, 0),  # Amarelo
    (1, 0, 1),  # Magenta
    (0, 1, 1),  # Ciano
    (1, 1, 1),  # Branco
    (0, 0, 0)   # Desligado
]

def medir_distancia_cm():
    trig.value(0)
    sleep_us(2)
    trig.value(1)
    sleep_us(10)
    trig.value(0)
    duracao = time_pulse_us(echo, 1, 30000)
    distancia = (duracao / 2) / 29.1  # Fórmula para cm
    return distancia

def aplicar_cor(r_val, g_val, b_val):
    for i in range(3):
        r_pins[i].value(r_val)
        g_pins[i].value(g_val)
        b_pins[i].value(b_val)

msg_bemvindo = True

while True:
    try:
        dist = medir_distancia_cm()
        print("Distância: {:.1f} cm".format(dist))

        if dist < 30:
            if msg_bemvindo:
                oled.fill(0)
                oled.text("Bem-vindo!", 10, 20)
                oled.show()
                msg_bemvindo = False
            for cor in cores:
                aplicar_cor(*cor)
                sleep(0.5)
        else:
            aplicar_cor(0, 0, 0)
            if not msg_bemvindo:
                oled.fill(0)
                oled.text("Volte sempre!", 0, 20)
                oled.show()
                msg_bemvindo = True

    except Exception as e:
        print("Erro:", e)
        aplicar_cor(0, 0, 0)
        oled.fill(0)
        oled.text("Erro no sensor", 0, 20)
        oled.show()

    sleep(0.2)
