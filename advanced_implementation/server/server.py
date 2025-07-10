import json
from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver
from logic import call_operator, answer_call, reject_call, hangup_call

commands_list = {
    "call": call_operator,
    "answer": answer_call,
    "reject": reject_call,
    "hangup": hangup_call
}

class CallcenterProtocol(LineReceiver):
    delimiter = b'\n'
    def connectionMade(self):
        print("Client connected!")
        
    def lineReceived(self, line):
        print(f"Line received: {line.decode()}")
        try:
            json_data = json.loads(line.decode())
            command = json_data["command"]
            
            status = commands_list[command](json_data["id"], self)
            if status:
                self.sendLine(status.encode())
            else:
                self.sendLine(b"unknown_command")
                
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Invalid command format: {e}")
            self.sendLine(b"invalid_command_format")
                      
    def connectionLost(self, reason):
        print("Client disconnected!")
    
class CallcenterFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return CallcenterProtocol()


print("CallCenter server running on port 5678...")
reactor.listenTCP(5678, CallcenterFactory())
reactor.run()