from Tkinter import *
import datetime
import thread        
import urllib2 as urllib
from PIL import Image, ImageTk
from cStringIO import StringIO

# my_url = 'http://aux.iconpedia.net/uploads/1440300232.png'

def displayFromWebAPI(message, picture_url):
    print 'Displaying Coupon!'
    root = Toplevel() #Tk() opens an interpreter, so Toplevel is what I want

    img_file = urllib.urlopen(picture_url)
    im = StringIO(img_file.read())
    image1 = Image.open(im)
    #f = open(picture_link)
    #image1 = Image.open(picture_link)
    #image1 = picture_link
    #root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
     
    # Convert the Image object into a TkPhoto object
    tkpi = ImageTk.PhotoImage(image1)
    print tkpi
    label_image = Label(root, image=tkpi, text=message, font=("default",12),compound='top',width=image1.size[0], height=image1.size[1]+20)
    label_image.image = tkpi # keep a reference or python Garbage collects this
    label_image.pack()  # pack it in the display windowv
	
    width = image1.size[0]
    height = image1.size[1]
    root.geometry("200x200-25-0")
    root.title("Your Reward!")
    #m = Message(root, text=message, width=400, font=("default",12), justify='center').pack()

    root.after(2000, root.destroy) # close the window after 2 seconds
    print 'Closing Coupon Window!'
    print image1
    print tkpi
    root.mainloop() #start the GUI

def displayFromLocalFiles(message, picture_link):
    root = Toplevel()
    image1 = Image.open(picture_link)
    # Convert the Image object into a TkPhoto object
    tkpi = ImageTk.PhotoImage(image1)
    label_image = Label(root, image=tkpi, text=message, font=("default",12),compound='top',width=image1.size[0], height=image1.size[1]+20)
    label_image.image = tkpi # keep a reference or python Garbage collects this
    label_image.pack()  # pack it in the display windowv
	
    width = image1.size[0]
    height = image1.size[1]
    root.geometry("400x200-25-0") # this control the size of the window and the position of it in relations to the screen
    root.title("Your Reward!")

    root.after(2000, root.destroy) # close the window after 2 seconds
    root.mainloop() #start the GUI
 
def displayLocalCoupon(message, picture_link):
  #image1 = Image.open(picture_link)
  thread.start_new_thread( displayFromLocalFiles, (message, picture_link, ) )

def displayWebCoupon(message, picture_url):
  picture_url = 'http://aux.iconpedia.net/uploads/1440300232.png'
  thread.start_new_thread( displayFromWebAPI, (message, picture_url, ) )

#print 'ladfadfadsadf'
#display('Coupon Coupon Coupon', 'coke-coupon.png')
#print 'ladfadfadsadf'
