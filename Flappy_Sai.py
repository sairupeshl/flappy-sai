# Initializing
import asyncio
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import random
import pygame
pygame.init()

# Game Setup
screen = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy_Sai")
g = 2
font=pygame.font.Font(None, 50)

async def main():
    score = 0
    score_sound = pygame.mixer.Sound("shortbeepaudio.mp3")
    end_sound = pygame.mixer.Sound("celebrationaudio.mp3")

    # Bird Properties
    sai_x, sai_y = 150, 300
    radius = 20
    pygame.draw.circle(screen, (255,0,0), (sai_x, sai_y), radius)

    # Pipe Properties
    pipe_width = 60
    pipe_gap = 150
    interval = 1500
    last_time = pygame.time.get_ticks()
    pipe_x = 400
    pipe_velocity = 3
    pipes = []

    # Defining a function to draw text
    def draw_text(text, x, y, color):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface,(x,y))

    # Game Loop
    draw_text(f"Score: {score}", 10, 10, (0, 0, 0))
    running = True
    while running:
        screen.fill((255,255,255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running  = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sai_y -= 50
                    
        sai_y+=g

        # Collision
        bird_sq = pygame.Rect(sai_x - radius, sai_y - radius, radius*2, radius*2)
        pygame.draw.circle(screen, (255,0,0), (sai_x, sai_y), radius)

        # Generate pipes
        current_time = pygame.time.get_ticks()
        if current_time - last_time > interval:
            last_time = current_time
            prev_h = pipes[-1]['height'] if pipes else 140
            pipe_height = random.randint(90, min(prev_h + 160, 300))
            pipes.append({'x': 1000, 'height': pipe_height, 'scored': False})

        for pipe in pipes[:]:
            pipe['x'] -= pipe_velocity

            top_pipe = pipe['x'], 0, pipe_width, pipe['height']
            bottom_pipe = pipe['x'], pipe['height']+pipe_gap, pipe_width, 600

            # Draw pipes
            pygame.draw.rect(screen, (0,0,255), top_pipe)
            pygame.draw.rect(screen, (0,0,255), bottom_pipe)

            # Scoring
            if not pipe['scored'] and pipe['x'] + pipe_width < sai_x:
                score += 1
                score_sound.play()
                pipe['scored'] = True

            # Check collision with pipes
            if bird_sq.colliderect(top_pipe) or bird_sq.colliderect(bottom_pipe):
                draw_text("Game Over", 100, 250, (255, 0, 0))
                draw_text(f"Score: {score}", 100, 280, (255, 0, 0))
                pygame.display.update()
                end_sound.play()
                pygame.time.delay(3500)
                running = False

            # Remove off-screen pipes
            if pipe['x'] + pipe_width < 0:
                pipes.remove(pipe)

        # Update Score
        draw_text(f"Score: {score}", 10, 10, (0, 0, 0))

        # Check if bird is out of bounds
        if sai_y - radius < 0 or sai_y + radius > 600:
            draw_text("Game Over", 100, 250, (255, 0, 0))
            draw_text(f"Score: {score}", 100, 280, (255, 0, 0))
            pygame.display.update()
            end_sound.play()
            pygame.time.delay(3500)
            running = False

        # Increase difficulty
        if score%5 == 0 and score > 0:
            pipe_velocity += 0.005
            interval = 4500//pipe_velocity
        
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

# Run the async function
asyncio.run(main())
