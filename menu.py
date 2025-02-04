import sys
import pygame


# Главная функция, которая запускает меню игры
def main_menu(achievements, language):
    pygame.init()  # Инициализация библиотеки pygame

    # Установка параметров экрана
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Roguelike Game - Main Menu")

    # Определение основных цветов
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    GREEN = (0, 255, 0)  # Для выделения полученных достижений

    # Загрузка фоновой музыки
    pygame.mixer.music.load("data/menu_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Включение музыки на повтор

    # Загрузка изображений фонов для разных экранов
    bg_main_menu = pygame.image.load("data/bg_main_menu.jpg")
    bg_settings = pygame.image.load("data/bg_settings.jpg")
    bg_achievements = pygame.image.load("data/bg_achievements.jpg")  # Фон для экрана достижений

    # Шрифты для текста
    font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 50)

    # Словарь с текстами для разных языков
    texts = {
        "ru": {
            "title": "Roguelike Игра",
            "buttons": ["Начать игру", "Настройки", "Достижения", "Выход"],
            "settings": ["Музыка: {status}", "Язык: Русский", "Громкость: {volume}%", "Уровень сложности"],
            "difficulty": ["Лёгкий", "Средний", "Тяжёлый"],
            "achievements": ["Достижения", "Первое прохождение", "Коллекционер", "Первый враг"]
        },
        "en": {
            "title": "Roguelike Game",
            "buttons": ["Start Game", "Settings", "Achievements", "Exit"],
            "settings": ["Music: {status}", "Language: English", "Volume: {volume}%", "Difficulty Level"],
            "difficulty": ["Easy", "Medium", "Hard"],
            "achievements": ["Achievements", "First Playthrough", "Collector", "First Enemy"]
        }
    }

    # Уровень сложности игры (по умолчанию Средний)
    difficulty_level = 1  # 0 - Лёгкий, 1 - Средний, 2 - Тяжёлый

    # Функция для получения текста на выбранном языке
    def get_text(key):
        return texts[language][key]

    # Создание кнопок для главного меню
    def create_buttons():
        button_labels = get_text("buttons")
        return [(button_font.render(label, True, WHITE), pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + i * 70, 300, 60))
                for i, label in enumerate(button_labels)]

    # Функция для отображения меню выбора уровня сложности
    def show_difficulty_menu():
        nonlocal difficulty_level
        while True:
            screen.blit(bg_settings, (0, 0))  # Используем фон из настроек для экрана сложности
            diff_texts = get_text("difficulty")
            button_rects = []

            for i, label in enumerate(diff_texts):
                color = (0, 255, 0) if i == difficulty_level else WHITE
                button_surf = button_font.render(label, True, color)
                button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 + i * 80, 200, 60)
                button_rects.append((button_surf, button_rect))

            for button_surf, button_rect in button_rects:
                pygame.draw.rect(screen, GRAY, button_rect, border_radius=15)
                screen.blit(button_surf, button_rect.topleft)

            # Обработка событий (нажатие кнопок)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, (_, button_rect) in enumerate(button_rects):
                        if button_rect.collidepoint(event.pos):
                            difficulty_level = i  # Устанавливаем выбранный уровень сложности
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            pygame.display.flip()

    # Функция для отображения настроек игры
    def show_settings():
        music_on = True
        volume = int(pygame.mixer.music.get_volume() * 100)

        while True:
            screen.blit(bg_settings, (0, 0))
            setting_texts = get_text("settings")
            buttons = [
                (button_font.render(setting_texts[0].format(status="Включена" if music_on else "Отключена"), True,
                                    WHITE), pygame.Rect(WIDTH // 2 - 150, HEIGHT // 4, 300, 60)),
                (button_font.render(setting_texts[1], True, WHITE),
                 pygame.Rect(WIDTH // 2 - 150, HEIGHT // 4 + 70, 300, 60)),
                (button_font.render(setting_texts[2].format(volume=volume), True, WHITE),
                 pygame.Rect(WIDTH // 2 - 150, HEIGHT // 4 + 140, 300, 60)),
                (button_font.render(setting_texts[3], True, WHITE),
                 pygame.Rect(WIDTH // 2 - 150, HEIGHT // 4 + 210, 300, 60))
            ]

            for button_surf, button_rect in buttons:
                pygame.draw.rect(screen, GRAY, button_rect, border_radius=15)
                screen.blit(button_surf, button_rect.topleft)

            # Обработка событий (нажатие кнопок)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0][1].collidepoint(event.pos):
                        music_on = not music_on  # Включаем или отключаем музыку
                        if music_on:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    elif buttons[1][1].collidepoint(event.pos):
                        nonlocal language
                        language = "en" if language == "ru" else "ru"  # Переключаем язык
                    elif buttons[2][1].collidepoint(event.pos):
                        volume = min(100, max(0, volume + (
                            10 if event.pos[0] > WIDTH // 2 else -10)))  # Увеличиваем/уменьшаем громкость
                        pygame.mixer.music.set_volume(volume / 100)
                    elif buttons[3][1].collidepoint(event.pos):
                        show_difficulty_menu()  # Переходим в меню выбора сложности
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            pygame.display.flip()

    # Функция для отображения экрана достижений
    def show_achievements():
        achievements["ach_1"] = True  # Сразу открываем первое достижение (для теста)

        while True:
            screen.blit(bg_achievements, (0, 0))  # Фон для меню достижений
            achievement_texts = get_text("achievements")
            y_offset = HEIGHT // 4
            for i, text in enumerate(achievement_texts[1:]):
                # Если достижение получено, делаем текст зелёным
                color = GREEN if achievements.get(f"ach_{i + 1}", False) else WHITE
                achievement_surf = button_font.render(
                    f"{text}: {'Получено' if achievements.get(f'ach_{i + 1}', False) else 'Не получено'}", True, color)
                screen.blit(achievement_surf, (WIDTH // 2 - achievement_surf.get_width() // 2, y_offset))
                y_offset += 70

            # Кнопка для выхода из меню достижений
            back_text = button_font.render("Назад", True, WHITE)
            screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 100))

            # Обработка событий (нажатие кнопки "Назад")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 100, back_text.get_width(),
                                   60).collidepoint(event.pos):
                        return  # Выход из экрана достижений
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            pygame.display.flip()

    # Создание кнопок для главного меню
    button_rects = create_buttons()

    # Главный игровой цикл
    while True:
        screen.blit(bg_main_menu, (0, 0))
        title_text = font.render(get_text("title"), True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        for button_text, button_rect in button_rects:
            pygame.draw.rect(screen, GRAY, button_rect, border_radius=15)
            screen.blit(button_text, button_rect.topleft)

        # Обработка событий (нажатие на кнопки)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (_, button_rect) in enumerate(button_rects):
                    if button_rect.collidepoint(event.pos):
                        if i == 1:
                            show_settings()  # Открытие настроек
                        elif i == 2:
                            show_achievements()  # Открытие достижений
                        elif i == 0:
                            # Начать игру с выбранным уровнем сложности
                            print(f"Starting game with difficulty: {difficulty_level}")
                            # запуск основного игрового цикла с нужным уровнем сложности
                        elif i == 3:
                            pygame.quit()
                            sys.exit()
        pygame.display.flip()


# Запуск программы с начальными достижениями
if __name__ == "__main__":
    achievements = {'ach_1': False, 'ach_2': False, 'ach_3': False}  # Пример начальных достижений
    language = "ru"
    main_menu(achievements, language)
