from Findy.commands import *

'''
тук трябва да направя инстанция на модема
да прочета ИМЕИ и Батт от модема
да прочета ИМЕ и ПАРОЛА от датабейса
да прочета данни за оператор и моб. клетка

'''
def command_action(command):
    global a
    a = Commands(command)
    r = a.recognition_name()
    return eval(r + ".return_result(a)")
    #return ModeQ.return_result(r)

def read_all_commands(command):
    while command:
        command = #read_command
