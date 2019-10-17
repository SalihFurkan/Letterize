# main.py file (RUN THIS)
# Description: This program allows you to draw any letter you want and predict the letter.
# Machine Learning Algorithm is used to predict. Model is trained over MNIST dataset. Neural Network is used.

import pygame
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from keras.models import model_from_json
import keras
from scipy import ndimage
from scipy import misc
import Draw
from Draw import pixelArt
from Draw import menu
from Draw import grid
import sys
import time

sys.setrecursionlimit(1000000)

pygame.init() #initalize pygame
paintBrush = pygame.image.load("Paintbrush.png")
currentVersion = 1.1

#Set defaults for our screen size and rows and columns
rows = 50
cols = 50
wid = 640
heigh = 540
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Labeltext
labeltext = ''
centerX = 0

json_file = open('Letter.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("Letter.h5")
loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

blur_matrix = np.array([[1,2,1],[2,4,2],[1,2,1]])*1/16

checked = []
def fill(spot, grid, color, c):
   if spot.color != c:
      pass
   else:
      spot.click(grid.screen, color)
      pygame.display.update()
      
      i = spot.col #the var i is responsible for denoting the current col value in the grid
      j = spot.row #the var j is responsible for denoting the current row value in the grid

      #Horizontal and vertical neighbors
      if i < cols-1: #Right
         fill(grid.getGrid()[i + 1][j], grid, color, c)
      if i > 0: #Left
         fill(grid.getGrid()[i - 1][j], grid, color, c)
      if j < rows-1: #Up
         fill(grid.getGrid()[i][j + 1], grid, color, c)
      if j > 0 : #Down
         fill(grid.getGrid()[i][j - 1], grid, color, c)

# Obtaining the values in the pixels
def obtain(cols, rows, grid):
  page = []
  for pixel in grid:
    for p in pixel:
      page.append(p.color[0])
  page = np.matrix(page)
  h,w = page.shape
  page = ((page/255) - np.ones((h,w))) * (-255)
  image = (page.reshape((28,28)))
  #image = ndimage.convolve(image,blur_matrix)
  #image = ndimage.uniform_filter(image)
  image = ndimage.gaussian_filter(image,sigma=0.75)
  image = image.astype(int)
  image = image.reshape((1,28,28,1))
  result = loaded_model.predict(image)
  letter = letters[np.argmax(result)]
  return letter




# Saves the current project into a text file that contains the size of the screen, if the gird is showing and all the colors of all the pixels
def save(cols, rows, show, grid, path):
   if len(path) >= 4: # This just makes sure we have .txt at the end of our file selection
      if path[-4:] != '.txt':
         path = path + '.txt'
   else:
      path = path + '.txt'

   # Overwrite the current file, or if it doesn't exist create a new one
   file = open(path, 'w')
   file.write(str(cols) + ' ' + str(rows) + ' ' + str(show) +'\n')

   for pixel in grid:
       for p in pixel: #For every pixel write the color in the text file
           wr = str(p.color[0])
           file.write(wr + '\n')
   file.write(str(currentVersion))

   file.close()
   name = path.split("/")
   changeCaption(name[-1])
   obtain(cols,rows,grid)


#Opens the file from the given path and displays it to the screen
def openFile(path):
    global grid
    
    file = open(path, 'r')
    f = file.readlines()
    if f[-1] == str(currentVersion):
       
       dimensions = f[0].split() #Dimesnions for the rows and cols
       columns = int(dimensions[0])
       rows = int(dimensions[1])
       
       if dimensions[2] == '0': #If the show grid attribute at the end of our dimensions line is 0 then don't show grid
          v = False
       else:
          v = True
       initalize(columns, rows, v) #Redraw the grid, tool bars, menu bars etc. 
       name = path.split("/")
       changeCaption(name[-1])
       
       line = 0
       for i in range(columns): # For every pixel, read the color and format it into a tuple
          for j in range(rows):
             line += 1
             nColor = []
             for char in f[line].strip().split(','):
                nColor.append(int(char))
                
             
             grid.getGrid()[i][j].show(win, tuple(nColor), 0) #Show the color on the grid
    else:
      window = Tk()
      window.withdraw()
      messagebox.showerror("Unsupported Version", "The file you have opened is created using a previous version of this program. Please open it in that version.")


#Change pygame caption
def changeCaption(txt):
   pygame.display.set_caption(txt)
          

# This shows the file navigator for opening and saving files
def showFileNav(op=False):
   #Op is short form for open as open is a key word
    window = Tk()
    window.attributes("-topmost", True)
    window.withdraw()
    myFormats = [('Windows Text File','*.txt')]
    if op:
       filename = askopenfilename(title="Open File",filetypes=myFormats) # Ask the user which file they want to open
    else:
       filename = asksaveasfilename(title="Save File",filetypes=myFormats) # Ask the user choose a path to save their file to
       
    if filename: #If the user seletced something 
       x = filename[:] # Make a copy
       return x

# Onsubmit function for tkinter form for choosing pixel size
def onsubmit(x=0):
    global cols, rows, wid, heigh
    cols, rows = 28, 28
    

# Update the lbale which shows the pixel size by getting input on rows and cols
def updateLabel(a, b, c):
   sizePixel = rowsCols.get().split(',') #Get the contents of the label
   l = 12
   w = 12
   
   try:
      l = 600/int(sizePixel[0])
   except:
      pass

   try:
      w = 600/(int(sizePixel[1]))
   except:
      pass

   label1.config(text='Pixel Size: ' + str(l) + ', ' + str(w)) #Change label to show pixel size


#CREATE SCREEN
def initalize(cols, rows, showGrid=False):
   global grid, win, tools, lineThickness, saveMenu

   #if grid already exsists delete it then recreate it
   try:
      del grid
   except:
      pass

   pygame.display.set_icon(paintBrush)   
   win = pygame.display.set_mode((int(wid), int(heigh) + 100))
   pygame.display.set_caption('Untitled')
   win.fill((255,255,255))

   #CREATION OF OBJECTS
   win.fill(pygame.Color('black'),(10,5,wid-20,35))
   font = pygame.font.Font('freesansbold.ttf', 24)
   text = font.render(labeltext, True, [255,0,0])
   textRect = text.get_rect()
   textRect.center = (40,26)
   win.blit(text,textRect)

   grid = pixelArt(win, int(wid), int(heigh-40), cols, rows, showGrid,starty = 40)
   grid.drawGrid()

   tools = menu(win, 200, 40, 3, 1, True, grid.width - 210, grid.height + 80)
   tools.drawGrid()

   buttons = ['D', 'E', 'C']
   tools.setText(buttons)
   tools.drawGrid()

   l = tools.getGrid()
   l[0][0].show(grid.screen, (255,0,0),1, True)

   saveMenu = menu(win, 140, 40, 3, 1, True, grid.width - 400, grid.height + 55)
   saveMenu.drawGrid()

   buttons = ['Erase', 'Open', 'Read']
   saveMenu.setText(buttons)

   pygame.display.update()


#MAIN LOOP
onsubmit()
initalize(cols, rows)
pygame.display.update()
color = (0,0,0) # Current drawing color
thickness = 1
savedPath = '' #Current path of file

run = True
while run:
    #Main loop for mouse collision
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            window = Tk()
            window.withdraw()
            #Ask the user if they want to save before closing
            if pygame.display.get_caption()[0].count('*') > 0: 
               if messagebox.askyesno("Save Work?", "Would you like to save before closing?"):
                  # If they have already saved the file simply save to that path otherwise they need to chose a location
                  if savedPath != "":
                     save(cols, rows, grid.showGrid, grid.getGrid(),savedPath)
                  else:
                     path = showFileNav()
                     if path:
                        savedPath = path
                        save(cols, rows, grid.showGrid, grid.getGrid(),savedPath)
            run = False
         
        if pygame.mouse.get_pressed()[0]: #See if the user has clicked or dragged their mouse
            try:
                pos = pygame.mouse.get_pos()
                if pos[1] >= grid.height: # If the mouse is below the main drawing grid
                    if pos[0] >= tools.startx and pos[0] <= tools.startx + tools.width and pos[1] >= tools.starty and pos[1] <+ tools.starty + tools.height: #If the mouse ic clicking on the tools grid
                        tools.drawGrid() #Redraw the grid so that we dont see the red highlight
                        buttons = ['D', 'E', 'C']
                        tools.setText(buttons)                      
                        clicked = tools.clicked(pos)
                        clicked.show(grid.screen, (255,0,0), 1, True)

                        #Depending what tool they click
                        if clicked.text == 'D': #Draw tool  
                            color = (0,0,0)
                        elif clicked.text == 'E': #Erase tool
                            color = (255,255,255)
                        elif clicked.text == 'C':# Clear grid tool
                            grid.clearGrid()
                            tools.drawGrid() #Redraw the grid so that we dont see the red highlight
                            buttons = ['D', 'E', 'C']
                            tools.setText(buttons)
                            l = tools.getGrid()
                            l[0][0].show(grid.screen, (255,0,0),1, True)

                    #If they click on the save menu 
                    elif pos[0] >= saveMenu.startx and pos[0] <= saveMenu.startx + saveMenu.width and pos[1] >= saveMenu.starty and pos[1] <= saveMenu.starty + saveMenu.height:
                        clicked = saveMenu.clicked(pos)

                        if clicked.text == 'Erase': # Erase the label
                            win.fill(pygame.Color('black'),(10,5,wid-20, 35))
                            labeltext = ''
                        elif clicked.text == 'Open': #otherwise open
                            path = showFileNav(True)
                            if path:
                               openFile(path)
                               savedPath = path
                              #open file
                        elif clicked.text == 'Read':
                            letter = obtain(cols,rows,grid.getGrid())
                            centerX += 5
                            labeltext = labeltext + letter
                            win.fill(pygame.Color('black'),(10,5,wid-20, 35))
                            font = pygame.font.Font('freesansbold.ttf', 24)
                            label = font.render(labeltext, True, [255,0,0])
                            labelRect = label.get_rect()
                            labelRect.center = (40 + centerX,20)
                            win.blit(label,labelRect)


                            
                else:                                    
                    #otherwise draw the pixels accoding to the line thickness
                      name = pygame.display.get_caption()[0]
                      if name.find("*") < 1:
                         changeCaption(name + '*')

                      clicked = grid.clicked(pos)
                      clicked.click(grid.screen,color)
                      if thickness == 2:
                          for pixel in clicked.neighbors:
                              pixel.click(grid.screen, color)
                      elif thickness == 3:
                          for pixel in clicked.neighbors:
                              pixel.click(grid.screen, color)
                              for p in pixel.neighbors:
                                  p.click(grid.screen, color)
                      elif thickness == 4:
                          for pixel in clicked.neighbors:
                              pixel.click(grid.screen, color)
                              for p in pixel.neighbors:
                                  p.click(grid.screen, color)
                                  for x in p.neighbors:
                                      x.click(grid.screen, color)
                                         
                pygame.display.update()
            except AttributeError:
                pass

pygame.quit()