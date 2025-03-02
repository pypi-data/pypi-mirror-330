import pygame


class shapeManager:
  def __init__(self, screen):
    self.screen = screen
    self.rects = []
    self.lines = []
    self.circles = []
    self.polygon = []
      

  def update(self):
    for rect in self.rects:
      pygame.draw.rect(self.screen, rect[4], pygame.Rect(rect[0], rect[1], rect[2], rect[3]))
    for line in self.lines:
      pygame.draw.line(self.screen, line[2], line[0], line[1], line[3])
    for circle in self.circles:
      pygame.draw.circle(self.screen, circle[0], circle[1], circle[2], circle[3])
    for item in self.polygon:
      pygame.draw.polygon(self.screen, item[0], item[1], item[2])

  def addRect(self, x, y, width, height, color, ID):
    self.rects.append([x, y, width, height, color, ID])

  def addLine(self, x1, y1, x2, y2, color, ID, width=1):
    self.lines.append([(x1, y1), (x2, y2), color, width, ID])

  def addCircle(self, centerPos, radius, color, width, ID):
    self.circles.append([color, centerPos, radius, width, ID])

  def addPolygon(self, color, points, width, ID):
    self.polygon.append([color, points, width, ID])

  def remove(self, type, ID):
    def rect(ID):
      for rect in self.rects:
        if rect[5] == ID:
          self.rects.remove(rect)
    def line(ID):
      for line in self.lines:
        if line[4] == ID:
          self.lines.remove(line)
    def circle(ID):
      for circle in self.circles:
        if circle[4] == ID:
          self.circles.remove(circle)
    def polygon(ID):
      for polygon in self.polygon:
        if polygon[3] == ID:
          self.polygon.remove(polygon)
          
    if type == "rect":
      rect(ID)
    elif type == "line":
      line(ID)
    elif type == "polygon":
      polygon(ID)
    else:
      circle(ID)


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


class Images:
  def __init__(self, screen):
      self.screen = screen
      self.images = {}  # Dictionary to store images with their properties

  def update(self):
      for image_data in self.images.values():
          self.screen.blit(image_data["image"], image_data["pos"])

  def addImage(self, path, pos, ID):
      if ID not in self.images:
          self.images[ID] = {
              "image": pygame.image.load(path).convert_alpha(),
              "pos": pos
          }
      else:
          raise ValueError(f"An image with ID '{ID}' already exists.")
