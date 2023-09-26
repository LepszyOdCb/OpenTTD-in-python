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

# Inicjalizacja ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("OpenTTD-Inspired Game")

# Inicjalizacja siatki
grid = [[0] * GRID_COLS for _ in range(GRID_ROWS)]

# Pozycja kamery
camera_x = 0
camera_y = 0

# Słownik do przechowywania torów
tracks = {}

# Wczytanie obrazów torów
track_images = {
    1: pygame.image.load("Rails1.png"),
    2: pygame.image.load("Rails2.png"),
    3: pygame.image.load("Rails3.png"),
    4: pygame.image.load("Rails4.png"),
    5: pygame.image.load("Rails5.png"),
    6: pygame.image.load("Rails6.png"),
    7: pygame.image.load("Platform1.png"),
    8: pygame.image.load("Platform2.png"),
}

# Aktualnie wybrany typ toru
current_track_type = None

# Sprawdzenie istnienia pliku CSV
csv_file_exists = os.path.isfile("tracks.csv")

# Jeśli plik CSV nie istnieje, utwórz pusty plik z danymi dla każdej komórki
if not csv_file_exists:
    with open("tracks.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                writer.writerow([row, col] + [0] * 8)  # Uwzględnienie torów typu 7 i 8

# Wczytaj dane o torach
with open("tracks.csv", "r", newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row_data in reader:
        row = int(row_data[0])
        col = int(row_data[1])
        track_types = {i for i in range(1, 9) if int(row_data[i + 1]) == 1}  # Uwzględnienie torów typu 7 i 8
        tracks[(row, col)] = track_types

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_track_type = 1
            elif event.key == pygame.K_2:
                current_track_type = 2
            elif event.key == pygame.K_3:
                current_track_type = 3
            elif event.key == pygame.K_4:
                current_track_type = 4
            elif event.key == pygame.K_5:
                current_track_type = 5
            elif event.key == pygame.K_6:
                current_track_type = 6
            elif event.key == pygame.K_7:
                current_track_type = 7
            elif event.key == pygame.K_8:
                current_track_type = 8
            elif event.key == pygame.K_w:
                camera_y += 1
            elif event.key == pygame.K_s:
                camera_y -= 1
            elif event.key == pygame.K_a:
                camera_x += 1
            elif event.key == pygame.K_d:
                camera_x -= 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_track_type is not None:
                row, col = event.pos[1] // GRID_SIZE + camera_y, event.pos[0] // GRID_SIZE + camera_x
                if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
                    if current_track_type == 7:
                        # Sprawdzenie, czy w danym miejscu jest tor typu 1
                        if 1 in tracks.get((row, col), set()):
                            # Sprawdzenie, czy w danym miejscu nie ma już toru typu 7
                            if not any(track == 7 for track in tracks.get((row, col), set())):
                                tracks[(row, col)] = tracks.get((row, col), set()).union({current_track_type})
                    elif current_track_type == 8:
                        # Sprawdzenie, czy w danym miejscu jest tor typu 2
                        if 2 in tracks.get((row, col), set()):
                            # Sprawdzenie, czy w danym miejscu nie ma już toru typu 8
                            if not any(track == 8 for track in tracks.get((row, col), set())):
                                tracks[(row, col)] = tracks.get((row, col), set()).union({current_track_type})
                    else:
                        tracks[(row, col)] = tracks.get((row, col), set()).union({current_track_type})

    # Wyczyszczenie ekranu
    screen.fill(WHITE)

    # Rysowanie siatki
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            pygame.draw.rect(screen, BLACK, (col * GRID_SIZE - camera_x * GRID_SIZE, row * GRID_SIZE - camera_y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    # Rysowanie torów
    for (row, col), track_types in tracks.items():
        for track_type in track_types:
            if track_type in track_images:
                image = track_images[track_type]
                image_rect = image.get_rect()
                image_rect.topleft = (col * GRID_SIZE - camera_x * GRID_SIZE, row * GRID_SIZE - camera_y * GRID_SIZE)
                screen.blit(image, image_rect)

    # Aktualizacja ekranu
    pygame.display.flip()

# Zapisywanie torów do pliku CSV
with open("tracks.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            track_types = tracks.get((row, col), set())
            row_data = [row, col] + [1 if i in track_types else 0 for i in range(1, 9)]  # Uwzględnienie torów typu 7 i 8
            writer.writerow(row_data)

# Zamknięcie Pygame
pygame.quit()
