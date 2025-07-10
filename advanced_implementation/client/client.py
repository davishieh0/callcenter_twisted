import json
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
import cmd
from twisted.internet import stdio

# ALTERADO: O protocolo do cliente agora usa LineReceiver para enviar linhas completas.
class CallcenterClient(LineReceiver):
    delimiter = b'\n' # Define que as mensagens são separadas por nova linha.

    def connectionMade(self):
        print("Conectado ao servidor. Digite 'help' para ver os comandos.")
        # A linha mais importante: dá ao "cérebro" (cmd_instance) o contato do "mensageiro" (self).
        self.factory.cmd_instance.protocol = self
        # Exibe o prompt inicial.
        print(self.factory.cmd_instance.prompt, end="", flush=True)

    def lineReceived(self, line):
        # Recebe a resposta do servidor e a exibe.
        print(f"\n<-- Servidor: {line.decode()}")
        # Redesenha o prompt para o próximo comando.
        print(self.factory.cmd_instance.prompt, end="", flush=True)

    def connectionLost(self, reason):
        print("\nConexão perdida com o servidor.")
        if reactor.running:
            reactor.stop()

class CallCenterFactory(protocol.ClientFactory):
    def __init__(self, cmd_instance):
        self.cmd_instance = cmd_instance
    
    def buildProtocol(self, addr):
        # A fábrica agora passa a si mesma para o protocolo, para que ele possa acessar cmd_instance.
        p = CallcenterClient()
        p.factory = self
        return p

    def clientConnectionFailed(self, connector, reason):
        print(f"Falha ao conectar: {reason.getErrorMessage()}")
        if reactor.running:
            reactor.stop()

class CallCenterCmd(cmd.Cmd):
    intro = 'Bem-vindo ao CallCenter. Conectando...'
    prompt = '(CallCenter) '
    protocol = None # O protocolo de rede será inserido aqui quando a conexão for feita.

    def __init__(self):
        super().__init__()

    def _send_command(self, command, **kwargs):
        if not self.protocol:
            print("Erro: Não conectado ao servidor.")
            return
        
        data_to_send = {"command": command}
        data_to_send.update(kwargs)
        
        json_data = json.dumps(data_to_send)
        # ALTERADO: Usa sendLine para enviar uma linha completa com o delimitador.
        self.protocol.sendLine(json_data.encode("utf-8"))

    def do_call(self, arg:str):   
        if not arg.isdigit():
            print("Error: Call ID must be a number. Usage: call <number>")
            return
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
        print("Saindo...")
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
  
# REMOVIDO: A classe TerminalLineReceiver não é mais necessária,
# o stdio pode se comunicar com a classe CallCenterCmd diretamente se ela herdar de LineReceiver,
# mas a abordagem atual de separar a lógica do terminal e da rede é mais clara.
# Usaremos o stdio para passar a entrada para o onecmd diretamente.

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
    
    # Conecta ao servidor na porta 5678.
    # No Docker, 'callcenter-server' é o nome do host. Fora do Docker, use 'localhost'.
    reactor.connectTCP('localhost', 5678, factory)

    # Conecta a entrada do terminal ao nosso processador de comandos.
    stdio.StandardIO(StdioProtocol(cmd_instance))

    reactor.run()