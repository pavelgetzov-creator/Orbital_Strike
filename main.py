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
        return {"high_score": 0, "coins": 0, "unlocked_ships": ["Assets/ship_b.png"]}


def save_data(data):
    with open(save_path(), "w", encoding="utf-8") as file:
        json.dump(data, file)


game_data = load_data()
game_data["unlocked_ships"] = game_data.get("unlocked_ships", ["Assets/ship_b.png"])
game_data["bonus_lives"] = game_data.get("bonus_lives", 0)

screen = pygame.display.set_mode((400, 700))
pygame.display.set_caption("Orbital Strike")
background = pygame.image.load(resource_path("Assets/space.png")).convert()
background = pygame.transform.scale(background, (400,700))

running = True

shop_ships = [
    ("Assets/ship_b.png", "Basic Ship", 0),
    ("Assets/ship_0.png", "Advanced Ship", 100),
    ("Assets/ship_1.png", "Fighter Ship", 200),
    ("Assets/ship_2.png", "Stealth Ship", 300),
    ("Assets/ship_3.png", "Interceptor Ship", 400),   
]

shop_index = 0
selected_ship = shop_ships[shop_index][0]

shop_powers = [
    ("Assets/hearth.png", "Extra Life", 50, "health"),
]

power_index = 0


class Player:
    def __init__(self):
        self.image = pygame.image.load(resource_path(selected_ship))
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
        self.state = "active"
        self.respawn_time = 0

        self.x = random.randint(0,340)
        self.y = 0
        self.speed = 0.5

    def move(self):
        if self.state == "waiting":
            self.check_respawn()
            
        if self.state == "active":
            self.y += self.speed

            if self.y > 700:
                return True
            return False
        return False

    
    def check_respawn(self):
        if self.state == "waiting":
            if pygame.time.get_ticks() - self.respawn_time >= 500:
                self.state = "active"
                self.x = random.randint(0,340)
                self.y = 0

    def draw(self,screen):
        if self.state == "active":
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
    def __init__(self, starting_value=1):
        self.value = starting_value
        self.font = pygame.font.SysFont("Arial", 24)

    def lose_life(self):
        self.value -= 1

    def draw(self,screen):
        lives_text = self.font.render("Lives: " + str(self.value), True, (255,255,255))
        screen.blit(lives_text, (10,40))

class HighScore:
    def __init__(self):
        self.value = game_data["high_score"]
        self.font = pygame.font.SysFont("Arial", 24)

    def new_high_score(self, new_score):
        if new_score > self.value:
            self.value = new_score
            game_data["high_score"] = new_score
            save_data(game_data)


    def draw(self,screen):
        high_score_text = self.font.render("High Score: " + str(self.value), True, (255,255,255))
        screen.blit(high_score_text, (10,100))

class Coins:
    def __init__(self, starting_value=0):
        self.value = starting_value
        self.font = pygame.font.SysFont("Arial", 24)
        self.x = 10
        self.y = 70


    def add_coin(self):
        self.value += 1
        game_data["coins"] = self.value
        save_data(game_data)

    def draw(self,screen):
        coins_text = self.font.render("Coins: " + str(self.value), True, (255,255,255))
        screen.blit(coins_text, (self.x, self.y))


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
lives = Lives(1 + game_data["bonus_lives"])
game_data["bonus_lives"] = 0
save_data(game_data)
coins = Coins(game_data["coins"])
high_score = HighScore()

start_button = Menu(120, 300, 150, 50 , "Start")
shop_button = Menu(120, 400, 150, 50, "Shop")
arrow_left_button = Menu(30, 280, 50, 50, "", resource_path("Assets/arrowLeft.png"))
arrow_right_button = Menu(320, 280, 50, 50, "", resource_path("Assets/arrowRight.png"))
buy_button = Menu(150, 530, 100, 50, "Buy")
quit_button = Menu(120, 600, 150, 50, "Quit")
free_play_button = Menu(120, 450, 150, 50, "Free Mode")
levels_button = Menu(120, 350, 150, 50, "Level Mode")
play_again_button = Menu(125, 500, 150, 50 , "Play Again")
back_to_menu = Menu(120, 600, 150, 50, "Back To Menu")
pause_button = Menu(350,25, 30, 30, "", resource_path("Assets/pause.png") )
sound_button = Menu(310, 25, 30, 30, "", resource_path("Assets/musicOn.png"))
power_ups_button = Menu(120, 400, 150, 50, "Power ups")
ship_button = Menu(120, 300, 150, 50, "Ships")
back_to_shop = Menu(125, 600, 150, 50, "Back To shop")

