from schemas import Operator, Call

operators = [
    Operator("A"),
    Operator("B")
]
call_queue = []
calls = []

def update_call_queue():
  if call_queue:
    next_call_id = call_queue.pop(0)
    status = call_operator(next_call_id)
    return status

def find_call_by_id(call_id):
  for call in calls:
    if call.id == call_id:
      return call
    
def call_operator(call_id):
  if not call_id:
    return f"Error: Call ID is required"
    
  call_obj = find_call_by_id(call_id)
  if not call_obj:
    # Criar novo objeto Call se não existir
    call_obj = Call(call_id, [])
    calls.append(call_obj)
    
  for operator in operators:
    if operator.state == "available" and operator.id not in call_obj.operators_recused:
        operator.state = "ringing"        
        operator.call_id = call_obj.id
        return f"Call {operator.call_id} ringing for operator {operator.id}"
        
  if len(call_obj.operators_recused) != 2:
    call_queue.append(call_obj.id)
    return f"Call {call_obj.id} waiting in queue"
  else:
    return f"Call {call_obj.id} missed"

def answer_call(operator_id):
  if not operator_id:
      return f"Error: Operator ID is required"
      
  for operator in operators:
      if operator.id == operator_id:
          if operator.state != "ringing":
              return f"Error: Operator {operator_id} has no ringing call to answer"
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

      for call_obj in calls:
        if call_obj.id == call_id:
          call_obj.operators_recused.append(operator.id) 
      return f"Call {call_id} rejected by operator {operator_id}"
        
  return f"Error: Operator {operator_id} not found"

def hangup_call(call_id):
  for operator in operators:
    if operator.call_id == call_id and operator.state == "busy":
        operator.state = "available"
        operator.call_id = ""
        return f"Call {call_id} finished and operator {operator.id} available"

  return f"Error: Call {call_id} not found or operator not busy"
