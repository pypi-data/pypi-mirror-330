import pygame
from GameFrame.shapesManager import shapeManager, text, Images
from GameFrame.InputManager import Inputmanager, Buttons
from GameFrame.TileMap import TileMap, Player


class GameMaker:

  def __init__(self, width, height, color, caption):
    self.WIDTH = width
    self.HEIGHT = height
    pygame.display.set_caption(caption)
    self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    self.color = color
    self.updates = {"basic": False, "tileMap": False}

  def INIT_basics(self):
    self.updates["basic"] = True
    self.shapes = shapeManager(self.screen)
    self.input = Inputmanager()
    self.text = text(self.screen)
    self.button = Buttons(self.screen)
    self.images = Images(self.screen)

  def INIT_tilemap(self, TileKey, scale = 1, dim = (32, 32),speed =5, Sspeed = 8, DIM=(500, 500)):
    self.updates["tileMap"] = True
    self.tilemap = TileMap(self.screen, TileKey, dim, scale, speed, Sspeed, DIM)
    self.player = Player(self.screen,speed, Sspeed)

  def update_independant_modules(self, offset):
    if self.updates["basic"] is True:
      self.shapes.update()
      self.text.update()
      self.button.update()
      self.images.update()
    if self.updates["tileMap"] is True:
      self.tilemap.display(offset)
      self.player.update()

  def update_display(self, offset=(0, 0)):
    self.screen.fill(self.color)
    self.update_independant_modules(offset)
    pygame.display.update()
    for event in pygame.event.get():
      if event.type is pygame.QUIT:
        pygame.quit()
        quit()

