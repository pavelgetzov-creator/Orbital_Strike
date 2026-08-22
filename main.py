import pygame
import random
import os
import sys
import json

pygame.init()
pygame.mixer.init()

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def save_path():
    if hasattr(sys, "_MEIPASS"):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.abspath(".")
    return os.path.join(exe_dir, "save.json")

def load_data():
    try:
        with open(save_path(), "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"high_score": 0, "coins": 0}


def save_data(data):
    with open(save_path(), "w", encoding="utf-8") as file:
        json.dump(data, file)


game_data = load_data()

screen = pygame.display.set_mode((400, 700))
pygame.display.set_caption("Orbital Strike")
background = pygame.image.load(resource_path("Assets/space.png")).convert()
background = pygame.transform.scale(background, (400,700))

running = True
class Player:
    def __init__(self):
        self.image = pygame.image.load(resource_path("Assets/ship_b.png"))
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
        self.image = pygame.image.load(resource_path("Assets/ship_a.png"))
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

        self.fire_image = pygame.image.load(resource_path("Assets/ebullet2.png"))
        self.fire_image = pygame.transform.scale(self.fire_image, (15,35))
        
        self.fire_sound = pygame.mixer.Sound(resource_path("Assets/piw.wav"))   
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


class Coins:
    def __init__(self, starting_value=0):
        self.value = starting_value
        self.font = pygame.font.SysFont("Arial", 24)

    def add_coin(self):
        self.value += 1
        game_data["coins"] = self.value
        save_data(game_data)

    def draw(self,screen):
        coins_text = self.font.render("Coins: " + str(self.value), True, (255,255,255))
        screen.blit(coins_text, (10,70))

class CoinDrop:
    def __init__(self):
        self.x = random.randint(0,340)
        self.y = 0
        self.speed = 2
        self.image = pygame.image.load(resource_path("Assets/coin.png"))
        self.image = pygame.transform.scale(self.image, (40,35))

    def move(self):
        self.y += self.speed

        if self.y > 700:
            return True
        return False

    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))

