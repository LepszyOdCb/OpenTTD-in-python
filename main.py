import pygame
import csv
import os

# Inicjalizacja Pygame
pygame.init()

# Stałe
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GRID_SIZE = 35
GRID_ROWS = SCREEN_HEIGHT // GRID_SIZE
GRID_COLS = SCREEN_WIDTH // GRID_SIZE

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Typy torów
TRACK_TYPES = {
    1: ("left-middle", "right-middle"),
    2: ("top-middle", "bottom-middle"),
    3: ("left-middle", "bottom-middle"),
    4: ("right-middle", "bottom-middle"),
    5: ("left-middle", "top-middle"),
    6: ("right-middle", "top-middle"),
}

# Inicjalizacja ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("OpenTTD-Inspired Game")

# Inicjalizacja siatki
grid = [[0] * GRID_COLS for _ in range(GRID_ROWS)]

# Słownik do przechowywania torów
tracks = {}

# Aktualnie wybrany typ toru
current_track_type = None

# Sprawdzenie istnienia pliku CSV
csv_file_exists = os.path.isfile("tracks.csv")

# Jeśli plik CSV istnieje, wczytaj dane
if csv_file_exists:
    with open("tracks.csv", "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row_data in reader:
            row = int(row_data[0])
            col = int(row_data[1])
            track_types = {int(i) for i in row_data[2:]}
            tracks[(row, col)] = track_types

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in range(pygame.K_1, pygame.K_6 + 1):
                current_track_type = event.key - pygame.K_0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_track_type is not None:
                row, col = event.pos[1] // GRID_SIZE, event.pos[0] // GRID_SIZE
                if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
                    tracks[(row, col)] = tracks.get((row, col), set()).union({current_track_type})

    # Wyczyszczenie ekranu
    screen.fill(WHITE)

    # Rysowanie siatki
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            pygame.draw.rect(screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    # Rysowanie torów
    for (row, col), track_types in tracks.items():
        for track_type in track_types:
            start, end = TRACK_TYPES[track_type]
            if start == "left-middle":
                start_pos = (col * GRID_SIZE, row * GRID_SIZE + GRID_SIZE // 2)
            elif start == "right-middle":
                start_pos = (col * GRID_SIZE + GRID_SIZE, row * GRID_SIZE + GRID_SIZE // 2)
            elif start == "top-middle":
                start_pos = (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE)
            elif start == "bottom-middle":
                start_pos = (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE)

            if end == "left-middle":
                end_pos = (col * GRID_SIZE, row * GRID_SIZE + GRID_SIZE // 2)
            elif end == "right-middle":
                end_pos = (col * GRID_SIZE + GRID_SIZE, row * GRID_SIZE + GRID_SIZE // 2)
            elif end == "top-middle":
                end_pos = (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE)
            elif end == "bottom-middle":
                end_pos = (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE)

            pygame.draw.line(screen, BLACK, start_pos, end_pos, 3)

    # Aktualizacja ekranu
    pygame.display.flip()

# Zapisywanie torów do pliku CSV
with open("tracks.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for (row, col), track_types in tracks.items():
        row_data = [row, col] + [1 if i in track_types else 0 for i in range(1, 7)]
        writer.writerow(row_data)

# Zamknięcie Pygame
pygame.quit()
