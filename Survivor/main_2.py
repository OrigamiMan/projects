import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Tile and character settings
TILE_WIDTH = 803
TILE_HEIGHT = 1335
CHARACTER_SIZE = 64
JOYSTICK_RADIUS = 50
MOVEMENT_DEADZONE = 20
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
TRANSPARENT_GRAY = (200, 200, 200, 150)
LARGE_AREA_RADIUS = 5000
LOADED_AREA_RADIUS = 3000

# Orb settings
ORB_SIZE = 8
TARGET_ORB_COUNT = 200
EXPERIENCE_BAR_HEIGHT = 15

# Enemy settings
ENEMY_SIZE = 20
ENEMY_SPEED = 2
ENEMY_DAMAGE = 10
ENEMY_ATTACK_COOLDOWN = 2  # Cooldown in seconds
MAX_ENEMIES = 100
SPAWN_RADIUS = 600
ENEMY_COLLISION_RADIUS = 25

# Base stats
BASE_PICKUP_RANGE = 10
BASE_SPEED = 5

# Load assets
stationary_spritesheet = pygame.image.load("assets/stationary.png")
stationary_spritesheet = pygame.transform.scale(stationary_spritesheet, (CHARACTER_SIZE * 4, CHARACTER_SIZE * 8))
moving_spritesheet = pygame.image.load("assets/moving.png")
moving_spritesheet = pygame.transform.scale(moving_spritesheet, (CHARACTER_SIZE * 4, CHARACTER_SIZE * 8))
tile_image = pygame.image.load("assets/Tiles.png")
tile_image = pygame.transform.scale(tile_image, (TILE_WIDTH, TILE_HEIGHT))

# Load orb sprites
blue_orb = pygame.image.load("assets/blue_orb.png")
blue_orb = pygame.transform.scale(blue_orb, (ORB_SIZE, ORB_SIZE))

orange_orb = pygame.image.load("assets/orange_orb.png")
orange_orb = pygame.transform.scale(orange_orb, (ORB_SIZE, ORB_SIZE))

purple_orb = pygame.image.load("assets/purple_orb.png")
purple_orb = pygame.transform.scale(purple_orb, (ORB_SIZE, ORB_SIZE))


class ExperienceOrb:
    def __init__(self, x, y, orb_type):
        self.x = x
        self.y = y
        self.type = orb_type
        self.image = blue_orb if orb_type == 'blue' else orange_orb if orb_type == 'orange' else purple_orb
        self.value = 1 if orb_type == 'blue' else 3 if orb_type == 'orange' else 20

    def draw(self, screen, offset_x, offset_y):
        screen_x = self.x - offset_x + SCREEN_WIDTH // 2
        screen_y = self.y - offset_y + SCREEN_HEIGHT // 2
        screen.blit(self.image, (int(screen_x - ORB_SIZE / 2), int(screen_y - ORB_SIZE / 2)))

    def is_near(self, player_x, player_y, pickup_range):
        return math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2) < pickup_range


