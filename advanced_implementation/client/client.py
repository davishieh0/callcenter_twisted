import json
from twisted.internet import reactor, protocol
import cmd

class CallcenterClient(protocol.Protocol):
    def connectionMade(self):
        print("Connection made")
        reactor.callInThread(self.start_cmd)

    def dataReceived(self,data):
        data = data.decode()
        print(f"\n{data}")
        print("(callCenter) ", end="", flush=True)

    
    def start_cmd(self):
            cmd_instance = CallCenter(self)
            self.cmd_instance = cmd_instance
            cmd_instance.cmdloop()
    
    
class CallcenterFactory(protocol.ClientFactory):
  def buildProtocol(self,addr):
    return CallcenterClient()

class CallCenter(cmd.Cmd):

  intro = 'Welcome'
  prompt = '(callCenter) '
  file = None

  def __init__(self, protocol_instance):
      super().__init__()
      self.protocol = protocol_instance
      
  def do_call(self, arg:str):   
      if not arg.isdigit():
          print("Error: Call ID must be a number. Usage: call <number>")
          return
      call_id = arg
      print(f"Call {call_id} received")
      json_data = json.dumps({"command": "call", "id": call_id})
      self.protocol.transport.write(json_data.encode("utf-8"))


  def do_answer(self, arg:str):
      if not arg.isalpha():
          print("Error: Operator ID must be letters only. Usage: answer <operator_id>")
          return
      operator_id = arg.upper()
      json_data = json.dumps({"command": "answer", "id": operator_id})
      self.protocol.transport.write(json_data.encode("utf-8"))


  def do_reject(self, arg):
      if not arg:
          print("Error: Operator ID is required. Usage: reject <operator_id>")
          return
      if not arg.isalpha():
          print("Error: Operator ID must be letters only. Usage: reject <operator_id>")
          return
      operator_id = arg.upper()
      json_data = json.dumps({"command": "reject", "id": operator_id})
      self.protocol.transport.write(json_data.encode("utf-8"))

          
  def do_hangup(self, arg):
      if not arg:
          print("Error: Call ID is required. Usage: hangup <call_id>")
          return
      if arg.isalpha():
          print("Error: Call ID must be numbers only. Usage: hangup <call_id>")
          return
      call_id = arg
      json_data = json.dumps({"command": "hangup", "id": call_id})
      self.protocol.transport.write(json_data.encode("utf-8"))

  def do_quit(self, arg):
    """Exit CallCenter client"""
    print("Exiting CallCenter...")
    if not self.protocol.transport.disconnecting:
        self.protocol.transport.loseConnection()

    if reactor.running:
        reactor.stop()
    return True  


  def do_exit(self, arg):
      """Exit CallCenter client"""
      return self.do_quit(arg)

  def do_EOF(self, arg):
      """Exit CallCenter client with Ctrl+D"""
      print("\nExiting CallCenter...")
      return self.do_quit(arg)

  def emptyline(self):
      pass


reactor.connectTCP("callcenter-server", 5678, CallcenterFactory())  # Em vez de "localhost"
reactor.run()reactor.run()

