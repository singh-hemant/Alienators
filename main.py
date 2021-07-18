import pygame
import random
import sys


class FighterShip:
    def __init__(self, background, image, x=500, y=470):
        self.x = x
        self.y = y
        self.size_x = 64
        self.size_y = 64
        self.max_life = 100
        self.current_life = 100
        self.is_alive = True
        self.fire = False
        self.bg = background
        self.img = image
        self.crashed = False

    def crash(self):
        self.crashed = True

    def move_left(self, speed):
        self.x -= speed

    def move_right(self, speed):
        self.x += speed

    def move_down(self, speed):
        self.y += speed

    def move_up(self, speed):
        self.y -= speed

    def attack(self):
        self.fire = True

    def lifes_bar(self):
        pygame.draw.rect(self.bg, (200, 0, 200), (self.x - 20, self.y + 65, self.current_life, 10))
        pygame.draw.rect(self.bg, (0, 0, 0), (self.x-20 + self.current_life, self.y + 65, self.max_life-self.current_life, 10))

    def show(self):
        self.bg.blit(self.img, (self.x, self.y))
        self.lifes_bar()


class Enemy:
    def __init__(self, background, width, image, bullet_img):
        self.x = random.randint(0, width -1)
        self.y = random.randint(0, 30)
        self.size_x =64
        self.size_y = 64
        self.maxlife_lvl1 = 30
        self.current_life = 30
        self.is_alive = True
        self.fire = False
        self.bg = background
        self.image = image
        self.bullet_img = bullet_img
        self.w = width
        self.left = True
        self.right = False

        self.bullet_list = []
        self. attacking = False


    def move(self):

        if self.left:
            if self.x == 0:
                self.y += 15
            self.x -= 3
        if self.right:
            if self.x == self.w - self.size_x:
                self.y += 15
            self.x += 3

        if self.x < 0:
            self.right = True
            self.left = False
        if self.x > self.w - self.size_x:
            self.left = True
            self.right = False

    def attack(self):
        self.attacking = True
        #self.bullet.shoot()
        #self.bullet.show()

    def kill(self):
        self.is_alive = False

    def lifes_bar(self):
        pygame.draw.rect(self.bg, (200, 100, 200), (self.x - 10, self.y + 10, (self.current_life), 5))
        pygame.draw.rect(self.bg, (0, 0, 0), (self.x - 10 +(self.current_life), self.y + 10, (self.maxlife_lvl1-self.current_life), 5))

    def show(self):
        self.bg.blit(self.image, (self.x, self.y))
        self.lifes_bar()


class FightersBullet:
    def __init__(self,bg, image, x=500, y=500):
        self.x = x
        self.y = y
        self.speed  = 5
        self.x_size = 32
        self.y_size = 32
        self.fire = False
        self.image = image
        self.bg = bg
        self.used = False

    def collide(self):
        self.used = True

    def show(self):
        self.bg.blit(self.image, (self.x+30, self.y))
        #self.bg.blit(self.image, (self.x+20, self.y))

    def shoot(self):
        self.y -= self.speed
        self.fire = True


class EnemyBullets:
    def __init__(self,bg, image, x=0, y=0):
        self.x = x
        self.y = y
        self.speed  = 2
        self.x_size = 32
        self.y_size = 32
        self.fire = False
        self.image = image
        self.bg = bg
        self.used = False

    def collide(self):
        self.used = True

    def show(self):
        self.bg.blit(self.image, (self.x+22, self.y))
        #self.bg.blit(self.image, (self.x+20, self.y))

    def shoot(self):
        self.y += self.speed
        self.fire = True


