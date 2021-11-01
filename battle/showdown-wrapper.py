import time
import os, signal
from subprocess import Popen, PIPE, STDOUT

CREATE_NO_WINDOW = 0x08000000

def stdin_write(p, towrite):
    p.stdin.write((towrite + '\n').encode())
    p.stdin.flush()

def stdout_read(p):
    while True:
        line = p.stdout.readline()
        print(line)
        if (line == b''):
            break;

def simulate_battle():
    p = Popen(['node', 'pokemon-showdown', 'simulate-battle'], cwd="pokemon-showdown", stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdin_write(p, '>start {"formatid":"gen7ou"}')
    stdin_write(p, '>player p1 {"name":"Alice"}')
    stdin_write(p, '>player p2 {"name":"Bob"}')
    stdout_read(p)
    p.kill()

simulate_battle()

