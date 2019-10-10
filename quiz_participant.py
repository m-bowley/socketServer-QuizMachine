from time import sleep
import socket
import pickle

quiz_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

quiz_server.connect(("0.0.0.0", 8083))
message = b""

while message.decode() != 'Quiz End':
    message = quiz_server.recv(32)
    if message.decode() == "Answers":
        options = quiz_server.recv(1024)
        answers = pickle.loads(options)
        for i in range(len(answers)):
            print(str(i) + ". " + answers[i])
        print('Enter the number of your answer')
        my_answer = input(">")
        quiz_server.send(my_answer.encode())
        reply = quiz_server.recv(1024)
        print(reply.decode())
    else:
        print(message.decode())

message = quiz_server.recv(32)
print(message.decode())