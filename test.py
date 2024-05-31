import sqlite3 as sq
import pygame
import random 

pygame.init()

class DBConnector:
    def __init__(self):
        self.open_connection()

    def open_connection(self):
        self.con = sq.connect("database.db")
        self.cur = self.con.cursor()

    def get_points(self):
        create_sql = "create table if not exists game (player1 integer,player2 integer);"
        self.cur.execute(create_sql)
        self.con.commit()
        sql = "select sum(player1), sum(player2) from game;"
        return self.cur.execute(sql).fetchall()

    def write_points(self,point1, point2):
        sql = f"insert into game (player1,player2) values ({point1}, {point2});"
        self.cur.execute(sql)
        self.con.commit()

class Text:
    def __init__(self, player, place):
        self.count = 0
        self.f = pygame.font.SysFont("arial", 48)
        self.player = player
        self.place = place
        self.update()

    def update(self):
        self.text = self.f.render(f"{self.player}: {self.count}", 1, (0,0,0))
        self.text_pos = self.text.get_rect(topleft=self.place) 
        
    def draw(self):
        win.blit(self.text, self.text_pos)

class Player(pygame.sprite.Sprite):

    def __init__(self, img_path, player, place):
        super().__init__()
        self.image = pygame.image.load(img_path).convert()
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey)

        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(W)
        self.rect.y = random.randrange(H)

        self.points = Text(player, place)

    def walls(self):
        if self.rect.x > W:
            self.rect.move_ip(-W, 0)
        elif self.rect.x < 0:
            self.rect.move_ip(W, 0)
        elif self.rect.y > H:
            self.rect.move_ip(0, -H)
        elif self.rect.y < 0:
            self.rect.move_ip(0, H)
        
    def move_1(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] == True:
            self.rect.move_ip(-1, 0)
        elif keys[pygame.K_d] == True:
            self.rect.move_ip(1, 0)
        elif keys[pygame.K_w] == True:
            self.rect.move_ip(0, -1)
        elif keys[pygame.K_s] == True:
            self.rect.move_ip(0, 1)

        self.walls()

        

    def move_2(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] == True:
            self.rect.move_ip(-1, 0)
        elif keys[pygame.K_RIGHT] == True:
            self.rect.move_ip(1, 0)
        elif keys[pygame.K_UP] == True:
            self.rect.move_ip(0, -1)
        elif keys[pygame.K_DOWN] == True:
            self.rect.move_ip(0, 1)

        self.walls()

        
    def draw(self, win):
        win.blit(self.image, self.rect)

pygame.init()

W = 800
H = 600
OVER_POINTS = 15
YELLOW = (255,255,0)
win = pygame.display.set_mode((W, H))

hamster = Player("hamster.jpeg", "Хомячок", (10, 10))
ezh = Player("ezh.jpeg",  "Ежик", (W-200, 10))
apple = Player("apple.png", None, (0,0))

db = DBConnector()
points = db.get_points()
f = pygame.font.SysFont("arial",48)
text = f.render(f"{points[0][0]}:{points[0][1]}",1,(0,0,0))
text_pos = text.get_rect(topleft=(W//2,10))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    win.fill(YELLOW)
    hamster.move_1()
    hamster.draw(win)
    ezh.move_2()
    ezh.draw(win)
    apple.draw(win)
    hamster.points.update()
    hamster.points.draw()
    ezh.points.update()
    ezh.points.draw()

    win.blit(text, text_pos)

    

    if apple.rect.colliderect(hamster.rect):
        hamster.points.count += 1
        apple.rect.x = random.randrange(W)
        apple.rect.y = random.randrange(H)

    if apple.rect.colliderect(ezh.rect):
        ezh.points.count += 1
        apple.rect.x = random.randrange(W)
        apple.rect.y = random.randrange(H)

    if ezh.points.count > OVER_POINTS or hamster.points.count > OVER_POINTS:
        pygame.time.delay(3000)
        db.write_points(hamster.points.count, ezh.points.count)
        exit()

    pygame.display.update()