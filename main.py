import pygame

import assets
import configs
from assets import load_high_score, save_high_score
from object.background import Background
from object.bird import Bird
from object.column import Column
from object.floor import Floor
from object.gameover_message import GameOverMessage
from object.gamestart_message import GameStartMessage
from object.score import Score

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False
is_day = False
level = 0

assets.load_sprites()
assets.load_audios()
high_score = load_high_score()

sprites = pygame.sprite.LayeredUpdates()

def create_sprites():
    Background(0, is_day, sprites)
    Background(1, is_day, sprites)
    Floor(0, sprites)
    Floor(1, sprites)

    return Bird(sprites), GameStartMessage(sprites), Score(sprites)

bird, game_start_message, score = create_sprites()

def update_difficult(score):
    global level
    if score % 10 == 0 and score != 0:
        configs.FPS = min(configs.FPS + 5, 120)
        configs.COLUMN_GAP = max(configs.COLUMN_GAP - 10, 90)  # Giảm khoảng cách giữa các cột
        pygame.time.set_timer(column_create_event, max(800, 1800 - score * 10))  # Giảm thời gian xuống 1 giây
        configs.GRAVITY = min(configs.GRAVITY + 0.05, 0.8)  # Tăng lực hấp dẫn
        level += 1
        assets.play_audio("level-up")

# def mode_background(score):
#     global is_day
#     if score % 5 == 0 and score != 0:
#         is_day = not is_day
#         Background(0, is_day, sprites)
#         Background(1, is_day, sprites)

def mode_background():
    global is_day
    current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại (mili-giây)
    if current_time // 30000 % 2 == 0:  # Mỗi 30 giây chuyển nền (30,000 ms)
        if not is_day:  # Nếu đang là đêm, đổi sang ngày
            is_day = True
            Background(0, is_day, sprites)
            Background(1, is_day, sprites)
    else:
        if is_day:  # Nếu đang là ngày, đổi sang đêm
            is_day = False
            Background(0, is_day, sprites)
            Background(1, is_day, sprites)


def reset_game():
    global is_day, level
    configs.FPS = 60
    configs.COLUMN_GAP = 170
    configs.GRAVITY = 0.35
    pygame.time.set_timer(column_create_event, 1800)
    is_day = False
    level = 0
    sprites.empty()
    return create_sprites()
assets.play_audio("start-game", loops=-1)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event and gamestarted:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                gamestarted = True
                game_start_message.kill()
                pygame.time.set_timer(column_create_event, 1800)
                assets.stop_audio("start-game")
            if event.key == pygame.K_ESCAPE and gameover:
                gameover = False
                gamestarted =  False
                sprites.empty()
                bird, game_start_message, score = reset_game()
                assets.play_audio("start-game", loops=-1)
        bird.handle_event(event)

    screen.fill(0)
    # Cập nhật nền dựa trên thời gian
    if not gameover:
        mode_background()

    sprites.draw(screen)
    if gamestarted and not gameover:
        sprites.update()

    if bird.check_collision(sprites) and not gameover:
        gameover = True
        gamestarted = False
        gameover_message = GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, 0)
        assets.play_audio("hit")

        if score.value > high_score:
            high_score = score.value
            save_high_score(high_score)

    if gameover:
        # Khung chữ nhật nhỏ hiển thị "Score" và "High Score"
        font_small = pygame.font.Font("assets/04B_19.TTF", 18)
        font_large = pygame.font.Font("assets/04B_19.TTF", 32)

        rect_width, rect_height = 120, 150  # Tăng chiều cao khung để cân đối
        rect_x = configs.SCREEN_WIDTH / 2 - rect_width / 2
        rect_y = configs.SCREEN_HEIGHT / 2 - 70 # Đặt khung thấp hơn một chút
        # Vẽ khung
        pygame.draw.rect(screen, (245, 234, 193), (rect_x, rect_y, rect_width, rect_height))  # Màu nền
        pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height), 2)  # Viền màu đen

        # Text "SCORE"
        score_label = font_small.render("YOUR SCORE", True, (255, 87, 51))  # Text màu đỏ cam
        screen.blit(score_label, (rect_x + rect_width // 2 - score_label.get_width() // 2, rect_y + 10))

        # Giá trị điểm số
        score_value = font_large.render(f"{score.value}", True, (0, 0, 0))  # Text màu đen
        screen.blit(score_value, (rect_x + rect_width // 2 - score_value.get_width() // 2, rect_y + 40))

        # Text "BEST"
        best_label = font_small.render("HIGH SCORE", True, (255, 87, 51))  # Text màu đỏ cam
        screen.blit(best_label, (rect_x + rect_width // 2 - best_label.get_width() // 2, rect_y + 80))

        # Giá trị High Score
        best_value = font_large.render(f"{high_score}", True, (0, 0, 0))  # Text màu đen
        screen.blit(best_value, (rect_x + rect_width // 2 - best_value.get_width() // 2, rect_y + 110))

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            update_difficult(score.value)
            # mode_background(score.value)
            assets.play_audio("point")

    # Hiển thị level ở góc trên cùng bên trái
    font = pygame.font.Font("assets/04B_19.TTF", 18)
    level_text = font.render(f"LEVEL: {level}", True, (255, 255, 255))  # Màu trắng
    screen.blit(level_text, (10, 10))

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()