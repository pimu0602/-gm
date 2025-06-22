import pygame
import sys
import random

# Pygameの初期化
pygame.init()

# 画面の設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩し")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

# パドルの設定
paddle_width = 100
paddle_height = 15
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 40
paddle_speed = 8

# ボールの設定
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 4 * random.choice([-1, 1])
ball_dy = -4

# ブロックの設定
block_width = 80
block_height = 30
blocks = []
for row in range(5):
    for col in range(10):
        block = {
            'rect': pygame.Rect(
                col * (block_width + 2) + 1,
                row * (block_height + 2) + 50,
                block_width,
                block_height
            ),
            'color': COLORS[row % len(COLORS)],
            'visible': True
        }
        blocks.append(block)

# ゲームの状態
game_over = False
score = 0
level = 1
font = pygame.font.Font(None, 36)

def draw_paddle():
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))

def draw_ball():
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

def draw_blocks():
    for block in blocks:
        if block['visible']:
            pygame.draw.rect(screen, block['color'], block['rect'])

def show_game_over():
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)

def show_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

# ゲームループ
clock = pygame.time.Clock()
running = True

while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # リセット
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx, ball_dy = 4 * random.choice([-1, 1]), -4
                paddle_x = (WIDTH - paddle_width) // 2
                game_over = False
                score = 0
                level = 1
                for block in blocks:
                    block['visible'] = True
    
    if not game_over:
        # パドルの移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed
        
        # ボールの移動
        ball_x += ball_dx
        ball_y += ball_dy
        
        # 壁との衝突判定
        if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
            ball_dx *= -1
        if ball_y <= ball_radius:
            ball_dy *= -1
            
        # ボールが画面外に出た場合
        if ball_y > HEIGHT:
            game_over = True
        
        # パドルとの衝突判定
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        if (ball_y + ball_radius >= paddle_y and 
            ball_x >= paddle_x and 
            ball_x <= paddle_x + paddle_width):
            ball_dy = -abs(ball_dy)  # 常に上向きに跳ね返るようにする
            
        # ブロックとの衝突判定
        ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 
                              ball_radius * 2, ball_radius * 2)
        
        for block in blocks:
            if block['visible'] and ball_rect.colliderect(block['rect']):
                block['visible'] = False
                ball_dy *= -1
                score += 10
                
                # すべてのブロックが消えたかチェック
                all_blocks_gone = all(not block['visible'] for block in blocks)
                if all_blocks_gone:
                    level += 1
                    # ボールの速度を上げる
                    ball_dx *= 1.2
                    ball_dy *= 1.2
                    # ブロックをリセット
                    for block in blocks:
                        block['visible'] = True
                    # ボールとパドルをリセット
                    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                    ball_dx = 4 * random.choice([-1, 1])
                    ball_dy = -4
                    paddle_x = (WIDTH - paddle_width) // 2
                break
    
    # 描画
    screen.fill(WHITE)
    draw_paddle()
    draw_ball()
    draw_blocks()
    show_score()
    
    if game_over:
        show_game_over()
        restart_text = font.render("Press 'R' to restart", True, BLUE)
        screen.blit(restart_text, (WIDTH//2 - 100, HEIGHT//2 + 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
