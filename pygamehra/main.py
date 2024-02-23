import pygame
import random
import time

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init(buffer=1024)

# Nastavení okna hry
width, height = 360, 480
x = width
y = height
screen = pygame.display.set_mode((x, y))

pygame.display.set_icon(pygame.image.load('Logo.png'))
pygame.display.set_caption("Geometry game")
font1 = pygame.font.SysFont("calibri", 24, bold=True)
font2 = pygame.font.SysFont("calibri", 18, bold=True)
font_sizes = [pygame.font.SysFont("calibri", size, bold=True) for size in range(14, 30)]

# Barvy
WHITE = (255, 255, 255)
BLUE = (50,50,50)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (20, 170, 20)
OKR = (230, 140, 0)
# Příprava proměnných
velocity = [0, 0]
acceleration = 1.4
friction = 0.25
pacman_width = 10
moving_objects = []
border_thickness = 3

# Zvuky
sounds = {
    "Soundbonus": pygame.mixer.Sound("soundbonus.mp3"),
    "sound2": pygame.mixer.Sound("sound2.mp3"),
    "sound3": pygame.mixer.Sound("sound3.mp3"),
    "SoundCoin": pygame.mixer.Sound("SoundCoin.mp3")
}
channels = {i: pygame.mixer.Channel(i) for i in range(4)}
channels[2].set_volume(0.4)
channels[3].set_volume(0.4)

# Funkce
def create_food():
    food = [random.randint(15, width - 20), random.randint(65, height - 20)]
    # 15% šance na vytvoření bonusového žetonu
    if random.randint(1, 100) <= 15:
        global second_food, second_food_timer
        second_food = [random.randint(15, width - 20), random.randint(65, height - 20)]
        second_food_timer = time.time()
    return food

def draw_food(screen, food):
    pygame.draw.circle(screen, GREEN, food, 11)

def check_food_collision(object1_pos, object2_pos, object1_radius, object2_radius):
    distance = ((object1_pos[0] - object2_pos[0]) ** 2 + (object1_pos[1] - object2_pos[1]) ** 2) ** 0.5
    return distance <= (object1_radius + object2_radius)

def check_object_collision(pacman, obj):
    pacman_rect = pygame.Rect(
        pacman.position[0] - pacman.radius,
        pacman.position[1] - pacman.radius,
        2 * pacman.radius,
        2 * pacman.radius
    )
    obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    return pacman_rect.colliderect(obj_rect)

time_effect_active = False
time_effect_scale = 1
time_effect_color = BLACK
def update_pacman_size(current_position):
    global acceleration, start_time, pacman, remaining_time1, time_effect_active, time_effect_scale, time_effect_color
    #acceleration += 0.05
    pacman = PacMan(current_position, pacman_width)
    #Animace času
    start_time += 3
    time_effect_active = True
    time_effect_scale = 1.5
    time_effect_color = OKR

# PACMAN
class PacMan:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius
    def draw(self, screen):
        # PacMan ohraničení
        border_width = 3
        border_rect = pygame.Rect(self.position[0] - self.radius - border_width,
                                self.position[1] - self.radius - border_width,
                                2 * (self.radius + border_width), 2 * (self.radius + border_width))
        pygame.draw.rect(screen, BLUE, border_rect)
        # PacMan vnitřek
        pacman_rect = pygame.Rect(self.position[0] - self.radius, self.position[1] - self.radius, 2 * self.radius, 2 * self.radius)
        pygame.draw.rect(screen, YELLOW, pacman_rect)

class MovingObject:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.alpha = 255

    def draw(self, screen):
        self.obj_surface = pygame.Surface((self.width, self.height))
        self.obj_surface.fill(BLUE)
        self.obj_surface.set_alpha(self.alpha)
        
        screen.blit(self.obj_surface, (self.x, self.y))

    def update(self):
        self.y += self.speed
        

    def set_alpha(self, alpha):
        self.alpha = alpha

def create_moving_object():
    object_type = random.choice(['small_square', 'small_square', 'large_square', 'horizontal_rectangle', 'vertical_rectangle'])
    speed = random.uniform(1.5, 3.1)

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

