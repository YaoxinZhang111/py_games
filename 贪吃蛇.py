import pygame, sys
from pygame.locals import *
import random
direction ='right'
changeDirection = direction
# 玩家
class Player(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__()
        self.surf = pygame.Surface((20,20))
        self.surf.fill((0,255,255))
        self.rect = self.surf.get_rect()
        
    def update(self, direction):
        last_rect = self.rect.center
        
        
        if direction=='up':
            self.rect.move_ip(0,-20)
        if direction=='down':
            self.rect.move_ip(0,20)
        if direction=='left':
            self.rect.move_ip(-20,0)
        if direction=='right':
            self.rect.move_ip(20,0)
            
        
        # 限定player在屏幕中
        if self.rect.left < 0:
            self.rect.right = 800
        elif self.rect.right > 800:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.bottom = 800
        elif self.rect.bottom >= 800:
            self.rect.top = 0
        return last_rect

# 尾巴
class Tail(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.surf = pygame.Surface((20,20))
        self.surf.fill((255,0,255))
        self.rect = self.surf.get_rect()


# 食物
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect(center=(random.randint(1, 39)*20, random.randint(1, 39)*20))
        


# 初始化
pygame.init()

# 屏幕对象
screen = pygame.display.set_mode((800,800)) # 尺寸

#设置游戏窗口标题
pygame.display.set_caption('贪吃蛇')

# 锁帧
FPSCLOCK=pygame.time.Clock()

# 玩家
player = Player()

# 三个精灵组
foods = pygame.sprite.Group()
tails = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# 窗口主循环
while True:
    # 遍历事件队列    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()       
        elif event.type == KEYDOWN:           
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()                
        
                
    
    # 更新屏幕
    pygame.display.flip()
    FPSCLOCK.tick(15)
    
    # 更新玩家
    key = pygame.key.get_pressed()
    
    if key[K_RIGHT]:
        changeDirection = 'right'
    if key[K_LEFT]:
        changeDirection = 'left'
    if key[K_UP]:
        changeDirection = 'up'
    if key[K_DOWN]:
        changeDirection = 'down'
    
    if changeDirection == 'right' and not direction == 'left':
        direction = changeDirection
    if changeDirection == 'left' and not direction == 'right':
        direction = changeDirection
    if changeDirection == 'up' and not direction == 'down':
        direction = changeDirection
    if changeDirection == 'down' and not direction == 'up':
        direction = changeDirection

    rect_ = player.update(direction)
    
    screen.fill((0,0,0))
    screen.blit(player.surf, player.rect)
    
    
    # 刷新食物
    if len(foods.sprites())==0:
        new_food = Food()
        foods.add(new_food)
        all_sprites.add(new_food)
    screen.blit(new_food.surf, new_food.rect)

    # 吃到食物，加长尾巴
    if pygame.sprite.spritecollideany(player,foods):
        new_food.kill()
        foods.remove(new_food)
        if len(tails.sprites())==0:
            new_tail = Tail()
            new_tail.rect.center = rect_
            tails.add(new_tail)
            all_sprites.add(new_tail)
        else:
            for idx,tail in enumerate(tails):
                if idx +1 == len(tails.sprites()):
                    
                    new_tail = Tail()
                    new_tail.rect.center = tail.rect.center
                    tails.add(new_tail)
                    all_sprites.add(new_tail)

    # 刷新尾巴位置
    for idx,tail in enumerate(tails):
        new_rect = tail.rect.center
        if idx == 0:
            tail.rect.center = rect_
        else:
            tail.rect.center = next_rect
        next_rect = new_rect
        screen.blit(tail.surf, tail.rect)



        
    # 检测是否吃到尾巴
    if pygame.sprite.spritecollideany(player, tails):
        player.kill()
        print('咬到尾巴了！')
        pygame.quit()
        sys.exit()
    # 重绘界面
    pygame.display.flip()