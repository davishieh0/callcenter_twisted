
class Operator:
  
  def __init__(self, id,state="available",call_id=""):
    self.id = id
    self.state = state
    self.call_id = call_id
    
class Call:
  def __init__(self, id,recused_operators):
    self.id = id
    self.operators_recused = []
    