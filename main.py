import pygame
import random
pygame.init()
pygame.mixer.init()


WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Pygame")

clock = pygame.time.Clock()

pygame.mixer.music.load("background_sound.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

coin_sound = pygame.mixer.Sound("coin_sound.mp3")
coin_sound.set_volume(0.5)


BACKGROUND_COLOR = (255, 255, 255)
background_img = pygame.image.load("background.jpg")

#იმისთვის, რომ ფოტო სრულად მოერგოს ჩვენს ფანჯარას
background_img = pygame.transform.scale(background_img, (800,600))

# მოთამაშის შექმნა
player_img = pygame.image.load("player.png")

player = pygame.Rect(50, 50, 75, 75)
player_speed = 5

# ლაბირინთის კედელი
walls = [
    pygame.Rect(200, 200, 20, 200),
    pygame.Rect(400, 200, 150, 20),
    pygame.Rect(200, 400, 200, 20)
]

#მოგების პლატფორმა
win_platform = pygame.Rect(700, 500, 90, 90)

# ფოტო მოგებისას გამოჩენისთვის
win_img = pygame.image.load("win_img.png")
win_img = pygame.transform.scale(win_img, (250, 250))

old_x = player.x
old_y = player.y

red = random.randint(0, 255)
green = random.randint(0, 255)
blue = random.randint(0, 255)

# მონეტის ფოტოს შემოტანა პითონში
coin_png = pygame.image.load("coin.png")
coin_png = pygame.transform.scale(coin_png, (60, 60))
coin = pygame.Rect(300, 300, 80, 80)

score = 0

font = pygame.font.SysFont(None, 48)

running = True
win = False
coin_visible = True

while running:
    clock.tick(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed

    # შევამოწმოთ საზღვარი
    if player.x < 0:
        player.x = 0
    if player.y < 0:
        player.y = 0
    if player.x + player.width > WIDTH:
        player.x = WIDTH - player.width
    if player.y + player.height > HEIGHT:
        player.y = HEIGHT - player.height

    # შევამოწმოთ შეჯახება კედელთან
    for wall in walls:
        if player.colliderect(wall):
            player.x = old_x
            player.y = old_y
            score = 0


    # შევამოწმოთ ფლეიერის და მოგების წერტილის შეხება
    if player.colliderect(win_platform):
        win = True

    if player.colliderect(coin):
        score += 1
        coin.x = random.randint(50, 700)
        coin.y = random.randint(50, 500)
        coin_sound.play()

    for wall in walls:
        if coin.colliderect(wall):
            coin.x = random.randint(50, 700)
            coin.y = random.randint(50, 500)

    screen.blit(background_img, (0, 0)) # რომელი წერტილიდან დაიწყოს ფოტოს გამოჩენა

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (620, 10))

    pygame.draw.rect(screen, (255, 123, 34), win_platform)
    screen.blit(player_img, (player.x, player.y))

    screen.blit(coin_png, (coin.x, coin.y))

    for wall in walls:
        pygame.draw.rect(screen, (red, green, blue), wall)
    # თასი ჩნდება მხოლოდ მოგების შემთხვევაში
    if win:
        screen.blit(win_img, (250, 200))
    pygame.display.flip()

pygame.quit()
