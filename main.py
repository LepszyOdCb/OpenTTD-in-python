import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Stałe
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 32
ROWS = SCREEN_HEIGHT // GRID_SIZE
COLS = SCREEN_WIDTH // GRID_SIZE

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Inicjalizacja okna gry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('OpenTTD-inspired Game')

# Funkcje pomocnicze
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

# Klasy obiektów w grze
class Track:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Train:
    def __init__(self, track_path):
        self.track_path = track_path  # Ścieżka pociągu jako lista punktów (x, y)
        self.current_index = 0  # Indeks aktualnej pozycji na trasie
        self.position = (self.track_path[self.current_index][0] * GRID_SIZE + GRID_SIZE // 2,
                         self.track_path[self.current_index][1] * GRID_SIZE + GRID_SIZE // 2)
        self.speed = 2  # Szybkość pociągu

    def move(self):
        # Sprawdź, czy pociąg nie osiągnął końca trasy
        if self.current_index < len(self.track_path) - 1:
            target_position = (self.track_path[self.current_index + 1][0] * GRID_SIZE + GRID_SIZE // 2,
                               self.track_path[self.current_index + 1][1] * GRID_SIZE + GRID_SIZE // 2)

            # Sprawdź, czy pociąg jest wystarczająco blisko celu
            if abs(self.position[0] - target_position[0]) <= self.speed and \
                    abs(self.position[1] - target_position[1]) <= self.speed:
                self.current_index += 1

            # Poruszaj pociąg w kierunku celu
            if self.current_index < len(self.track_path) - 1:
                dx = target_position[0] - self.position[0]
                dy = target_position[1] - self.position[1]
                distance = (dx ** 2 + dy ** 2) ** 0.5
                self.position = (self.position[0] + dx / distance * self.speed,
                                 self.position[1] + dy / distance * self.speed)

    def draw(self):
        pygame.draw.circle(screen, GREEN, (int(self.position[0]), int(self.position[1])), GRID_SIZE // 4)

# Inicjalizacja list przechowujących obiekty
tracks = []
platforms = []
trains = []
blue_path = []

# Pętla gry
running = True
selected_mode = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            x = pos[0] // GRID_SIZE
            y = pos[1] // GRID_SIZE

            if selected_mode == 1:
                track = Track(x, y)
                tracks.append(track)
                blue_path.append((x, y))
            elif selected_mode == 2:
                platform = Platform(x, y)
                platforms.append(platform)
            elif selected_mode == 3:
                pass  # Pociąg może być dodany tylko po zdefiniowaniu trasy
            elif selected_mode == 4:
                pass  # Punkt początkowy/końcowy będzie dodany po zdefiniowaniu trasy

    # Rysowanie tła
    screen.fill(WHITE)
    draw_grid()

    # Rysowanie tras
    for track in tracks:
        track.draw()

    # Rysowanie peronów
    for platform in platforms:
        platform.draw()

    # Rysowanie pociągów
    for train in trains:
        train.move()
        train.draw()

    # Rysowanie niebieskiej ścieżki
    if len(blue_path) > 1:
        for i in range(len(blue_path) - 1):
            start_pos = (blue_path[i][0] * GRID_SIZE + GRID_SIZE // 2, blue_path[i][1] * GRID_SIZE + GRID_SIZE // 2)
            end_pos = (blue_path[i + 1][0] * GRID_SIZE + GRID_SIZE // 2, blue_path[i + 1][1] * GRID_SIZE + GRID_SIZE // 2)
            pygame.draw.line(screen, BLUE, start_pos, end_pos, 5)

    # Aktualizacja okna
    pygame.display.flip()

    # Obsługa wyboru trybu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        selected_mode = 1
    elif keys[pygame.K_2]:
        selected_mode = 2
    elif keys[pygame.K_3]:
        selected_mode = 3
    elif keys[pygame.K_4]:
        selected_mode = 4

pygame.quit()
sys.exit()
