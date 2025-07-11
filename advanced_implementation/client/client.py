import json
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
import cmd
from twisted.internet import stdio

class CallcenterClient(LineReceiver):
    delimiter = b'\n' # Defines that messages are separated by newline.

    def connectionMade(self):
        print("Connected to server. Type 'help' to see commands.")
        # The most important line: gives the "brain" (cmd_instance) contact with the "messenger" (self).
        self.factory.cmd_instance.protocol = self
        # Shows the initial prompt.
        print(self.factory.cmd_instance.prompt, end="", flush=True)

    def lineReceived(self, line):
        # Receives response from server and displays it.
        print(f"{line.decode()}")
        # Redraws the prompt for the next command.
        print(self.factory.cmd_instance.prompt, end="", flush=True)

    def connectionLost(self, reason):
        print("\nConnection lost with server.")
        if reactor.running:
            reactor.stop()

class CallCenterFactory(protocol.ClientFactory):
    def __init__(self, cmd_instance):
        self.cmd_instance = cmd_instance
    
    def buildProtocol(self, addr):
        # The factory now passes itself to the protocol, so it can access cmd_instance.
        p = CallcenterClient()
        p.factory = self
        return p

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed: {reason.getErrorMessage()}")
        if reactor.running:
            reactor.stop()

class CallCenterCmd(cmd.Cmd):
    intro = 'Welcome to CallCenter. Connecting...'
    prompt = '(CallCenter) '
    protocol = None # Network protocol will be inserted here when connection is made.

    def __init__(self):
        super().__init__()

    def _send_command(self, command, **kwargs):
        if not self.protocol:
            print("Error: Not connected to server.")
            return
        
        data_to_send = {"command": command}
        data_to_send.update(kwargs)
        
        json_data = json.dumps(data_to_send)
        self.protocol.sendLine(json_data.encode("utf-8"))

    def do_call(self, arg:str):   
        if not arg.isdigit():
            print("Error: Call ID must be a number. Usage: call <number>")
            return
        print(f"call {arg} received")
        self._send_command("call", id=arg)

    def do_answer(self, arg:str):
        if not arg.isalpha():
            print("Error: Operator ID must be letters only. Usage: answer <operator_id>")
            return
        self._send_command("answer", id=arg.upper())

    def do_reject(self, arg):
        if not arg.isalpha():
            print("Error: Operator ID must be letters only. Usage: reject <operator_id>")
            return
        self._send_command("reject", id=arg.upper())

    def do_hangup(self, arg):
        if not arg.isdigit():
            print("Error: Call ID must be numbers only. Usage: hangup <call_id>")
            return
        self._send_command("hangup", id=arg)

    def do_quit(self, arg):
        """Exit CallCenter client"""
        print("Exiting...")
        if self.protocol:
            self.protocol.transport.loseConnection()
        else:
            if reactor.running:
                reactor.stop()
        return True  

    def do_exit(self, arg):
        """Exit CallCenter client"""
        return self.do_quit(arg)

    def do_EOF(self, arg):
        """Exit CallCenter client with Ctrl+D"""
        print()
        return self.do_quit(arg)

    def emptyline(self):
        pass
  

class StdioProtocol(protocol.Protocol):
    def __init__(self, cmd_instance):
        self.cmd = cmd_instance

    def dataReceived(self, data):
        cmd_line = data.decode().strip()
        if self.cmd.onecmd(cmd_line):
            if reactor.running:
                reactor.stop()

if __name__ == "__main__":
    cmd_instance = CallCenterCmd()
    factory = CallCenterFactory(cmd_instance)
    
    # Connects to server on port 5678.
    # In Docker, 'callcenter-server' is the hostname. Outside Docker, use 'localhost'.
    reactor.connectTCP('callcenter-server', 5678, factory)

    # Connects terminal input to our command processor.
    stdio.StandardIO(StdioProtocol(cmd_instance))

    reactor.run()