class Game:
    def __init__(self):
        pygame.init()
        self.width = 700
        self.height = 600

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 24, "bold")
        self.score = 0

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Alienators")

        self.background = pygame.Surface((self.width, self.height))
        self.bg = pygame.image.load("bg1crop.png")

        # For Fighter jet
        fighter_img = pygame.image.load("spaceship2-64.ico")
        self.fighter = FighterShip(self.background, fighter_img)

        self.fighter_speed = 30.

        # For Fighter's bullets
        bullet_img = pygame.image.load("bullet2-32.ico")
        self.bullet_img = pygame.transform.rotate(bullet_img, 90)
        self.bullet_list = []

        # Show enemy's bullets
        enemy_bullet_img = pygame.image.load("bullet3-32.ico")
        self.enemy_bullet_img = pygame.transform.rotate(enemy_bullet_img, 90)
        self.enemy_bullet_list = []

        # For Enemies
        self.enemy_list = [0, 0, 0]
        self.enemy_image = pygame.image.load("spaceship1-64.ico")
        for i in range(len(self.enemy_list)):
            enemy = Enemy(self.background, self.width, self.enemy_image, self.enemy_bullet_img)
            self.enemy_list[i] = enemy

        self.gameloop()

    def event_handler(self, run):
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.fighter.y <= 0:
                        self.fighter.y = 0
                    else:
                        self.fighter.move_up(self.fighter_speed)

                if event.key == pygame.K_DOWN:
                    if self.fighter.y >= self.height - self.fighter.size_y - 70:
                        self.fighter.y = self.height - self.fighter.size_y - 70
                    else:
                        self.fighter.move_down(self.fighter_speed)

                if event.key == pygame.K_LEFT:
                    if self.fighter.x <= 0:
                        self.fighter.x = 0
                    else:
                        self.fighter.move_left(self.fighter_speed)

                if event.key == pygame.K_RIGHT:
                    if self.fighter.x >= self.width - self.fighter.size_x:
                        self.fighter.x = self.width - self.fighter.size_x
                    else:
                        self.fighter.move_right(self.fighter_speed)

                if event.key == pygame.K_SPACE:
                    bullet = FightersBullet(self.background, self.bullet_img, self.fighter.x, self.fighter.y)
                    self.bullet_list.append(bullet)

        return run

    # main Game Loop
    def gameloop(self):
        run = True
        last = pygame.time.get_ticks()
        while run:
            self.window.blit(self.background, (0, 50))
            self.background.blit(self.bg, (0, 0))

            # events
            run = self.event_handler(run)

            # Collision 1 Fighter bullets and Enemy
            for h in range(len(self.enemy_list)):
                for i in range(len(self.bullet_list)):
                    if not self.bullet_list[i].used:
                        if self.enemy_list[h].is_alive:
                            if self.collision(self.bullet_list[i].x+22, self.bullet_list[i].y, self.enemy_list[h].x, self.enemy_list[h].y,
                                       self.bullet_list[i].x_size, self.bullet_list[i].y_size, self.enemy_list[h].size_x, self.enemy_list[h].size_y):
                                self.bullet_list[i].collide()
                                self.enemy_list[h].current_life -= 20
                                if self.enemy_list[h].current_life <= 0:
                                    self.enemy_list[h].kill()
                                self.score += 15

            # show fighters bullets
            for i in range(len(self.bullet_list)):
                if self.bullet_list[i].used:
                    self.bullet_list[i] = FightersBullet(self.background, self.bullet_img, self.fighter.x, self.fighter.y)
                else:
                    self.bullet_list[i].show()
                    self.bullet_list[i].shoot()

            # show enemy's bullets


            # respawn enemy and show enemy

            for i in range(len(self.enemy_list)):

                if not self.enemy_list[i].is_alive:
                    self.enemy_list[i] = Enemy(self.background, self.width, self.enemy_image, self.enemy_bullet_img)
                else:
                    self.enemy_list[i].move()
                    self.enemy_list[i].show()

                    #print(first-last)
                    first = pygame.time.get_ticks()
                    if first - last > 1000:
                        last = first
                        if self.enemy_list[i].attacking == False:
                            random_bullet = EnemyBullets(self.enemy_list[i].bg, self.enemy_list[i].bullet_img, self.enemy_list[i].x, self.enemy_list[i].y)
                            self.enemy_list[i].bullet_list.append(random_bullet)
                            self.enemy_list[i].attacking = True
                        else:
                            for j in range(len(self.enemy_list[i].bullet_list)):
                                if self.enemy_list[i].bullet_list[j] is None:
                                    self.enemy_list[i].bullet_list[j] = EnemyBullets(self.enemy_list[i].bg, self.enemy_list[i].bullet_img,self.enemy_list[i].x, self.enemy_list[i].y)
                                else:
                                    self.enemy_list[i].bullet_list[j].shoot()
                                    self.enemy_list[i].bullet_list[j].show()
                                    if self.enemy_list[i].bullet_list[j].fire == True:
                                        self.enemy_bullet_list.append(self.enemy_list[i].bullet_list[j])
                                        self.enemy_list[i].bullet_list[j] = None
                                        self.enemy_list[i].attack()


            for bullet in self.enemy_bullet_list:
                bullet.shoot()
                bullet.show()

            # Show Fighter jet
            self.fighter.show()
            self.scoring()
            pygame.display.update()
            self.clock.tick(15)

    def collision(self, x1, y1, x2, y2, size_x1, size_y1, size_x2, size_y2):
        if (x2 <= x1 <= x2 + size_x2 and y2 <= y1 <= y2 + size_y2) or (x2 <= x1 + size_x1 <= x2 + size_x2 and y2 <= y1 <= y2 + size_y2)\
                or (x2 <= x1 <= x2 +size_x2 and y2 <= y1 +size_y1 <= y2 +size_y2) or (x2 <= x1 + size_x1 < x2 +size_x2 and y2 <= y1 + size_y1 <= y2 + size_y2):
            print("Collision")
            return True
        else:
            return False

    def scoring(self):
        pygame.draw.rect(self.window, (240, 240, 240), (30, 10, 150, 30))
        text_surface = self.font.render(f"Score: {self.score}", False, (0, 0, 0))
        self.window.blit(text_surface, (40, 10))

        pygame.draw.rect(self.window, (240, 240, 240), (510, 10, 150, 30))


def main():
    Game()


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
