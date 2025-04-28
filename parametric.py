from sys import exit 
import pygame 
import math

pygame.init()

def calc(exp, var):
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed_names.update(var)
        res = eval(exp, {"__builtins__": {}}, allowed_names)
        return res
    except Exception as e:
        return None
    
def create_points(expx, expy, expt):
    points = []
    t = 0
    while t <= eval(expt):
        x = calc(expx, {"t": t, "T": t})
        y = calc(expy, {"t": t, "T": t})
        if x != None and y != None:
            y *= -1
            points.append((x, y))
        t += 0.1
    
    for i, point in enumerate(points):
        new_point = (point[0]*SQUARE)+(SCREEN_RES/2), (point[1]*SQUARE)+(SCREEN_RES/2)
        points[i] = new_point

    points_to_delete = []

    for point in points:
        if point[0] < -50 or point[0] > SCREEN_RES + 50 or point[1] < -50 or point[1] > SCREEN_RES + 50:
            points_to_delete.append(point)
    
    filtred_points = [point for point in points if point not in points_to_delete]

    return filtred_points

SCREEN_RES = 600
screen = pygame.display.set_mode((SCREEN_RES, SCREEN_RES))
pygame.display.set_caption("Function Representation")
icon = pygame.image.load("Function-Graphs\icon.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FPS = 60

SQUARE = 200

points = [create_points("cos(t)", "sin(t)", "10"),
          create_points("pow(cos(t), 3)", "pow(sin(t), 3)", "10"),
          create_points("pow(cos(t), 2)", "pow(sin(t), 2)", "10"),
          create_points("pow(cos(t), 4)", "pow(sin(t), 4)", "10"),
          create_points("pow(cos(t), 5)", "pow(sin(t), 5)", "10"),
          create_points("pow(cos(t), 6)", "pow(sin(t), 6)", "10")]

anim_index = 0

def draw_map():
    for i in range(0, SCREEN_RES, SQUARE):
        for j in range(0, SCREEN_RES, SQUARE):
            pygame.draw.line(screen, (30,30,30), (i, 0), (i, SCREEN_RES))
            pygame.draw.line(screen, (30,30,30), (0, j), (SCREEN_RES, j))

    pygame.draw.line(screen, "white", (SCREEN_RES/2, 0), (SCREEN_RES/2, SCREEN_RES))
    pygame.draw.line(screen, "white", (0, SCREEN_RES/2), (SCREEN_RES, SCREEN_RES/2))

# input = pygame.Surface((SCREEN_RES, 50))
# input_rect = input.get_rect(bottomleft=(0, SCREEN_RES+50))
# font = pygame.font.SysFont("Courier New", 24)
# text = ""

# def draw_text():
#     input.fill((30,30,30))
#     text_surf = font.render(text, True, "white")
#     text_rect = text_surf.get_rect(midleft=(5, 25))
#     input.blit(text_surf, text_rect)
    
running = True 
while running:
    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_BACKSPACE:
        #         text = text[:-1]
        #     elif event.key == pygame.K_RETURN:
        #         points = [create_points(text)]
        #         anim_index = 0
        #     else:
        #         text += event.unicode

    # draw_text()
    draw_map()

    for points_of in points:
        for i in range(1, anim_index):
            try: pygame.draw.line(screen, "orange", points_of[i - 1], points_of[i], 2)
            except IndexError as e: continue

        if anim_index < len(points_of):
            anim_index += 2

    # screen.blit(input, input_rect)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
exit()
