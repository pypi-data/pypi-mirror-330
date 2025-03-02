import pygame
from GameFrame import Math


class Inputmanager:
  def mousePos(self):
    return pygame.mouse.get_pos()


class text:
  def __init__(self, screen):
    pygame.font.init()
    self.text = []
    self.screen = screen

  def update(self):
    for text in self.text:
      self.screen.blit(text[0], text[1])

  def renderText(self, text, x, y, color, size):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    self.text.append([text_surface, (x, y)])

  def clearText(self):
    self.text = []




class Buttons:
  def __init__(self, screen):
    self.screen = screen
    self.t = text(screen)
    self.buttons = []
    self.BaseColors = {}
    self.images = {}

  def update(self):
    for button in self.buttons:
      pygame.draw.rect(self.screen, button[2], pygame.Rect(button[0][0], button[0][1], button[1][0], button[1][1]), button[5])
      self.t.update()
      if button[4] is not None:
        self.screen.blit(self.images[button[6]], button[0])

  def addButton(self, pos, size, color, textData, ID, width=0, image=None):
    self.BaseColors[ID] = color
    self.buttons.append([pos, size, color, textData, image, width, ID])
    if textData is not False:
      self.t.renderText(textData[0], pos[0], pos[1], textData[1], textData[2])
    if image is not None:
      self.images[ID] = pygame.image.load(image)

  def changeColor(self, color, ID):
    for x in self.buttons:
      if x[6] == ID:
        self.buttons.remove(x)
        self.buttons.append([x[0], x[1], color, x[3], x[4], x[5], ID])

  def buttonState(self, ID, hoverColor, pressColor):
    for x in self.buttons:
      if x[6] == ID:
        pos = x[0]
        dim = x[1]
        mouse = pygame.mouse.get_pos()
        if Math.is_point_in_rectangle(pos, dim, mouse):
          if pygame.mouse.get_pressed()[0]:
            self.buttons.remove(x)
            self.buttons.append([x[0], x[1], pressColor, x[3], x[4], x[5], ID])
            return "pressed"
          else:
            self.buttons.remove(x)
            self.buttons.append([x[0], x[1], hoverColor, x[3], x[4], x[5], ID])
            return "hovering"
        else:
          self.buttons.remove(x)
          self.buttons.append([x[0], x[1], self.BaseColors[ID], x[3], x[4], x[5], ID])
          return "none"

