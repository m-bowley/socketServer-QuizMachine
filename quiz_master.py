import socketserver
from quiz_player import Player
from Questions import Question 
from time import time, sleep
import random 
import threading
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
def wait_for_ack(socket):
    receiving = True
    while receiving:
        incoming = socket.recv(1)
        if incoming == chr(6).encode():
            receiving = False

END_CHAR = chr(8).encode()

players = []
MAX_PLAYERS = 0
while MAX_PLAYERS == 0:
    try:
        MAX_PLAYERS = input('How many players would you like?')
        MAX_PLAYERS = int(MAX_PLAYERS)
    except:
        print('Try again please.')

questions = []
answered = 0

current_q = None

with open("questions.csv", 'r') as file:
    for line in file.readlines():
        line = line.split(',')
        if len(line) > 4:
            new_q = Question(line[0], line[1:5], line[5])
            questions.append(new_q)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class QuizGame(socketserver.BaseRequestHandler):

    def handle(self):
        # Accept client state
        global current_q, answered
        print(self.client_address)
        players.append(self.request)
        welcome = pickle.dumps((0, "Welcome to the quiz"))
        welcome += END_CHAR
        self.request.sendall(welcome)
        wait_for_ack(self.request)
        # Back to listening state
        while len(players) < MAX_PLAYERS:
            sleep(0.5)
        # Quiz starting
        message = pickle.dumps((1, "None"))
        message += END_CHAR
        print(message)
        self.request.sendall(message)
        wait_for_ack(self.request)
        # Quiz Loop
        score = 0
        while len(questions) > 0:
            if current_q == None:
                current_q = random.choice(questions)
                answered = 0
            # Send Question
            message = pickle.dumps((2, current_q.question))
            message += END_CHAR
            self.request.sendall(message)
            wait_for_ack(self.request)
            # Send Answers
            message = pickle.dumps((3, current_q.answers))
            message += END_CHAR
            self.request.sendall(message)
            wait_for_ack(self.request)
            # Request Answer
            message = pickle.dumps((4, "None"))
            message += END_CHAR
            self.request.sendall(message)
            wait_for_ack(self.request)
            # Get Feedback
            receiving = True
            message = b''
            while receiving:
                incoming = self.request.recv(1)
                if incoming == END_CHAR:
                    receiving = False
                else:
                    message += incoming
            data = pickle.loads(message)
            if data[1]:
                score += 1
            while answered < len(players):
                sleep(0.5)
            if current_q in questions:
                questions.remove(current_q)
                current_q = None


def server_tasks():
    while len(players) < MAX_PLAYERS:
        sleep(0.5)
    global STATUS, current_q, answered
    STATUS = "Quiz Starting"
    while len(questions) > 0:
        current_q = random.choice(questions)
        answered = 0
        while answered < len(players):
            sleep(0.5)
        questions.remove(current_q)
        STATUS = "Next Question"


        

# Open the quiz server and bind it to a port - creating a socket
quiz_server = ThreadedTCPServer(('0.0.0.0', 2065), QuizGame)
x = threading.Thread(target=server_tasks)
x.start()
quiz_server.serve_forever()
player_ID = 0

