import pygame
import sys
import random

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("射击游戏")


    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)

    # 玩家
    player_x, player_y = 400, 300
    player_speed = 5
    player_size = 50

    # 子弹系统
    bullets = []
    bullet_speed = 10
    bullet_size = 5

    # 敌人
    enemy_x = random.randint(100, 700)
    enemy_y = random.randint(100, 500)
    enemy_speed = random.randint(2, 4)
    enemy_size = 50

    enemya_x = random.randint(100, 700)
    enemya_y = random.randint(100, 500)
    enemya_speed = random.randint(2, 4)
    enemya_size = 50

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 按J键发射子弹
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:

                    bullet_x = player_x + player_size // 2 - bullet_size // 2
                    bullet_y = player_y
                    bullets.append([bullet_x, bullet_y])
                    print(f"发射子弹！位置: ({bullet_x}, {bullet_y})")

        # 键盘控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player_y -= player_speed
        if keys[pygame.K_s]: player_y += player_speed
        if keys[pygame.K_a]: player_x -= player_speed
        if keys[pygame.K_d]: player_x += player_speed

        # 敌人移动
        enemy_x += enemy_speed
        if enemy_x > 750 or enemy_x < 0:
            enemy_speed = -enemy_speed
        enemya_x += enemya_speed
        if enemya_x > 750 or enemya_x < 0:
            enemya_speed = -enemya_speed

        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            # 移除超出屏幕的子弹
            if bullet[1] < -bullet_size:
                bullets.remove(bullet)
                print("移除超出屏幕的子弹")

        # 边界检测
        player_x = max(0, min(player_x, 750))
        player_y = max(0, min(player_y, 550))

        # 碰撞检测
        if (abs(player_x - enemy_x) < player_size and
                abs(player_y - enemy_y) < player_size):
            print("💥 碰撞！游戏结束！")
            running = False
        if (abs(player_x - enemya_x) < player_size and
                abs(player_y - enemya_y) < player_size):
            print("💥 碰撞！游戏结束！")
            running = False

        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)
            enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

            if bullet_rect.colliderect(enemy_rect):
                print("🎯 消灭敌人！")
                bullets.remove(bullet)
                # 重置敌人
                enemy_x = random.randint(100, 700)
                enemy_y = random.randint(100, 500)
                enemy_speed = random.randint(2, 4)
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)
            enemy_rect = pygame.Rect(enemya_x, enemya_y, enemya_size, enemya_size)

            if bullet_rect.colliderect(enemy_rect):
                print("🎯 消灭敌人！")
                bullets.remove(bullet)

                enemya_x = random.randint(100, 700)
                enemya_y = random.randint(100, 500)
                enemya_speed = random.randint(2, 4)
        # 绘制所有元素
        pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
        pygame.draw.rect(screen, BLUE, (enemy_x, enemy_y, enemy_size, enemy_size))
        pygame.draw.rect(screen, BLUE, (enemya_x, enemya_y, enemya_size, enemya_size))

        for bullet in bullets:
            pygame.draw.rect(screen, BLACK, (bullet[0], bullet[1], bullet_size, bullet_size))


        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()