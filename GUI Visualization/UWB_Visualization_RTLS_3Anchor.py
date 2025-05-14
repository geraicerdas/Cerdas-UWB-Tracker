import time
import math
import socket
import json
import pygame
import threading
import numpy as np

# Inisialisasi jaringan
hostname = socket.gethostname()
UDP_IP = socket.gethostbyname(hostname)
print("***Local IP: " + str(UDP_IP) + "***")
UDP_PORT = 80

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((UDP_IP, UDP_PORT))
sock.listen(5)

data_lock = threading.Lock()  # Lock untuk sinkronisasi akses ke tags_data
tags_data = {}  # Dictionary untuk menyimpan data TAG dari setiap klien

# Inisialisasi Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 700), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Cerdas UWB Tracker")

# Warna
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Konfigurasi anchor
distance_between_anchors = 3.0  # Jarak antara anchor (meter)
meter2pixel = 100  # Skala konversi meter ke pixel
range_offset = 0.9

# Posisi anchor di layar (dalam pixel)
# Anchor disusun dalam segitiga sama sisi
X_CENTER = 600  # Pusat layar X
Y_CENTER = 350  # Pusat layar Y

# Hitung posisi ketiga anchor
X_ANCHOR1 = X_CENTER
Y_ANCHOR1 = Y_CENTER - int((distance_between_anchors * meter2pixel) * math.sqrt(3) / 3)

X_ANCHOR2 = X_CENTER - int((distance_between_anchors * meter2pixel) / 2)
Y_ANCHOR2 = Y_CENTER + int((distance_between_anchors * meter2pixel) * math.sqrt(3) / 6)

X_ANCHOR3 = X_CENTER + int((distance_between_anchors * meter2pixel) / 2)
Y_ANCHOR3 = Y_ANCHOR2  # Same Y as anchor2 for equilateral triangle


def handle_client(client_socket, client_address):
    global tags_data
    client_id = f"{client_address[0]}:{client_address[1]}"
    client_socket.settimeout(10.0)  # Set timeout 10 detik untuk menunggu data

    while True:
        try:
            data = client_socket.recv(1024).decode('UTF-8')
            if not data:  # Jika recv() mengembalikan data kosong, koneksi terputus
                print(f"Connection lost from client {client_id}")
                break

            if not data.strip():
                print("Received empty data, skipping...")
                continue  # Skip processing if data is empty

            uwb_data = json.loads(data)
            print(f"Data received from client {client_id}: {uwb_data}")

            with data_lock:
                tags_data[client_id] = [uwb_data["links"]]

        except socket.timeout:
            print(f"Client {client_id} timed out.")
            break  # Koneksi dianggap terputus jika terjadi timeout

        except socket.error as e:
            print(f"Socket error occurred: {e}")
            break  # Tangani berbagai kesalahan socket, dianggap koneksi terputus

        except Exception as e:
            print(f"Unexpected error: {e}")
            #break  # Tangani kesalahan tak terduga, dianggap koneksi terputus, sementara skip dulu
            continue

    with data_lock:
        if client_id in tags_data:
            del tags_data[client_id]  # Hapus data TAG dari klien yang terputus
    client_socket.close()


def accept_clients():
    while True:
        client_socket, addr = sock.accept()
        print(f"Connection accepted from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


def draw_grid(x, y, width, height, cell_size, color="gray"):
    # Menggambar garis vertikal
    for i in range(x, x + width, cell_size):
        pygame.draw.line(screen, color, (i, y), (i, y + height), 1)
    # Menggambar garis horizontal
    for j in range(y, y + height, cell_size):
        pygame.draw.line(screen, color, (x, j), (x + width, j), 1)


def draw_ui():
    screen.fill(BLACK)
    wall_length = 800
    wall_height = 40
    grid_cell_size = int(0.3 * meter2pixel)  # Ukuran kotak grid dalam pixel

    grid_width = wall_length
    grid_height = 600  # Tentukan tinggi grid sesuai kebutuhan

    # Menggambar grid
    draw_grid(200, 95, grid_width, grid_height, grid_cell_size)

    # Menggambar outline persegi di sekitar grid (seukuran panjang WALL)
    pygame.draw.rect(screen, WHITE, pygame.Rect(200, 95, grid_width, grid_height), 1)

    pygame.draw.rect(screen, WHITE, [200, 50, 800, 40])
    font = pygame.font.SysFont('Arial', 32)
    text = font.render("Cerdas UWB Tracker", True, WHITE)
    screen.blit(text, (450, 10))
    font = pygame.font.SysFont('Arial', 24)
    text = font.render("THREE ANCHOR TRIANGULATION", True, BLACK)
    screen.blit(text, (420, 55))


def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)


