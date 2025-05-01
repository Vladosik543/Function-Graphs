from sys import exit 
import pygame 
import math

class InputBox(pygame.sprite.Sprite):
    def __init__(self, pos, index):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH-50, 50))
        self.rect = self.image.get_rect(bottomleft=pos)
        self.text = ""
        self.index = index

    def draw_text(self):
        self.image.fill("black")
        text_surf = font.render(self.text, True, "white")
        text_rect = text_surf.get_rect(midleft=(5, 25))
        self.image.blit(text_surf, text_rect)

    def update(self, events, act):
        if active_input == self:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        act(self.text, self.index)
                    else:
                        self.text += event.unicode

        self.draw_text()
        pygame.draw.rect(self.image, "white", self.image.get_rect(), 2)

class PlusButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.plus = pygame.transform.scale(pygame.image.load("Function-Graphs\plus.png").convert_alpha(), (50, 50))
    
    def update(self, event, act):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        act()

        self.image.blit(self.plus, (0, 0))
        pygame.draw.rect(self.image, "white", self.image.get_rect(), 2)

class MinusButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect(bottomright=(SCREEN_WIDTH-50, SCREEN_HEIGHT))
        self.minus = pygame.transform.scale(pygame.image.load("Function-Graphs\minus.png").convert_alpha(), (50, 50))
    
    def update(self, event, act):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        act()

        self.image.blit(self.minus, (0, 0))
        pygame.draw.rect(self.image, "white", self.image.get_rect(), 2)

pygame.init()

    
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
        y = calc(exp, {"x": x, "X": x})
        if y != None:
            y *= -1
            points.append((x, y))
        x += 1

    for i, point in enumerate(points):
        new_point = (point[0]*SQUARE)+(SCREEN_WIDTH/2), (point[1]*SQUARE)+(600/2)
        points[i] = new_point

    curve_points = generate_catmull_rom(points)
    points_to_delete = []

    for point in curve_points:
        if point[0] < -50 or point[0] > SCREEN_WIDTH + 50 or point[1] < -50 or point[1] > 600 + 50:
            points_to_delete.append(point)
    
    filtred_points = [point for point in curve_points if point not in points_to_delete]

    return filtred_points

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Function Representation")
icon = pygame.image.load("Function-Graphs\icon.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FPS = 60

SQUARE = 30
font = pygame.font.SysFont("Courier New", 16)

points = []
anim_index = 0

def draw_map():
    for i in range(0, SCREEN_WIDTH, SQUARE):
        for j in range(0, 600, SQUARE):
            pygame.draw.line(screen, (30,30,30), (i, 0), (i, SCREEN_WIDTH))
            pygame.draw.line(screen, (30,30,30), (0, j), (600, j))

    pygame.draw.line(screen, "white", (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, 600))
    pygame.draw.line(screen, "white", (0, 600/2), (SCREEN_WIDTH, 600/2))

def change_points(exp, index):
    global points, anim_index

    try: points[index] = create_points(exp)
    except IndexError as e: points.append(create_points(exp))
    anim_index = 0

def create_inputs_buttons():
    global SCREEN_HEIGHT, screen, inp_index, inputs, plus_buttons
    SCREEN_HEIGHT += 50
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    inp_index += 1
    inputs.add(InputBox((0, SCREEN_HEIGHT), inp_index))
    plus_buttons.add(PlusButton())
    minus_buttons.add(MinusButton())

def delete_inputs_buttons():
    global SCREEN_HEIGHT, screen, inp_index, inputs, plus_buttons, points
    if inp_index != 0:
        SCREEN_HEIGHT -= 50
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        inp_index -= 1
        inputs.remove(inputs.sprites()[-1])
        plus_buttons.remove(plus_buttons.sprites()[-1])
        minus_buttons.remove(minus_buttons.sprites()[-1])
        points.pop(-1)

inp_index = 0
inputs = pygame.sprite.Group()
inputs.add(InputBox((0, SCREEN_HEIGHT), inp_index))
active_input = None 

plus_buttons = pygame.sprite.Group()
plus_buttons.add(PlusButton())

minus_buttons = pygame.sprite.Group()
minus_buttons.add(MinusButton())
    
running = True 
while running:
    screen.fill("black")

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for inp in inputs:
                if inp.rect.collidepoint(event.pos):
                    active_input = inp
                    break
            else:
                active_input = None 

    draw_map()

    for points_of in points:
        for i in range(1, anim_index):
            try: pygame.draw.line(screen, "orange", points_of[i - 1], points_of[i], 2)
            except IndexError as e: continue

        if anim_index < len(points_of):
            anim_index += 2

    inputs.update(events, change_points)
    inputs.draw(screen)

    plus_buttons.draw(screen)
    plus_buttons.update(events, create_inputs_buttons)

    minus_buttons.draw(screen)
    minus_buttons.update(events, delete_inputs_buttons)

    pygame.draw.rect(screen, "white", (0, 0, 600, 600), 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
exit()
