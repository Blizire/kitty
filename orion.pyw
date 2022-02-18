import os
import sys
import pygame
import win32api
import win32con
import win32gui

# initalize game engine library
pygame.init()

# grab display info and set window size and position accordingly
displayInfo = pygame.display.Info()
size = width, height = displayInfo.current_w, 180
# positions at bottom of screen just above task bar
# values may need to be changed depending on screen resolution
os.environ['SDL_VIDEO_WINDOW_POS'] = f"0,{displayInfo.current_h - 219}"
screen = pygame.display.set_mode(size, pygame.NOFRAME)

# movement speed
speed = [3, 0] 

# pygame cannot animate gifs, so load each frame individually
kittyFrames = [pygame.image.load(f'frame_{x}.gif') for x in range(0,4)]
kittyRect = [x.get_rect() for x in kittyFrames]
clock = pygame.time.Clock()

# hack that allows layered window transparency
transparency = (255, 0, 128) # transparency color
hwnd = pygame.display.get_wm_info()['window']

win32gui.SetWindowLong(hwnd,
    win32con.GWL_EXSTYLE,
    win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

win32gui.SetLayeredWindowAttributes(hwnd, 
    win32api.RGB(*transparency), 
    0, 
    win32con.LWA_COLORKEY)

#pygame loop
frameIndex = 0
frameCount = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # applying movement to all frames
    kittyRect = [x.move(speed) for x in kittyRect]
    # detect end of screen collision to move other direction
    if kittyRect[frameIndex].left < 0 or kittyRect[frameIndex].right > width:
        speed[0] = -speed[0]
        kittyFrames = [pygame.transform.flip(x, True, False) for x in kittyFrames]
    # hack to set window focus at all times
    win32gui.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 2|1)        
    screen.fill(transparency)
    screen.blit(kittyFrames[frameIndex], kittyRect[frameIndex])
    # hacky way to show same frame for 8 ticks
    if frameCount >= 8:
        frameIndex += 1
        frameCount = 0
    if frameIndex >= 4:
        frameIndex = 0
    frameCount += 1
    clock.tick(60)
    pygame.display.update()