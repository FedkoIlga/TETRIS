# импортируем библиотеку pygame
import pygame
# импортируем библиотеку random для генерации случайных чисел
import random
# импортируем библиотеку copy для глубокого копирования
import copy

# инициализация всех модулей pygame
pygame.init()

# количество столбцов сетки
columns = 10  # ИЗМЕНЕНО: теперь реальное количество столбцов
# количество строк сетки
strings = 20  # ИЗМЕНЕНО: теперь реальное количество строк

# ширина окна игры
screen_x = 300  # ИЗМЕНЕНО: немного увеличил для лучшего отображения
# высота окна игры
screen_y = 600  # ИЗМЕНЕНО: соответственно увеличил высоту

# создаём окно игры
screen = pygame.display.set_mode((screen_x, screen_y))
# устанавливаем заголовок окна
pygame.display.set_caption("Tetris CODE")
# создаём объект для отслеживания времени
clock = pygame.time.Clock()

# ширина одной ячейки сетки
cell_x = screen_x / columns  # ИЗМЕНЕНО: убрал -1
# высота одной ячейки сетки
cell_y = screen_y / strings  # ИЗМЕНЕНО: убрал -1

# частота кадров в секунду
fps = 60

# создаём пустой список для хранения сетки
grid = []

# проходим по каждому столбцу
for i in range(columns):
    # добавляем пустой список для каждого столбца
    grid.append([])
    # создаём количество ячеек, равное строкам,
    # и заполняем их значениями 1 (ячейка свободна)
    for j in range(strings):
        grid[i].append([1])

# проходим по каждой ячейке ещё раз
for i in range(columns):
    for j in range(strings):
        # добавляем ещё два параметра: создаём область прямоугольника и задаём цвет для каждой ячейки
        grid[i][j].append(pygame.Rect(i * cell_x, j * cell_y, cell_x, cell_y))
        grid[i][j].append(pygame.Color("Gray"))

# описание фигур Тетриса
details = [
    # линия
    [[-2, 0], [-1, 0], [0, 0], [1, 0]], 
    # L-образная
    [[-1, 1], [-1, 0], [0, 0], [1, 0]], 
    # обратная L-образная
    [[1, 1], [-1, 0], [0, 0], [1, 0]], 
    # квадрат
    [[-1, 1], [0, 1], [0, 0], [-1, 0]], 
    # Z-образная
    [[1, 0], [1, 1], [0, 0], [-1, 0]], 
    # обратная Z-образная
    [[0, 1], [-1, 0], [0, 0], [1, 0]], 
    # T-образная
    [[-1, 1], [0, 1], [0, 0], [1, 0]], 
]

# создаём список для хранения всех 7 фигур
det = [[], [], [], [], [], [], []]

