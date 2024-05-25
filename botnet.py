import socketserver
import threading

class BotHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(f"Bot with IP {self.client_address[0]} sent: {self.data.decode('utf-8')}")
        
        # Чтение команд из файла
        with open('commands.txt', 'r') as file:
            commands = file.readlines()
        
        # Отправка команд ботам
        for command in commands:
            command = command.strip()
            self.request.sendall(command.encode('utf-8'))
            response = self.request.recv(1024).strip()
            print(f"Response from {self.client_address[0]}: {response.decode('utf-8')}")
        
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "", 8000
    with ThreadedTCPServer((HOST, PORT), BotHandler) as server:
        try:
            print("Server started at {}:{}".format(HOST, PORT))
            server.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")
