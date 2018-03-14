import pygame
import random
import time


size = width, height = 400, 400
black = [0, 0, 0]
white = [255, 255, 255]
grey = [200, 200, 200]
w = 40
mines = 10
countMarkers = 0
score = 0

def init2DArray(cols, rows):
    arr = [None] * cols
    for i in range(len(arr)):
        arr[i] = [None] * rows
    return arr

def gameOver():
    for i in range(w//2):
        for j in range(w//2):
        	grid[i][j].visible = True
    return True

class Cell():
    def __init__(self, i, j, w):
        self.i = i
        self.j = j
        self.x = i*w
        self.y = j*w
        self.w = w
        self.neighborCount = 0
        self.mine = False
        self.visible = False
        self.marked = False

    def markAsMine(self):
        global countMarkers
        self.marked = True
        countMarkers += 1

    def reveal(self):
        self.visible = True
        if self.neighborCount == 0:
            self.floodFill()

    def floodFill(self):
        for xOff in range(-1, 2):
            for yOff in range(-1, 2):
                i = self.i + xOff
                j = self.j + yOff
                if (i > -1 and i < width//w and j > -1 and j < height//w):
                    neighbor = grid[i][j]
                    if not neighbor.mine and not neighbor.visible:
                        neighbor.reveal()

    def show(self):
        pygame.draw.rect(screen, black, [self.x, self.y, self.w, self.w], 1)
        if self.visible:
            if self.mine:
                pygame.draw.ellipse(screen, black, [self.x+10, self.y+10, self.w-20, self.w-20], 0)
            else:
                pygame.draw.rect(screen, grey, [self.x+1, self.y+1, self.w-2, self.w-2], 0)
                if self.neighborCount > 0:
                    textSurface = text.render(str(self.neighborCount), False, (0, 0, 0))
                    screen.blit(textSurface, (self.x+10, self.y))
        if self.marked:
            pygame.draw.rect(screen, black, [self.x, self.y, self.w, self.w], 1)
            textSurface = text.render('X', False, (220, 0, 0))
            screen.blit(textSurface, (self.x+10, self.y))

    def inCell(self, pos):
        return (pos[0] > self.x and pos[0] < self.x + self.w
                and pos[1] > self.y and pos[1] < self.y + self.w)

    def neighbors(self):
        if self.mine:
            self.neighborCount = -1
        count = 0
        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                i = self.i + xoff
                j = self.j + yoff
                if (i > -1 and i < width//w and j > -1 and j < height//w):
                    neighbor = grid[i][j]
                    if neighbor.mine:
                        count += 1
        self.neighborCount = count


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
text = pygame.font.SysFont('Verdana', 30)
grid = init2DArray(width//10, width//10)

for i in range(w//2):
    for j in range(w//2):
        grid[i][j] = Cell(i, j, w)

mineCount = 0
while mineCount < mines:
    i = random.randint(0, (width//w)-1)
    j = random.randint(0, (height//w)-1)
    if not grid[i][j].mine:
        grid[i][j].mine = True
        mineCount += 1

for i in range(w//2):
    for j in range(w//2):
        grid[i][j].neighbors()

lost = False
win = False
end = False
while not end:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True

#        countMarkers = 0
#        for i in range(w//2):
#               for j in range(w//2):
#                   if grid[i][j].marked:
#                       countMarkers += 1

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
           mousePos = pygame.mouse.get_pos()
           print(((mousePos[0]//w)+1, (mousePos[1]//w)+1))
           for i in range(w//2):
               for j in range(w//2):
                   if grid[i][j].inCell(mousePos) and not grid[i][j].visible:
                      grid[i][j].marked = False
                      grid[i][j].reveal()
                      if grid[i][j].mine:
                          lost = True
                          gameOver()
#                          end = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
           mousePos = pygame.mouse.get_pos()
           for i in range(w//2):
               for j in range(w//2):
                   if grid[i][j].inCell(mousePos):
                      if grid[i][j].marked == True and not grid[i][j].visible:
                         grid[i][j].marked = False
                         countMarkers -= 1
                      elif not grid[i][j].visible:
                         grid[i][j].markAsMine()
                         if grid[i][j].marked and grid[i][j].mine:
                             score += 1
                             print(score)

    if score == mines:
        win = True
        gameOver()

    for i in range(w//2):
        for j in range(w//2):
            grid[i][j].show()

    if lost:
        pygame.display.set_caption('GAME OVER!')
    elif win:
        pygame.display.set_caption('YOU WON!')
    else:
        pygame.display.set_caption('Mines on field: ' + str(mines) + '  /  ' + 'Markers: ' + str(countMarkers))

    clock.tick()
    pygame.display.update()

time.sleep(0)
pygame.quit()
#quit()