import sys
import os
import curses
from curses.textpad import Textbox, rectangle
from time import sleep


class player:
    x = 0
    y = 0
    key_up = 0
    key_down = 0
    score = 0

    def move(self, x, y):
        self.x = x
        self.y = y

    def draw_player(self, window):
        rectangle(window, self.y, self.x, self.y + 10, self.x+1)


class ball:
    x = 0
    y = 0
    speed_x = 0
    speed_y = 0

    def __init__(self, height, width):
        self.speed_y = 1
        self.speed_x = 1
        self.y = height//2
        self.x = width//2

    def reverse_x_speed(self):
        self.speed_x *= -1

    def reverse_y_speed(self):
        self.speed_y *= -1

    def move_ball(self, x, y):
        self.x = x
        self.y = y

    def draw_ball(self, window):
        window.addstr(self.y, self.x, "O")


def ball_touch_player(player_x, player_y, ball_x, ball_y):
    if player_x == ball_x or player_x == ball_x+1:
        if ball_y >= player_y and ball_y <= player_y + 10:
            return 1
        else:
            return 0
    else:
        return 0


def restart_game(height, width, ball, player1, player2):
    player1.move(int(width/10), int(height/2-(5)))
    player2.move(int(width-(width/10)), int(height/2-(5)))
    ball.move_ball(width//2, height//2)


def pong_game(stdscr):

    # quit variable
    k = 0
    l = 0

    # getch is no blocking function after this call
    stdscr.nodelay(True)
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # heigh and width of or window is
    height, width = stdscr.getmaxyx()

    # score
    score = 0

    # create first player
    player1 = player()
    player1.key_up = curses.KEY_UP
    player1.key_down = curses.KEY_DOWN
    player1.move(int(width/10), int(height/2-(5)))
    player1.draw_player(stdscr)

    # creat second player
    player2 = player()
    player2.key_up = 122  # z character
    player2.key_down = 115  # s character
    player2.move(width-(int(width/10)), int(height/2-(5)))
    player2.draw_player(stdscr)

    # create ball
    ball_game = ball(height, width)
    ball_game.draw_ball(stdscr)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Refresh screen
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.addstr(5, width//2 - 10, "SCORE PLAYER 1 : "+str(player1.score))
        stdscr.addstr(5, width//2 + 10, "SCORE PLAYER 2 : "+str(player2.score))

        # draw middle line
        stdscr.vline(0, int(width/2), height-1, int(width/2))

        # key action
        if k == player1.key_down and player1.y + 1 < height-10:
            player1.y += 1
        elif k == player1.key_up and player1.y - 1 >= 0:
            player1.y -= 1
        elif k == player2.key_down and player2.y + 1 < height-10:
            player2.y += 1
        elif k == player2.key_up and player2.y - 1 >= 0:
            player2.y -= 1
        else:
            pass

        # deal with players
        player1.move(player1.x, player1.y)
        player1.draw_player(stdscr)
        player2.move(player2.x, player2.y)
        player2.draw_player(stdscr)

        # deal with the ball
        if ball_game.x-1 < 0 or ball_game.x+1 >= width:
            if ball_game.x < width//2:
                player2.score += 1
            else:
                player1.score += 1
            restart_game(height, width, ball_game, player1, player2)
        elif ball_game.y+2 > height or ball_game.y-1 < 0:
            ball_game.reverse_y_speed()
        elif ball_touch_player(player1.x, player1.y, ball_game.x, ball_game.y) == 1 or ball_touch_player(player2.x, player2.y, ball_game.x, ball_game.y) == 1:
            ball_game.reverse_x_speed()

        ball_game.x += ball_game.speed_x
        ball_game.y += ball_game.speed_y
        ball_game.move_ball(ball_game.x, ball_game.y)
        ball_game.draw_ball(stdscr)

        # check if user want to quit the game
        k = stdscr.getch()
        sleep(0.05)


def main():
    curses.wrapper(pong_game)


if __name__ == "__main__":
    main()

# le probleme de k et l c'est que l'on ne peux pas rester appuyer sur une touche