#Inicializace PacMana a žetonů
pacman = PacMan([width // 2, height // 2], pacman_width)
food = create_food()
second_food = None
collision_deactivated = False
collision_deactivated_time = None
start_time = time.time()
last_spawn_time = pygame.time.get_ticks()

def finalskore():
    print("tvoje skore je: ", skore)
    return skore
skore = 0

# Hlavní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    current_time = pygame.time.get_ticks()
    # Výpočet zbývajícího času a ukončení hry po vypršení času
    elapsed_time = time.time() - start_time
    remaining_time1 = max(40 - int(elapsed_time), 0)
    if remaining_time1 == 0:
        running = False
        finalskore()

    # Ovládání
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        velocity[0] -= acceleration
    if keys[pygame.K_RIGHT]:
        velocity[0] += acceleration
    if keys[pygame.K_UP]:
        velocity[1] -= acceleration
    if keys[pygame.K_DOWN]:
        velocity[1] += acceleration
    # Setrvačnost
    velocity[0] *= (1 - friction)
    velocity[1] *= (1 - friction)

    # Aktualizace pozice Pac-Mana
    pacman.position[0] += int(velocity[0])
    pacman.position[1] += int(velocity[1])

    # Ohraničení pohybu PacMan
    pacman.position[0] = max(pacman.radius + 5, min(pacman.position[0], width - pacman.radius - 5))
    pacman.position[1] = max(pacman.radius + 5, min(pacman.position[1], height - pacman.radius - 5))

    # Kontrola kolize s žetonem
    if check_food_collision(pacman.position, food, pacman.radius, 13):
        food = create_food()
        skore_nove = skore + 1
        skore = skore_nove
        channels[0].play(sounds["SoundCoin"])
    # Kontrola kolize s bonusovým žetonem
    if second_food and check_food_collision(pacman.position, second_food, pacman.radius, 13):
        second_food = None
        channels[3].play(sounds["Soundbonus"])
        skore = skore_nove
        collision_deactivated = True
        collision_deactivated_time = time.time()
        channels[2].play(sounds["sound3"])
        # aktualizace velikosti při zachování pozice
        current_position = pacman.position
        update_pacman_size(pacman.position)
        
    # Změna průhlednosti všech pohybujících se objektů
        for obj in moving_objects:
            obj.set_alpha(100)
    
    # Pokud byla deaktivována kolize a uplynulo 6 sekund, obnovení původní průhlednosti objektů
    if collision_deactivated and time.time() - collision_deactivated_time > 6:
        for obj in moving_objects:
            obj.set_alpha(255)
        collision_deactivated = False

    # VYKRESLENÍ
    screen.fill(WHITE)
    pacman.draw(screen)
    draw_food(screen, food)
    if second_food: # Bonusový žeton
        pygame.draw.circle(screen, OKR, second_food, 11)
        if time.time() - second_food_timer > 5:
            second_food = None

# OBJEKTY 
    # Přidání nových objektů do seznamu (max 10)
    if current_time - last_spawn_time > 1000:
        if len(moving_objects) < 10 and random.randint(1, 100) < 7:
            obj = create_moving_object()
            moving_objects.append(obj)
            last_spawn_time = current_time
            if collision_deactivated:
                obj.set_alpha(100)
    # Vykreslení pohybujících se objektů
    for obj in moving_objects[:]:
        obj.update()
        obj.draw(screen)
        # Odstranění objektu po opuštění oherní plochy
        if obj.y > height:
            moving_objects.remove(obj)
        # Detekce kolize s Pac-Manem
        if not collision_deactivated:
            if check_object_collision(pacman, obj):
                channels[0].play(sounds["sound2"])
                finalskore()
                pygame.time.delay(1500)
                running = False

#VYKRESLENÍ NÁPISŮ:
    if collision_deactivated:
        remaining_time = max(0, int(6 - (time.time() - collision_deactivated_time)))
        time_text = font2.render(f"{remaining_time}", True, OKR)
        screen.blit(time_text, (330, 30))

    # Zbývající čas
    if time_effect_active:
        time_effect_scale -= 0.03
        if time_effect_scale <= 1.0:
            time_effect_active = False
            time_effect_scale = 1.0
            time_effect_color = BLACK
    # Výběr fontu z předvytvořených
    font_index = max(0, min(len(font_sizes) - 1, int((18 * time_effect_scale) - 14)))
    scaled_font = font_sizes[font_index]
    # Render textu času s efektem
    time1_text = scaled_font.render(f"{remaining_time1} s", True, time_effect_color)
    text_rect = time1_text.get_rect(center=(335, 18))
    screen.blit(time1_text, text_rect)

    # Skóre
    skore_text = font1.render(f"Skóre: {skore}", True, (0, 0, 0))
    text_rect = skore_text.get_rect(center=(width // 2, 20))
    screen.blit(skore_text, text_rect)

    pygame.draw.rect(screen, BLACK, (0, 0, width, border_thickness))  # Horní okraj
    pygame.draw.rect(screen, BLACK, (0, height - border_thickness, width, border_thickness))  # Dolní okraj
    pygame.draw.rect(screen, BLACK, (0, 0, border_thickness, height))  # Levý okraj
    pygame.draw.rect(screen, BLACK, (width - border_thickness, 0, border_thickness, height))  # Pravý okraj
    
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(60)

pygame.mixer.quit()
pygame.quit()