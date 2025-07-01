from schemas import Operator

# Lista global de operadores
operators = [
    Operator("A"),
    Operator("B")
]

def call_operator(call_id):
  if not call_id:
    return f"Error: Call ID is required"
  for operator in operators:
    if operator.state == "available":
        operator.state = "ringing"
        operator.call_id = call_id
        return f"Call {operator.call_id} ringing for operator {operator.id}"
      
  return f"Call {call_id} waiting in queue"
  
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
      if operator.state!= "ringing":
          return f"Error: Operator {operator_id} has no call to reject"
          
      call_id = operator.call_id
      operator.state = "available"
      operator.call_id = ""
      return f"Call {call_id} rejected by operator {operator_id}"
        
    return f"Error: Operator {operator_id} not found"

def hangup_call(call_id):
  for operator in operators:
    if operator.call_id == call_id and operator.state == "busy":
        operator.state = "available"
        operator.call_id = ""
        return f"Call {call_id} finished and operator {operator.id} available"

  return (
      f"Error: Call {call_id} not found or operator not busy\n"
      f"Error: Call {call_id} not found or operator not busy"
  )