class PowerUps:
    def __init__(self):
            self.x = random.randint(0,340)
            self.y = 0
            self.speed = 2
            self.type = random.choice(("health", "slow"))

            if self.type == "health":
                self.image = pygame.image.load(resource_path("Assets/hearth.png"))
                self.image = pygame.transform.scale(self.image, (40,40))
            else:
                self.image = pygame.image.load(resource_path("Assets/Hourglass.png"))
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
            self.image = pygame.image.load(resource_path(image_path))
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
        pygame.mixer.music.load(resource_path("Assets/spacesong.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def mute(self):
        pygame.mixer.music.pause()


    def unmute(self):
        pygame.mixer.music.unpause()

sound = Sound()
player = Player()
villans = [Villan()]
laser = Laser()
score = Score()
lives = Lives()
coins = Coins(game_data["coins"])

menu_font = pygame.font.SysFont("impact", 50)
title_center_pos = (200, 150)

start_button = Menu(120, 300, 150, 50 , "Start")
shop_button = Menu(120, 400, 150, 50, "Shop")
quit_button = Menu(120, 600, 150, 50, "Quit")
free_play_button = Menu(120, 450, 150, 50, "Free Mode")
levels_button = Menu(120, 350, 150, 50, "Level Mode")
play_again_button = Menu(120, 500, 150, 50 , "Play Again")
back_to_menu = Menu(120, 600, 150, 50, "Back To Menu")
continue_button = Menu(120, 400, 150, 50 , "Continue")
pause_button = Menu(350,25, 30, 30, "", resource_path("Assets/pause.png") )
sound_button = Menu(310, 25, 30, 30, "", resource_path("Assets/musicOn.png"))

game_over_font = pygame.font.SysFont("impact", 50)
game_state = "menu"
game_mode = "level_mode"

clock = pygame.time.Clock()

level_2 = False
level_3 = False
level_4 = False
level_finished = False
is_muted = False
current_level_text = ""
power_up = None
coin_drop = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type== pygame.MOUSEBUTTONDOWN:

            if game_state == "menu" and start_button.is_clicked(event.pos):
                game_state = "mode"

            if game_state == "mode" and levels_button.is_clicked(event.pos):
                player = Player()
                villans = [Villan()]
                laser = Laser()
                score = Score()
                lives = Lives()
                coins = Coins(game_data["coins"])
                level_2 = False
                level_3 = False
                level_4 = False
                level_finished = False
                game_state = "playing"
                game_mode = "level_mode"
                power_up = None
                coin_drop = None

            if game_state == "mode" and free_play_button.is_clicked(event.pos):
                player = Player()
                villans = [Villan()]
                laser = Laser()
                score = Score()
                lives = Lives()
                coins = Coins(game_data["coins"])
                game_state = "playing"
                game_mode = "free_play_mode"
                power_up = None
                coin_drop = None

            if game_state == "menu" and quit_button.is_clicked(event.pos):
                running = False

            if game_state == "menu" and shop_button.is_clicked(event.pos):
                game_state = "shop"

            if game_state == "shop" and back_to_menu.is_clicked(event.pos):
                game_state = "menu"
                
            if game_state == "ending" and play_again_button.is_clicked(event.pos):
                player = Player()
                villans = [Villan()]
                laser = Laser()
                score = Score()
                lives = Lives()
                coins = Coins(game_data["coins"])
                level_2 = False
                level_3 = False
                level_4 = False
                level_finished = False
                game_state = "playing"
                power_up = None
                coin_drop = None

            if game_state == "ending" and back_to_menu.is_clicked(event.pos):
                game_state = "menu"

            if game_state == "paused" and back_to_menu.is_clicked(event.pos):
                pause_button.image = pygame.image.load(resource_path("Assets/pause.png"))
                pause_button.image = pygame.transform.scale(pause_button.image, (30,30))
                game_state = "menu"

            if game_state == "level_complete" and back_to_menu.is_clicked(event.pos):
                game_state = "menu"
            elif game_state == "level_complete" and play_again_button.is_clicked(event.pos):
                player = Player()
                villans = [Villan()]
                laser = Laser()
                score = Score()
                lives = Lives()
                coins = Coins(game_data["coins"])
                level_2 = False
                level_3 = False
                level_4 = False
                level_finished = False
                game_state = "playing"
                power_up = None
                coin_drop = None

            if game_state == "level_up" and continue_button.is_clicked(event.pos):
                game_state = "playing"


            if game_state == "playing" and pause_button.is_clicked(event.pos):
                pause_button.image = pygame.image.load(resource_path("Assets/return.png"))
                pause_button.image = pygame.transform.scale(pause_button.image, (30,30))
                game_state = "paused"

            elif game_state == "paused" and pause_button.is_clicked(event.pos):
                pause_button.image = pygame.image.load(resource_path("Assets/pause.png"))
                pause_button.image = pygame.transform.scale(pause_button.image, (30,30))
                game_state = "playing"
             
            if (game_state == "playing" or game_state == "paused" or game_state == "ending") and not is_muted and sound_button.is_clicked(event.pos):
                sound.mute()
                sound_button.image = pygame.image.load(resource_path("Assets/musicOff.png"))
                sound_button.image = pygame.transform.scale(sound_button.image, (30,30))
                is_muted = True
            elif (game_state == "playing" or game_state == "paused" or game_state == "ending") and is_muted and sound_button.is_clicked(event.pos):
                sound.unmute()
                sound_button.image = pygame.image.load(resource_path("Assets/musicOn.png"))
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
        shop_button.draw(screen)

    if game_state == "mode":
        mode_name = menu_font.render("Choose mode!", True, (255,255,255))
        mode_text_rect = mode_name.get_rect(center = title_center_pos)
        screen.blit(mode_name, mode_text_rect)

        free_play_button.draw(screen)
        levels_button.draw(screen)

    if game_state == "shop":
        shop_name = menu_font.render("Shop", True, (255,255,255))
        shop_text_rect = shop_name.get_rect(center = title_center_pos)
        screen.blit(shop_name, shop_text_rect)

        back_to_menu.draw(screen)

    if game_state == "paused":
        pause_name = menu_font.render("Game Paused!", True, (255,255,255))
        pause_name_rect = pause_name.get_rect(center = (200,300))
        screen.blit(pause_name, pause_name_rect)


        pause_button.draw(screen)
        sound_button.draw(screen)
        back_to_menu.draw(screen)


    if game_state == "playing":
        
        player.move()
        player.draw(screen)
        for v in villans:
            v.draw(screen)
        laser.update(screen)
        score.draw(screen)

        if game_mode == "level_mode" and score.value >= 30 and not level_2:
            game_state = "level_up"
            level_2 = True
            current_level_text = "Level 2!"
        elif game_mode == "level_mode" and score.value >= 60 and not level_3:
            game_state = "level_up"
            level_3 = True
            current_level_text = "Level 3!"
            villans.append(Villan())
            for v in villans:
                v.speed = 4
        elif game_mode == "level_mode" and score.value >= 90 and not level_4:
            game_state = "level_up"
            level_4 = True
            current_level_text = "Level 4!"
        elif game_mode == "level_mode" and score.value >= 120 and not level_finished:
            game_state = "level_complete"
            level_finished = True
            current_level_text = ["You successfully", "finished all levels!"]

        coins.draw(screen)
        lives.draw(screen)
        pause_button.draw(screen)   
        sound_button.draw(screen)

        for v in villans:
            if v.move():
                lives.lose_life()
                v.y = 0

        if lives.value == 0:
            game_state = "ending"

        player_rect = pygame.Rect(player.x,player.y, 60, 60)        
        laser_rect = pygame.Rect(laser.x, laser.y, 10, 10)

        if power_up is not None:
            power_up.draw(screen)
            if power_up.move():
                power_up = None

        if coin_drop is not None:
            coin_drop.draw(screen)
            if coin_drop.move():
                coin_drop = None

        if power_up is not None:
            power_up_rect = pygame.Rect(power_up.x,power_up.y, 40,40)
            if player_rect.colliderect(power_up_rect):
                if power_up.type == "health":
                    lives.value += 1
                elif power_up.type == "slow":
                    for v in villans:
                        v.speed = v.speed / 2
                else:
                    coins.add_coin()
                power_up = None


        if coin_drop is not None:
            coin_drop_rect = pygame.Rect(coin_drop.x,coin_drop.y, 40,35)
            if player_rect.colliderect(coin_drop_rect):
                coins.add_coin()
                coin_drop = None



        for v in villans:
            v_rect= pygame.Rect(v.x, v.y, 60,60)

            if laser.state == "fire" and v_rect.colliderect(laser_rect):
                v.x = random.randint(0,340)
                v.y = 0
                if score.value >= 30:
                    v.speed += 0.4
                else:
                    v.speed += 0.2

                laser.y = 600
                laser.state = "ready" 
                score.add_point()

                if power_up is None and random.random() < 0.3:
                    power_up = PowerUps()
                    if score.value >= 30:
                        power_up.speed += 2
                    elif score.value >= 100:
                        power_up.speed += 3


                if coin_drop is None and random.random() < 0.4:
                    coin_drop = CoinDrop()
                    if score.value >= 30:
                        coin_drop.speed += 2
                    elif score.value >= 100:
                        coin_drop.speed += 3
                     

    if game_state == "level_up":
        surface = pygame.Surface((400, 700), pygame.SRCALPHA)
        surface.fill((0,0,0,180))
        screen.blit(surface,(0,0))

        level_up_text = game_over_font.render(current_level_text, True, (0,255,100))
        level_up_rect = level_up_text.get_rect(center = (200,300))
        screen.blit(level_up_text,level_up_rect)

        continue_button.draw(screen)

    if game_state == "level_complete":
        surface = pygame.Surface((400, 700), pygame.SRCALPHA)
        surface.fill((0,0,0,180))
        screen.blit(surface,(0,0))

        y_offset = 270
        for line in current_level_text:
            line_text = game_over_font.render(line, True, (0,255,100))
            line_rect = line_text.get_rect(center = (200,y_offset))
            screen.blit(line_text,line_rect)
            y_offset += 60

        back_to_menu.draw(screen)
        play_again_button.draw(screen)

   
        
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