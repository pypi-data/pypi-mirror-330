This is the basic library for xkit.

### History
- V0.5.0
  - Supports InetCAN
  - Improved UDPServer local address allocation method 
- V0.3.0
  - wrapper SLIP
  - Supports UDP and multicast
  - Supports ANSI Escape Codes 

### Install
```sh
pip install genlib
```

### ANSI Escape Codes
- Foreground color settings
  - ANSIEC.FG.\<BLACK | RED | GREEN | YELLOW | BLUE | MAGENTA | CYAN | WHITE>
  - ANSIEC.FG.\<BRIGHT_BLACK | BRIGHT_RED | BRIGHT_GREEN | BRIGHT_YELLOW | BRIGHT_BLUE | BRIGHT_MAGENTA | BRIGHT_CYAN | BRIGHT_WHITE>
  - ANSIEC.FG.rgb(r, g, b)
- Background color settings
  - ANSIEC.BG.\<BLACK | RED | GREEN | YELLOW | BLUE | MAGENTA | CYAN | WHITE>
  - ANSIEC.BG.\<BRIGHT_BLACK | BRIGHT_RED | BRIGHT_GREEN | BRIGHT_YELLOW | BRIGHT_BLUE | BRIGHT_MAGENTA | BRIGHT_CYAN | BRIGHT_WHITE>
  - ANSIEC.BG.rgb(r, g, b)
- Styles
  - ANSIEC.OP.\<RESET | BOLD | UNDER_LINE | REVERSE>
- Screen
  - ANSIEC.OP.\<CLEAR | CLEAR_LINE>
- Cursor Navigation
  - ANSIEC.OP.\<TOP>
  - ANSIEC.OP.\<up(n) | down(n) | right(n) | left(n) | next_line(n) | prev_line(n) | to(row, column)>

```python
from genlib.ansiec import ANSIEC
import time, sys, random

def loading(count):
    all_progress = [0] * count
    sys.stdout.write("\n" * count) 
    colors = [0] * count
    for i in range(count):
        colors[i] = ANSIEC.FG.rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
    while any(x < 100 for x in all_progress):
        time.sleep(0.01)
        unfinished = [(i, v) for (i, v) in enumerate(all_progress) if v < 100]
        index, _ = random.choice(unfinished)
        all_progress[index] += 1
        
        sys.stdout.write(ANSIEC.OP.left(27))
        sys.stdout.write(ANSIEC.OP.up(count))
        for i, progress in enumerate(all_progress): 
            sys.stdout.write(colors[i])
            width = progress // 4
            print(f"[{'#'* width}{' ' * (25 - width)}] {ANSIEC.OP.RESET}{width*4}%")
            sys.stdout.write(ANSIEC.OP.RESET)

def main():
    loading(4)

if __name__ == "__main__":
    main()    
```

### Serial Line Internet Protocol
```python
from genlib.slip import Slip

def test_encode_decode(slip):
    data = "0.9992676 0.02764893 0.02612305 0.0"
    packet_send = slip.encode(data)
    print(packet_send)
    packet_recv = slip.decode(packet_send)[0]
    print(packet_recv, packet_recv == data)

def test_stream_decode(slip):
    data = []
    data.append(b'\xc00.9992676 0.02764893 0.02612305 0.0\xc0')
    data.append(b'\xc00.99')
    data.append(b'92676 0.02764893 0.02612305 0.0\xc0')
    data.append(b'\xc00.9992676 ')
    data.append(b'0.02764893 0.02612305 0.0\xc0')
    data.append(b'\xc00.9992676 0.')
    data.append(b'02764893 0.02612305 0.0\xc0')
    data.append(b'\xc00.9992676 0.02764893 0.0')
    data.append(b'2612305 0.0\xc0')
    data.append(b'\xc00.9992676 0.02764893 0.02612305 0.0\xc0')
        
    for d in data:
        for packet in slip.decode(d):
            print(packet)

def main():
    slip = Slip()
    
    test_encode_decode(slip)
    test_stream_decode(slip)
    
if __name__ == "__main__":
    main()    
```

