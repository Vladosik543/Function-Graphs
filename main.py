from sys import exit 
import pygame 
import math
import colorama

pygame.init()
colorama.init()

    
def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t

    x = 0.5 * (2*p1[0] + (-p0[0] + p2[0])*t + 
              (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0])*t2 +
              (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0])*t3)

    y = 0.5 * (2*p1[1] + (-p0[1] + p2[1])*t +
              (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1])*t2 +
              (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1])*t3)

    return x, y

def generate_catmull_rom(points, samples_per_segment=20):
    result = []
    for i in range(1, len(points) - 2):
        for t in range(samples_per_segment):
            pt = catmull_rom(points[i - 1], points[i], points[i + 1], points[i + 2], t / samples_per_segment)
            result.append(pt)
    return result


def calc(exp, var):
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed_names.update(var)
        res = eval(exp, {"__builtins__": {}}, allowed_names)
        return res
    except Exception as e:
        return None
    
def create_points(exp):
    points = []
    x = -50
    while x <= 50:
        y = calc(exp, {"x": x})
        if y != None:
            y *= -1
            points.append((x*2, y))
        x += 1

    for i, point in enumerate(points):
        new_point = (point[0]*SQUARE)+(SCREEN_RES/2), (point[1]*SQUARE)+(SCREEN_RES/2)
        points[i] = new_point

    curve_points = generate_catmull_rom(points)
    points_to_delete = []

    for point in curve_points:
        if point[0] < -50 or point[0] > SCREEN_RES + 50 or point[1] < -50 or point[1] > SCREEN_RES + 50:
            points_to_delete.append(point)
    
    filtred_points = [point for point in curve_points if point not in points_to_delete]

    return filtred_points

SCREEN_RES = 600
screen = pygame.display.set_mode((SCREEN_RES, SCREEN_RES+50))
pygame.display.set_caption("Function Representation")
icon = pygame.image.load("Function-Graphs\icon.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FPS = 60

SQUARE = 30

exp = ""
points = [create_points(exp)]

anim_index = 0

def draw_map():
    for i in range(0, SCREEN_RES, SQUARE):
        for j in range(0, SCREEN_RES, SQUARE):
            pygame.draw.line(screen, (30,30,30), (i, 0), (i, SCREEN_RES))
            pygame.draw.line(screen, (30,30,30), (0, j), (SCREEN_RES, j))

    pygame.draw.line(screen, "white", (SCREEN_RES/2, 0), (SCREEN_RES/2, SCREEN_RES))
    pygame.draw.line(screen, "white", (0, SCREEN_RES/2), (SCREEN_RES, SCREEN_RES/2))

input = pygame.Surface((SCREEN_RES, 50))
input_rect = input.get_rect(bottomleft=(0, SCREEN_RES+50))
font = pygame.font.SysFont("Courier New", 24)
text = ""

def draw_text():
    input.fill((30,30,30))
    text_surf = font.render(text, True, "white")
    text_rect = text_surf.get_rect(midleft=(5, 25))
    input.blit(text_surf, text_rect)
    
running = True 
while running:
    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            elif event.key == pygame.K_RETURN:
                exp = text
                points = [create_points(exp)]
                anim_index = 0
            else:
                text += event.unicode

    draw_text()
    draw_map()

    for points_of in points:
        for i in range(1, anim_index):
            try: pygame.draw.line(screen, "orange", points_of[i - 1], points_of[i], 2)
            except IndexError as e: continue

        if anim_index < len(points_of):
            anim_index += 1

    screen.blit(input, input_rect)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
exit()
