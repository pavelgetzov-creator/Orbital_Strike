import pygame
import random


pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((400, 700))
pygame.display.set_caption("Orbital Strike")
background = pygame.image.load("Assets/space.png").convert()
background = pygame.transform.scale(background, (400,700))

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
            self.x -= 12
        
        if keys[pygame.K_RIGHT]:
            self.x += 12
        
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
        self.speed = 0.5
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

        self.fire_image = pygame.image.load("Assets/ebullet2.png")
        self.fire_image = pygame.transform.scale(self.fire_image, (15,35))
        
        self.fire_sound = pygame.mixer.Sound("Assets/piw.wav")
        self.state = "ready"

    def fire(self,player_x):
        if self.state == "ready":
            self.state = "fire"
            self.x = player_x + 25
            self.fire_sound.set_volume(0.3)
            self.fire_sound.play()


    def update(self,screen):
        if self.state == "fire":
            self.y -= 20
            screen.blit(self.fire_image, (self.x, self.y))
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

class Lives:
    def __init__(self):
        self.value = 3
        self.font = pygame.font.SysFont("Arial", 24)

    def lose_life(self):
        self.value -= 1

    def draw(self,screen):
        lives_text = self.font.render("Lives: " + str(self.value), True, (255,255,255))
        screen.blit(lives_text, (10,40))

class PowerUps:
    def __init__(self):
            self.x = random.randint(0,340)
            self.y = 0
            self.speed = 2
            self.type = random.choice(("health", "slow"))

            if self.type == "health":
                self.image = pygame.image.load("Assets/hearth.png")
                self.image = pygame.transform.scale(self.image, (40,40))
            else:
                self.image = pygame.image.load("Assets/Hourglass.png")
                self.image = pygame.transform.scale(self.image, (40,40))

    def move(self):
        self.y += self.speed


        if self.y > 700:
            return True
        return False
    
    
    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))