### Multicast

**Multicast recv**
```python
import copy
from genlib.ansiec import ANSIEC
from genlib.udp import MulticastReceiver
         

MAX_RECV_LINE = 15
recv_data_list = []

def on_async_chatting_recv(receiver, message):
    recv_data_list.append(copy.deepcopy(message))
    if len(recv_data_list) > MAX_RECV_LINE:
        recv_data_list.pop(0)

    for i, data in enumerate(recv_data_list[: min(len(recv_data_list), MAX_RECV_LINE)]):
        print(ANSIEC.OP.to(i+1,1) + ANSIEC.OP.CLEAR_LINE, end='')
        print(ANSIEC.OP.to(i+1,1) + ANSIEC.FG.BRIGHT_YELLOW + f">>> RECEIVE {data.remote}: {data.payload}")
    
    print(ANSIEC.OP.to(MAX_RECV_LINE, 1) + ANSIEC.FG.BRIGHT_BLUE)

def main():
    receiver = MulticastReceiver()
    print(ANSIEC.OP.CLEAR, end='')
    receiver.onRecv(on_async_chatting_recv, unpickling=True)
    receiver.loopStart()
    
    while True:
        try:
            data = input(f"{ANSIEC.OP.to(MAX_RECV_LINE+1, 1) + ANSIEC.FG.BRIGHT_BLUE + ANSIEC.OP.CLEAR_LINE}{receiver.remote}: ")
            if data:
                receiver.sendTo(data) #Multiple unicast
        except KeyboardInterrupt:
            break
    
    receiver.loopStop()

if __name__ == "__main__":
    main()
```

**Multicast send**
```python
import copy
from genlib.ansiec import ANSIEC
from genlib.udp import MulticastSender


MAX_RECV_LINE = 15
recv_data_list = []

def on_async_chatting_recv(sender, message): #Multiple Unicast
    recv_data_list.append(copy.deepcopy(message))
    if len(recv_data_list) > MAX_RECV_LINE:
        recv_data_list.pop(0)
    
    for i, data in enumerate(recv_data_list[: min(len(recv_data_list), MAX_RECV_LINE)]):
        print(ANSIEC.OP.to(i+1,1) + ANSIEC.OP.CLEAR_LINE, end='')
        print(ANSIEC.OP.to(i+1,1) + ANSIEC.FG.BRIGHT_RED + f">>> RECEIVE {data.remote}: {data.payload}")
    
    print(ANSIEC.OP.to(MAX_RECV_LINE, 1) + ANSIEC.FG.BRIGHT_BLUE)

def main():
    sender = MulticastSender() 
    print(ANSIEC.OP.CLEAR, end='')
    sender.onRecv(on_async_chatting_recv, unpickling=True)
    sender.loopStart()
    
    print(ANSIEC.OP.CLEAR, end='')

    while True:
        try:
            data = input(f"{ANSIEC.OP.to(MAX_RECV_LINE+1, 1) + ANSIEC.FG.BRIGHT_BLUE + ANSIEC.OP.CLEAR_LINE}{sender.group}: ")
            if data:
                sender.sendTo(data) #Only Multicast
        except KeyboardInterrupt:
            break
    
    sender.loopStop()
    
if __name__ == "__main__":
    main()
```


### InetCAN (Client)
> The ICANServer must be running on the device (SerBot2 etc)

```python
from genlib.ican import InetCAN

ican = InetCAN("127.0.0.1") # ICANServer address

def onUltrasonic(data):
    for pos, d in enumerate(data):
        print(f"{d: >3.0f}", flush=True)    

ican.setFilter(us.id)
ican.write(0x012, [0x07])

while True:
    id, data = ican.read()
    data = struct.unpack("hhh", struct.pack("BBBBBB", *data))
    print(id, data)
```