
import time 

timeout = time.time() + 5
while time.time() < timeout :
    percentage = str((time.time() / timeout))[9:11]

    print(percentage)