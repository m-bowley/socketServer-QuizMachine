from time import sleep
import socket
import pickle

'''
OP Codes

0 - Information
1 - Quiz Starting
2 - Sending Question
3 - Sending Answers
4 - Request Answer
5 - Sending Answer
6 - Feedback
7 - Quiz over
EOT - End of transmission

'''

quiz_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

quiz_server.connect(("0.0.0.0", 2065))

status = "Start"
END_CHAR = chr(8).encode()
score = 0

while status != "END":
    receiving = True
    message = b''
    while receiving:
        incoming = quiz_server.recv(1)
        if incoming == END_CHAR:
            receiving = False
        else:
            message += incoming
    quiz_server.send(chr(6).encode())
    print(message)
    data = pickle.loads(message)
    if data[0] == 0:
        print(data[1])
    elif data[0] == 1:
        print("Quiz Starting")
    elif data[0] == 2:
        print("Question incoming")
        print(data[1])
    elif data[0] == 3:
        answers = data[1]
        for i in range(len(answers)):
            print(str(i) + ". " + answers[i])
    elif data[0] == 4:
        print('Enter the number of your answer')
        my_answer = input(">")
    elif data[0] == 5:
        feedback = True
        if my_answer == data[1]:
            print("You were right")
            score += 1
        else:
            print("You were wrong")
            feedback = False
        reply = (6, feedback)
        reply = pickle.dumps(reply)
        quiz_server.send(reply)
    elif data[0] == 7:
        print("Quiz Over")
        status = "END"