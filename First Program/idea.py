from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time

# Global variables
spray = False
water_droplets = []
car_position = -1.0  # Start from left side
car_target = 0.0
fire_positions = []
fire_active = False
house_positions = [
    (-0.7, -0.2), (-0.35, -0.2), (0.0, -0.2), (0.35, -0.2), (0.7, -0.2),  # Top row
    (-0.7, -0.5), (-0.35, -0.5), (0.0, -0.5), (0.35, -0.5), (0.7, -0.5)   # Bottom row
] # House positions
current_burning_house = None
car_moving = False
flame_particles = []
fire_start_time = 0
FIRE_DURATION = 5

def generate_water_spray():
    droplets = []
    for _ in range(300):
        x = random.uniform(-0.1, 0.1)
        y = -math.sqrt(abs(x)) * 0.2 - 0.6
        droplets.append([x, y])
    return droplets

def drawHouse(x, y, is_burning=False):
    # Main house body
    if is_burning:
        glColor3f(1.0, 0.4, 0.4)  # Lighter red for burning house
    else:
        glColor3f(0.8, 0.0, 0.0)  # Dark red for normal house
    
    # House base
    glBegin(GL_QUADS)
    glVertex2f(x - 0.1, y)
    glVertex2f(x + 0.1, y)
    glVertex2f(x + 0.1, y + 0.2)
    glVertex2f(x - 0.1, y + 0.2)
    glEnd()

    # Roof
    glColor3f(0.4, 0.2, 0.0)  # Brown roof
    glBegin(GL_TRIANGLES)
    glVertex2f(x - 0.15, y + 0.2)
    glVertex2f(x + 0.15, y + 0.2)
    glVertex2f(x, y + 0.35)
    glEnd()

    # Window
    glColor3f(0.8, 0.9, 1.0)  # Light blue window
    glBegin(GL_QUADS)
    glVertex2f(x - 0.05, y + 0.05)
    glVertex2f(x + 0.05, y + 0.05)
    glVertex2f(x + 0.05, y + 0.15)
    glVertex2f(x - 0.05, y + 0.15)
    glEnd()

    # Window cross
    glColor3f(0.4, 0.2, 0.0)  # Brown window frame
    glLineWidth(2.0)
    glBegin(GL_LINES)
    # Vertical line
    glVertex2f(x, y + 0.05)
    glVertex2f(x, y + 0.15)
    # Horizontal line
    glVertex2f(x - 0.05, y + 0.1)
    glVertex2f(x + 0.05, y + 0.1)
    glEnd()

    # Door
    glColor3f(0.4, 0.2, 0.0)  # Brown door
    glBegin(GL_QUADS)
    glVertex2f(x - 0.03, y)
    glVertex2f(x + 0.03, y)
    glVertex2f(x + 0.03, y + 0.08)
    glVertex2f(x - 0.03, y + 0.08)
    glEnd()

    # Door knob
    glColor3f(1.0, 0.8, 0.0)  # Golden knob
    glPointSize(3.0)
    glBegin(GL_POINTS)
    glVertex2f(x + 0.02, y + 0.04)
    glEnd()

    # Chimney
    glColor3f(0.5, 0.5, 0.5)  # Gray chimney
    glBegin(GL_QUADS)
    glVertex2f(x + 0.06, y + 0.25)
    glVertex2f(x + 0.09, y + 0.25)
    glVertex2f(x + 0.09, y + 0.32)
    glVertex2f(x + 0.06, y + 0.32)
    glEnd()

def drawCar():
    # Main body
    glColor3f(0.2, 0.2, 0.8)  # Dark blue
    glBegin(GL_QUADS)
    glVertex2f(car_position - 0.08, -0.8)
    glVertex2f(car_position + 0.08, -0.8)
    glVertex2f(car_position + 0.08, -0.65)
    glVertex2f(car_position - 0.08, -0.65)
    glEnd()

    # Car top
    glColor3f(0.1, 0.1, 0.7)  # Darker blue
    glBegin(GL_QUADS)
    glVertex2f(car_position - 0.06, -0.65)
    glVertex2f(car_position + 0.06, -0.65)
    glVertex2f(car_position + 0.04, -0.6)
    glVertex2f(car_position - 0.04, -0.6)
    glEnd()

    # Windows
    glColor3f(0.8, 0.8, 1.0)  # Light blue
    glBegin(GL_QUADS)
    glVertex2f(car_position - 0.05, -0.65)
    glVertex2f(car_position + 0.05, -0.65)
    glVertex2f(car_position + 0.03, -0.61)
    glVertex2f(car_position - 0.03, -0.61)
    glEnd()

    # Wheels
    glColor3f(0.1, 0.1, 0.1)  # Black
    for x_offset in [-0.06, 0.06]:
        glBegin(GL_POLYGON)
        for i in range(32):
            angle = 2 * math.pi * i / 32
            x = car_position + x_offset + 0.02 * math.cos(angle)
            y = -0.79 + 0.02 * math.sin(angle)
            glVertex2f(x, y)
        glEnd()

    # Water cannon
    glColor3f(0.5, 0.5, 0.5)  # Gray
    glBegin(GL_QUADS)
    glVertex2f(car_position - 0.02, -0.6)
    glVertex2f(car_position + 0.02, -0.6)
    glVertex2f(car_position + 0.02, -0.55)
    glVertex2f(car_position - 0.02, -0.55)
    glEnd()

    # Front lights
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    for x_offset in [-0.07, 0.07]:
        glBegin(GL_QUADS)
        glVertex2f(car_position + x_offset - 0.01, -0.77)
        glVertex2f(car_position + x_offset + 0.01, -0.77)
        glVertex2f(car_position + x_offset + 0.01, -0.75)
        glVertex2f(car_position + x_offset - 0.01, -0.75)
        glEnd()

