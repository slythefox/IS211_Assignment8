#!/usr/bin/env python
# -*- Coding: utf-8 -*-

"""
Game of Pig
"""

import random
import adts
import argparse
from threading import Timer


class TimedGameProxy(object):
    def __init__(self, players):
        self.pig = Game(players)
        self.time_up = Timer(60.0, self.pig.quit)

    def start_game(self):
        self.time_up.start()
        self.pig.start_game()


class Game(object):
    """
    Game of Pig class
    """

    def __init__(self, players=['Human', 'Computer']):
        """
        Pig game constructor
        :param players: (Int) - Number of players
        :return: None
        """
        self.players = adts.Queue()
        for num in xrange(len(players)):
            player = PlayerFactory(players[num] + str(num)).get_player()
            self.players.enqueue(player)
        self.current_player = self.players.dequeue()
        self.current_player.turn = True
        print 'Current player: {}'.format(self.current_player.name)
        self.die = Die()

    def next_player(self):
        """
        Switch game to next player.
        :return: None
        """
        self.current_player.turn = False
        self.players.enqueue(self.current_player)
        self.current_player = self.players.dequeue()
        print 'Next player is {}'.format(self.current_player.name)
        self.current_player.turn = True

    def start_game(self):
        """
        Play the game
        :return: None
        """

        ask_player = self.current_player.next_action()
        while ask_player and self.current_player.turn:
            if ask_player.upper()[0] == 'Q':
                self.quit()
                break

            if ask_player.upper()[0] == 'R':
                self.play()

            elif ask_player.upper()[0] == 'H':
                print '{} Holds. Score: {}'\
                    .format(self.current_player.name,
                            self.current_player.get_score())
                self.next_player()

            score = self.current_player.get_score()

            if score >= 100:
                print '{} wins. Score: {}'.format(self.current_player.name, score)
                break

            print 'Player: ', self.current_player.name
            print 'Score: ', self.current_player.get_score()
            ask_player = self.current_player.next_action()
            if not ask_player:
                self.quit()

    def play(self):
        num = self.current_player.play(self.die)
        if num == 1:
            self.current_player.points = []
            print '{} loses turn. Score set to {}' \
                .format(self.current_player.name,
                        self.current_player.get_score())
            self.next_player()
        else:
            self.current_player.points.append(num)

    def quit(self):
        print 'Quitting game...'
        self.players.enqueue(self.current_player)
        while self.players.size() > 0:
            player = self.players.dequeue()
            print 'Player {}: {}'.format(player.name, player.score)
        self.current_player.turn = False


class Die(object):
    """
    Die class
    """
    faces = (1, 2, 3, 4, 5, 6)

    def roll(self):
        """
        Alea jacta est
        :return: (Int) - The die face
        """
        face = random.choice(self.faces)
        print 'Die face: {}'.format(face)
        return face


class Player(object):
    """
    Player
    """

    def __init__(self, name):
        """
        Constructor
        :param name: (String) Player identifier
        :return: (None)
        """
        self.name = name
        self.turn = False
        self.points = []
        self.score = 0
        self.plays = 0
        self.die = Die()

    def hold(self):
        """
        Take points and lose turn
        :return: (Int) - Player points
        """
        self.turn = False

    def play(self, die):
        """
        Roll the die
        :param die: (Object) Die instance
        :return: (None)
        """
        if self.turn:
            print 'Rolling the die...'
            return die.roll()

    def get_score(self):
        """
        Sum and return accumulated points
        :return: (Int) - Player's score
        """
        self.score = sum(self.points)
        return self.score

    def next_action(self):
        ask = 'Roll (R) Hold (H) or Quit (Q)?[Q]'
        return raw_input(ask)


class ComputerPlayer(Player):
    """
    Computer player, subclass of Player class
    """

    def next_action(self):
        """
        Player.next_action() overload.
        :return: (String) - Return Hold or Roll
        """
        score = self.get_score()
        if score == 25 or (100 - score) < 25:
            return 'Hold'
        else:
            return 'Roll'


class PlayerFactory(object):
    """
    Player factory
    """
    def __init__(self, player):
        if player[0] == 'H':
            self.player = Player(player)
        elif player[0] == 'C':
            self.player = ComputerPlayer(player)

    def get_player(self):
        return self.player


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--player1', required=False, type=str, default='Computer')
    PARSER.add_argument('--player2', required=False, type=str, default='Computer')
    PARSER.add_argument('--timed', required=False, type=int, default=1)
    ARGS = PARSER.parse_args()
    PLAYER1 = str(ARGS.player1).title()
    PLAYER2 = str(ARGS.player2).title()
    TIMED = ARGS.timed
    if PLAYER1 and PLAYER2:
        if TIMED == 1:
            game = TimedGameProxy([PLAYER1, PLAYER2])
        else:
            game = Game([PLAYER1, PLAYER2])
        game.start_game()
    else:
        print 'You need at least two players for this game.'