class Menu():
    def __init__(self, x,y ,width,height,text, image_path = None):
        self.rect = pygame.Rect(x, y , width, height)
        self.text = text
        self.font = pygame.font.SysFont("Arial", 24)

        if image_path is not None:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image,(width,height))
        else:
            self.image = None
            
    def draw(self,screen):
        
        if self.image is not None:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            self.button = pygame.draw.rect(screen, (255,0,0), self.rect)
            self.text_button = self.font.render(self.text, True, (255,255,255))
            text_rect = self.text_button.get_rect(center = self.rect.center)
            screen.blit(self.text_button, text_rect)



    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Sound:
    def __init__(self):
        pygame.mixer.music.load("Assets/spacesong.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def mute(self):
        pygame.mixer.music.pause()


    def unmute(self):
        pygame.mixer.music.unpause()

sound = Sound()
player = Player()
villan = Villan()
laser = Laser()
score = Score()
lives = Lives()

menu_font = pygame.font.SysFont("impact", 50)
title_center_pos = (200, 150)

start_button = Menu(120, 300, 150, 50 , "Start")
quit_button = Menu(120, 400, 150, 50, "Quit")
play_again_button = Menu(120, 500, 150, 50 , "Play Again")
back_to_menu = Menu(120, 600, 150, 50, "Back To Menu")
continue_button = Menu(120, 400, 150, 50 , "Continue")
pause_button = Menu(350,25, 30, 30, "", "Assets/pause.png" )
sound_button = Menu(310, 25, 30, 30, "", "Assets/musicOn.png")



game_over_font = pygame.font.SysFont("impact", 50)
game_state = "menu"

clock = pygame.time.Clock()

level_2 = False
level_3 = False
is_muted = False
current_level_text = ""
power_up = None


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type== pygame.MOUSEBUTTONDOWN:
            if game_state == "menu" and start_button.is_clicked(event.pos):
                player = Player()
                villan = Villan()
                laser = Laser()
                score = Score()
                lives = Lives()
                level_2 = False
                level_3 = False
                game_state = "playing"
                
            if game_state == "menu" and quit_button.is_clicked(event.pos):
                running = False


            if game_state == "ending" and play_again_button.is_clicked(event.pos):
                player = Player()
                villan = Villan()
                laser = Laser()
                score = Score()
                lives = Lives()
                level_2 = False
                level_3 = False
                game_state = "playing"

            if game_state == "ending" and back_to_menu.is_clicked(event.pos):
                game_state = "menu"

            if game_state == "level_up" and continue_button.is_clicked(event.pos):
                game_state = "playing"


            if game_state == "playing" and pause_button.is_clicked(event.pos):
                pause_button.image = pygame.image.load("Assets/return.png")
                pause_button.image = pygame.transform.scale(pause_button.image, (30,30))
                game_state = "paused"

            elif game_state == "paused" and pause_button.is_clicked(event.pos):
                pause_button.image = pygame.image.load("Assets/pause.png")
                pause_button.image = pygame.transform.scale(pause_button.image, (30,30))
                game_state = "playing"
             
            if (game_state == "playing" or game_state == "paused" or game_state == "ending") and not is_muted and sound_button.is_clicked(event.pos):
                sound.mute()
                sound_button.image = pygame.image.load("Assets/musicOff.png")
                sound_button.image = pygame.transform.scale(sound_button.image, (30,30))
                is_muted = True
            elif (game_state == "playing" or game_state == "paused" or game_state == "ending") and is_muted and sound_button.is_clicked(event.pos):
                sound.unmute()
                sound_button.image = pygame.image.load("Assets/musicOn.png")
                sound_button.image = pygame.transform.scale(sound_button.image, (30,30))
                is_muted = False
                


            


    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        laser.fire(player.x)


    screen.blit(background, (0,0))

    if game_state == "menu":
        game_name = menu_font.render("Orbital Strike", True, (255,255,255))
        menu_text_rect = game_name.get_rect(center = title_center_pos)
        screen.blit(game_name, menu_text_rect)

        start_button.draw(screen)
        quit_button.draw(screen)


    if game_state == "paused":
        pause_name = menu_font.render("Game Paused!", True, (255,255,255))
        pause_name_rect = pause_name.get_rect(center = (200,300))
        screen.blit(pause_name, pause_name_rect)
        pause_button.draw(screen)
        sound_button.draw(screen)


    if game_state == "playing":
        
        player.move()
        player.draw(screen)
        villan.draw(screen)
        laser.update(screen)
        score.draw(screen)
        if score.value >= 20 and not level_2:
            game_state = "level_up"
            level_2 = True
            current_level_text = "Level 2!"
        elif score.value >= 40 and not level_3:
            game_state = "level_up"
            level_3 = True
            current_level_text = "Level 3!"

        lives.draw(screen)
        pause_button.draw(screen)   
        sound_button.draw(screen)

        if villan.move():
            lives.lose_life()
            villan.y = 0

        if lives.value == 0:
            game_state = "ending"

        if power_up is not None:
            power_up.draw(screen)
            if power_up.move():
                power_up = None


        player_rect = pygame.Rect(player.x,player.y, 60, 60)        
        villan_rect= pygame.Rect(villan.x, villan.y, 60,60)
        laser_rect = pygame.Rect(laser.x, laser.y, 10, 10)


        if power_up is not None:
            power_up_rect = pygame.Rect(power_up.x,power_up.y, 40,40)
            if player_rect.colliderect(power_up_rect):
                if power_up.type == "health":
                    lives.value += 1
                else:
                    villan.speed = villan.speed / 2
                power_up = None
        

        if laser.state == "fire" and villan_rect.colliderect(laser_rect):
            villan.x = random.randint(0,340)
            villan.y = 0
            if score.value >= 20:
                villan.speed += 0.4
            else:
                villan.speed += 0.2

            laser.y = 600
            laser.state = "ready" 
            score.add_point()
            if power_up is None and random.random() < 0.3:
                power_up = PowerUps()
                if score.value >= 20:
                    power_up.speed += 2

    if game_state == "level_up":
        surface = pygame.Surface((400, 700), pygame.SRCALPHA)
        surface.fill((0,0,0,180))
        screen.blit(surface,(0,0))

        level_up_text = game_over_font.render(current_level_text, True, (0,255,100))
        level_up_rect = level_up_text.get_rect(center = (200,300))
        screen.blit(level_up_text,level_up_rect)

        continue_button.draw(screen)

   
        
    if game_state == "ending":
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
        back_to_menu.draw(screen)
        sound_button.draw(screen)


    pygame.display.update()
    clock.tick(60)



pygame.quit()