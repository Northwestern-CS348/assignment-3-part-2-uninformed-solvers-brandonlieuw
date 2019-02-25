from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        ask = Fact(Statement(["on", "?X", "peg1"]))
        answer = self.kb.kb_ask(ask)
        l = []
        if answer:
            for x in answer:
                l.append(int(x.bindings_dict['?X'][-1]))
            l.sort()
        t1 = tuple(l)

        ask = Fact(Statement(["on", "?X", "peg2"]))
        answer = self.kb.kb_ask(ask)
        l = []
        if answer:
            for x in answer:
                l.append(int(x.bindings_dict['?X'][-1]))
            l.sort()
        t2 = tuple(l)

        ask = Fact(Statement(["on", "?X", "peg3"]))
        answer = self.kb.kb_ask(ask)
        l = []
        if answer:
            for x in answer:
                l.append(int(x.bindings_dict['?X'][-1]))
            l.sort()
        t3 = tuple(l)
        
        return tuple((t1, t2, t3))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        t = movable_statement.terms

        self.kb.kb_retract(Fact(Statement(["on", t[0], t[1]])))
        self.kb.kb_retract(Fact(Statement(["topOfStack", t[0], t[1]])))
        self.kb.kb_retract(Fact(Statement(["empty", t[2]])))
        answer = self.kb.kb_ask(Fact(Statement(["onTopOf", t[0], "?X"])))
        if answer:
            self.kb.kb_retract(Fact(Statement(["onTopOf", t[0], answer[0].bindings_dict['?X']])))
            self.kb.kb_assert(Fact(Statement(["topOfStack", answer[0].bindings_dict['?X'], t[1]])))
        else:
            self.kb.kb_assert(Fact(Statement(["empty", t[1]])))

        answer = self.kb.kb_ask(Fact(Statement(["topOfStack", "?X", t[2]])))
        if answer:
            self.kb.kb_retract(Fact(Statement(["topOfStack", answer[0].bindings_dict['?X'], t[2]])))
            self.kb.kb_assert(Fact(Statement(["onTopOf", t[0], answer[0].bindings_dict['?X']])))

        self.kb.kb_assert(Fact(Statement(["on", t[0], t[2]])))
        
        self.kb.kb_assert(Fact(Statement(["topOfStack", t[0], t[2]])))



        # game_state = self.getGameState()
        # disk = str(movable_statement.terms[0])
        # initial = str(movable_statement.terms[1])
        # initial_num = int(initial[-1])
        # target = str(movable_statement.terms[2])
        # target_num = int(target[-1])

        # self.kb.kb_retract(parse_input("fact: (on " + disk + " " + initial + ")"))
        # self.kb.kb_add(parse_input("fact: (on " + disk + " " + target + ")"))

        # #updates facts regarding state of target peg
        # if not game_state[target_num-1]:
        #     self.kb.kb_retract(parse_input("fact: (empty " +target+ ")"))
        # else:
        #     self.kb.kb_retract(
        #         parse_input("fact: (onTopOf disk" + str(game_state[target_num - 1][0]) + " " + target + ")"))

        # self.kb.kb_add(parse_input("fact: (onTopOf " + disk + " " + target + ")"))
        # self.kb.kb_retract(parse_input("fact: (onTopOf " + disk + " " + initial + ")"))

        # #updates facts regarding state of initial peg
        # game_state = self.getGameState()
        # if not game_state[initial_num-1]:
        #     self.kb.kb_add(parse_input("fact: (empty " + initial + ")"))
        # else:
        #     self.kb.kb_add(parse_input("fact: (onTopOf disk" + str(game_state[initial_num-1][0])+ " " +initial+ ")"))


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        l = [[0,0,0],[0,0,0],[0,0,0]]

        for i in range(1,9):
            ask = Fact(Statement(["cord", "tile"+str(i), "?x", "?y"]))
            answer = self.kb.kb_ask(ask)
            l[int(answer[0].bindings_dict['?y'])][int(answer[0].bindings_dict['?x'])] = i

        ask = Fact(Statement(["cord", "empty", "?x", "?y"]))
        answer = self.kb.kb_ask(ask)
        l[int(answer[0].bindings_dict['?y'])][int(answer[0].bindings_dict['?x'])] = -1
        

        return tuple((tuple(l[0]), tuple(l[1]), tuple(l[2])))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        t = movable_statement.terms
        self.kb.kb_retract(Fact(Statement(["cord", t[0], t[1], t[2]])))

        self.kb.kb_retract(Fact(Statement(["cord", "empty", t[3], t[4]])))

        self.kb.kb_assert(Fact(Statement(["cord", t[0], t[3], t[4]])))

        self.kb.kb_assert(Fact(Statement(["cord", "empty", t[1], t[2]])))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))


    # def jumpToGameState(self, state)
    #     #Retracts all Facts
    #     ask = Fact(Statement(["cord", "?tile", "?x", "?y"]))
    #     answer = self.kb.kb_ask(ask)
    #     for b in answer:
    #         tile = b.bindings_dict['?tile']
    #         x = b.bindings_dict['?x']
    #         y = b.bindings_dict['?y']
    #         self.kb.kb_retract(Fact(Statement(["cord", tile, x, y])))

    #     #Asserts all tiles in the right position
    #     for i in range(0,3):
    #         for j in range(0,3):
    #             self.kb.kb_assert(Fact(Statement(["cord", state[j][i], i, j])))
