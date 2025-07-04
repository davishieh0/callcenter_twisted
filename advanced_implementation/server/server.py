import json
from twisted.internet import protocol, reactor
from logic import call_operator, answer_call, reject_call, hangup_call

commands_list = {
    "call": call_operator,
    "answer": answer_call,
    "reject": reject_call,
    "hangup": hangup_call
}

class CallcenterProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Client connected!")
        
    def dataReceived(self, data):
        print(f"Data received: {data.decode()}")
        try:
            json_data = json.loads(data.decode())
            command = json_data["command"]
            
            if command in commands_list:
                if command == "call":
                    status = commands_list[command](json_data["id"], self.transport)
                else:
                    status = commands_list[command](json_data["id"])
                
            else:
                status = "unknown_command"
        except json.JSONDecodeError:
            status = "invalid_json"
            
        self.transport.write(status.encode())
            
    def connectionLost(self, reason):
        print("Client disconnected!")
    
class CallcenterFactory(protocol.Factory):
    def buildProtocol(self, addr):
        print(f"New connection from: {addr}")
        return CallcenterProtocol()


print("CallCenter server running on port 5678...")
reactor.listenTCP(5678, CallcenterFactory())
reactor.run()