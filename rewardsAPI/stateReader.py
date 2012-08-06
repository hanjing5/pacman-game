import util
import displayEngine
from gtktest import Image_Example

# detects 3 things
# achievement (passed a level)
# high score (score achieved)
# close calls (enemy close, almost dying)
# CUSTOM #
# GHOST HUNTER #

from datetime import datetime

class reader():
  def __init__(self):
     self.highScoresLimit = 1
     self.achievementsLimit = 1
     self.closeCallsLimit = 2
     self.specialsLimit = 1
     
     # delay 20sec between displaying coupons
     self.bufferTime = 5
     self.lastCallTime = datetime.now()
  
  # calculate the amount of time passed
  # uses to delay call time between coupons
  def timePassed(self):
     t =  datetime.now() - self.lastCallTime
     return t.seconds

  def highScore(self, currentScore, targetScore):
     if (self.highScoresLimit > 0 and currentScore >= targetScore):
       self.highScoresLimit -= 1
       print 'Display NEW HIGH SCORE coupon!'
       displayEngine.displayCoupon('New High Score!', 'coupons/coke-coupon.png')
       #Image_Example().threadMain()
 
  def victory(self, yesNo):
     if (self.achievementsLimit > 0 and yesNo):
       self.achievementsLimit -= 1
       print 'Display ACHIEVEMENT coupon!'
       displayEngine.displayCoupon('Victory!', 'coupons/gamestop-coupon.jpeg')

  # accept a boolean isInSpecialState. If in special state, we call the coupon 
  def special(self, isInSpecialState, message='Special'):
     if (self.specialsLimit > 0 and isInSpecialState):
       self.specialsLimit -= 1
       print 'Display SPECIAL coupon!'
       displayEngine.displayCoupon(message, 'coupons/redbull-coupon.png')
   
  def isCloseCall(self, player, enemy):
    for e in enemy:
      if util.manhattanDistance(player, e) > 2:
         return False
    return True
       
  def closeCall(self, pacmanState, allGhostStates):
    if (self.timePassed() > self.bufferTime and self.closeCallsLimit > 0 and self.isCloseCall(pacmanState, allGhostStates)):
      self.closeCallsLimit -= 1
      print 'Display CLOSE CALL coupon!'
      self.lastCallTime = datetime.now()
      displayEngine.displayCoupon('Close Call!', 'coupons/popchips-coupon.jpg')


