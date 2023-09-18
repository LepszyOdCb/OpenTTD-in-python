import pygame
import csv
import os

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
screen_width = 800
screen_height = 800
cell_size = 32  # Rozmiar komórki w siatce
rows = 25  # Liczba wierszy
cols = 25  # Liczba kolumn

# Inicjalizacja okna
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Siatka 25x25")

# Ścieżka do pliku CSV
csv_file_path = 'grid_positions.csv'

# Sprawdzenie czy plik CSV istnieje, jeśli nie to utworzenie go
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Row', 'Column', 'Position']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Słownik przechowujący pozycje dla każdej kratki w siatce
grid_positions = {(i, j): f'{i + 1},{j + 1}' for i in range(rows) for j in range(cols)}

# Zapisanie danych do pliku CSV
with open(csv_file_path, 'a', newline='') as csvfile:
    fieldnames = ['Row', 'Column', 'Position']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    for (row, col), position in grid_positions.items():
        writer.writerow({'Row': row + 1, 'Column': col + 1, 'Position': position})

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # LPM
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row = mouse_y // cell_size
            col = mouse_x // cell_size
            print(f"Kliknięto na pozycji: {row + 1},{col + 1}")

    # Wyczyszczenie ekranu
    screen.fill((255, 255, 255))

    # Rysowanie siatki
    for i in range(rows):
        for j in range(cols):
            pygame.draw.rect(screen, (0, 0, 0), (j * cell_size, i * cell_size, cell_size, cell_size), 1)

    # Aktualizacja ekranu
    pygame.display.flip()

# Zakończenie pracy z Pygame
pygame.quit()
