from commands import *


def command_action(command):
    global a
    a = Commands(command)
    r = a.recognition_name()
    return eval(r + ".return_result(a)")
    #return ModeQ.return_result(r)

def read_all_commands(command):
    while command:
        command = 5#read_command
