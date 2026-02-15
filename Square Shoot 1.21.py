import pygame
import sys
import random
import os  # 1.21新增导入os模块（显示文字）

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
        self.y = 545  # 玩家初始y坐标
        self.speed = 5  # 玩家移动速度
        self.size = 50  # 玩家大小
        self.color = (255, 0, 0)  # 玩家颜色（红色）
        self.max_bullets = 3
        self.current_bullets = 0

    def can_shoot(self):
        """检查子弹是否可以发射"""
        return self.current_bullets < self.max_bullets

    def shoot(self):
        if self.can_shoot():
            bullet_x = self.x + self.size // 2 - 2
            bullet_y = self.y
            self.current_bullets += 1  # 子弹数量+1
            return Bullet(bullet_x, bullet_y)
        return None

    def bullet_destroyed(self):
        """"当子弹被销毁时调用"""
        self.current_bullets -= 1
        self.current_bullets = max(0, self.current_bullets)

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

    def draw_bullet_count(self, screen, font):
        """显示剩余子弹数量 - 修改：接收字体参数"""
        text = font.render(f"子弹: {self.max_bullets - self.current_bullets}/{self.max_bullets}", True, (0, 0, 0))
        screen.blit(text, (self.x, self.y - 30))


def main():
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # 创建800x600的窗口
    pygame.display.set_caption("射击游戏")  # 设置窗口标题
    score = 0
    # 颜色定义
    WHITE = (255, 255, 255)  # 白色，用于清屏

    # ========== 1.21新增：中文字体初始化 ==========
    font_path = None
    # 查找系统中文字体
    if os.name == 'nt':  # Windows系统
        possible_paths = [
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "C:/Windows/Fonts/simsun.ttc"  # 宋体
        ]
        for path in possible_paths:
            if os.path.exists(path):
                font_path = path
                break

    # 创建字体对象
    if font_path:
        try:
            font = pygame.font.Font(font_path, 24)  # 使用中文字体
            chinese_font = pygame.font.Font(font_path, 30)  # 大号字体用于分数显示
        except:
            font = pygame.font.Font(None, 24)
            chinese_font = pygame.font.Font(None, 30)
    else:
        font = pygame.font.Font(None, 24)  # 备用字体
        chinese_font = pygame.font.Font(None, 30)
    # ========== 中文字体初始化结束 ==========

    # 创建游戏对象
    player = Player()  # 创建玩家对象
    bullets = []  # 存储所有子弹对象的列表
    enemies = []  # 存储所有敌人对象的列表

    # 初始化敌人 - 创建随机数量的敌人
    for _ in range(Enemy_number):
        enemies.append(Enemy())

    # 游戏循环控制
    clock = pygame.time.Clock()  # 创建时钟对象，控制游戏帧率
    running = True  # 游戏运行标志

    enemy_timer = 0  # 记录时间
    spawn_interval = generate_interval

    # 游戏主循环
    while running:
        clock.tick(60)  # 控制游戏帧率为60FPS
        screen.fill(WHITE)  # 用白色清屏

        # 处理游戏事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 如果点击关闭窗口
                running = False

            # 按J键发射子弹 - 修正这里的错误
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    new_bullet = player.shoot()  # 获取新子弹
                    if new_bullet:  # 如果有子弹（未达到上限）
                        bullets.append(new_bullet)  # 添加到子弹列表

        # 更新玩家位置
        keys = pygame.key.get_pressed()  # 获取当前按下的所有键
        player.update(keys)  # 根据按键更新玩家位置

        # 更新所有敌人的位置
        for enemy in enemies:
            enemy.update()

        # 更新所有子弹的位置并检查是否飞出屏幕
        for bullet in bullets[:]:  # 遍历子弹列表的副本
            bullet.update()  # 更新子弹位置
            if bullet.is_off_screen():  # 如果子弹飞出屏幕
                bullets.remove(bullet)  # 从列表中移除子弹
                player.bullet_destroyed()  # 通知玩家子弹已销毁

        # 碰撞检测 - 玩家与敌人
        player_rect = player.get_rect()  # 获取玩家的矩形区域
        for enemy in enemies:
            if player_rect.colliderect(enemy.get_rect()):  # 如果玩家和敌人矩形重叠
                print("💥 碰撞！游戏结束！")
                running = False  # 结束游戏

        # 碰撞检测 - 子弹与敌人
        for bullet in bullets[:]:  # 遍历子弹列表的副本
            for enemy in enemies[:]:  # 遍历敌人列表的副本
                if bullet.get_rect().colliderect(enemy.get_rect()):  # 如果子弹和敌人矩形重叠
                    print("🎯 消灭敌人！")

                    bullets.remove(bullet)  # 移除子弹
                    player.bullet_destroyed()  # 通知子弹已销毁
                    enemies.remove(enemy)  # 移除敌人
                    score += 10  # 加分

                    if len(enemies) == 0:  # 检测敌人数量
                        enemies.append(Enemy())  # 添加新敌人

                    break  # 跳出内层循环

        # 更新敌人生成计时器
        enemy_timer += 1 / 60

        # 检查是否该生成敌人
        if enemy_timer >= spawn_interval:
            # 生成新敌人
            enemies.append(Enemy())
            # 重置计时器
            enemy_timer = 0
            # 重新随机生成时间
            spawn_interval = random.randint(2, 5)
            print(f'生成敌人了！下次在{spawn_interval}秒后生成')

            # 检测敌人数量
            if len(enemies) > 5:
                # 删除最旧的敌人
                enemies.remove(enemies[0])

        # ========== 1.21修改：绘制文本部分 ==========
        # 使用中文字体显示分数
        score_text = chinese_font.render(f'分数：{score}', True, (0, 0, 0))  # 黑色字体
        screen.blit(score_text, (10, 10))  # 左上角显示

        player.draw(screen)  # 绘制玩家
        player.draw_bullet_count(screen, font)  # 修改：传入字体参数

        for enemy in enemies:  # 绘制所有敌人
            enemy.draw(screen)
        for bullet in bullets:  # 绘制所有子弹
            bullet.draw(screen)

        # 更新屏幕显示
        pygame.display.flip()

    # 退出游戏
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