# инициализация фигур: проходим по списку с описанием координат
for i in range(len(details)):
    for j in range(4):
        # создаём прямоугольные области для каждого составного квадрата
        # ИСПРАВЛЕНО: правильное позиционирование по центру
        det[i].append(pygame.Rect(
            details[i][j][0] * cell_x + cell_x * (columns // 2), 
            details[i][j][1] * cell_y, 
            cell_x, 
            cell_y
        ))

# создаём область Rect для одной ячейки фигуры
detail = pygame.Rect(0, 0, cell_x, cell_y)

# счётчик для управления скоростью падения фигур
count = 0
# флаг для управления игровым циклом
game = True
# флаг для управления поворотом фигур
rotate = False

# ДОБАВЛЕННЫЕ ПЕРЕМЕННЫЕ ДЛЯ УПРАВЛЕНИЯ ИГРОЙ
game_over = False  # флаг окончания игры
score = 0  # счётчик очков
font = pygame.font.Font(None, 36)  # шрифт для текста
small_font = pygame.font.Font(None, 24)  # маленький шрифт

# Функция для создания новой фигуры
def new_figure():
    return copy.deepcopy(random.choice(det))

# ИСПРАВЛЕНО: функция проверки столкновений
def check_collision(figure, offset_x=0, offset_y=0):
    for rect in figure:
        # Вычисляем координаты в сетке
        x = int(rect.x // cell_x) + offset_x
        y = int(rect.y // cell_y) + offset_y
        
        # Проверяем выход за границы
        if x < 0 or x >= columns or y >= strings:
            return True
        
        # Проверяем столкновение с другими фигурами
        if y >= 0:
            if grid[x][y][0] == 0:  # ячейка занята
                return True
    return False

# Функция для фиксации фигуры на поле
def fix_figure(figure, color):
    for rect in figure:
        x = int(rect.x // cell_x)
        y = int(rect.y // cell_y)
        if 0 <= x < columns and 0 <= y < strings:
            grid[x][y][0] = 0  # помечаем как занятую
            grid[x][y][2] = color  # устанавливаем цвет фигуры

# ИСПРАВЛЕНО: функция удаления заполненных линий
def remove_lines():
    global score
    lines_removed = 0
    lines_to_remove = []
    
    # Находим заполненные линии
    for y in range(strings):
        line_full = True
        for x in range(columns):
            if grid[x][y][0] == 1:  # если есть свободная ячейка
                line_full = False
                break
        if line_full:
            lines_to_remove.append(y)
    
    # Удаляем линии сверху вниз
    for y in sorted(lines_to_remove, reverse=True):
        lines_removed += 1
        # Сдвигаем все строки выше вниз
        for y2 in range(y, 0, -1):
            for x in range(columns):
                grid[x][y2][0] = grid[x][y2-1][0]
                grid[x][y2][2] = grid[x][y2-1][2]
        # Очищаем верхнюю строку
        for x in range(columns):
            grid[x][0][0] = 1
            grid[x][0][2] = pygame.Color("Gray")
    
    # Обновляем счёт
    if lines_removed == 1:
        score += 100
    elif lines_removed == 2:
        score += 300
    elif lines_removed == 3:
        score += 500
    elif lines_removed >= 4:
        score += 800

# ИСПРАВЛЕНО: функция проверки поражения
def check_game_over(figure):
    for rect in figure:
        y = int(rect.y // cell_y)
        # Если фигура коснулась верха (y < 0)
        if y < 0:
            return True
        # Проверяем столкновение с блоками в верхней части
        if y >= 0:
            x = int(rect.x // cell_x)
            if 0 <= x < columns:
                if grid[x][y][0] == 0:
                    return True
    return False

# Функция для сброса игры
def reset_game():
    global grid, game_over, score, det_choice
    # Очищаем сетку
    for i in range(columns):
        for j in range(strings):
            grid[i][j][0] = 1  # все ячейки свободны
            grid[i][j][2] = pygame.Color("Gray")  # серый цвет
    
    game_over = False
    score = 0
    det_choice = new_figure()

# Функция для отображения текста
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Создаём первую фигуру
det_choice = new_figure()

# Игровой цикл
while game:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        
        # Обработка нажатий клавиш только если игра не окончена
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Проверяем возможность движения влево
                    if not check_collision(det_choice, -1, 0):
                        for rect in det_choice:
                            rect.x -= cell_x
                
                elif event.key == pygame.K_RIGHT:
                    # Проверяем возможность движения вправо
                    if not check_collision(det_choice, 1, 0):
                        for rect in det_choice:
                            rect.x += cell_x
                
                elif event.key == pygame.K_UP:
                    # Поворот фигуры
                    if len(det_choice) > 2:
                        center = det_choice[2].copy()
                        
                        # Создаём повёрнутую фигуру
                        rotated_figure = []
                        for rect in det_choice:
                            # Вычисляем относительные координаты
                            rel_x = rect.x - center.x
                            rel_y = rect.y - center.y
                            
                            # Поворачиваем на 90 градусов (по часовой стрелке)
                            new_x = center.x - rel_y
                            new_y = center.y + rel_x
                            
                            # Создаём новый прямоугольник
                            new_rect = pygame.Rect(new_x, new_y, cell_x, cell_y)
                            rotated_figure.append(new_rect)
                        
                        # Проверяем, можно ли повернуть
                        if not check_collision(rotated_figure):
                            det_choice = rotated_figure
                
                elif event.key == pygame.K_DOWN:
                    # Ускоренное падение
                    count += fps
        
        # Обработка нажатия клавиш для перезапуска игры
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                reset_game()
    
    # Основная логика игры (только если не проиграли)
    if not game_over:
        # Управление скоростью падения
        count += 1
        speed = fps // 2  # нормальная скорость (30 кадров для падения)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            speed = fps // 10  # ускоренная скорость (6 кадров для падения)
        
        # Падение фигуры
        if count >= speed:
            count = 0
            
            # Проверяем возможность падения
            if not check_collision(det_choice, 0, 1):
                for rect in det_choice:
                    rect.y += cell_y
            else:
                # Фиксируем фигуру на поле
                fix_figure(det_choice, pygame.Color("Blue"))
                
                # Удаляем заполненные линии
                remove_lines()
                
                # Создаём новую фигуру
                det_choice = new_figure()
                
                # Проверяем поражение после появления новой фигуры
                if check_game_over(det_choice):
                    game_over = True
                    # Фиксируем фигуру для отображения
                    fix_figure(det_choice, pygame.Color("Red"))
    
    # Отрисовка
    screen.fill(pygame.Color(222, 248, 116, 100))
    
    # ИСПРАВЛЕНО: отрисовка сетки (теперь все ячейки видимы)
    for i in range(columns):
        for j in range(strings):
            if grid[i][j][0] == 0:  # если ячейка занята
                pygame.draw.rect(screen, grid[i][j][2], grid[i][j][1])
            else:  # если свободна
                pygame.draw.rect(screen, pygame.Color("Gray"), grid[i][j][1], 1)  # контур
    
    # Отрисовка текущей падающей фигуры
    if not game_over:
        for rect in det_choice:
            y = int(rect.y // cell_y)
            if y >= 0 and y < strings:  # отрисовываем только видимые части
                pygame.draw.rect(screen, pygame.Color("Blue"), rect)
    
    # Отображение счёта
    score_text = small_font.render(f"Счёт: {score}", True, pygame.Color("Black"))
    screen.blit(score_text, (10, 10))
    
    # Отображение окна поражения
    if game_over:
        # Затемняем экран
        s = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))
        
        # Рисуем окно поражения
        pygame.draw.rect(screen, pygame.Color("Red"), (screen_x//2 - 100, screen_y//2 - 60, 200, 120))
        pygame.draw.rect(screen, pygame.Color("White"), (screen_x//2 - 100, screen_y//2 - 60, 200, 120), 3)
        
        # Текст поражения
        draw_text("ВЫ ПРОИГРАЛИ!", small_font, pygame.Color("White"), 
                  screen_x//2, screen_y//2 - 30)
        draw_text(f"Счёт: {score}", small_font, pygame.Color("White"), 
                  screen_x//2, screen_y//2)
        draw_text("Пробел - заново", small_font, pygame.Color("White"), 
                  screen_x//2, screen_y//2 + 30)
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()