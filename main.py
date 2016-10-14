
import pygame
import sys
from Entity import *
from Vector2 import Vector2
from random import randint, uniform
from pygame import mixer

# Init pygame libraries
mixer.pre_init(22050, -16, 40, 4096 / 4)
pygame.init()
mixer.init()

# Setup pygame window
screen_size = (1280, 720)

# Bits per pixel, 8 bits for each RGBA value.
bpp = 32
screen = pygame.display.set_mode(screen_size, pygame.HWSURFACE, bpp)

# Load some sound effects
laser_shot_sfx = mixer.Sound("Assets/laser_shot.wav")
hit_sfx = mixer.Sound("Assets/hit.wav")

# Setup the player entity
player = Entity()
player.graphicsBounds.radius = 10
player.collider.radius = 10

player.position = Vector2(screen_size[0]/2, screen_size[1]/2)
player.color = (255, 0, 0)
player.max_speed = 200
accel = 200
score=0

bullets = list()
asteroids = list()
emitters = list()
trail = list()

myfont = pygame.font.SysFont("monospace", 15)


mixer.music.load("Assets/song.mp3")

mixer.music.play(-1)

def spawn_asteroid():

    if player is None:
        return

    screen_center = Vector2(screen_size[0]/2, screen_size[0]/2)

    spawn_radius = max(screen_center.x, screen_center.y)

    spawn_x = uniform(-1, 1)
    spawn_y = uniform(-1, 1)
    spawn_direction = Vector2(spawn_x, spawn_y)
    spawn_direction.normalize()

    spawn_point = screen_center + spawn_direction * spawn_radius

    a = Asteroid(player, 250)

    a.position = spawn_point
    a.color = (0, 0, 255)

    size = randint(8, 20)
    a.graphicsBounds.radius = size
    a.collider.radius = size
    a.max_speed = 280

    asteroids.append(a)


def shoot():

    if player is None:
        return

    # get pos returns a tuple (mx, my)
    mouse_tuple = pygame.mouse.get_pos()

    mouse_pos = Vector2(mouse_tuple[0], mouse_tuple[1])

    # direction pointing at the mouse from the player
    to_mouse = Vector2.get_normal(mouse_pos - player.position)

    vel = to_mouse * 400.0


    b = Bullet(500, player.position, vel)

    b.color = (255, 150, 80)
    b.graphicsBounds.radius = 5
    b.collider.radius = 5

    bullets.append(b)
    

    
    
   
    laser_shot_sfx.play()


def take_input(keys):

    if player is None:
        return

    xdir = 0.0
    ydir = 0.0

    if keys[pygame.K_a]:
        xdir = -1

    elif keys[pygame.K_d]:
        xdir = 1

    if keys[pygame.K_w]:
        ydir = -1

    elif keys[pygame.K_s]:
        ydir = 1

    direction = Vector2(xdir, ydir)
    direction.normalize()

    player.acceleration = direction * accel


def check_collision():

    global player

    if player is None:
        return

	
    if player.position.x > screen_size[0] or player.position.x < 0:
            e = BurstEmitter(100, 3)
            e.emit(player.position)
            emitters.append(e)

            player = None
            hit_sfx.play()
            return

    elif player.position.y > screen_size[1] or player.position.y < 0:
            e = BurstEmitter(100, 3)
            e.emit(player.position)
            emitters.append(e)

            player = None
            hit_sfx.play()
            return


    for a, asteroid in reversed(list(enumerate(asteroids))):

        if player.collider.overlaps(asteroid.collider):

            e = BurstEmitter(100, 3)
            e.emit(player.position)
            emitters.append(e)


            player = None
            hit_sfx.play()
            break




        for b, bullet in reversed(list(enumerate(bullets))):

            if asteroid.collider.overlaps(bullet.collider):

                e = BurstEmitter(15, 3)

                e.emit(bullet.position)

                emitters.append(e)
                global score 
                score = score+1


                del asteroids[a]
                del bullets[b]
                hit_sfx.play()
                break


delta_time = 0.0
last_frame_time = 0.0

asteroid_spawn_time = 2.0
asteroid_timer = 0.0

shoot_timer=0.25
shoot_time=0

quit = False
while not quit:

    start_frame_time = pygame.time.get_ticks()
    
    shoot_time += delta_time
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit = True


        if shoot_time >= shoot_timer:
            if pygame.mouse.get_pressed()[0]:
                shoot()
                shoot_time = 0
        
            
            

    keys = pygame.key.get_pressed()
    take_input(keys)

    if player is not None:
        player.update(delta_time)

    # for b in bullets:
    #    b.update(delta_time)

    for i, bullet in reversed(list(enumerate(bullets))):
        bullet.update(delta_time)
        e = BurstEmitter2(1, 1)

        e.emit(bullet.position)

        emitters.append(e)
        if bullet.life <= 0:
            del bullets[i]

    for a in asteroids:
        a.update(delta_time)

    asteroid_timer += delta_time
    if asteroid_timer >= asteroid_spawn_time:
        spawn_asteroid()
        asteroid_timer = 0

    for i, emitter in reversed(list(enumerate(emitters))):

        emitter.update(delta_time)

        if emitter.is_done():
            del emitters[i]

    check_collision()

    screen.fill((25, 10, 35))
    label = myfont.render("Score: %s" % score, 2, (255,255,255))
    screen.blit(label, (20, 20))

    if player is not None:
        player.render(screen)

    for b in bullets:
        b.render(screen)

    for a in asteroids:
        a.render(screen)

    for e in emitters:
        e.render(screen)

    pygame.display.update()


    # Get elapsed time between frames in seconds
    delta_time = (start_frame_time - last_frame_time) / 1000.0

    last_frame_time = start_frame_time

# Clean up
pygame.quit()
sys.exit()
