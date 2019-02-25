
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if self.currentState.state == self.victoryCondition:
                return True

        self.expandDFS()

        while True:
            if self.currentState.state == self.victoryCondition:
                return True
            n = self.currentState.nextChildToVisit

            if n < len(self.currentState.children):
                self.currentState.nextChildToVisit+=1
                self.gm.makeMove(self.currentState.children[n].requiredMovable)
                self.currentState = self.currentState.children[n]
                self.visited[self.currentState] = True
                return self.currentState.state == self.victoryCondition
            else:
                # if isinstance(self.currentState.parent, GameState):
                    self.currentState = self.currentState.parent
                # else:
                #     return False


    def expandDFS(self): 
        moves = self.gm.getMovables()
        if moves:
            for x in moves:
                self.gm.makeMove(x)
                newState = GameState(self.gm.getGameState(), self.currentState.depth+1, x)
                newState.parent = self.currentState
                self.gm.reverseMove(x)
                if not newState in self.visited:
                    self.currentState.children.append(newState)


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = []

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
                return True
        if self.currentState.depth == 0:
            self.currentState.requiredMovable = []

        self.expandBFS()

        if self.queue:

            n = self.queue.pop(0)

            diffIndex = 0
            for i in range(0, len(self.currentState.requiredMovable)):
                if not self.currentState.requiredMovable[i] == n.requiredMovable[i]:
                    diffIndex = i
                    break

            for i in range(len(self.currentState.requiredMovable)-1, diffIndex-1, -1):
                self.gm.reverseMove(self.currentState.requiredMovable[i])

            for i in range(diffIndex, len(n.requiredMovable)):
                self.gm.makeMove(n.requiredMovable[i])

            self.currentState = n
            return self.currentState.state == self.victoryCondition


        


    def expandBFS(self): 
        moves = self.gm.getMovables()
        if moves:
            for x in moves:
                self.gm.makeMove(x)
                newState = GameState(self.gm.getGameState(), self.currentState.depth+1, self.currentState.requiredMovable+[x])
                self.gm.reverseMove(x)
                if not newState in self.visited:
                    self.visited[newState] = True
                    self.queue.append(newState)
                    self.currentState.children.append(newState)