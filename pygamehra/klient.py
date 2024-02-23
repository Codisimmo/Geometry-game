import pygame
import sys
import subprocess
import random

# Initialize
pygame.init()
pygame.mixer.init()

synthsong = pygame.mixer.Sound('synthsong.mp3')
pohybmysi = pygame.mixer.Sound('pohybmysi.mp3')
kliknuti = pygame.mixer.Sound('kliknuti.mp3')
synthsong.set_volume(0.5)
synthsong.play(loops=-1)

screen = pygame.display.set_mode((360, 480))
pygame.display.set_caption("Geometry game")
pygame.display.set_icon(pygame.image.load('Logo.png'))

width, height = 360, 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50,100,50)
skore = 0
moving_objects = []
last_spawn_time = pygame.time.get_ticks()

# OBJEKTY
class MovingObject:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.alpha = 30
        self.obj_surface = pygame.Surface((self.width, self.height))
        self.obj_surface.set_alpha(self.alpha)
        self.obj_surface.fill(GREY)

    def draw(self, screen):
        screen.blit(self.obj_surface, (self.x, self.y))

    def update(self):
        self.y += self.speed

    def set_alpha(self, alpha):
        self.alpha = alpha

def create_moving_object():
    object_type = random.choice(['small_square', 'small_square', 'large_square', 'horizontal_rectangle', 'vertical_rectangle'])
    speed = 1

    if object_type == 'small_square':
        size = 35
        return MovingObject(random.randint(5, width - size-5), -35, size, size, speed)
    elif object_type == 'large_square':
        size = random.randint(55, 80)
        return MovingObject(random.randint(5, width - size-5), -size, size, size, speed)
    elif object_type == 'horizontal_rectangle':
        size = random.randint(90, 130)
        return MovingObject(random.randint(5, width - size-5), -25, size, 25, speed)
    else:  # vertical_rectangle
        size = random.randint(90, 130)
        return MovingObject(random.randint(5, width - 30), -size, 25, size, speed)
    
font = pygame.font.SysFont(None, 36)
font2 = pygame.font.SysFont(None, 25)

def render_text(text, font, position, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.hovered = False

    def draw(self, screen):
        if self.mys_na_tlacitku():
            
            button_color = (50,100,50)
            if not self.hovered:
                pohybmysi.play()
                self.hovered = True
        else:
            button_color = BLACK
            self.hovered = False
        # Vykreslit tlačítko
        pygame.draw.rect(screen, button_color, (self.x, self.y, self.width, self.height), 2)
        render_text(self.text, font, (self.x + 10, self.y + 10), BLACK)

    def mys_na_tlacitku(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.mys_na_tlacitku():
                if self.action:
                    synthsong.stop() 
                    kliknuti.play()
                    self.action()
                    

def play_game():
    global skore
    result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    output = result.stdout
    skore = int(output.split()[-1])
    synthsong.play()

def quit_game():
    pygame.quit()
    sys.exit()

play_button = Button("Hrát", 100, 200, 160, 40, play_game)
quit_button = Button("Odejít", 100, 250, 160, 40, quit_game)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        play_button.handle_event(event)
        quit_button.handle_event(event)

    screen.fill(WHITE)
    render_text("Vítej ve hře!", font, (110, 40), BLACK)
    if skore > 0:
        render_text(f"Zajištěných perel: {skore}", font2, (100, 100), BLACK)
    else:
        render_text("Zabezpeč co nejvíce zelených perel,", font2, (34, 100), BLACK)
        render_text("žluté ti přidají čas a pozastaví nepřítele.", font2, (22, 130), BLACK) 

    play_button.draw(screen)
    quit_button.draw(screen)

    # OBJEKTY 
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > 2000:
        if len(moving_objects) < 10 and random.randint(1, 100) < 5:
            obj = create_moving_object()
            moving_objects.append(obj)
            last_spawn_time = current_time
    # Vykreslení objektů
    for obj in moving_objects[:]:
        obj.update()
        obj.draw(screen)
        # Odstranění objektu po opuštění oherní plochy
        if obj.y > height:
            moving_objects.remove(obj)
        
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(60)

pygame.quit()