import pygame
import threading
import socket
import pickle
import random
import sys

from network import Network

# initialize window
pygame.init()
FPS = 30
WIDTH = 800
HEIGHT = 500
win = None #pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hang mamatay ng dahil sa iyo!")

# load images
images = []
for i in range(7):
    images.append(pygame.image.load(f'images/hangmang{i}.png'))

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 40)

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# hangman variables
hangman_status = 0
words = ["IDE", "REPLIT", "PYTHON", "PYGAME"]
with open('words.txt', 'r') as r:
    while line := r.readline():
        words.append(line.upper().strip())
word = random.choice(words)
guessed = []

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def draw():
    global win

    win.fill(WHITE)

    # draw title
    text = TITLE_FONT.render("Hang mamatay ng dahil sa iyo - JRiz", 1, BLACK)
    win.blit(text, (WIDTH//2 - text.get_width()//2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()//2, y - text.get_height()//2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()

def game(conn, addr):
    global win, hangman_status

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()        
    
    run = True
    print(f'[CLIENT] Client connected from {addr}')

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
        
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        
        if won:
            display_message("You WON!")
            break

        if hangman_status == 6:
            display_message("You LOST!")
            break

    pygame.quit()

def threaded_guessed(conn, addr):
    global hangman_status

    net.send(conn=conn, data=guessed)

    while True:
        try:
            data = net.recv(conn=conn)
            
            if data == net.disconnect_msg:
                print(f'[SERVER] {addr} disconnected.')
                break
            else:
                guessed.append(data) # letter ex: a
                for letter in letters:
                    if data.upper() == letter[2].upper():
                        letter[3] = False
                if data not in word:
                    hangman_status += 1

                net.send(conn=conn, data=guessed)

        except socket.error as e:
            print(e)
            break
        except Exception as e:
            print(e)
            break

    conn.close()
    print(f'[SERVER] {addr} closed.')

if __name__ == '__main__':
    net = Network(is_server=True, max_connections=1)
    conn, addr = net.accept()

    client_listener = threading.Thread(target=threaded_guessed, args=(conn, addr))
    client_listener.start()
    game(conn, addr)