class World:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.orbs = []

    def draw(self, screen):
        horizontal_tiles = (SCREEN_WIDTH // TILE_WIDTH) + 2
        vertical_tiles = (SCREEN_HEIGHT // TILE_HEIGHT) + 2

        for i in range(-horizontal_tiles, horizontal_tiles + 1):
            for j in range(-vertical_tiles, vertical_tiles + 1):
                tile_x = i * TILE_WIDTH - self.offset_x % TILE_WIDTH
                tile_y = j * TILE_HEIGHT - self.offset_y % TILE_HEIGHT
                screen.blit(
                    tile_image,
                    (tile_x + SCREEN_WIDTH // 2 - TILE_WIDTH // 2, tile_y + SCREEN_HEIGHT // 2 - TILE_HEIGHT // 2),
                )

    def update(self, mouse_anchor, mouse_position, player_speed):
        dx = mouse_position[0] - mouse_anchor[0]
        dy = mouse_position[1] - mouse_anchor[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance < MOVEMENT_DEADZONE:
            return 0, 0

        move_x = (dx / distance) * player_speed
        move_y = (dy / distance) * player_speed

        self.offset_x += move_x
        self.offset_y += move_y

        return move_x, move_y

    def maintain_orb_count(self):
        """Ensure the number of orbs stays at the target count."""
        while len(self.orbs) < TARGET_ORB_COUNT:
            orb_type = random.choices(['blue', 'orange', 'purple'], [100, 10, 1])[0]
            x = random.randint(
                int(self.offset_x - LOADED_AREA_RADIUS), int(self.offset_x + LOADED_AREA_RADIUS)
            )
            y = random.randint(
                int(self.offset_y - LOADED_AREA_RADIUS), int(self.offset_y + LOADED_AREA_RADIUS)
            )
            self.orbs.append(ExperienceOrb(x, y, orb_type))

    def clean_up_orbs(self):
        self.orbs = [orb for orb in self.orbs if math.sqrt(orb.x**2 + orb.y**2) < LARGE_AREA_RADIUS]


class Enemy:
    def __init__(self, player_x, player_y):
        """Spawn an enemy offscreen around the player."""
        angle = random.uniform(0, 2 * math.pi)
        distance = random.randint(SPAWN_RADIUS, SPAWN_RADIUS + 200)
        self.x = player_x + math.cos(angle) * distance
        self.y = player_y + math.sin(angle) * distance
        self.last_attack_time = 0  # Keeps track of the last attack time for cooldown

    def move_towards(self, target_x, target_y):
        """Move the enemy towards the target position."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.x += (dx / distance) * ENEMY_SPEED
            self.y += (dy / distance) * ENEMY_SPEED

    def handle_collisions(self, enemies):
        """Prevent enemies from overlapping by applying a simple repulsion force."""
        for other in enemies:
            if other is self:
                continue
            distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
            if distance < ENEMY_COLLISION_RADIUS and distance > 0:
                dx = self.x - other.x
                dy = self.y - other.y
                self.x += dx / distance * 0.5
                self.y += dy / distance * 0.5

    def draw(self, screen, offset_x, offset_y):
        """Draw the enemy on the screen."""
        screen_x = self.x - offset_x + SCREEN_WIDTH // 2
        screen_y = self.y - offset_y + SCREEN_HEIGHT // 2
        pygame.draw.rect(screen, (0, 0, 0), (int(screen_x - ENEMY_SIZE / 2), int(screen_y - ENEMY_SIZE / 2), ENEMY_SIZE, ENEMY_SIZE))

    def can_attack(self, current_time):
        """Check if the enemy can attack based on cooldown."""
        if current_time - self.last_attack_time >= ENEMY_ATTACK_COOLDOWN:
            self.last_attack_time = current_time
            return True
        return False

    def is_colliding(self, target_x, target_y):
        """Check if the enemy is colliding with the target (player)."""
        return math.sqrt((self.x - target_x) ** 2 + (self.y - target_y) ** 2) < ENEMY_SIZE

class Character:
    def __init__(self):
        # Basic attributes
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.last_direction = 0
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.frame_count = 4

        # Player stats
        self.health = 100
        self.max_health = 100
        self.level = 0
        self.experience = 0
        self.experience_to_level_up = 20
        self.pickup_range = 100  # Percentage
        self.speed = 100  # Percentage
        self.regeneration = 0.001  # Percentage of max health per second
        self.show_stats = False

    def get_direction(self, dx, dy):
        angle = math.degrees(math.atan2(-dy, dx))
        if -22.5 <= angle < 22.5:
            return 6
        elif 22.5 <= angle < 67.5:
            return 5
        elif 67.5 <= angle < 112.5:
            return 4
        elif 112.5 <= angle < 157.5:
            return 3
        elif -67.5 <= angle < -22.5:
            return 7
        elif -112.5 <= angle < -67.5:
            return 0
        elif -157.5 <= angle < -112.5:
            return 1
        else:
            return 2

    def load_frame(self, spritesheet, direction, frame):
        x = frame * CHARACTER_SIZE
        y = direction * CHARACTER_SIZE
        return spritesheet.subsurface((x, y, CHARACTER_SIZE, CHARACTER_SIZE))

    def draw(self, screen, dx, dy, is_moving):
        if is_moving:
            self.last_direction = self.get_direction(dx, dy)
            self.animation_frame += self.animation_speed
        else:
            self.animation_frame += self.animation_speed

        frame = int(self.animation_frame) % self.frame_count
        spritesheet = moving_spritesheet if is_moving else stationary_spritesheet
        sprite = self.load_frame(spritesheet, self.last_direction, frame)
        screen.blit(sprite, (self.x - CHARACTER_SIZE // 2, self.y - CHARACTER_SIZE // 2))

        # Draw the health bar below the character
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        """Draw a health bar below the character."""
        bar_width = 40
        bar_height = 5
        bar_x = self.x - bar_width // 2
        bar_y = self.y + CHARACTER_SIZE // 2 + 5

        # Health percentage
        health_percentage = self.health / self.max_health

        # Health bar color based on percentage
        if health_percentage > 0.5:
            color = (0, 255, 0)  # Green
        elif health_percentage > 0.25:
            color = (255, 165, 0)  # Orange
        else:
            color = (255, 0, 0)  # Red

        # Draw the background bar (gray)
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        # Draw the filled portion
        pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_width * health_percentage), bar_height))

    def add_experience(self, amount):
        """Add experience, level up if needed."""
        self.experience += amount
        if self.experience >= self.experience_to_level_up:
            self.experience = 0
            self.level += 1
            self.experience_to_level_up = int(self.experience_to_level_up * 1.05)

    def regenerate_health(self, delta_time):
        """Regenerate health over time."""
        regen_amount = self.regeneration * self.max_health * delta_time
        self.health = min(self.health + regen_amount, self.max_health)

    def toggle_stats(self):
        """Toggle the display of stats."""
        self.show_stats = not self.show_stats
        
    def draw_experience_bar(self, screen):
        """Draw the semi-transparent experience bar at the top of the screen."""
        # Background of the bar
        bar_surface = pygame.Surface((SCREEN_WIDTH, EXPERIENCE_BAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(bar_surface, TRANSPARENT_GRAY, (0, 0, SCREEN_WIDTH, EXPERIENCE_BAR_HEIGHT))
        screen.blit(bar_surface, (0, 0))

        # Filled portion of the bar
        fill_width = (self.experience / self.experience_to_level_up) * SCREEN_WIDTH
        pygame.draw.rect(screen, LIGHT_BLUE, (0, 0, fill_width, EXPERIENCE_BAR_HEIGHT))


    def draw_stats(self, screen):
        """Display the player's stats on the screen."""
        if not self.show_stats:
            return

        font = pygame.font.SysFont(None, 24)
        stats = [
            f"Health: {int(self.health)}/{self.max_health}",
            f"Level: {self.level}",
            f"XP: {self.experience}/{self.experience_to_level_up}",
            f"Pickup Range: {self.pickup_range}%",
            f"Speed: {self.speed}%",
            f"Regeneration: {self.regeneration:.2%} / sec",
        ]
        for i, stat in enumerate(stats):
            text = font.render(stat, True, (0, 0, 0))
            screen.blit(text, (10, 20 + i * 20))

    def get_pickup_range(self):
        """Calculate the actual pickup range based on the stat."""
        return BASE_PICKUP_RANGE * (self.pickup_range / 100)

    def get_speed(self):
        """Calculate the actual movement speed based on the stat."""
        return BASE_SPEED * (self.speed / 100)
            
class Joystick:
    def __init__(self):
        self.anchor = None
        self.active = False

    def activate(self, anchor):
        self.anchor = anchor
        self.active = True

    def deactivate(self):
        self.active = False

    def draw(self, screen, mouse_position):
        if not self.active:
            return

        joystick_surface = pygame.Surface((JOYSTICK_RADIUS * 2, JOYSTICK_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(joystick_surface, TRANSPARENT_GRAY, (JOYSTICK_RADIUS, JOYSTICK_RADIUS), JOYSTICK_RADIUS)
        screen.blit(joystick_surface, (self.anchor[0] - JOYSTICK_RADIUS, self.anchor[1] - JOYSTICK_RADIUS))

        dx = mouse_position[0] - self.anchor[0]
        dy = mouse_position[1] - self.anchor[1]
        distance = min(math.sqrt(dx**2 + dy**2), JOYSTICK_RADIUS - 10)

        if distance > 0:
            angle = math.atan2(dy, dx)
            handle_x = self.anchor[0] + distance * math.cos(angle)
            handle_y = self.anchor[1] + distance * math.sin(angle)
            pygame.draw.circle(screen, WHITE, (int(handle_x), int(handle_y)), 10)



def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Character, World, and Enemies")

    clock = pygame.time.Clock()
    running = True

    character = Character()
    world = World()
    joystick = Joystick()
    enemies = []

    mouse_held = False
    mouse_anchor = (0, 0)
    enemy_spawn_timer = 0
    start_time = pygame.time.get_ticks()

    while running:
        screen.fill(WHITE)
        current_time = (pygame.time.get_ticks() - start_time) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_held = True
                    mouse_anchor = pygame.mouse.get_pos()
                    joystick.activate(mouse_anchor)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_held = False
                joystick.deactivate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Toggle stats display
                    character.toggle_stats()

        if character.health <= 0:
            font = pygame.font.SysFont(None, 48)
            game_over_text = font.render(f"Game Over! Time Survived: {int(current_time)}s", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
            continue
        
        if mouse_held:
            mouse_position = pygame.mouse.get_pos()
            dx, dy = world.update(mouse_anchor, mouse_position, character.get_speed())
        else:
            dx, dy = 0, 0

        # Ensure 100 orbs exist
        world.maintain_orb_count()

        # Enemy spawning logic
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= 60 and len(enemies) < MAX_ENEMIES:
            enemies.append(Enemy(world.offset_x, world.offset_y))
            enemy_spawn_timer = 0

        for enemy in enemies:
            enemy.move_towards(world.offset_x, world.offset_y)
            enemy.handle_collisions(enemies)
            if enemy.is_colliding(world.offset_x, world.offset_y) and enemy.can_attack(current_time):
                character.health -= ENEMY_DAMAGE

        for orb in world.orbs[:]:
            if orb.is_near(world.offset_x, world.offset_y, character.pickup_range):
                character.add_experience(orb.value)
                world.orbs.remove(orb)

        # Draw world, orbs, enemies, and character
        world.draw(screen)
        for orb in world.orbs:
            orb.draw(screen, world.offset_x, world.offset_y)
        for enemy in enemies:
            enemy.draw(screen, world.offset_x, world.offset_y)
        joystick.draw(screen, pygame.mouse.get_pos())
        character.draw(screen, dx, dy, is_moving=mouse_held)
        character.draw_experience_bar(screen)
        character.draw_stats(screen)
        character.regenerate_health(1/FPS)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


main()