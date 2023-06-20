import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
window_width = 1000
window_height = 700

# Создание окна
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Игра с лампочкой")

# Загрузка изображения лампочки и изменение размера
lamp_image = pygame.image.load("lamp.png")
lamp_image = pygame.transform.scale(lamp_image, (lamp_image.get_width() // 4, lamp_image.get_height() // 4))

lamp_mirror_image = pygame.transform.flip(lamp_image, True, False)

# Загрузка изображения посоха и изменение размера
staff_image = pygame.image.load("staff.png")
staff_image = pygame.transform.scale(staff_image, (staff_image.get_width() // 12, staff_image.get_height() // 12))

# Загрузка зеркального изображения посоха
staff_mirror_image = pygame.transform.flip(staff_image, True, False)

# Загрузка изображения снаряда и изменение размера
projectile_image = pygame.image.load("projectile.png")
projectile_image = pygame.transform.scale(projectile_image,
                                          (projectile_image.get_width() // 6, projectile_image.get_height() // 6))

# Позиция и скорость лампочки
lamp_x = window_width // 2 - lamp_image.get_width() // 2
lamp_y = window_height - lamp_image.get_height() - 50  # Отступ под лампочкой
lamp_speed = 4
jump_speed = 6

# Позиция и скорость посоха
staff_x = lamp_x + lamp_image.get_width() // 2 - staff_image.get_width() // 2
staff_y = lamp_y + lamp_image.get_height() // 5 - staff_image.get_height() // 5
staff_speed = 8

# Список снарядов
projectiles = []

# Создание горизонта
horizon_height = window_height - 100

# Загрузка фоновых изображений для каждой локации
background_images = {
    "location1": pygame.image.load("background1.jpg"),
    "location2": pygame.image.load("background2.jpg"),
    "location3": pygame.image.load("background3.jpg")
}

# Индекс текущей локации
current_location = "location1"

clock = pygame.time.Clock()

# Флаги для направления движения
move_left = False
move_right = False
jumping = False
lamp_flipped = False
staff_flipped = False


class Boss:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.projectiles = []  # Список патронов босса

    def update(self, player_x, player_y):
        self.move_towards_player(player_x, player_y)
        self.shoot_projectile()

        # Обновление патронов босса
        updated_projectiles = []
        for projectile in self.projectiles:
            projectile.update()
            if projectile.rect.x < window_width:  # Проверка, чтобы патроны не выходили за границы окна
                updated_projectiles.append(projectile)
        self.projectiles = updated_projectiles

    def move_towards_player(self, player_x, player_y):
        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance
        if not self.flipped:
            self.rect.x += dx * self.speed
        else:
            self.rect.x -= dx * self.speed
        self.rect.y += dy * self.speed

    def shoot_projectile(self):
        if random.randint(0, 100) < 2:  # Вероятность выстрела патрона
            projectile = Projectile(projectile_image, self.rect.centerx, self.rect.centery)
            self.projectiles.append(projectile)

    def draw_projectiles(self):
        if self.flipped:
            flipped_projectiles = [pygame.transform.flip(projectile.image, True, False) for projectile in
                                   self.projectiles]
            for projectile in flipped_projectiles:
                window.blit(projectile, projectile.rect)
        else:
            for projectile in self.projectiles:
                window.blit(projectile.image, projectile.rect)

        for projectile in self.projectiles:
            if lamp_flipped:
                window.blit(pygame.transform.flip(projectile.image, True, False), projectile.rect)
            else:
                window.blit(projectile.image, projectile.rect)


class Projectile:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed


# Создание босса
boss_image = pygame.image.load("boss.png")
boss_image = pygame.transform.scale(boss_image, (lamp_image.get_width(), lamp_image.get_height()))
boss = Boss(boss_image, 500, 200)

# Главный цикл игры
running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            elif event.key == pygame.K_d:
                move_right = True
            elif event.key == pygame.K_w and not jumping and lamp_y == window_height - lamp_image.get_height() - 50:
                jumping = True
            elif event.key == pygame.K_RETURN:
                projectile_x = staff_x + staff_image.get_width()
                projectile_y = staff_y + staff_image.get_height() // 2 - projectile_image.get_height() // 2
                if move_left:
                    projectile_x -= projectile_image.get_width()  # Смещение снаряда влево
                projectiles.append((projectile_x, projectile_y))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            elif event.key == pygame.K_d:
                move_right = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                current_slot = "staff"
                staff_selected = True
            elif event.button == 5:
                current_slot = None
                staff_selected = False

    # Движение лампочки и посоха
    if move_left and lamp_x > 0:
        lamp_x -= lamp_speed
        staff_x -= lamp_speed
    if move_right and lamp_x + lamp_image.get_width() < window_width:
        lamp_x += lamp_speed
        staff_x += lamp_speed

    # Прыжок лампочки
    if jumping:
        lamp_y -= jump_speed
        jump_speed -= 1
        if jump_speed == -7:
            jumping = False
            jump_speed = 6
        if lamp_y == horizon_height - lamp_image.get_height():
            jumping = False
            jump_speed = 6

    # Загрузка фона текущей локации
    background_image = background_images[current_location]
    window.blit(background_image, (0, 0))

    boss.flipped = lamp_flipped

    # Отрисовка и обновление босса
    boss.update(lamp_x, lamp_y)
    window.blit(boss.image, boss.rect)
    boss.draw_projectiles()

    # Отрисовка горизонта
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, horizon_height, window_width, window_height - horizon_height))

    # Отрисовка снарядов
    updated_projectiles = []
    for projectile in projectiles:
        projectile_x, projectile_y = projectile
        window.blit(projectile_image, (projectile_x, projectile_y))
        projectile_x += 10  # Скорость снаряда
        if projectile_x < window_width:
            updated_projectiles.append((projectile_x, projectile_y))
    projectiles = updated_projectiles

    # Отрисовка лампочки и посоха
    if move_left:
        window.blit(lamp_mirror_image, (lamp_x, lamp_y))
        window.blit(staff_mirror_image, (staff_x, staff_y))
    else:
        window.blit(lamp_image, (lamp_x, lamp_y))
        window.blit(staff_image, (staff_x, staff_y))

    # Обновление окна
    pygame.display.flip()
    clock.tick(60)

# Завершение игры
pygame.quit()
