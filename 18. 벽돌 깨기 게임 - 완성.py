# 벽돌 깨기 게임

import pygame
import random

pygame.init()

screen = pygame.display.set_mode((480, 360))

pygame.display.set_caption("벽돌 깨기 게임!")

clock = pygame.time.Clock()

# 배경 사이즈
screen_l = screen.get_size()[0]
screen_h = screen.get_size()[1]


# 페달 사이즈, 좌표, 사각화
pedal_l = 100
pedal_h = 15

pedal_x = screen_l//2 - pedal_l//2
pedal_y = screen_h - pedal_h

pedal_rect = pygame.Rect(pedal_x, pedal_y, pedal_l, pedal_h)

pedla_to_x = 0


# 공의 사이즈, 좌표, 사각화
ball_size = 20

ball_x = screen_l//2
ball_y = screen_h - pedal_h - ball_size

ball_rect = pygame.Rect(0, 0, ball_size*2, ball_size*2)
ball_rect.center = (ball_x, ball_y)

ball_speed_x = 0.05
ball_speed_y = 0.05


# 블록 사이즈, 좌표, 사각화
block_l = screen_l//10
block_h = 30

block_x = 0
block_y = 0

block_rect = [[] for _ in range(10)]
block_color = [[] for _ in range(10)]

for i in range(10) :
    for j in range(3) :
        block_rect[i].append(pygame.Rect(i*block_l, j*block_h, block_l, block_h))
        block_color[i].append((random.randrange(255), random.randrange(150, 255), random.randrange(150, 255)))

                              
# 마우스 좌표
mouse_x = 0
mouse_y = 0

# 점수
point = 0

# 시작
start = True

# 글자 찍기 함수
def game_text(word) :
    font = pygame.font.SysFont(None, 100)

    text = font.render(word, True, (0, 255, 255))

    text_l = text.get_rect().size[0]
    text_h = text.get_rect().size[1]

    text_x = screen_l/2 - text_l/2
    text_y = screen_h/2 - text_h/2

    screen.blit(text, (text_x, text_y))

         
running = True

def runGame() :
    global running
    global pedal_x, pedal_y, pedal_l, pedal_h, pedal_to_x
    global ball_x, ball_y, ball_speed_x, ball_speed_y, ball_size
    global block_l, block_y, block_rect, block_color
    global block_rect, block_color
    global mouse_x, mouse_y
    global point, start
    
    while running :
        
        # 시작 시간
        if start :
            start = False

            for i in range(3, 0, -1) :
                screen.fill((255, 255, 255))
                game_text(str(i))

                pygame.display.update()
                pygame.time.delay(1000)
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False

            # 마우스로 페달 움직이기
            if event.type == pygame.MOUSEMOTION :
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if mouse_x - pedal_l//2 >= 0 and mouse_x + pedal_l//2 <= screen_l :
                    pedal_x = mouse_x - pedal_l//2
                    pedal_rect.left = mouse_x - pedal_l//2
                    

        screen.fill((255, 255, 255))

        # 페달 그리기
        pygame.draw.rect(screen, (255, 255, 0), pedal_rect)

        # 공 좌표 계산
        if ball_x - ball_size <= 0 :
            ball_speed_x = -ball_speed_x
        elif ball_x >= screen_l - ball_size :
            ball_speed_x = -ball_speed_x
        
        if ball_y - ball_size <= 0 :
            ball_speed_y = -ball_speed_y
        elif ball_y >= screen_h - ball_size :
            ball_speed_y = -ball_speed_y

            screen.fill((255, 255, 255))
            game_text("GAME OVER")

            pygame.display.update()
            pygame.time.delay(1000)

            break


        # 공 스피드 변경
        ball_x += ball_speed_x
        ball_y += ball_speed_y


        # 공 그리기
        ball_rect.center = (ball_x, ball_y)
        
        pygame.draw.circle(screen, (255, 0, 255), (ball_x, ball_y), ball_size)
        

        # 공이랑 페달 충돌했을 때
        if ball_rect.colliderect(pedal_rect) :
            ball_speed_y = -ball_speed_y
            
        # 블록 그리기
        for i in range(10) :
            for j in range(3) :
                if block_rect[i][j] :
                    pygame.draw.rect(screen, block_color[i][j], block_rect[i][j])
                    block_rect[i][j].topleft = (i*block_l, j*block_h)

                    # 공이랑 벽돌이 닿았을 때
                    if ball_rect.colliderect(block_rect[i][j]) :
                        ball_speed_x = -ball_speed_x
                        ball_speed_y = -ball_speed_y
                        block_rect[i][j] = 0

                        point += 1

        # 게임 클리어
        if point == 30 :
            screen.fill((255, 255, 255))
            game_text("GAME CLEAR")

            pygame.display.update()
            pygame.time.delay(1000)

            running = False
            
                
        pygame.display.update()

    pygame.quit()

runGame()

