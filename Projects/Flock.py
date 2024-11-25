import turtle
from random import random, randint
from math import sqrt

turtle.tracer(3)

class Target:
    def __init__(self) -> None:
        self.t = turtle.Turtle() 
        self.t.hideturtle()
        self.t.speed(0)
        self.t.penup()
        self.x, self.y = 0, 0
    
    def remove(self) -> None:
        self.t.clear()
    
    def place(self, x, y) -> None:
        self.t.setpos(x, y)
        self.t.dot(15, "red")
        self.x, self.y = x, y
        self.left_angle = 0

class Bird:
    def __init__(self, speed: int) -> None:
        self.speed = speed
        self.t = turtle.Turtle()
        self.x, self.y = self.t.pos()
        self.vel_x, self.vel_y = 0, 0
        self.best_x, self.best_y = self.x, self.y
        self.left_angle = 0
        self.t.penup()
        self.t.speed(0)

    def update_pos(self, x, y, target) -> None:
        target_left_angle = self.t.towards(x, y)
        angle = (target_left_angle - self.left_angle) % 360
        if angle < 180:
            self.t.left(angle)
        else:
            self.t.right(360 - angle)
        self.left_angle = target_left_angle
        
        self.t.setpos(x, y)
        self.x, self.y = self.t.pos()
        old_distance = sqrt((self.best_x - target.x) ** 2 + (self.best_y - target.y) ** 2)
        new_distance = sqrt((x - target.x) ** 2 + (y - target.y) ** 2)
        if new_distance < old_distance:
            self.best_x = x
            self.best_y = y

class Flock:
    def __init__(self, n: int) -> None:
        self.particles = [Bird(25) for _ in range(n)]
        self.gbest_x, self.gbest_y = 0, 0

    def in_prox_to(self, x, y, radius) -> bool:
        for p in self.particles:
            if p.t.distance(x, y) > radius:
                return False
        return True

    def spread(self, target) -> None:
        for p in self.particles:
            rand_x = randint(target.x - 50, target.x + 50)
            rand_y = randint(target.y - 50, target.y + 50)
            p.update_pos(rand_x, rand_y, target)
    
    def fly_to(self, target: Target) -> None:
        while not self.in_prox_to(target.x, target.y, 50):
            distances = {}
            for p in self.particles:
                cur_x, cur_y = p.x, p.y
                vel_x0, vel_y0 = p.vel_x, p.vel_y
                best_x, best_y = p.best_x, p.best_y

                r1 = random()
                r2 = random()
                c1 = 0.1
                c2 = 0.05
                
                vel_x1 = vel_x0 + c1 * r1 * (best_x - cur_x) + c2 * r2 * (self.gbest_x - cur_x)
                vel_y1 = vel_y0 + c1 * r1 * (best_y - cur_y) + c2 * r2 * (self.gbest_y - cur_y)
                
                if vel_x1 > p.speed:
                    vel_x1 = p.speed
                elif vel_x1 < -1 * p.speed:
                    vel_x1 = -1 * p.speed
                    
                if vel_y1 > p.speed:
                    vel_y1 = p.speed
                elif vel_y1 < -1 * p.speed:
                    vel_y1 = -1 * p.speed
                
                new_x = cur_x + vel_x1
                new_y = cur_y + vel_y1

                p.update_pos(new_x, new_y, target)
                p.vel_x, p.vel_y = vel_x1, vel_y1

                new_distance = sqrt((p.x - target.x) ** 2 + (p.y - target.y) ** 2)
                distances[new_distance] = (p.x, p.y)
            old_global_distance = sqrt((self.gbest_x - target.x) ** 2 + (self.gbest_y - target.y) ** 2)
            new_global_distance = min(distances)

            if new_global_distance < old_global_distance:
                self.gbest_x, self.gbest_y = distances[new_global_distance]


birds = Flock(50)
target = Target()

birds.spread(target)

def on_click(x, y):
    target.remove()
    target.place(x, y)
    birds.fly_to(target)

turtle.onscreenclick(on_click)
turtle.mainloop()