menu_font = pygame.font.SysFont("impact", 50)
title_center_pos = (200, 150)

game_over_font = pygame.font.SysFont("impact", 50)

shop_font = pygame.font.SysFont("impact", 30)
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

            elif game_state == "menu"  and shop_button.is_clicked(event.pos):
                game_state = "shop"

            elif game_state == "menu" and quit_button.is_clicked(event.pos):
                running = False


            elif game_state == "mode" and levels_button.is_clicked(event.pos):
                player = Player()
                villans = [Villan()]
                laser = Laser()
                score = Score()
                lives = Lives(1 + game_data["bonus_lives"])
                game_data["bonus_lives"] = 0
                save_data(game_data)
                coins = Coins(game_data["coins"])
                high_score = HighScore()
                level_2 = False
                level_3 = False
                level_4 = False
                level_finished = False
                game_state = "playing"
                game_mode = "level_mode"
                power_up = None
                coin_drop = None

            elif game_state == "mode" and free_play_button.is_clicked(event.pos):
                player = Player()
                villans = [Villan()]
                laser = Laser()
                score = Score()
                lives = Lives(1 + game_data["bonus_lives"])
                game_data["bonus_lives"] = 0
                save_data(game_data)
                coins = Coins(game_data["coins"])
                high_score = HighScore()
                game_state = "playing"
                game_mode = "free_play_mode"
                power_up = None
                coin_drop = None



            elif (game_state == "shop" or game_state == "ending" or game_state == "level_complete" or game_state == "mode") and back_to_menu.is_clicked(event.pos):
                game_state = "menu"

            elif game_state == "shop" and ship_button.is_clicked(event.pos):
                game_state = "shop_ships"


            elif game_state == "shop" and power_ups_button.is_clicked(event.pos):
                game_state = "shop_power_ups"

            elif game_state == "shop_power_ups" and back_to_shop.is_clicked(event.pos):
                game_state = "shop"

            elif game_state == "shop_power_ups" and arrow_left_button.is_clicked(event.pos):
                shop_index = (shop_index - 1) % len(shop_ships)

                
            elif game_state == "shop_power_ups" and arrow_right_button.is_clicked(event.pos):
                shop_index = (shop_index + 1) % len(shop_ships)
            

            elif game_state == "shop_ships" and back_to_shop.is_clicked(event.pos):
                game_state = "shop"

            elif game_state == "shop_ships" and arrow_left_button.is_clicked(event.pos):
                shop_index = (shop_index - 1) % len(shop_ships)

                
            elif game_state == "shop_ships" and arrow_right_button.is_clicked(event.pos):
                shop_index = (shop_index + 1) % len(shop_ships)


            elif game_state == "shop_ships" and buy_button.is_clicked(event.pos):
                ship_cost = shop_ships[shop_index][2]
                current_ship = shop_ships[shop_index][0]
                if current_ship in game_data["unlocked_ships"]:
                    selected_ship = current_ship
                elif game_data["coins"] >= ship_cost:
                    game_data["coins"] -= ship_cost
                    coins.value -= ship_cost
                    game_data["unlocked_ships"].append(current_ship)
                    selected_ship = current_ship
                    save_data(game_data)


            elif game_state == "shop_power_ups" and buy_button.is_clicked(event.pos):
                power_cost = shop_powers[power_index][2]
                power_type = shop_powers[power_index][3]

                if game_data["coins"] >= power_cost:
                    game_data["coins"] -= power_cost
                    coins.value -= power_cost

                    if power_type == "health":
                        game_data["bonus_lives"] += 1

                    save_data(game_data)


            elif (game_state == "ending" or game_state == "level_complete") and play_again_button.is_clicked(event.pos):
                player = Player()
                villans = [Villan()]
                laser = Laser()
                score = Score()
                lives = Lives(1 + game_data["bonus_lives"])
                game_data["bonus_lives"] = 0
                save_data(game_data)
                coins = Coins(game_data["coins"])
                high_score = HighScore()
                level_2 = False
                level_3 = False
                level_4 = False
                level_finished = False
                game_state = "playing"
                power_up = None
                coin_drop = None


            elif game_state == "paused" and back_to_menu.is_clicked(event.pos):
                pause_button.image = pygame.image.load(resource_path("Assets/pause.png"))
                pause_button.image = pygame.transform.scale(pause_button.image, (30,30))
                game_state = "menu"





            elif game_state == "playing" and pause_button.is_clicked(event.pos):
                pause_button.image = pygame.image.load(resource_path("Assets/return.png"))
                pause_button.image = pygame.transform.scale(pause_button.image, (30,30))
                game_state = "paused"

            elif game_state == "paused" and pause_button.is_clicked(event.pos):
                pause_button.image = pygame.image.load(resource_path("Assets/pause.png"))
                pause_button.image = pygame.transform.scale(pause_button.image, (30,30))
                game_state = "playing"
             
            elif (game_state == "menu" or game_state == "playing" or game_state == "paused" or game_state == "ending" or game_state == "shop" or game_state == "shop_ships" or game_state == "shop_power_ups" or game_state == "mode") and not is_muted and sound_button.is_clicked(event.pos):
                sound.mute()
                sound_button.image = pygame.image.load(resource_path("Assets/musicOff.png"))
                sound_button.image = pygame.transform.scale(sound_button.image, (30,30))
                is_muted = True
            elif (game_state == "menu" or game_state == "playing" or game_state == "paused" or game_state == "ending" or game_state == "shop" or game_state == "shop_ships" or game_state == "shop_power_ups" or game_state == "mode") and is_muted and sound_button.is_clicked(event.pos):
                sound.unmute()
                sound_button.image = pygame.image.load(resource_path("Assets/musicOn.png"))
                sound_button.image = pygame.transform.scale(sound_button.image, (30,30))
                is_muted = False
                

            


    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        laser.fire(player.x)

    if game_state == "playing" or game_state == "paused": 
        sound_button.rect = pygame.Rect(310, 25, 30, 30)
    else:
        sound_button.rect = pygame.Rect(350, 25, 30, 30)

    if game_state == "shop_ships" or game_state == "shop_power_ups":
        coins.x = 10
        coins.y = 25
    else:
        coins.x = 10
        coins.y = 70

    screen.blit(background, (0,0))

    

    if game_state == "menu":
        game_name = menu_font.render("Orbital Strike", True, (255,255,255))
        menu_text_rect = game_name.get_rect(center = title_center_pos)
        screen.blit(game_name, menu_text_rect)

        sound_button.draw(screen)
        start_button.draw(screen)
        quit_button.draw(screen)
        shop_button.draw(screen)

    if game_state == "mode":
        mode_name = menu_font.render("Choose mode!", True, (255,255,255))
        mode_text_rect = mode_name.get_rect(center = title_center_pos)
        screen.blit(mode_name, mode_text_rect)

        sound_button.draw(screen)
        back_to_menu.draw(screen)
        free_play_button.draw(screen)
        levels_button.draw(screen)


    if game_state == "shop":
        shop_name = menu_font.render("Shop", True, (255,255,255))
        shop_name_rect = shop_name.get_rect(center = title_center_pos)
        screen.blit(shop_name,shop_name_rect)

        ship_button.draw(screen)
        power_ups_button.draw(screen)
        back_to_menu.draw(screen)
        sound_button.draw(screen)


    if game_state == "shop_power_ups":
        shop_name_power = shop_font.render(str(shop_powers[power_index][1]) + " - " + str(shop_powers[power_index][2]) + " coins", True, (255,255,255))
        shop_power_text_rect = shop_name_power.get_rect(center = title_center_pos)
        screen.blit(shop_name_power, shop_power_text_rect)
        

        power_preview = pygame.image.load(resource_path(shop_powers[power_index][0]))
        power_preview = pygame.transform.scale(power_preview, (120,120))
        screen.blit(power_preview, (140, 260))

        
        buy_button.text = "Buy" 

  
        coins.draw(screen)
        arrow_left_button.draw(screen)
        arrow_right_button.draw(screen)
        sound_button.draw(screen)
        buy_button.draw(screen)
        back_to_shop.draw(screen)


    if game_state == "shop_ships":
        shop_name = shop_font.render(str(shop_ships[shop_index][1]) + " - " + str(shop_ships[shop_index][2]) + " coins", True, (255,255,255))
        shop_text_rect = shop_name.get_rect(center = title_center_pos)
        screen.blit(shop_name, shop_text_rect)
        ship_preview = pygame.image.load(resource_path(shop_ships[shop_index][0]))
        ship_preview = pygame.transform.scale(ship_preview, (120,120))
        screen.blit(ship_preview, (140, 260))

        current_ship = shop_ships[shop_index][0]
        if current_ship == selected_ship:
            buy_button.text = "Selected"
        elif current_ship in game_data["unlocked_ships"]:
            buy_button.text = "Select"
        else:
            buy_button.text = "Buy"


        
        coins.draw(screen)
        arrow_left_button.draw(screen)
        arrow_right_button.draw(screen)
        sound_button.draw(screen)
        buy_button.draw(screen)
        back_to_shop.draw(screen)

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
            level_up_start_time = pygame.time.get_ticks()
            level_2 = True
            current_level_text = "Level 2!"
        elif game_mode == "level_mode" and score.value >= 60 and not level_3:
            game_state = "level_up"
            level_up_start_time = pygame.time.get_ticks()
            level_3 = True
            current_level_text = "Level 3!"
            villans.append(Villan())
            for v in villans:
                v.speed = 6
        elif game_mode == "level_mode" and score.value >= 90 and not level_4:
            game_state = "level_up"
            level_up_start_time = pygame.time.get_ticks()
            level_4 = True
            current_level_text = "Level 4!"
        elif game_mode == "level_mode" and score.value >= 120 and not level_finished:
            game_state = "level_complete"
            level_finished = True
            current_level_text = ["You successfully", "finished all levels!"]

        
        coins.draw(screen)
        lives.draw(screen)
        high_score.draw(screen)
        pause_button.draw(screen)   
        sound_button.draw(screen)

        for v in villans:
            if v.move():
                lives.lose_life()
                if len(villans) > 1:
                    v.state = "waiting"
                    v.respawn_time = pygame.time.get_ticks()
                else:
                    v.x = random.randint(0,340)
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

            if v.state == "active" and laser.state == "fire" and v_rect.colliderect(laser_rect):
                if len(villans) > 1:
                    v.state = "waiting"
                    v.respawn_time = pygame.time.get_ticks()
                else:
                    v.x = random.randint(0,340)
                    v.y = 0

                if score.value >= 30:
                    v.speed += 0.4
                else:
                    v.speed += 0.2

                laser.y = 600
                laser.state = "ready" 
                score.add_point()
                high_score.new_high_score(score.value)

                if power_up is None and random.random() < 0.1:
                    power_up = PowerUps()
                    if score.value >= 30:
                        power_up.speed += 2
                    elif score.value >= 100:
                        power_up.speed += 3


                if coin_drop is None and random.random() < 0.5:
                    coin_drop = CoinDrop()
                    if score.value >= 30:
                        coin_drop.speed += 2
                    elif score.value >= 100:
                        coin_drop.speed += 3
                     

    if game_state == "level_up":
        surface = pygame.Surface((400, 700), pygame.SRCALPHA)
        surface.fill((0,0,0,180))
        screen.blit(surface,(0,0))


    
        if pygame.time.get_ticks() - level_up_start_time >= 2000:
            game_state = "playing"


        level_up_text = game_over_font.render(current_level_text, True, (0,255,100))
        level_up_rect = level_up_text.get_rect(center = (200,300))
        screen.blit(level_up_text,level_up_rect)

        

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