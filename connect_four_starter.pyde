
from board import Board

board = Board(6,7,100)
answer = ""
record = False

def setup():
    size(720, 720)
    global answer 

    if answer:
        print('hi ' + answer)
    elif answer == '':
        answer = input('enter your name').lower()
    else:
        print(answer) # Canceled dialog will print None

def draw():
    background(200)
    if board.win_check == board.EMPTY:
        if (mousePressed):
            board.generate_disk(mouseX, mouseY)
        if board.cur_player == board.YELLOW:
            board.ai_move()
        board.draw_drop_disk()
    elif board.win_check == board.RED and not record:
        score()
    board.update_board()
    board.draw_board()
    board.draw_text()


def mouseReleased():
    if board.win_check == board.EMPTY and board.cur_player == board.RED:
        board.player_move(mouseX, mouseY)

def input(self, message=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)

def score():
    f = open("score.txt", "r+")
    rank = {}
    scores =  f.readlines()
    for score in scores:
        score = score.split(" ")
        rank[score[0]] = int(score[1])
    if answer in rank.keys():
        rank[answer] += 1
    else:
        rank[answer] = 1
    f.seek(0) 
    f.truncate()
    rank = sorted(rank.items(),
               key=lambda x: x[1], 
               reverse=True)
    for n in rank:
        f.write(str(n[0]) + " " + str(n[1]) + "\n")
    global record
    record = True
