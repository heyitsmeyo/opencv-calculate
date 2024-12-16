import time
from sys import stdin
import uselect
from machine import Pin



buzzer = Pin(15 , Pin.OUT)
print("Waiting for data...")
while True:
    select_result = uselect.select([stdin], [], [], 0) 
    while select_result[0]:  
        input_character = stdin.read(1)  
        print(input_character, end=" ")  
        if input_character =="0" :
            buzzer.low()
        elif input_character =="1":
            buzzer.high()
            
        select_result = uselect.select([stdin], [], [], 0)  # Check again for more data

    time.sleep(0.1) 