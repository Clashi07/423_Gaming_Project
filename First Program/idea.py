from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time

# Global variables
spray = False
water_droplets = []
car_position = -1.0
car_target = 0.0
fire_active = False
house_positions = [
    (-0.7, -0.2), (-0.35, -0.2), (0.0, -0.2), (0.35, -0.2), (0.7, -0.2),
    (-0.7, -0.5), (-0.35, -0.5), (0.0, -0.5), (0.35, -0.5), (0.7, -0.5)
]
current_burning_house = None
car_moving = False
fire_start_time = 0
FIRE_DURATION = 5  # Fire duration

def draw_circle_points(xc, yc, x, y):
    glVertex2f(xc + x, yc + y)
    glVertex2f(xc - x, yc + y)
    glVertex2f(xc + x, yc - y)
    glVertex2f(xc - x, yc - y)
    glVertex2f(xc + y, yc + x)
    glVertex2f(xc - y, yc + x)
    glVertex2f(xc + y, yc - x)
    glVertex2f(xc - y, yc - x)

def midpoint_circle(xc, yc, radius):
    """Draws a circle using GL_POINTS and the midpoint circle algorithm."""
    x = 0
    y = radius
    p = 1 - radius
    glBegin(GL_POINTS)
    draw_circle_points(xc, yc, x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        draw_circle_points(xc, yc, x, y)
    glEnd()

# 
def drawCar():
    glPointSize(2.0)
    
    # Main body - solid red
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)  # Pure red
    for px in range(int((car_position - 0.12)*100), int((car_position + 0.12)*100)):
        for py in range(-82, -70):
            glVertex2f(px/100.0, py/100.0)
    glEnd()

    # Windows - solid blue
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.0, 1.0)  # Pure blue
    for px in range(int((car_position - 0.08)*100), int((car_position + 0.08)*100)):
        for py in range(-70, -63):
            glVertex2f(px/100.0, py/100.0)
    glEnd()

    # Headlights - solid yellow
    for offset in [-0.09, 0.09]:
        glColor3f(1.0, 1.0, 0.0)  # Pure yellow
        midpoint_circle(car_position + offset, -0.75, 0.015)

    # Wheels - solid black with silver rims
    for wheel_x in [car_position - 0.08, car_position + 0.08]:
        # Tire
        glColor3f(0.0, 0.0, 0.0)  # Pure black
        midpoint_circle(wheel_x, -0.79, 0.025)
        # Rim
        glColor3f(0.8, 0.8, 0.8)  # Silver
        midpoint_circle(wheel_x, -0.79, 0.015)

    # Water cannon - solid gray
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.5, 0.5)  # Pure gray
    for px in range(int((car_position - 0.02)*100), int((car_position + 0.02)*100)):
        for py in range(-63, -58):
            glVertex2f(px/100.0, py/100.0)
    glEnd()

def drawHouse(x, y, is_burning=False):
    glPointSize(2.0)

    # Main house body (solid color)
    glBegin(GL_POINTS)
    if is_burning:
        glColor3f(1.0, 0.4, 0.4)  # Burning red
    else:
        glColor3f(0.8, 0.2, 0.2)  # Dark red for normal house
        
    # Fill house body with solid color
    for px in range(int((x - 0.1)*100), int((x + 0.1)*100)):
        for py in range(int(y*100), int((y + 0.2)*100)):
            glVertex2f(px/100.0, py/100.0)
    glEnd()

    # Roof (brown)
    glBegin(GL_POINTS)
    glColor3f(0.4, 0.2, 0.1)
    for px in range(int((x - 0.15)*100), int((x + 0.15)*100)):
        for py in range(int((y + 0.2)*100), int((y + 0.35)*100)):
            real_px = px/100.0
            real_py = py/100.0
            if (real_py <= (y + 0.35) and
               real_py >= (y + 0.2) and
               abs(real_px - x) <= 0.15 * (1 - (real_py - (y + 0.2)) / 0.15)):
                glVertex2f(real_px, real_py)
    glEnd()

    # Windows
    glBegin(GL_POINTS)
    glColor3f(0.8, 0.9, 1.0)  # Light blue windows
    # Left window
    for px in range(int((x - 0.08)*100), int((x - 0.02)*100)):
        for py in range(int((y + 0.07)*100), int((y + 0.13)*100)):
            glVertex2f(px/100.0, py/100.0)
    # Right window
    for px in range(int((x + 0.02)*100), int((x + 0.08)*100)):
        for py in range(int((y + 0.07)*100), int((y + 0.13)*100)):
            glVertex2f(px/100.0, py/100.0)
    glEnd()

    # Door
    glBegin(GL_POINTS)
    glColor3f(0.4, 0.2, 0.1)  # Brown door
    for px in range(int((x - 0.03)*100), int((x + 0.03)*100)):
        for py in range(int(y*100), int((y + 0.08)*100)):
            glVertex2f(px/100.0, py/100.0)
    glEnd()

    # Door knob
    glColor3f(0.8, 0.7, 0.0)  # Golden
    midpoint_circle(x + 0.02, y + 0.04, 0.004)

    # Chimney
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.5, 0.5)  # Gray
    for px in range(int((x + 0.06)*100), int((x + 0.09)*100)):
        for py in range(int((y + 0.25)*100), int((y + 0.32)*100)):
            glVertex2f(px/100.0, py/100.0)
    glEnd()
