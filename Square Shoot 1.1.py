import pygame
import sys
import random

# 随机数生成 - 敌人出现的间隔时间和初始敌人数量
generate_interval = random.randint(5, 10)  # 生成间隔时间（秒）
Enemy_number = random.randint(1, 5)  # 初始敌人数量


# 子弹类
class Bullet:
    def __init__(self, x, y):
        self.x = x  # 子弹的x坐标
        self.y = y  # 子弹的y坐标
        self.speed = 10  # 子弹移动速度
        self.size = 5  # 子弹大小
        self.color = (0, 0, 0)  # 子弹颜色（黑色）

    def update(self):
        """更新子弹位置 - 每帧向上移动"""
        self.y -= self.speed  # 向上移动

    def draw(self, screen):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def is_off_screen(self):
        """检查子弹是否飞出屏幕上方"""
        return self.y < -self.size

    def get_rect(self):
        """获取子弹的矩形区域，用于碰撞检测"""
        return pygame.Rect(self.x, self.y, self.size, self.size)


# 敌人类
class Enemy:
    def __init__(self):
        self.size = 50  # 敌人大小
        self.x = random.randint(100, 700)  # 敌人初始x坐标（随机）
        self.y = random.randint(100, 500)  # 敌人初始y坐标（随机）
        self.speed = random.randint(2, 4)  # 敌人移动速度（随机）
        self.color = (0, 0, 255)  # 敌人颜色（蓝色）

    def update(self):
        """更新敌人位置 - 水平移动，碰到边界反弹"""
        self.x += self.speed  # 水平移动

        # 碰到边界反弹
        if self.x > 800 - self.size or self.x < 0:
            self.speed = -self.speed  # 反转移动方向

    def draw(self, screen):
        """在屏幕上绘制敌人"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def get_rect(self):
        """获取敌人的矩形区域，用于碰撞检测"""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def respawn(self):
        """重新生成敌人 - 重置位置和速度"""
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 500)
        self.speed = random.randint(2, 4)


# 玩家类
class Player:
    def __init__(self):
        self.x = 400  # 玩家初始x坐标
        self.y = 300  # 玩家初始y坐标
        self.speed = 5  # 玩家移动速度
        self.size = 50  # 玩家大小
        self.color = (255, 0, 0)  # 玩家颜色（红色）

    def update(self, keys):
        """根据按键更新玩家位置"""
        # 键盘控制：W上，S下，A左，D右
        if keys[pygame.K_w]: self.y -= self.speed
        if keys[pygame.K_s]: self.y += self.speed
        if keys[pygame.K_a]: self.x -= self.speed
        if keys[pygame.K_d]: self.x += self.speed

        # 边界检测 - 确保玩家不会移出屏幕
        self.x = max(0, min(self.x, 800 - self.size))
        self.y = max(0, min(self.y, 600 - self.size))

    def draw(self, screen):
        """在屏幕上绘制玩家"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def get_rect(self):
        """获取玩家的矩形区域，用于碰撞检测"""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def shoot(self):
        """发射子弹 - 从玩家中心位置发射"""
        # 从玩家中心发射子弹
        bullet_x = self.x + self.size // 2 - 2
        bullet_y = self.y
        return Bullet(bullet_x, bullet_y)


def main():

    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("射击游戏")
    score = 0
    # 颜色定义
    WHITE = (255, 255, 255)

    # 创建游戏对象
    player = Player()
    bullets = []
    enemies = []

    # 初始化敌人
    for _ in range(Enemy_number):
        enemies.append(Enemy())

    # 游戏循环控制
    clock = pygame.time.Clock()
    running = True

    enemy_timer = 0
    spawn_interval = generate_interval

    # 游戏主循环
    while running:
        clock.tick(60)
        screen.fill(WHITE)

        # 处理游戏事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 按J键发射子弹
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    bullets.append(player.shoot())



        # 更新玩家位置
        keys = pygame.key.get_pressed()
        player.update(keys)

        # 更新所有敌人的位置
        for enemy in enemies:
            enemy.update()

        # 更新所有子弹的位置
        for bullet in bullets[:]:
            bullet.update()  # 更新子弹位置
            if bullet.is_off_screen():
                bullets.remove(bullet)

        # 碰撞检测 - 玩家与敌人
        player_rect = player.get_rect()
        for enemy in enemies:
            if player_rect.colliderect(enemy.get_rect()):
                print("💥 碰撞！游戏结束！")
                running = False  # 结束游戏

        # 碰撞检测 - 子弹与敌人
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    print("🎯 消灭敌人！")
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10 #加分
                    if len(enemies) == 0 :
                        enemies.append(Enemy())

                    break
        #更新敌人生成计时器
        enemy_timer += 1/60
        #检查是否该生成敌人
        if enemy_timer>=spawn_interval:
            enemies.append(Enemy())

            enemy_timer = 0

            spawn_interval = random.randint(2,5, )
            print(f'生成敌人了！下次在{spawn_interval}秒后生成')

            if len(enemies) > 5:

                enemies.remove(enemies[0])


        # 绘制所有游戏元素
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'分数：{score}', True,(0,0,0))
        screen.blit(score_text,(10,10))
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # 更新屏幕显示
        pygame.display.flip()

    # 退出游戏
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()