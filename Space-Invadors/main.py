import pygame
import os
import time
import random
pygame.font.init()


# Global Vars & Conts ======================================
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")
main_font = pygame.font.SysFont("comicsans", 35)
lost_font = pygame.font.SysFont("comicsans", 45)


# Global Functions ==========================================
# detect collision between two objects
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


# Draw Screen UI
def draw_lives(lives):
    lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
    WIN.blit(lives_label, (10, 10))


def draw_level(level):
    level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
    WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))


def draw_lost():
    lost_label = lost_font.render(f"You Lost!!", 1, (255, 255, 255))
    WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))


# Loading Assets =================================================
RED_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))

# Player Ship
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


# Ship Classes ========================================================
class Ship:
    FRAMES_BETWEEN_SHOTS = 30  # .5 second

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.frames_counter = 0

    # ------------------ Ship Update ---------------------
    # move the ship lasers and check collision with the player and if OFF_screen
    def move_lasers(self, vel, obj):  # obj is the player
        self.frames_counter -= 1
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    # handle shooting lasers
    def shoot(self):
        if self.frames_counter <= 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.frames_counter = self.FRAMES_BETWEEN_SHOTS
        else:
            self.frames_counter -= 1

    # get width and height of the ship
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    # ------------------ Ship Draw -----------------------
    # draw ship and its lasers
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # --------------- Laser Update --------------------

    def move(self, vel):
        self.y += vel

    # check if laser is out of the screen
    def off_screen(self, height):
        return self.y > height or self.y < 0

    def collision(self, obj):
        return collide(self, obj)

    # --------------- Laser Draw --------------------
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


# Player & Enemy Ships ===============================================
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    # -------------- Player Update -------------
    # move the player ship lasers and check collision with the enemies and if OFF_screen
    def move_lasers(self, vel, objs):  # objs are the enemies
        self.frames_counter -= 1
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    # --------------- Player Draw ---------------
    def draw(self, window):
        super().draw(window)
        self.draw_healthbar(window)

    # for drawing healthbar
    def draw_healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                                               self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height(
        ) + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    # ------------ Enemy Update ----------------------
    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.frames_counter <= 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.frames_counter = self.FRAMES_BETWEEN_SHOTS
        else:
            self.frames_counter -= 1


# Main Game Loop =======================================================
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5  # number of enemy pass

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    player = Player(250, 450)

    clock = pygame.time.Clock()

    lost = False
    Lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        draw_lives(lives)
        draw_level(level)

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            draw_lost()

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            Lost_count += 1

        if lost:
            if Lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(
                    50, WIDTH-100), random.randrange(-1300, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        # down (15 for healthbar)
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel

        # for shooting:
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


# Draw Main Menu =======================================
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 45)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render(
            "Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
