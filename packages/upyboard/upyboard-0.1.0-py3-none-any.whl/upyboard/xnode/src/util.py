import sys
import utime
import uos
import machine

from micropython import const


class ANSIEC:
    class FG:
        BLACK = "\u001b[30m"
        RED = "\u001b[31m"
        GREEN = "\u001b[32m"
        YELLOW = "\u001b[33m"
        BLUE = "\u001b[34m"
        MAGENTA = "\u001b[35m"
        CYAN = "\u001b[36m"
        WHITE = "\u001b[37m"
        BRIGHT_BLACK= "\u001b[30;1m"
        BRIGHT_RED = "\u001b[31;1m"
        BRIGHT_GREEN = "\u001b[32;1m"
        BRIGHT_YELLOW = "\u001b[33;1m"
        BRIGHT_BLUE = "\u001b[34;1m"
        BRIGHT_MAGENTA = "\u001b[35;1m"
        BRIGHT_CYAN = "\u001b[36;1m"
        BRIGHT_WHITE = "\u001b[37;1m"
                
        @classmethod
        def rgb(cls, r, g, b): return "\u001b[38;2;{};{};{}m".format(r, g, b)

    class BG:
        BLACK = "\u001b[40m"
        RED = "\u001b[41m"
        GREEN = "\u001b[42m"
        YELLOW = "\u001b[43m"
        BLUE = "\u001b[44m"
        MAGENTA = "\u001b[45m"
        CYAN = "\u001b[46m"
        WHITE = "\u001b[47m"
        BRIGHT_BLACK= "\u001b[40;1m"
        BRIGHT_RED = "\u001b[41;1m"
        BRIGHT_GREEN = "\u001b[42;1m"
        BRIGHT_YELLOW = "\u001b[43;1m"
        BRIGHT_BLUE = "\u001b[44;1m"
        BRIGHT_MAGENTA = "\u001b[45;1m"
        BRIGHT_CYAN = "\u001b[46;1m"
        BRIGHT_WHITE = "\u001b[47;1m"
                
        @classmethod
        def rgb(cls, r, g, b): return "\u001b[48;2;{};{};{}m".format(r, g, b)

    class OP:
        RESET = "\u001b[0m"
        BOLD = "\u001b[1m"
        UNDER_LINE = "\u001b[4m"
        REVERSE = "\u001b[7m"
        CLEAR = "\u001b[2J"
        CLEAR_LINE = "\u001b[2K"
        TOP = "\u001b[0;0H"

        @classmethod
        def up(cls, n):
            return "\u001b[{}A".format(n)

        @classmethod
        def down(cls, n):
            return "\u001b[{}B".format(n)

        @classmethod
        def right(cls, n):
            return "\u001b[{}C".format(n)

        @classmethod
        def left(cls, n):
            return "\u001b[{}D".format(n)
        
        @classmethod
        def next_line(cls, n):
            return "\u001b[{}E".format(n)

        @classmethod
        def prev_line(cls, n):
            return "\u001b[{}F".format(n)
                
        @classmethod
        def to(cls, row, colum):
            return "\u001b[{};{}H".format(row, colum)

def sqrt(x, epsilon=1e-10):
    guess = x / 2.0

    op_limit = 5
    while abs(guess * guess - x) > epsilon and op_limit:
        guess = (guess + x / guess) / 2.0
        op_limit -= 1

    return guess

def abs(x):
    return x if x >= 0 else -x

def rand(size=4):
    return int.from_bytes(uos.urandom(size), "big")

def map(x, min_i, max_i, min_o, max_o):
    return (x - min_i) * (max_o - min_o) / (max_i - min_i) + min_o

def intervalChecker(interval):
    current_tick = utime.ticks_us()   
    
    def check_interval():
        nonlocal current_tick
        
        if utime.ticks_diff(utime.ticks_us(), current_tick) >= interval * 1000:
            current_tick = utime.ticks_us()
            return True
        return False
    
    return check_interval

def WDT(timeout):
    return machine.WDT(0, timeout)

def i2cdetect(bus=1, decorated=True):
    i2c = machine.I2C(bus)
    devices = i2c.scan()

    if decorated:
        output = "     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f"
        for i in range(0, 8):
            output += ANSIEC.FG.YELLOW + "\n{:02x}:".format(i*16) + ANSIEC.OP.RESET
            for j in range(0, 16):
                address = i * 16 + j
                if address in devices:
                    output += " {:02x}".format(address)
                else:
                    output += " --"
    else:
        output = devices
    
    return output
    
class Uart:
    SLIP_END = const(0xC0)		# dec: 192
    SLIP_ESC = const(0xDB)		# dec: 219
    SLIP_ESC_END = const(0xDC)	# dec: 220
    SLIP_ESC_ESC = const(0xDD)	# dec: 221
    
    @classmethod
    def read(cls, size=1, **kwargs):
        slip = kwargs.get('slip', False)
        decoding = kwargs.get('decoding', True)
        
        if not slip:
            if size == 0:
                raise ValueError("size >= 1")
            data = sys.stdin.buffer.read(size)
        else:
            started = False
            skip= False
            data = b''
            while True:
                char = sys.stdin.buffer.read(1)
                if not skip:
                    if char == cls.SLIP_END:
                        if not started:
                            started = True
                        else:                                  
                            data.replace(cls.SLIP_ESC + cls.SLIP_ESC_END, cls.SLIP_END).replace(cls.SLIP_ESC + cls.SLIP_ESC_ESC, cls.SLIP_ESC)        
                            break
                    else:
                        if not started:
                            skip = True
                        else:
                            data += char
                else:
                    if char == cls.SLIP_END:
                        skip = False
        
        return data.decode() if decoding else data

    @classmethod
    def readline(cls, **kwargs):
        decoding = kwargs.get('decoding', True)
        
        data = b''
        while True:
            char = sys.stdin.buffer.read(1)
            if char == b'\r' or char == b'\n':
                break
            else:
                data += char
        return data.decode() if decoding else data
                        
    @classmethod 
    def write(cls, *data, **kwargs):
        end = kwargs.get('end', '\n')
        sep = kwargs.get('sep', ' ')
        slip = kwargs.get('slip', False)

        t_data = ''
        for d in data:
            t_data += str(d) + sep
        data = t_data
                
        if not slip:        
            data += end
            sys.stdout.buffer.write(data.encode())
        else:
            data = data.rstrip()
            data = bytes(data.encode())
            sys.stdout.buffer.write(cls.SLIP_END + data.replace(cls.SLIP_ESC, cls.SLIP_ESC + cls.SLIP_ESC_ESC).replace(cls.SLIP_END, cls.SLIP_ESC + cls.SLIP_ESC_END) + cls.SLIP_END)
