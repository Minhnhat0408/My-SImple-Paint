import pygame, math

pygame.init()
fill_coor = []


def button(x, y, w, h, color, win):
    rect = pygame.draw.rect(win, (0, 0, 0), (x - 5, y - 5, w + 10, h + 10))
    pygame.draw.rect(win, color, (x, y, w, h))
    return rect


def text(text, size, color, pos, win):
    font = pygame.font.SysFont("comicsans", size, True)
    display = font.render(text, 10, color)
    win.blit(display, pos)


def roundline(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + i / distance * dx)
        y = int(start[1] + i / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)


def getneighbor(pos):
    y, x = pos
    adj = []
    if x > 0:
        adj.append((y, x - 1))
    if x < 430:
        adj.append((y, x + 1))
    if y > 0:
        adj.append((y - 1, x))
    if y < 499:
        adj.append((y + 1, x))
    return adj


def floodFill(pos, poscolor, br_color, win):
    y, x = pos
    hashmap = {(y, x)}
    stack = [(y, x)]
    win.set_at((y, x), br_color)
    while stack:
        po1 = stack.pop()
        adj = getneighbor(po1)
        for i in adj:
            y1, x1 = i
            if tuple(win.get_at((y1, x1))) == poscolor and (y1, x1) not in hashmap:
                hashmap.add((y1, x1))
                stack.append((y1, x1))
                win.set_at((y1, x1), br_color)


def main():
    paint = True
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Paint")
    br_color = (0, 0, 0)
    br_radius = 1
    draw_on = False
    cur_c_pos = (0, 0)
    last_pos = (0, 0)
    win.fill((255, 255, 255))
    choose = False
    count = 0
    fill_func = False
    cur = ()
    draw = True
    while paint:

        button(5, 415, 490, 80, (255, 255, 255), win)
        clear = button(20, 20, 80, 30, (255, 255, 255), win)
        red = button(20, 430, 50, 50, (255, 69, 69), win)
        blue = button(100, 430, 50, 50, (59, 131, 247), win)
        green = button(180, 430, 50, 50, (61, 255, 64), win)
        yellow = button(260, 430, 50, 50, (255, 249, 61), win)
        purple = button(340, 430, 50, 50, (218, 69, 255), win)
        orange = button(420, 430, 50, 50, (255, 255, 255), win)
        intruct = button(440, 20, 30, 30, (255, 255, 255), win)
        text("?", 30, (0, 0, 0), (445, 25), win)
        text("RESET", 20, (0, 0, 0), (421, 450), win)
        text("CLEAR", 20, (0, 0, 0), (30, 30), win)
        if not fill_func:
            fillbox = button(250, 20, 30, 30, (255, 255, 255), win)
            text("fill", 25, (0, 0, 0), (252, 27), win)
        else:
            fillbox = button(250, 20, 30, 30, (0, 0, 0), win)
            text("fill", 25, (255, 255, 255), (252, 27), win)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                paint = False
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 4:
                    br_radius += 3
                elif i.button == 5:
                    br_radius -= 3
                cur = i.pos
            if pygame.mouse.get_pressed()[2]:
                choose = False
                br_color = (255, 255, 255)
            if i.type == pygame.MOUSEBUTTONUP:
                draw_on = False
                count = 0
            if i.type == pygame.MOUSEMOTION:
                if draw_on:
                    roundline(win, br_color, i.pos, last_pos, br_radius)
                last_pos = i.pos

            if pygame.mouse.get_pressed() == (1, 0, 0):
                if draw:
                    pygame.draw.circle(win, br_color, cur, br_radius)
                    count += 1
                    draw_on = True
                if fill_func:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        point = pygame.mouse.get_pos()
                        pointcolor = tuple(win.get_at(point))
                        floodFill(point, pointcolor, br_color, win)
                        if fillbox.collidepoint(point):
                            fill_func = False
                if count <= 1:
                    if clear.collidepoint(cur):
                        win.fill((255, 255, 255))
                    elif red.collidepoint(cur):
                        br_color = (255, 69, 69)
                        choose = True
                        cur_c_pos = (25, 450)
                    elif blue.collidepoint(cur):
                        br_color = (59, 131, 247)
                        choose = True
                        cur_c_pos = (105, 450)
                    elif green.collidepoint(cur):
                        br_color = (61, 255, 64)
                        choose = True
                        cur_c_pos = (185, 450)
                    elif yellow.collidepoint(cur):
                        br_color = (255, 249, 61)
                        choose = True
                        cur_c_pos = (265, 450)
                    elif purple.collidepoint(cur):
                        br_color = (218, 69, 255)
                        choose = True
                        cur_c_pos = (345, 450)
                    elif orange.collidepoint(cur):
                        br_color = (0, 0, 0)
                        choose = False
                        draw = True
                        fill_func = False
                    elif fillbox.collidepoint(cur):
                        fill_func = True
                        draw = False
                    elif intruct.collidepoint(cur):
                        pygame.draw.rect(win, (0, 0, 0), (70, 100, 380, 250))
                        text("Welcome to my Paint --Minhnhat--", 20, (0, 120, 0), (100, 130), win)
                        text("Instructions :", 20, (0, 120, 0), (100, 150), win)
                        text("1.(clear-button) clean all your sketch", 20, (0, 120, 0), (100, 170), win)
                        text("2.(right click-mouse) eraser ", 20, (0, 120, 0), (100, 190), win)
                        text("3.Choose color box to switch painted color", 20, (0, 120, 0), (100, 210), win)
                        text("4.(reset-button) reset the color to black", 20, (0, 120, 0), (100, 230), win)
                        text("5.Scroll your wheel to modify the size of brush", 20, (0, 120, 0), (100, 250), win)
                        text("6.Choose (fill) and color to fill color", 20, (0, 120, 0), (100, 270), win)
                        text("7.To close this window click (clear-button)", 20, (0, 120, 0), (100, 290), win)

        if choose:
            text("PICK", 20, (0, 0, 0), cur_c_pos, win)
        if br_radius < 1:
            br_radius = 1
        elif br_radius > 40:
            br_radius = 40
        pygame.display.update()


main()
