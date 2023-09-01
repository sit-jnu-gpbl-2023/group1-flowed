def on_received_number(receivedNumber):
    global angle
    angle = 0
    if receivedNumber == 2 and rain < 40:
        basic.show_icon(IconNames.HEART)
        angle = 90
        servos.P1.set_angle(angle)
        ESP8266_IoT.send_get("192.168.0.73:8000", "/", "open")
    else:
        basic.show_icon(IconNames.SAD)
        angle = 0
        servos.P1.set_angle(angle)
        ESP8266_IoT.send_get("192.168.0.73:8000", "/", "close")
    if angle == 90:
        basic.show_icon(IconNames.DUCK)
        if Environment.sonarbit_distance(Environment.Distance_Unit.DISTANCE_UNIT_CM, DigitalPin.P14) < 3:
            music.play(music.tone_playable(988, music.beat(BeatFraction.HALF)),
                music.PlaybackMode.UNTIL_DONE)
            Environment.led_brightness(AnalogPin.P4, True)
    Environment.led_brightness(AnalogPin.P4, False)
    basic.show_icon(IconNames.SQUARE)
radio.on_received_number(on_received_number)

rain = 0
angle = 0
OLED.init(128, 64)
basic.clear_screen()
Environment.led_brightness(AnalogPin.P4, False)
radio.set_group(50)
ESP8266_IoT.init_wifi(SerialPin.P8, SerialPin.P12, BaudRate.BAUD_RATE115200)
ESP8266_IoT.connect_wifi("iptime", "")

def on_forever():
    global rain
    rain = Environment.read_water_level(AnalogPin.P2)
    OLED.clear()
    OLED.write_string("water level:")
    OLED.write_num_new_line(rain)
    # 手動で扉を開く
    while input.button_is_pressed(Button.A):
        servos.P1.set_angle(90)
    # 手動で扉を閉める
    while input.button_is_pressed(Button.B):
        servos.P1.set_angle(0)
    if rain < 40:
        radio.send_number(1)
    else:
        radio.send_number(0)
    basic.pause(1000)
basic.forever(on_forever)