def drawRoads():
    glPointSize(2.0)
    
    # Main parallel roads
    for road_y in [-0.73, -0.43]:  # Two road positions
        glBegin(GL_POINTS)
        for px in range(-100, 100):
            for py in range(int((road_y-0.12)*100), int((road_y+0.12)*100)):
                x = px/100.0
                y = py/100.0
                
                # Road texture with random dark spots
                is_asphalt = random.random() < 0.1
                if is_asphalt:
                    glColor3f(0.3, 0.3, 0.3)  # Darker spots
                else:
                    glColor3f(0.4, 0.4, 0.4)  # Base road color
                glVertex2f(x, y)
        glEnd()

        # Yellow center lines
        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 0.0)
        for px in range(-100, 100, 20):
            for x in range(10):  # Dashed line length
                glVertex2f((px + x)/100.0, road_y)
        glEnd()

        # White edge lines
        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 1.0)
        for px in range(-100, 100):
            glVertex2f(px/100.0, road_y - 0.12)  # Bottom edge
            glVertex2f(px/100.0, road_y + 0.12)  # Top edge
        glEnd()

    # Driveways to houses
    glBegin(GL_POINTS)
    for house_x, house_y in house_positions:
        for px in range(int((house_x - 0.05)*100), int((house_x + 0.05)*100)):
            for py in range(int((house_y - 0.1)*100), int(house_y*100)):
                glColor3f(0.45, 0.45, 0.45)
                glVertex2f(px/100.0, py/100.0)
    glEnd()

def drawFire():
    if current_burning_house is not None:
        x, y = house_positions[current_burning_house]
        glPointSize(2.0)
        glBegin(GL_POINTS)
        glColor3f(1.0, 0.5, 0.0)
        for i in range(80):
            px = random.uniform(x - 0.08, x + 0.08)
            py = random.uniform(y + 0.2, y + 0.35)
            glVertex2f(px, py)
        glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    drawRoads()  
    for i, (hx, hy) in enumerate(house_positions):
        drawHouse(hx, hy, i == current_burning_house)

    drawCar()

    if fire_active:
        drawFire()

    if water_droplets:
        glColor3f(0.0, 0.7, 1.0)
        glPointSize(3.0)
        glBegin(GL_POINTS)
        for dx, dy in water_droplets:
            glVertex2f(car_position + dx, dy)
        glEnd()

    glutSwapBuffers()

def update(value):
    global spray, water_droplets, fire_active, current_burning_house
    global car_position, car_target, car_moving, fire_start_time
    
    current_time = time.time()
    
    if not fire_active and random.random() < 0.01:
        fire_active = True
        fire_start_time = current_time
        current_burning_house = random.randint(0, len(house_positions) - 1)
        car_target = house_positions[current_burning_house][0]
        car_moving = True

    if car_moving:
        if abs(car_position - car_target) > 0.01:
            direction = 1 if car_target > car_position else -1
            car_position += direction * 0.02
        else:
            car_moving = False
            spray = True

    if spray and not car_moving:
        water_droplets = [(random.uniform(-0.1, 0.1), random.uniform(-0.7, -0.5)) 
                          for _ in range(70)]
        if current_time - fire_start_time >= FIRE_DURATION:
            if random.random() < 0.05:
                fire_active = False
                current_burning_house = None
                spray = False
                water_droplets = []
                car_target = -1.0
                car_moving = True

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def init():
    glClearColor(0.8, 0.9, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glPointSize(2.0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b'Fire & Water - GL_POINTS Only')
    glutDisplayFunc(display)
    glutTimerFunc(16, update, 0)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()