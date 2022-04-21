import pygame
import requests


def update():
    global count
    global params
    global delta
    print(params)
    response = requests.get(serv, params=params)
    with open('static/map.png', mode='wb') as file:
        file.write(response.content)
    count += 1


pygame.init()
size = height, width = 650, 450
running = True
screen = pygame.display.set_mode(size)

serv = 'http://static-maps.yandex.ru/1.x/'
lon = "0"
lat = "0"
delta = "90"
params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": "map",
    "size": "650,450"
}
map = 'map.png'
count = 0
c = 0
x0 = lon
y0 = lat
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.button)
            if event.button == 1:
                x0, y0 = pygame.mouse.get_pos()
            elif event.button == 5:
                params['spn'] = f'{int(delta) + 1},{int(delta) + 1}'
                delta = f'{int(delta) + 1}'
            elif event.button == 4:
                print(1)
                params['spn'] = f'{int(delta) - 1},{int(delta) - 1}'
                delta = f'{int(delta) - 1}'
        if event.type == pygame.MOUSEBUTTONUP:
            x1, y1 = pygame.mouse.get_pos()
            changed_pos_x, changed_pos_y = abs(int(x0) - int(x1)), abs(int(y0) - int(y1))
            params['ll'] = f'{int(lon) + changed_pos_x},{int(lat) + changed_pos_y}'
            lon = int(lon) + changed_pos_x
            lat = int(lat) + changed_pos_y
    update()
    screen.blit(pygame.image.load(map), (0, 0))
    pygame.display.flip()
pygame.quit()
