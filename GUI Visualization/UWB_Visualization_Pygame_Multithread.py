import time
import math
import socket
import json
import pygame
import threading

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

# Load the background image (denah)
# background_image = pygame.image.load('d:\imagekling.png')

# Warna
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

distance_a1_a2 = 3.0
meter2pixel = 100
range_offset = 0.9

Y_ANCHOR1 = 350
X_ANCHOR1 = 400


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
            break  # Tangani kesalahan tak terduga, dianggap koneksi terputus

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
    #screen.blit(background_image, (0, 0))  # Render the background image first
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
    text = font.render("TWO ANCHOR VISUALIZATION", True, BLACK)
    screen.blit(text, (420, 55))


def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)


def draw_uwb_anchor(x, y, label):
    font = pygame.font.SysFont('Arial', 14)
    #text = f"{label}: {range_val:.1f}m"
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
    x_meter = (x - X_ANCHOR1) / meter2pixel
    y_meter = (Y_ANCHOR1 - y) / meter2pixel

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


def tag_pos(a, b, c):
    cos_a = (b * b + c * c - a * a) / (2 * b * c)
    cos_a = max(-1, min(1, cos_a))

    x = b * cos_a
    y = b * math.sqrt(1 - cos_a * cos_a)

    return round(x, 1), round(y, 1)


def uwb_range_offset(uwb_range):
    return uwb_range  # Placeholder for range offset logic


def read_data():
    global data
    try:
        line = data.recv(1024).decode('UTF-8')
        uwb_data = json.loads(line)
        print(uwb_data)
        uwb_list = uwb_data.get("links", [])
        return uwb_list
    except json.JSONDecodeError:
        print("Received data is not valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return []


def accept_client():
    global data
    data, addr = sock.accept()
    print(f"Connection accepted from {addr}")


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
                node_count = 0

                for sub_list in uwb_list:
                    for one in sub_list:
                        if one["A"] == "1782":
                            a1_range = uwb_range_offset(float(one["R"]))
                            node_count += 1

                        if one["A"] == "1783":
                            a2_range = uwb_range_offset(float(one["R"]))
                            node_count += 1

                if node_count == 2:
                    if a2_range == 0 or a1_range == 0:
                        continue  # Skip this iteration if the calculation was invalid
                    x, y = tag_pos(a2_range, a1_range, distance_a1_a2)
                    current_positions[client_id] = (x, y)

            # Refresh entire grid and anchors each time
            draw_ui()
            draw_uwb_anchor(X_ANCHOR1, Y_ANCHOR1, "A1782(0,0)")
            draw_uwb_anchor(X_ANCHOR1 + int(distance_a1_a2 * meter2pixel), Y_ANCHOR1, f"A1783({distance_a1_a2})")

            # Draw only the active TAGs
            for client_id, (x, y) in current_positions.items():
                draw_uwb_tag(X_ANCHOR1 + int(x * meter2pixel), Y_ANCHOR1 - int(y * meter2pixel), f"TAG-{client_id}")

            pygame.display.flip()

            previous_positions = current_positions  # Update previous positions with the current

        time.sleep(0.1)

    pygame.quit()


if __name__ == '__main__':
    main()