def draw_uwb_anchor(x, y, label):
    font = pygame.font.SysFont('Arial', 14)
    text = f"{label}"

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(topleft=(x + 30, y - 10))

    padding = 5
    rect_width = text_rect.width + 2 * padding
    rect_height = text_rect.height + 2 * padding
    rect = pygame.Rect(text_rect.x - padding, text_rect.y - padding, rect_width, rect_height)

    draw_rounded_rect(screen, WHITE, rect, corner_radius=9)

    square_size = 30  # Ukuran persegi
    anchor_rect = pygame.Rect(x - square_size // 2, y - square_size // 2, square_size, square_size)
    pygame.draw.rect(screen, GREEN, anchor_rect)

    screen.blit(text_surface, text_rect)


def draw_uwb_tag(x, y, label):
    x_meter = (x - X_CENTER) / meter2pixel
    y_meter = (Y_CENTER - y) / meter2pixel

    font = pygame.font.SysFont('Arial', 14)
    text = f"{label}: ({x_meter:.1f}m, {y_meter:.1f}m)"

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(topleft=(x + 30, y - 10))

    padding = 5
    rect_width = text_rect.width + 2 * padding
    rect_height = text_rect.height + 2 * padding
    rect = pygame.Rect(text_rect.x - padding, text_rect.y - padding, rect_width, rect_height)

    draw_rounded_rect(screen, WHITE, rect, corner_radius=9)

    size = 15  # Ukuran segitiga
    triangle_points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
    pygame.draw.polygon(screen, BLUE, triangle_points)

    screen.blit(text_surface, text_rect)


def trilaterate(anchor_positions, distances):
    """
    Fungsi untuk melakukan trilaterasi dengan 3 anchor
    anchor_positions: list of tuples (x,y) dalam meter
    distances: list of distances ke masing-masing anchor dalam meter
    """
    # Konversi ke numpy array untuk perhitungan
    A = np.array(anchor_positions)
    d = np.array(distances)

    # Anchor pertama sebagai referensi
    p1 = A[0]
    p2 = A[1]
    p3 = A[2]

    # Hitung vektor antara anchor
    ex = (p2 - p1) / np.linalg.norm(p2 - p1)
    i = np.dot(ex, p3 - p1)
    ey = (p3 - p1 - i * ex) / np.linalg.norm(p3 - p1 - i * ex)
    ez = np.cross(ex, ey)

    # Hitung komponen dalam sistem koordinat baru
    d1 = d[0]
    d2 = d[1]
    d3 = d[2]

    j = np.dot(ey, p3 - p1)

    # Hitung posisi tag
    x = (d1 ** 2 - d2 ** 2 + np.linalg.norm(p2 - p1) ** 2) / (2 * np.linalg.norm(p2 - p1))
    y = (d1 ** 2 - d3 ** 2 + i ** 2 + j ** 2) / (2 * j) - (i / j) * x

    # Kadang ada kasus di mana z^2 negatif karena noise, kita set ke 0
    z_squared = d1 ** 2 - x ** 2 - y ** 2
    z = np.sqrt(z_squared) if z_squared >= 0 else 0

    # Konversi kembali ke sistem koordinat asli
    pos = p1 + x * ex + y * ey

    return pos[0], pos[1]


def uwb_range_offset(uwb_range):
    return uwb_range  # Placeholder for range offset logic


def main():
    global data

    client_thread = threading.Thread(target=accept_clients)
    client_thread.start()

    previous_positions = {}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        with data_lock:
            current_positions = {}
            for client_id, uwb_list in tags_data.items():
                a1_range = 0.0
                a2_range = 0.0
                a3_range = 0.0
                node_count = 0

                for sub_list in uwb_list:
                    for one in sub_list:
                        if one["A"] == "1782":
                            a1_range = uwb_range_offset(float(one["R"]))
                            node_count += 1
                        elif one["A"] == "1783":
                            a2_range = uwb_range_offset(float(one["R"]))
                            node_count += 1
                        elif one["A"] == "1784":
                            a3_range = uwb_range_offset(float(one["R"]))
                            node_count += 1

                if node_count >= 3:  # Minimal 3 anchor untuk trilaterasi
                    if a1_range == 0 or a2_range == 0 or a3_range == 0:
                        continue  # Skip jika ada range yang 0

                    # Posisi anchor dalam meter (dalam sistem koordinat lokal)
                    anchor_positions = [
                        (0, distance_between_anchors * math.sqrt(3) / 3),  # A1 (atas)
                        (-distance_between_anchors / 2, -distance_between_anchors * math.sqrt(3) / 6),
                        # A2 (kiri bawah)
                        (distance_between_anchors / 2, -distance_between_anchors * math.sqrt(3) / 6)  # A3 (kanan bawah)
                    ]

                    distances = [a1_range, a2_range, a3_range]

                    try:
                        x, y = trilaterate(anchor_positions, distances)
                        current_positions[client_id] = (x, y)
                    except Exception as e:
                        print(f"Trilateration error: {e}")
                        continue

            # Refresh entire grid and anchors each time
            draw_ui()

            # Gambar ketiga anchor
            draw_uwb_anchor(X_ANCHOR1, Y_ANCHOR1, "A1782(0,0.58)")
            draw_uwb_anchor(X_ANCHOR2, Y_ANCHOR2, f"A1783(-1.5,-0.29)")
            draw_uwb_anchor(X_ANCHOR3, Y_ANCHOR3, f"A1784(1.5,-0.29)")

            # Draw all active TAGs
            for client_id, (x, y) in current_positions.items():
                # Konversi koordinat meter ke pixel
                tag_x = X_CENTER + int(x * meter2pixel)
                tag_y = Y_CENTER - int(y * meter2pixel)  # Negatif karena sumbu Y pygame kebalik
                draw_uwb_tag(tag_x, tag_y, f"TAG-{client_id}")

            pygame.display.flip()
            previous_positions = current_positions

        time.sleep(0.1)

    pygame.quit()


if __name__ == '__main__':
    main()