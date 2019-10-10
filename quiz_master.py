import socketserver
from quiz_player import Player
from Questions import Question 
from time import time, sleep
import random 
import threading
import pickle

players = []
player_addresses = []
MAX_PLAYERS = 0
while MAX_PLAYERS == 0:
    try:
        MAX_PLAYERS = input('How many players would you like?')
        MAX_PLAYERS = int(MAX_PLAYERS)
    except:
        print('Try again please.')

players = []
player_addresses = []

questions = []
answered = 0

current_q = None

STATUS = "Set up"

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
        print(self.client_address)
        players.append(self.request)
        self.request.sendall(b"Welcome to the quiz")
        while STATUS != "Quiz Starting":
            self.request.send(b"Waiting for players...")
            sleep(5)
        self.request.sendall(b"Quiz Starting")
        sleep(0.5)
        while STATUS != "Quiz End":
            self.request.sendall(b"Next Question")
            sleep(0.5)
            self.request.sendall(current_q.question.encode())
            sleep(0.5)
            self.request.sendall(b"Answers")
            sleep(0.5)
            answers = pickle.dumps(current_q.answers)
            self.request.sendall(answers)
            reply = self.request.recv(32)
            answer = reply.decode()
            if int(answer) == int(current_q.correct):
                self.request.sendall(b"Correct")
            else:
                self.request.sendall(b"Incorrect")
            global answered
            answered += 1
            while STATUS != "Next Question":
                sleep(0.5)



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
quiz_server = ThreadedTCPServer(('0.0.0.0', 8083), QuizGame)
x = threading.Thread(target=server_tasks)
x.start()
quiz_server.serve_forever()
player_ID = 0

