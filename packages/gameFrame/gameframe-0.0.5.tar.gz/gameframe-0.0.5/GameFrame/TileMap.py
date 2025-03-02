import pygame
import ast

class Camera:
  def __init__(self, screen, pos=(0, 0)):
    self.screen = screen
    self.pos = pos

  def update(self, pos):
    self.pos = pos


class TileMap:
  def __init__(self, screen, tileKeyFile, dim, scale, speed = 5, sprintSpeed = 8, DIM=(500, 500)):
      self.screen = screen
      self.tileKey = read_tile_key(tileKeyFile)  
      self.tiles = []  # A list of tile data [(tile_id, (x, y))]
      self.images = {}  # A dictionary to store loaded images
      self.dim = (dim[0]*scale, dim[1]*scale)
      self.speed = speed
      self.Sspeed = sprintSpeed
      self.Editor = False
      self.DIM = DIM
      self.editClick = False
      self.tilePick = False
      self.editorInfo = {}
      self.editorOffset = 0
      self.NewTileMap = False
      self.editorTilePick = False
      self.collide = []
      self.keyCollide = "CT"

      # Load images for all tile IDs
      for tile_id, file_path in self.tileKey.items():
          image = pygame.image.load(file_path).convert_alpha()
          self.images[tile_id] = pygame.transform.scale(image, self.dim)

  def createTileMap(self, fileName):
      self.NewTileMap = fileName
      self.tiles = read_tile_map(fileName)  # Assume this returns a list of tuples [(tile_id, (x, y))]

  def editor(self, offset, speed):
    if self.editClick is False and pygame.mouse.get_pressed()[0]:
        self.editClick = True
        x, y = pygame.mouse.get_pos()
        box_width, box_height = self.dim
        offset_x, offset_y = offset
        # Reverse the rendering adjustments
        adjusted_x = x + offset_x + speed
        adjusted_y = y + offset_y + speed
        # Calculate the top-left position of the box
        box_x = int(((adjusted_x // box_width) * box_width) / self.dim[0])
        box_y = int(((adjusted_y // box_height) * box_height) / self.dim[1])
        self.editClick = True
        self.tilePick = (box_x, box_y)
        self.editorTilePick = [box_x, box_y]
    else:
       #open side panel and make selection
       self.Editor_side_panel(speed, offset)
       if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.editClick = False
                self.editorInfo = {}

  def Editor_side_panel(self, speed, screenOff):
       self.editorInfo={}
       #create basic
       padding = int(self.dim[0] // 10)
       if self.editorTilePick is not False:
          x = ((self.editorTilePick[0]*self.dim[0])-(self.dim[0]*19.5))
       else:
          x = (self.DIM[0]-self.dim[0])-(padding*2)
       width = self.dim[0]+padding*2
       self.editorInfo["back"] = {'pos':(x, 0), 'dim':(width, self.DIM[1]), 'rect':pygame.Rect((x, 0), (width, self.DIM[1]))}
       #add images
       pos = (x+padding, 0)
       imageList = []
       for key, image in self.tileKey.items():
          imageList.append([pos, key])
          pos = (pos[0], (pos[1] + padding)+self.dim[1])
       self.editorInfo['images'] = imageList
       #check for click
       self.checkTileClicked(padding, self.editorOffset, speed, screenOff)
       #create offset for scrolling
       if pygame.key.get_pressed()[pygame.K_UP]:
            self.editorOffset += int(self.dim[1]//5)
       if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.editorOffset -= int(self.dim[1]//5)

  def checkTileClicked(self, padding, offset, speed, off):
     if pygame.key.get_pressed()[pygame.K_c] and self.editClick:
            x, y = pygame.mouse.get_pos()
            box_width, box_height = self.dim
            offset_x, offset_y = off
            # Reverse the rendering adjustments
            adjusted_x = x + offset_x + speed
            adjusted_y = y + offset_y + speed
            # Calculate the top-left position of the box
            box_x = int(((adjusted_x // box_width) * box_width) / self.dim[0])
            box_y = int(((adjusted_y // box_height) * box_height) / self.dim[1])
            self.tiles.append([self.keyCollide, (box_x, box_y)])
     if pygame.mouse.get_pressed()[0] and self.editorInfo['back']['rect'].collidepoint(pygame.mouse.get_pos()):
        y = pygame.mouse.get_pos()[1]
        box_height = int(self.dim[1]+(self.dim[1]//2))
        # Reverse the rendering adjustments
        adjusted_y =( y - offset)-padding*2
        box_y = (int(((adjusted_y // box_height) * box_height) / self.dim[1]))+1
        #add to tilemap
        if box_y in range(len(self.editorInfo['images'])):
            #remove past tile
            for tile in self.tiles:
               if tile[1] == self.tilePick:
                  self.tiles.remove(tile)
            #create tile
            self.editClick = False
            key = self.editorInfo['images'][box_y][1]
            self.tiles.append([key, self.tilePick])
     #save to file
     if self.NewTileMap is not False:
        with open(self.NewTileMap, 'w') as file:
            file.write(str(self.tiles))
        
          
  def editorUpdate(self, speed, offset):
     if self.editClick:
        back=self.editorInfo['back']
        images = self.editorInfo['images']
        for item in self.tiles:
           if item[0] == self.keyCollide:
            pos = item[1]
            x = ((pos[0] * self.dim[0]) - offset[0]) - speed
            y = ((pos[1] * self.dim[1]) - offset[1]) - speed
            pygame.draw.rect(self.screen, 'red', pygame.Rect((x, y), self.dim))
        pygame.draw.rect(self.screen, 'black', back['rect'])
        for image in images:
           x = image[0][0]
           y = image[0][1] + self.editorOffset
           self.screen.blit(self.images[image[1]], (x, y))
       
  def display(self, offset):
      if pygame.key.get_mods() & pygame.KMOD_SHIFT:
         speed = self.Sspeed
      else:
         speed = self.speed

      pygame.event.get()
      if self.Editor:
         self.editor(offset, speed)

      for tile in self.tiles:
          tile_id, position = tile
          x = ((position[0] * self.dim[0]) - offset[0]) - speed
          y = ((position[1] * self.dim[1]) - offset[1]) - speed
          if tile_id != self.keyCollide:
            self.screen.blit(self.images[tile_id], (x, y))
      self.editorUpdate(speed, offset)

  def get_collision_tiles(self):
     collisions = []
     for tile in self.tiles:
        if tile[0] == self.keyCollide:
           collisions.append([tile[1], self.dim])
     return collisions

class Player:
  def __init__(self, screen, speed=5, sprintSpeed = 8):
        self.screen = screen
        self.init = False
        self.speed=speed
        self.Sspeed = sprintSpeed

  def INIT(self, pos, folderData, scale, dim=32, Size=(32, 32)):
      self.Scale = scale
      self.Dim = dim
      self.spw = pos
      self.init = True
      self.pos = pos
      self.sprites = self.sprite_list(folderData)
      self.count = 0
      self.Top = len(folderData)
      self.rect = pygame.Rect(pos, Size)
      self.Size = Size

  def sprite_list(self, folder):
     data = {}
     counter = 0
     scale, dim = self.Scale, self.Dim
     for item in folder:
        counter+=1
        data[counter] = pygame.transform.scale(pygame.image.load(item), (scale*dim, scale*dim))
     return data


  def update(self):
     if self.init is True:
      self.count+=1
      if self.count>self.Top:
         self.count = 1
      self.screen.blit(self.sprites[self.count], self.spw)

  def key_movement(self, dt=1):
      keys = pygame.key.get_pressed()
      x, y = self.pos
      speed= self.speed
      if pygame.key.get_mods() & pygame.KMOD_SHIFT:
         speed = self.Sspeed

      if keys[pygame.K_w]:
          y -= speed * dt
      if keys[pygame.K_a]:
          x -= speed * dt
      if keys[pygame.K_s]:
          y += speed * dt
      if keys[pygame.K_d]:
          x += speed * dt
      self.pos = (x, y)



           



def read_tile_key(file):
    with open(file, "r") as file:
        content = file.read()
        # Safely evaluate the dictionary format
        return ast.literal_eval(content)

def read_tile_map(file_path):
  with open(file_path, "r") as file:
      content = file.read()
      # Safely evaluate the list format
      return ast.literal_eval(content)
