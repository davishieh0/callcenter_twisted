import cmd


class CallCenterCmd(cmd.Cmd):
    intro = 'Welcome to CallCenter'
    prompt = '(CallCenter) '
    network_protocol = None
  
        
    def do_call(self, arg):   
        if not arg or not arg.isdigit():
            print("Error: Call ID must be a number. Usage: call <number>")
            return
        print(f"Call {arg} received")

    def do_answer(self, arg):
        if not arg or not arg.isalpha():
            print("Error: Operator ID must be letters only. Usage: answer <operator_id>")
            return

    def do_reject(self, arg):
        if not arg or not arg.isalpha():
            print("Error: Operator ID must be letters only. Usage: reject <operator_id>")
            return
          
    def do_hangup(self, arg):
        if not arg or not arg.isdigit():
            print("Error: Call ID must be numbers only. Usage: hangup <call_id>")
            return

    def do_quit(self, arg):
      pass
    def do_exit(self, arg):
        """Exit CallCenter client"""
        return self.do_quit(arg)

    def do_EOF(self, arg):
        """Exit CallCenter client with Ctrl+D"""
        print("\nExiting CallCenter...")
        return self.do_quit(arg)

    def emptyline(self):
        pass


if __name__ == "__main__":
  instance_cmd = CallCenterCmd().onecmd('call 1')