from schemas import Operator
from twisted.internet import reactor
from collections import deque

operators = {
    "A": {"state": "available", "call_id": ""},
    "B": {"state": "available", "call_id": ""},
}
calls = {}
timeouts = {}
available_ops = {"A", "B"}
call_queue = deque()

def get_id_available_op():
  if not available_ops:
    return None
  return next(iter(available_ops))

def set_operator_available(operator_id):
    if operator_id in operators:
        operators[operator_id]["state"] = "available"   
        operators[operator_id]["call_id"] = ""
        
        available_ops.add(operator_id)
        print(f"Operator {operator_id} is now available.")

def set_operator_ringing(operator_id, call_id):
    if operator_id in operators and operator_id in available_ops:
        operators[operator_id]["state"] = "ringing"
        operators[operator_id]["call_id"] = call_id
        
        available_ops.remove(operator_id)
        print(f"Operator {operator_id} is now ringing for call {call_id}.")

def set_operator_busy(operator_id):
    if operator_id in operators:
        operators[operator_id]["state"] = "busy"
        print(f"Operator {operator_id} is now busy.")


def timeout(operator_id, call_id, protocol):
    if operators[operator_id]["state"] == "ringing":
      set_operator_available(operator_id)      
      status = update_call_queue(protocol)
      
    if protocol:
      message = f"Call {call_id} ignored by operator {operator_id}"
      protocol.sendLine(message.encode())
      
def update_call_queue(protocol=None):
  if call_queue:
    next_call_id = call_queue.popleft() # Removes head from queue
    status = call_operator(next_call_id, protocol)
    return status 
  
def call_operator(call_id,protocol=None):
  if not call_id:
    return f"Error: Call ID is required"
  
  id_op_available =  get_id_available_op()
  if id_op_available:
    set_operator_ringing(id_op_available,call_id)
    timeouts[id_op_available] = reactor.callLater(10, timeout, id_op_available, call_id, protocol)
    
    calls[call_id] = {"op_id": id_op_available} # Adding call with operator ID to calls dictionary 
    return f"Call {call_id} ringing for operator {id_op_available}"
      
  call_queue.append(call_id)
  return f"Call {call_id} waiting in queue"

def answer_call(operator_id,protocol=None):
  if not operator_id:
      return f"Error: Operator ID is required"
  
  if operators[operator_id]["state"] != "ringing":
    return f"Error: Operator {operator_id} has no ringing call to answer"
  
  if operator_id in timeouts:
      timeouts[operator_id].cancel()
      del timeouts[operator_id]
  set_operator_busy(operator_id)
  call_id = operators[operator_id]["call_id"]
  
  return f"Call {call_id} answered by operator {operator_id}"

def reject_call(operator_id,protocol=None):
  if not operator_id:
    return f"Error: Operator {operator_id} not found"
  if operators[operator_id]["state"] != "ringing":
    return f"Error: Operator {operator_id} has no call to reject"

  if operator_id in timeouts:
      timeouts[operator_id].cancel()
      del timeouts[operator_id]
    
  call_id = operators[operator_id]["call_id"]
  
  if call_id in calls:
      del calls[call_id]
    
  set_operator_available(operator_id)   
  call_queue.append(call_id)
  status = update_call_queue(protocol)
  
  message = f"Call {call_id} rejected by operator {operator_id}"
  if status:
        return f"{message}\n{status}"
  return message
    
def hangup_call(call_id,protocol=None):
  if call_id in call_queue:
    call_queue.remove(call_id)
    return f"Call {call_id} missed"
  
  if call_id in calls:
    op_id = calls[call_id]["op_id"]
    if operators[op_id]["state"] == "busy":
      set_operator_available(op_id)
      del calls[call_id]
      status = update_call_queue(protocol)
      message = f"Call {call_id} finished and operator {op_id} available"
      if status:
          return f"{message}\n{status}"
      return message
      
    if operators[op_id]["state"] == "ringing":
      set_operator_available(op_id)
      status = update_call_queue(protocol)
      message = f"Call {call_id} missed"
      if op_id in timeouts:
        timeouts[op_id].cancel()
        del timeouts[op_id]
        
      if status:
            return f"{message}\n{status}"
      return message 
  return f"Error: Call {call_id} not found or operator not busy"
