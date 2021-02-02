from microbit import *

bots = [0]
bot_states = [0]

def on_forever():
    def on_received_string(receivedString):
        if "connect-" in receivedString:
            bot_id = int(receivedString.split('connect-')[1])
            bots.push(bot_id)
            bot_states[bot_id] = 3 # connecting
            print(f'[microbot] new connection ({str(bot_id)})')

        if "pong-" in receivedString:
            bot_id = int(receivedString.split('pong-')[1])
            if bot_states[bot_id] == 4:
                bot_states[bot_id] = 2 # alive

    def kill_bots():
        basic.show_string("killing")
        for bot_iterator in range(1, len(bots)):
            bot_id = bots[bot_iterator]
            radio.send_string(f'kill-{str(bot_id)}')
            bot_states[bot_id] = 4 # waiting for response
    def print_pwn():
        basic.show_string("pwn'")
        for bot_iterator in range(1, len(bots)):
            bot_id = bots[bot_iterator]
            radio.send_string(f'pwn-{str(bot_id)}')
            bot_states[bot_id] = 4 # waiting for response
    for bot_iterator in range(1, len(bots)):
        bot_id = bots[bot_iterator]
        radio.send_string(f'ping-{str(bot_id)}')
        bot_states[bot_id] = 4 # waiting for response

    radio.on_received_string(on_received_string)
    input.on_button_pressed(Button.A, kill_bots)
    input.on_button_pressed(Button.B, print_pwn)

    basic.show_number(len(bots)-1)

radio.set_group(231) # running on group 231 / port 231
radio.set_transmit_power(7) # set high transmit power.
radio.set_transmit_serial_number(False) # don't leak serial number to bots :/
print('[microbot] initialized radio')
basic.forever(on_forever) # create thread
