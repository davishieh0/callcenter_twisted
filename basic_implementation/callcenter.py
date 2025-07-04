import cmd
from logic import(
    call_operator,
    answer_call,
    list_call,
    reject_call,
    hangup_call,
    show) 

class CallCenter(cmd.Cmd):
 
    intro = 'Welcome'
    prompt = '(callCenter)'
    file = None

    def do_call(self, arg:str):   
        if not arg.isdigit():
            print("Error: Call ID must be a number. Usage: call <number>")
            return()
        call_id = arg
        print(f"Call {call_id} received")
        status = call_operator(call_id)
        print(status)
        list_call()

    def do_answer(self, arg:str):
        if not arg.isalpha():
            return(print("Error: Operator ID must be letters only. Usage: answer <operator_id>"))
        operator_id = arg.upper()
        status = answer_call(operator_id)
        print (status)

    def do_reject(self, arg):
        if not arg:
            print("Error: Operator ID is required. Usage: reject <operator_id>")
            return
        if not arg.isalpha():
            print("Error: Operator ID must be letters only. Usage: reject <operator_id>")
            return
        operator_id = arg.upper()
        status = reject_call(operator_id)
        print(status)
        
    def do_hangup(self, arg):
        if not arg:
            print("Error: Call ID is required. Usage: hangup <call_id>")
            return
        if arg.isalpha():
            print("Error: Call ID must be numbers only. Usage: hangup <call_id>")
            return
        call_id = arg
        status_hangup = hangup_call(call_id)
        print(status_hangup)
    def do_show(self, arg):
        show()
    def do_list(self,arg):
        list_call()
if __name__ == '__main__':
    CallCenter().cmdloop()

