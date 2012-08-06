# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

import displayEngine
import stateReader

gameReader = stateReader.reader()

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    heuristic = 0

    #print "newpos",newPos
    
    ghostDistances = []
    for gs in newGhostStates:
        ghostDistances += [manhattanDistance(gs.getPosition(),newPos)]
    #print "ghostDist",ghostDistances
    
    foodList = newFood.asList()
    
    foodDistances = []
    for f in foodList:
        foodDistances += [manhattanDistance(newPos,f)]
    #print "food",foodDistances

    inverseFoodDist = 0
    if len(foodDistances) > 0:
        inverseFoodDist = 1.0/(min(foodDistances))
    
    #print "ifd",inverseFoodDist        
    
   #print "st",newScaredTimes
    
    heuristic = (min(ghostDistances)*((inverseFoodDist)**2))
    #heuristic += min(ghostDistances)*2
    heuristic += successorGameState.getScore()#/len(foodDistances)
    #heuristic *= 1.0/len(foodDistances)
    #heuristic -= inverseFoodDist**2
    #print "heuristic:",heuristic
    return heuristic

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())

    self.depth = int(depth)
    self.agentCount = 0

  def result(self,state,agent,action):
    return state.generateSuccessor(agent,action)

  def utility(self,state):
    return self.evaluationFunction(state)

  def terminalTest(self,state,depth):
    if depth == (self.depth*self.agentCount) or state.isWin() or state.isLose():
        return True
    else:
        return False


    
class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """
  def minimax(self,state,agent,depth):
    #print "minimax"," agent:",agent," depth:",depth
    #print state
    retval = 0
    if agent == self.agentCount:
        agent = self.index
    if self.terminalTest(state,depth):
        retval =  self.utility(state)
    elif agent == self.index:
        retval = self.maxval(state,agent,depth)
    else:
        retval = self.minval(state,agent,depth)
    #print "minimax returns:",retval," agent:",agent
    return retval
  
  def maxval(self,state,agent,depth):
    v = float("-inf")
    actions = state.getLegalActions(agent)
    actions.remove(Directions.STOP)
    for action in actions:
        v = max(v,self.minimax(self.result(state,agent,action),agent+1,depth+1))          
    return v
  
  def minval(self,state,agent,depth):
    v = float("inf")
    for action in state.getLegalActions(agent):
        v = min(v,self.minimax(self.result(state,agent,action),agent+1,depth+1))          
    return v
    
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    state = gameState
    self.agentCount = state.getNumAgents()
    depth = 0
    agent = self.index
    actionDict = {}
    actions = state.getLegalActions(agent)
    actions.remove(Directions.STOP)
    for action in actions:
        val = self.minimax(self.result(state,agent,action),agent+1,depth+1)
        actionDict[val] = action
    #print actionDict,max(actionDict),min(actionDict),actionDict.keys(),max(actionDict.keys())
    #print "SELECTED",max(actionDict)
    return actionDict[max(actionDict)]
    

class abVal():
    def __init__(self,value,action):
        self.action = action
        self.value = value
    
    def __repr__(self):
        return self.action + ": " + str(self.value)
    
    def __cmp__(self,other):
        if self.value == other.value:
            return 0
        elif self.value > other.value:
            return 1
        else:
            return -1
        
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  
  def alphabeta(self,state,agent,depth,action,alpha,beta):
    #print "alphabeta"," agent:",agent," depth:",depth," alpha:",alpha," beta:",beta
    #print state
    retval = []
    if agent == self.agentCount:
        agent = self.index
    if self.terminalTest(state,depth):
        retval = abVal(self.utility(state),action)
    elif agent == self.index:
        retval = self.maxval(state,agent,depth,alpha,beta)
    else:
        retval = self.minval(state,agent,depth,alpha,beta)
    #print "alphabeta returns:",retval," agent:",agent
    return retval
  
  def maxval(self,state,agent,depth,alpha,beta):
    v = abVal(float("-inf"),Directions.STOP)
    actions = state.getLegalActions(agent)
    actions.remove(Directions.STOP)
    for action in actions:
        #print "max Action...",v
        tempv = self.alphabeta(self.result(state,agent,action),agent+1,depth+1,action,alpha,beta)
        tempv.action = action
        v = max(v,tempv)
        #print v,"end max action"
        if v.value >= beta:
            return v
        alpha = max (alpha,v.value)          
    return v
  
  def minval(self,state,agent,depth,alpha,beta):
    v = abVal(float("inf"),Directions.STOP)
    for action in state.getLegalActions(agent):
        #print "min Action...",v
        tempv = self.alphabeta(self.result(state,agent,action),agent+1,depth+1,action,alpha,beta) 
        tempv.action = action
        v = min(v,tempv)
        #print v,"end min action"
        if v.value <= alpha:
            return v
        beta = min(beta,v.value)          
    return v

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    state = gameState
    self.agentCount = state.getNumAgents()
    depth = 0
    agent = self.index
    alpha = float("-inf")
    beta = float("inf")
    action = Directions.STOP
    v = self.alphabeta(state,agent,depth,action,alpha,beta)
    #print "SELECTING",v
    return v.action
    
class ExpectimaxAgent(MinimaxAgent):
  """
    Your expectimax agent (question 4)
  """

  # def getAction(self, gameState):
  """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
  def minval(self,state,agent,depth):
    v = 0
    for action in state.getLegalActions(agent):
        v += self.minimax(self.result(state,agent,action),agent+1,depth+1)          
    return v/len(state.getLegalActions(agent))

