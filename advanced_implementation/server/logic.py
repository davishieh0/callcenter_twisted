from schemas import Operator
from twisted.internet import reactor

operators = [
    Operator("A"),
    Operator("B")
]
call_queue = []



def timeout(operator_id, call_id, transport=None):
  for operator in operators:
    if operator_id == operator.id and operator.state=="ringing" and operator.call_id == call_id:
      operator.state = "available"
      operator.call_id = ""
      
      status = update_call_queue()
      
      if transport:
        message = f"Call {call_id} ignored by operator {operator_id}"
        transport.write(message.encode())
        
        if status:
          transport.write(f"\n{status}".encode())
      
def update_call_queue():
  if call_queue:
    next_call_id = call_queue.pop(0)
    status = call_operator(next_call_id)
    return status
    
def call_operator(call_id,transport=None):
  if not call_id:
    return f"Error: Call ID is required"

  for operator in operators:
    if operator.state == "available":
        operator.state = "ringing"        
        operator.call_id = call_id
        print(operator.id)
        print(operator.state)
        timeout_var = reactor.callLater(10, timeout, operator.id, call_id, transport)
        return f"Call {operator.call_id} ringing for operator {operator.id}"
      
  call_queue.append(call_id)
  return f"Call {call_id} waiting in queue"

def answer_call(operator_id):
  if not operator_id:
      return f"Error: Operator ID is required"
      
  for operator in operators:
      if operator.id == operator_id:
          if operator.state != "ringing":
              return f"Error: Operator {operator_id} has no ringing call to answer"
          timeout_var.cancel()
          operator.state = "busy"
          return f"Call {operator.call_id} answered by operator {operator.id}"
  return f"Error: Operator {operator_id} not found"

def reject_call(operator_id):
  for operator in operators:
    if operator.id == operator_id:
      if operator.state != "ringing":
          return f"Error: Operator {operator_id} has no call to reject"

      call_id = operator.call_id         
      operator.state = "available"
      operator.call_id = ""         
      call_queue.append(call_id)
      status = update_call_queue()
      
      message = f"Call {call_id} rejected by operator {operator_id}"
      if status:
            return f"{message}\n{status}"
      return message
        
  return f"Error: Operator {operator_id} not found"

def hangup_call(call_id):
  if call_id in call_queue:
    call_queue.remove(call_id)
    return f"Call {call_id} missed"
  
  for operator in operators:
    if operator.call_id == call_id:
      if operator.state == "busy":
          operator.state = "available"
          operator.call_id = ""
          status = update_call_queue()
          message = f"Call {call_id} finished and operator {operator.id} available"
          if status:
              return f"{message}\n{status}"
          return message
        
      if operator.state == "ringing":
        operator.state = "available"
        operator.call_id = ""
        status = update_call_queue()
        message = f"Call {call_id} missed"
        if status:
          return f"{message}\n{status}"
        return message 
  return f"Error: Call {call_id} not found or operator not busy"
