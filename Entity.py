
from pygame import draw
from Vector2 import Vector2
from Circle import Circle
import random
import math
import weakref


# This class describes game objects in our game
class Entity(object):

    def __init__(self):

        # R G B
        # default color is white
        self.color = (255, 255, 255)

        self.graphicsBounds = Circle(Vector2(0.0, 0.0), 1)

        self.collider = Circle(Vector2(0.0, 0.0), 1)

        self.position = Vector2(0.0, 0.0)
        self.velocity = Vector2(0.0, 0.0)

        self.acceleration = Vector2(0.0, 0.0)

        self.max_speed = 400

    def update(self, dt):

        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

        # cap speed
        if self.velocity.magnitude() >= self.max_speed:
            self.velocity.set_magnitude(self.max_speed)

        # Update graphical and physical bounds
        self.graphicsBounds.center = self.position
        self.collider.center = self.position

    def render(self, screen):

        center = self.graphicsBounds.center
        radius = self.graphicsBounds.radius

        # Pygame needs a 2-tuple of integers as the center of a circle
        center_int = (int(center.x), int(center.y))

        draw.circle(screen, self.color, center_int, radius)


class Bullet(Entity):

    def __init__(self, range, position, velocity):

        # Construct parent so we have all of the Entities properties
        # like position, velocity...
        super(Bullet, self).__init__()

        # How far the bullet travels
        self.range = range

        self.position = Vector2(position.x, position.y)
        self.velocity = Vector2(velocity.x, velocity.y)

        # The time needed to travel a certain range
        self.life = range / self.velocity.magnitude()

    def update(self, dt):

        # Call parent update so we can still move
        super(Bullet, self).update(dt)

        # Kill the bullet slowly
        self.life -= dt


class Asteroid(Entity):

    def __init__(self, target, homing_speed):

        super(Asteroid, self).__init__()

        self.target = weakref.ref(target)

        self.homing_speed = homing_speed

    def update(self, dt):

        super(Asteroid, self).update(dt)

        self.follow()

    def follow(self):

        if self.target() is None:
            return

        to_target = Vector2.get_normal(self.target().position - self.position)

        self.acceleration = to_target * self.homing_speed


class Particle(Entity):

    def __init__(self, life, position, velocity):

        super(Particle, self).__init__()

        self.life = life
        self.position = Vector2(position.x, position.y)
        self.velocity = Vector2(velocity.x, velocity.y)

        self.active = False

    def update(self, dt):

        if not self.active:
            return

        super(Particle, self).update(dt)

        self.life -= dt

        if self.life <= 0:
            self.active = False

    def render(self, screen):

        if self.active:
            super(Particle, self).render(screen)


class BurstEmitter(Entity):

    def __init__(self, particle_count, max_life):

        self.particles = list()

        for i in xrange(0, particle_count):
            self.particles.append(Particle(1, Vector2(0, 0), Vector2(0, 0)))

        self.life = max_life

    def update(self, dt):

        for p in self.particles:
            p.update(dt)

        self.life -= dt

    def render(self, screen):

        for p in self.particles:
            p.render(screen)

    def emit(self, position):

        for p in self.particles:

            p.active = True

            p.position = Vector2(position.x, position.y)

            p.velocity = Vector2(1, 0)
            p.velocity.set_direction(random.uniform(0, 2 * math.pi))
            p.velocity.set_magnitude(random.randint(200, 500))

            size = random.randint(2, 8)
            p.graphicsBounds.radius = size

            p.life = random.uniform(0.2, 2.5)

            p.color = (0, 255, 0)

    def is_done(self):
        return self.life <= 0
        
class BurstEmitter2(Entity):

    def __init__(self, particle_count, max_life):

        self.particles = list()

        for i in xrange(0, particle_count):
            self.particles.append(Particle(1, Vector2(0, 0), Vector2(0, 0)))

        self.life = max_life

    def update(self, dt):

        for p in self.particles:
            p.update(dt)

        self.life -= dt

    def render(self, screen):

        for p in self.particles:
            p.render(screen)

    def emit(self, position):

        for p in self.particles:

            p.active = True

            p.position = Vector2(position.x, position.y)

            p.velocity = Vector2(1, 0)
            p.velocity.set_direction(random.uniform(0, 1 * math.pi))
            p.velocity.set_magnitude(random.randint(50, 100))

            size = random.randint(2, 8)
            p.graphicsBounds.radius = size

            p.life = random.uniform(0.2, 2.5)

            p.color = (0, 255, 255)

    def is_done(self):
        return self.life <= 0
