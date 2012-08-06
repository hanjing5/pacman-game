from Tkinter import *
import datetime
import thread        
import urllib2 as urllib
from PIL import Image, ImageTk
from cStringIO import StringIO


def display(message, picture_link):
    print 'Displaying Coupon!'

    root = Toplevel()
    #root = Tk()
    #my_url = 'http://aux.iconpedia.net/uploads/1440300232.png'
    #img_file = urllib.urlopen(my_url)
    #im = StringIO(img_file.read())
    #image1 = Image.open(im)

    #f = open(picture_link)
    image1 = Image.open(picture_link)
    #image1 = picture_link
    #root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
     
    # Convert the Image object into a TkPhoto object
    tkpi = ImageTk.PhotoImage(image1)
    print tkpi
    label_image = Label(root, image=tkpi, text=message, font=("default",12),compound='top',width=image1.size[0], height=image1.size[1]+20)
    label_image.image = tkpi # keep a reference or python Garbage collects this
    label_image.pack()  # pack it in the display windowv

    #root.geometry('300x300')
    root.title("Your Reward!")
    #m = Message(root, text=message, width=400, font=("default",12), justify='center').pack()

    root.after(2000, root.destroy) # close the window after 2 seconds
    print 'Closing Coupon Window!'
    print image1
    print tkpi
    root.mainloop() #start the GUI
 
def displayCoupon(message, picture_link):
  #image1 = Image.open(picture_link)
  thread.start_new_thread( display, (message, picture_link, ) )

#print 'ladfadfadsadf'
#display('Coupon Coupon Coupon', 'coke-coupon.png')
#print 'ladfadfadsadf'
