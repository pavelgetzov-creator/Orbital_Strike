import pygame
import random


pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((400, 700))
pygame.display.set_caption("Orbital Strike")
background = pygame.image.load("Assets/space.png").convert()
background = pygame.transform.scale(background, (400,700))
pygame.mixer.music.load("Assets/spacesong.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

running = True
class Player:
    def __init__(self):
        self.image = pygame.image.load("Assets/ship_b.png")
        self.image = pygame.transform.scale(self.image, (60,60))
        self.x = 180
        self.y = 600

    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 0.5
        
        if keys[pygame.K_RIGHT]:
            self.x += 0.5
        
        if self.x < 0:
            self.x = 0
        elif self.x > 340:
            self.x = 340
class Villan:
    def __init__(self):
        self.image = pygame.image.load("Assets/ship_a.png")
        self.image = pygame.transform.scale(self.image, (60,60))

        self.x = random.randint(0,340)
        self.y = 0
        self.speed = 0.02
    def move(self):
        self.y += self.speed
        
        if self.y > 700:
            return True
        return False


    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))


class Laser:
    def __init__(self):
        self.x = 0
        self.y = 600

        self.state = "ready"

    def fire(self,player_x):
        if self.state == "ready":
            self.state = "fire"
            self.x = player_x + 5
            fire_sound = pygame.mixer.Sound("Assets/piw.wav")
            fire_sound.set_volume(0.3)
            fire_sound.play()


    def update(self,screen):
        if self.state == "fire":
            self.y -= 5
            pygame.draw.rect(screen, (255,255,0), (self.x , self.y , 10, 10))
            if self.y < 0:
                self.y = 600
                self.state = "ready"
class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.SysFont("Arial", 24)

    def add_point(self):
        self.value += 1

    def draw(self,screen):
        score_text = self.font.render("Points: " + str(self.value), True, (255,255,255))
        screen.blit(score_text, (10,10))

class Game_Over_Button():
    def __init__(self, x,y ,width,height,text):
        self.rect = pygame.Rect(x, y , width, height)
        self.text = text
        self.font = pygame.font.SysFont("Arial", 24)
    def draw(self,screen):
        
        self.button = pygame.draw.rect(screen, (255,0,0), self.rect)
        self.text_button = self.font.render(self.text, True, (255,255,255))
        text_rect = self.text_button.get_rect(center = self.rect.center)
        screen.blit(self.text_button, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


player = Player()
villan = Villan()
laser = Laser()
score = Score()
play_again_button = Game_Over_Button(120,500, 150, 50 , "Play Again")
game_over_font = pygame.font.SysFont("impact", 50)
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type== pygame.MOUSEBUTTONDOWN:
            if game_over and play_again_button.is_clicked(event.pos):
                player = Player()
                villan = Villan()
                laser = Laser()
                score = Score()
                game_over = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        laser.fire(player.x)



    screen.blit(background, (0,0))
    if not game_over:
        
        player.move()
        game_over = villan.move()
        player.draw(screen)
        villan.draw(screen)
        laser.update(screen)
        score.draw(screen)
    
        villan_rect= pygame.Rect(villan.x, villan.y, 60,60)
        laser_rect = pygame.Rect(laser.x, laser.y, 10, 10)


        if laser.state == "fire" and villan_rect.colliderect(laser_rect):
            villan.x = random.randint(0,340)
            villan.y = 0
            villan.speed += 0.01
            laser.y = 600
            laser.state = "ready" 
            score.add_point()
            
        
    if game_over:
        surface = pygame.Surface((400, 700), pygame.SRCALPHA)
        surface.fill((0,0,0,180))
        screen.blit(surface,(0,0))

        center_pos = (200, 300)
        cx, cy = center_pos

        offsets = [(3,3), (3,-3), (-3,3), (-3,-3), (3,0), (-3,0), (0,3), (0,-3)]
        glow_text = game_over_font.render("GAME OVER!", True, (120,0,0))

        for dx, dy in offsets:
            glow_pos = (cx + dx, cy + dy)
            glow_rect = glow_text.get_rect(center = glow_pos)
            screen.blit(glow_text, glow_rect)

        game_over_text = game_over_font.render("GAME OVER!", True, (255,0,0))
        text_rect = game_over_text.get_rect(center = center_pos)
        screen.blit(game_over_text, text_rect)

        play_again_button.draw(screen)  

    pygame.display.update()

pygame.quit()