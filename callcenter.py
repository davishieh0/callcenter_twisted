import cmd
# operador: tem um id e state
operators = [
        {"id": "A", "state": "available","call_id":""},
        {"id": "B", "state": "available","call_id":""}
    ]
    
call = [
        {"id": "A", "state": ""},
        {"id": "B", "state": ""}
    ]

def search_operator(call_id):
    # Validar se call_id foi fornecido
    if not call_id:
        return None
        
    for operator in operators:
        if operator["state"] == "available":
            return operator["id"]
    
    # Se não encontrou operador disponível
    print(f"Call {call_id} waiting in queue")
    return None

def redirect_call(id_operator, call_id):
    # Validar se os parâmetros foram fornecidos
    if not id_operator or not call_id:
        return False
        
    for operator in operators:
        if operator["id"] == id_operator:
            operator["state"] = "ringing"
            operator["call_id"] = call_id
            return True
    return False

def answer_call(operator_id):
    # Validar se operator_id foi fornecido
    if not operator_id:
        return print("Error: Operator ID is required")
        
    for operator in operators:
        if operator["id"] == operator_id:
            if operator["state"] != "ringing":
                return print(f"Error: Operator {operator_id} has no ringing call to answer")
            operator["state"] = "busy"
            return print(f"Call {operator['call_id']} answered by operator {operator_id}")
    
    # Se operador não foi encontrado
    return print(f"Error: Operator {operator_id} not found")

class CallCenter(cmd.Cmd):
 
    intro = 'Welcome'
    prompt = '(test)'
    file = None

    def do_call(self, arg:str):   
        if not arg.isdigit():
            print("Error: Call ID must be a number. Usage: call <number>")
            return()
        call_id = arg
        print(f"Call {call_id} received")
        available_operator_id = search_operator(call_id)
        if redirect_call(available_operator_id,call_id):
            print(f"Call {call_id} ringing for operator {available_operator_id}")

    def do_answer(self, arg:str):
        if not arg.isalpha():
            return(print("Error: Operator ID must be letters only. Usage: answer <operator_id>"))
        operator_id = arg.upper()
        answer_call(operator_id)

    def do_reject(self, arg):
        if not arg:
            print("Error: Operator ID is required. Usage: reject <operator_id>")
            return
        if not arg.isalpha():
            print("Error: Operator ID must be letters only. Usage: reject <operator_id>")
            return
            
        operator_id = arg.upper()
        for operator in operators:
            if operator["id"] == operator_id:
                if operator["state"] != "ringing":
                    print(f"Error: Operator {operator_id} has no call to reject")
                    return
                call_id = operator["call_id"]
                operator["state"] = "available"
                operator["call_id"] = ""
                print(f"Call {call_id} rejected by operator {operator_id}")
                return
        print(f"Error: Operator {operator_id} not found")
            
    def do_hangup(self, arg):
        if not arg:
            print("Error: Operator ID is required. Usage: hangup <operator_id>")
            return
        if not arg.isalpha():
            print("Error: Operator ID must be letters only. Usage: hangup <operator_id>")
            return
            
        operator_id = arg.upper()
        for operator in operators:
            if operator["id"] == operator_id:
                if operator["state"] != "busy":
                    print(f"Error: Operator {operator_id} has no active call to hangup")
                    return
                call_id = operator["call_id"]
                operator["state"] = "available"
                operator["call_id"] = ""
                print(f"Call {call_id} ended by operator {operator_id}")
                return
        print(f"Error: Operator {operator_id} not found")

    def do_show(self, arg:str):
        print(operators)

if __name__ == '__main__':
    CallCenter().cmdloop()

