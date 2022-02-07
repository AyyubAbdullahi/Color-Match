# Color Game

import pygame
import random
import time

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Color Game')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 

# User-defined classes

class Game:
   def __init__(self, surface):
      # === universal game objects
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === Color Match specific objects
      self.score_mismatch = 0
      self.score_match = 0
      self.colors = ['red', 'yellow', 'blue', 'green']
      self.tile1 = Tile('white', 312, 133, 63, 133, self.surface)
      self.tile2 = Tile('white', 125, 133, 63, 133, self.surface)
      self.tiles = [self.tile1, self.tile2]
      self.other_tile = None
      
   def play(self):
      # plays the game until the player exits
      # self is the Game itself
      while not self.close_clicked:
         self.handle_events()
         self.draw()
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS)
      
   def handle_events(self):
      # Handle every event appropiatly
      # self is the Game itself
      
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up(event.pos)
   
   def handle_mouse_up(self, position):
      # handles the mouse up event
      # self is the Game
      # position is the coordinates of the cursor
      for tile in self.tiles:
         if tile.is_selected(position) and tile.is_white():
            self.randomize(tile)
            self.draw()
            self.check_match(tile)   
            
   def randomize(self,tile):
      # select a random color for the color list for the tile to change into
      # self is the game
      # tile is Tile who's color is being changed
      new_color = random.choice(self.colors)
      tile.change_color(new_color)
      
   def check_match(self, tile):
      # assigns tiles to a variable other_tile. when both variables have an appropiate value, compare them and see if they match
      # self is the game
      # tile is the tile thats going to be checked
      if self.other_tile is None:
         self.other_tile = tile
      elif tile is not self.other_tile:
         if tile.check_match(self.other_tile):
            self.score_match+=1
         else:
            self.score_mismatch+=1
         time.sleep(1)
         self.other_tile = None   
         
   def draw(self):
      # Draw all game objects
      # self is the Game itself
      
      self.surface.fill(self.bg_color)
      self.tile1.draw()
      self.tile2.draw()
      self.draw_score()
      pygame.display.update()
      
   def draw_score(self):
      # draws score at the top left corner of the window's surface
      score_string_mismatch = 'Mismatch: ' + str(self.score_mismatch)
      score_string_match = 'Match: ' + str(self.score_match)
      font_size = 42
      fg_color = pygame.Color('white') # game = Game(w_surface)
      # bg_color = pygame.Color('black')
      
      # Step 1 create a font object
      font = pygame.font.SysFont('',font_size) # SysFont is a function
      # Step 2 Creating a textbox by rendering the font
      text_box_right = font.render(score_string_mismatch,True,fg_color,self.bg_color)
      text_box_left = font.render(score_string_match,True,fg_color,self.bg_color)
      # Step 3 Compute the location of top_left corner of the text_box on the target surface
      # get dimensions of the text box and screen
      txt_width, txt_height = font.size(score_string_mismatch)
      surface_width, surface_height = self.surface.get_size()
      location_right = (surface_width - txt_width,0)
      location_left = (0,0)
      # Step 4 
      self.surface.blit(text_box_right,location_right) 
      self.surface.blit(text_box_left,location_left)
      
   def update(self):
      #update the game objects
      if self.other_tile == None:
         self.tile1.reset()
         self.tile2.reset()
      
   def decide_continue(self):
      # Check if the game should continue
      # self is the Game
      if self.score_mismatch >= 5:
         self.continue_game = False
      
class Tile:
   # An object of this class represents a paddle that the players use to move
   def __init__(self, color, left , top, width, height, surface):
      # self is the Paddle being initialzed
      # top is the int representing the top of the paddle
      # left is the int representing the left of the Paddle
      # width is the int representing the width of the Paddle
      # height is the int representing the height of the Paddle
      # surface is the window's pygame.Suface object
      self.color = color
      self.left = left
      self.top = top
      self.width = width
      self.height = height
      self.surface = surface
      self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
      
   def draw(self):
      # draw the tile on the surface
      # self is Tile being drawn
      pygame.draw.rect(self.surface, pygame.Color(self.color), self.rect)
      
   def is_selected(self, position):
      # flip the selected tile
      # position is the coordinates
      return self.rect.collidepoint(position)
   
   def is_white(self):
      # returns self.show_front to see if the card is already flipped
      # self is the tile
      return self.color == 'white'
   
   def change_color(self, new_color):
      # changes the color of the tile
      # self is the tile
      # new_color is a string containing the name of the new color
      self.color = new_color
      
   def reset(self):
      # resets the color of the tile
      # self is the tile being reset
      self.color = 'white'
      
   def get_color(self):
      # returns the color of the tile
      # self is the tile who's color is being checked
      return self.color
   
   def check_match(self, other_tile):
      # checks if another tile matches with itself
      # self is this tile
      # other_tile is another tile that was previously clicked
      color1 = self.get_color()
      color2 = other_tile.get_color()
      return color1 == color2
   
main()