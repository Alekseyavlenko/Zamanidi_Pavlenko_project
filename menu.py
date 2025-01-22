import sys
from game import game_sobstvenno
import pygame


def main_menu(achievements, language):
    pygame.init()

    # Настройки окна
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Roguelike Game - Main Menu")

    # Цвета
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Загрузка музыки
    pygame.mixer.music.load("data/menu_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # музыка в цикле

    # Загрузка фонов
    bg_main_menu = pygame.image.load("data/bg_main_menu.jpg")
    bg_settings = pygame.image.load("data/bg_settings.jpg")
    bg_achievements = pygame.image.load("data/bg_achievements.jpg")

    # Шрифты
    font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 50)
    achievement_font = pygame.font.Font(None, 36)

    # Текст для языков
    texts = {
        "ru": {
            "title": "Roguelike Игра",
            "buttons": ["Начать игру", "Настройки", "Достижения", "Выход"],
            "achievements": [
                "Первооткрыватель - {status}",
                "Исследователь - {status}",
                "Спартанец - {status}"
            ],
            "settings": ["Музыка: {status}", "Язык: Русский"],
        },
        "en": {
            "title": "Roguelike Game",
            "buttons": ["Start Game", "Settings", "Achievements", "Exit"],
            "achievements": [
                "Pioneer - {status}",
                "Explorer - {status}",
                "Spartan - {status}"
            ],
            "settings": ["Music: {status}", "Language: English"],
        }
    }

    def get_text(key):
        return texts[language][key]

    # Кнопки
    def create_buttons():
        button_labels = get_text("buttons")
        button_rects = []
        for i, button in enumerate(button_labels):
            button_text = button_font.render(button, True, WHITE)
            button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))
            button_rects.append((button_text, button_rect))
        return button_rects

    button_rects = create_buttons()

    def show_achievements():
        while True:
            screen.blit(bg_achievements, (0, 0))
            achievement_texts = get_text("achievements")
            for i, text in enumerate(achievement_texts):
                status = "✓" if achievements[list(achievements.keys())[i]] else "✗"
                formatted_text = text.format(status=status)
                color = GREEN if "✓" in formatted_text else RED
                achievement_surf = achievement_font.render(formatted_text, True, color)
                text_rect = achievement_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4 + i * 70))
                pygame.draw.rect(screen, GRAY, text_rect.inflate(20, 10), border_radius=15)
                screen.blit(achievement_surf, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            pygame.display.flip()

    def show_settings():
        music_on = True

        while True:
            screen.blit(bg_settings, (0, 0))
            setting_texts = get_text("settings")
            formatted_music = setting_texts[0].format(status="Включена" if music_on else "Отключена")
            formatted_language = setting_texts[1]

            music_text = button_font.render(formatted_music, True, WHITE)
            lang_text = button_font.render(formatted_language, True, WHITE)

            music_rect = music_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            lang_rect = lang_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 70))

            pygame.draw.rect(screen, GRAY, music_rect.inflate(20, 10), border_radius=15)
            pygame.draw.rect(screen, GRAY, lang_rect.inflate(20, 10), border_radius=15)

            screen.blit(music_text, music_rect)
            screen.blit(lang_text, lang_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if music_rect.collidepoint(event.pos):
                        music_on = not music_on
                        if music_on:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    if lang_rect.collidepoint(event.pos):
                        nonlocal language
                        language = "en" if language == "ru" else "ru"
                        button_rects.clear()
                        button_rects.extend(create_buttons())

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            pygame.display.flip()

    # Основной цикл меню
    while True:
        screen.blit(bg_main_menu, (0, 0))
        title_text = font.render(get_text("title"), True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        for button_text, button_rect in button_rects:
            pygame.draw.rect(screen, GRAY, button_rect.inflate(20, 10), border_radius=15)
            screen.blit(button_text, button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, (_, button_rect) in enumerate(button_rects):
                    if button_rect.collidepoint(event.pos):
                        if i == 0:  # Start Game
                            print("Starting game...")
                            achievements['first_game'] = True
                            return "start"
                        elif i == 1:  # Settings
                            print("Opening settings...")
                            show_settings()
                        elif i == 2:  # Achievements
                            print("Showing achievements...")
                            show_achievements()
                        elif i == 3:  # Exit
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    achievements = {
        'first_game': False,
        'collector': False,
        'first_enemy': False
    }
    language = "ru"  # Начальный язык - русский
    action = main_menu(achievements, language)
    if action == "start":
        game_sobstvenno()
        print("Игра запускается... (реализуйте игровой цикл)")
