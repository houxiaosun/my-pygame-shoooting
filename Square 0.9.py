import pygame
import sys


def main():

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("移动的方块")

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0,0,255)

    
    player_x,player_y = 400,300
    player_speed = 5
    player_size = 50

    clock = pygame.time.Clock()
    running = True

    print("游戏已启动! 使用WASD移动，按Esc或窗口X退出")

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 键盘控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player_y -= player_speed
        if keys[pygame.K_s]: player_y += player_speed
        if keys[pygame.K_a]: player_x -= player_speed
        if keys[pygame.K_d]: player_x += player_speed
        if keys[pygame.K_ESCAPE]:
            running = False

        # 边界检测
        player_x = max(0, min(player_x, 750))
        player_y = max(0, min(player_y, 550))

        # 绘制
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
        pygame.display.flip()

    print("游戏结束")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()