def drawRoad():
    # Main roads
    glColor3f(0.4, 0.4, 0.4)  # Dark gray for roads
    for y_pos in [-0.35, -0.65]:
        glBegin(GL_QUADS)
        glVertex2f(-1.0, y_pos - 0.1)
        glVertex2f(1.0, y_pos - 0.1)
        glVertex2f(1.0, y_pos + 0.1)
        glVertex2f(-1.0, y_pos + 0.1)
        glEnd()

    # Road markings
    glColor3f(1.0, 1.0, 1.0)  # White for markings
    for y_pos in [-0.35, -0.65]:
        glBegin(GL_LINES)
        for x in range(-10, 11, 2):
            x_pos = x / 10.0
            glVertex2f(x_pos - 0.1, y_pos)
            glVertex2f(x_pos + 0.1, y_pos)
        glEnd()


def drawFire():
    if current_burning_house is not None:
        x, y = house_positions[current_burning_house]
        # Draw multiple flame particles
        for i in range(15):
            time_offset = time.time() * 5
            # Oscillating movement
            wave_x = math.sin(time_offset + i) * 0.02
            wave_y = math.cos(time_offset + i * 0.5) * 0.01
            
            # Base positions
            base_x = x + wave_x
            base_y = y + 0.2 + wave_y
            
            # Color gradient from yellow to red
            t = (math.sin(time_offset + i) + 1) * 0.5
            glBegin(GL_TRIANGLES)
            # Yellow core
            glColor3f(1.0, 1.0, 0.0)
            glVertex2f(base_x, base_y)
            # Orange-red tips
            glColor3f(1.0, 0.2, 0.0)
            glVertex2f(base_x + 0.05, base_y + 0.1)
            glVertex2f(base_x - 0.05, base_y + 0.1)
            glEnd()
            
            # Small particles
            glPointSize(2.0)
            glBegin(GL_POINTS)
            glColor3f(1.0, 0.5 + random.random() * 0.5, 0.0)
            for _ in range(5):
                spark_x = base_x + random.uniform(-0.05, 0.05)
                spark_y = base_y + random.uniform(0.0, 0.15)
                glVertex2f(spark_x, spark_y)
            glEnd()

def update(value):
    global spray, water_droplets, fire_active, current_burning_house
    global car_position, car_target, car_moving, fire_start_time

    current_time = time.time()

    # Random fire generation
    if not fire_active and random.random() < 0.01:  # 1% chance each update
        fire_active = True
        fire_start_time = current_time
        current_burning_house = random.randint(0, len(house_positions) - 1)
        car_target = house_positions[current_burning_house][0]
        car_moving = True

    # Car movement with smooth acceleration
    if car_moving:
        if abs(car_position - car_target) > 0.01:
            direction = 1 if car_target > car_position else -1
            distance = abs(car_target - car_position)
            speed = min(0.03, distance * 0.1)  # Adaptive speed
            car_position += direction * speed
        else:
            car_position = car_target  # Snap to exact position
            car_moving = False
            spray = True

    # Water spray logic
    if spray and not car_moving:
        water_droplets = generate_water_spray()
        if current_time - fire_start_time >= FIRE_DURATION:
            if random.random() < 0.05:  # 5% chance to extinguish
                fire_active = False
                current_burning_house = None
                spray = False
                water_droplets = []
                car_target = -1.0  # Return to start
                car_moving = True

    # Clear water droplets when not spraying
    if not spray:
        water_droplets = []

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)  # ~60 FPS

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    drawRoad()
    drawCar()
    
    # Draw houses
    for i, (x, y) in enumerate(house_positions):
        drawHouse(x, y, i == current_burning_house)
    
    if fire_active:
        drawFire()
    
    if water_droplets:
        glColor3f(0.0, 0.7, 1.0)
        glBegin(GL_POINTS)
        for droplet in water_droplets:
            glVertex2f(car_position + droplet[0], droplet[1])
        glEnd()
    
    glutSwapBuffers()

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
    glutCreateWindow(b'Fire and Water Simulation')
    glutDisplayFunc(display)
    glutTimerFunc(16, update, 0)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()