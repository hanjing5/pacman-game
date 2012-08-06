import util
import displayEngine
from gtktest import Image_Example
from datetime import datetime

# detects 3 things
# achievement (passed a level)
# high score (score achieved)
# close calls (enemy close, almost dying)
# CUSTOM #
# GHOST HUNTER #

path = '/home/innovision/Downloads/pacman_ingidio_demo/'

# web or local. web gets picture from web, 
# local displays picture from coupons/ folder
API_CONTROL = 'local'

class reader():
  def __init__(self):
     self.highScoresLimit = 1
     self.achievementsLimit = 1
     self.closeCallsLimit = 3
     self.specialsLimit = 1
     
     # delay 20sec between displaying coupons
     self.bufferTime = 5
     self.lastCallTime = datetime.now()
      
  # prevent multiple coupons from displaying
  # at the same time

  # calculate the amount of time passed
  # uses to delay call time between coupons
  def isBufferOver(self):
     if self.timePassed() > self.bufferTime:
       return True
     #print 'No'
     #print self.timePassed()
     return False

  def timePassed(self):
     t =  datetime.now() - self.lastCallTime
     return t.seconds

  def highScore(self, currentScore, targetScore):
     if (self.isBufferOver() and self.highScoresLimit > 0 and currentScore >= targetScore):
       self.lastCallTime = datetime.now()
       self.highScoresLimit -= 1
       print 'Display NEW HIGH SCORE coupon!'
       if (API_CONTROL == 'web'):
         displayEngine.displayWebCoupon('New High Score!', path + 'coupons/coke-coupon.png')
       else:
         displayEngine.displayLocalCoupon('New High Score!', path + 'coupons/coke-coupon.png')
       #Image_Example().threadMain()
 
  def victory(self, yesNo):
     if (self.achievementsLimit > 0 and yesNo):
       self.achievementsLimit -= 1
       print 'Display ACHIEVEMENT coupon!'
       if (API_CONTROL == 'web'):
         displayEngine.displayWebCoupon('Victory!', path + 'coupons/gamestop-coupon.jpeg')
       else:
         displayEngine.displayLocalCoupon('Victory!', path + 'coupons/gamestop-coupon.jpeg')

  # accept a boolean isInSpecialState. If in special state, we call the coupon 
  def special(self, isInSpecialState, message='Special'):
     if (self.isBufferOver() and self.specialsLimit > 0 and isInSpecialState):
       self.lastCallTime = datetime.now()
       self.specialsLimit -= 1
       print 'Display SPECIAL coupon!'
       if (API_CONTROL == 'web'):
         displayEngine.displayWebCoupon(message, path + 'coupons/redbull-coupon.jpg')
       else:
         displayEngine.displayLocalCoupon(message, path + 'coupons/redbull-coupon.jpg')
   
  def isCloseCall(self, player, enemy):
    for e in enemy:
      if util.manhattanDistance(player, e) > 2:
         return False
    return True
       
  def closeCall(self, pacmanState, allGhostStates):
    if (self.isBufferOver() and self.closeCallsLimit > 0 and self.isCloseCall(pacmanState, allGhostStates)):
      self.lastCallTime = datetime.now()
      self.closeCallsLimit -= 1
      print 'Display CLOSE CALL coupon!'
      if (API_CONTROL == 'web'):
        displayEngine.displayWebCoupon('Close Call!', path + 'coupons/popchips-coupon.jpg')
      else:
        displayEngine.displayLocalCoupon('Close Call!', path + 'coupons/popchips-coupon.jpg')


