from subprocess import Popen, PIPE, STDOUT

CREATE_NO_WINDOW = 0x08000000

def stdin_write(p, towrite):
    p.stdin.write((towrite + '\n').encode())
    p.stdin.flush()

def stdout_read(p):
    p.stdout.flush()
    output = ""
    while True:
        output += p.stdout.read(1).decode(errors='ignore')
        if output.endswith("\n\n"):
            return output

def simulate_battle(team1=None, team2=None):
    p = Popen(['node', 'pokemon-showdown', 'simulate-battle'], cwd="battle/pokemon-showdown", stdout=PIPE, stdin=PIPE, stderr=PIPE, creationflags=CREATE_NO_WINDOW)

    stdin_write(p, '>start {"formatid":"gen6ag"}')

    if team1:
        stdin_write(p, '>player p1 {"name":"Alice","team":"' + team1 + '"}')
    else:
        stdin_write(p, '>player p1 {"name":"Alice"}')
    if team2:
        stdin_write(p, '>player p2 {"name":"Bob","team":"' + team2 + '"}')
    else:
        stdin_write(p, '>player p2 {"name":"Bob"}')
    
    print(stdout_read(p))
    print(stdout_read(p))
    print(stdout_read(p))
    p.terminate()