def betterEvaluationFunction(currentGameState):
     """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
    
      DESCRIPTION: <write something here so we know what you did>
     """
     "*** YOUR CODE HERE ***"

     newPos = currentGameState.getPacmanPosition()
     newFood = currentGameState.getFood()
     newGhostStates = currentGameState.getGhostStates()
     ghost1Pos = newGhostStates[0].getPosition()
     ghost2Pos = newGhostStates[1].getPosition()
  
     newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
     
     ######## GAME STATE READER HACKS ##########
     gameReader.closeCall(newPos, (ghost1Pos, ghost2Pos))
     gameReader.closeCall(newPos, (ghost1Pos,))
     score = currentGameState.getScore()
     gameReader.highScore(score, 50)
     gameReader.victory(currentGameState.isWin())
     
     if (newScaredTimes[0] > 0 and newScaredTimes[1] > 0):
       gameReader.special(True, 'GHOST HUNTER Reward Unlock!')
     #print scoreEvaluationFunction(currentGameState)
     #print newPos
     #print newPos, ghost1Pos, ghost2Pos
     #isClose(newPos, ghost1Pos)
     #isClose(newPos, ghost2Pos)
     #print
     #couponCounter = 1
     #if (couponCounter != 0 and newScaredTimes[0] > 0):
       #print 'Display POWER Coupon!'
       #couponCounter = 0
     #print newScaredTimes
     ######## END GAME STATE READER HACKS #######
     heuristic = 0
    
     #print "newpos",newPos
     
     ghostDistances = []
     for gs in newGhostStates:
         ghostDistances += [manhattanDistance(gs.getPosition(),newPos)]
     #print "ghostDist",ghostDistances
     
     foodList = newFood.asList()
     
     foodDistances = []
     for f in foodList:
         foodDistances += [manhattanDistance(newPos,f)]
     #print "food",foodDistances
    
     inverseFoodDist = 0
     if len(foodDistances) > 0:
         inverseFoodDist = 1.0/(min(foodDistances))
     
     #print "ifd",inverseFoodDist        
     
    #print "st",newScaredTimes
     
     heuristic = (min(ghostDistances)*((inverseFoodDist)**2))
     #heuristic += min(ghostDistances)*2
     heuristic += currentGameState.getScore()#/len(foodDistances)
     #heuristic *= 1.0/len(foodDistances)
     #heuristic -= inverseFoodDist**2
     #print "heuristic:",heuristic
     return heuristic
  

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

