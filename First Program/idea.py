from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Global variables
spray = False  # Spray starts inactive
water_droplets = []
car_position = 0.0  # Initial car position (centered on the X-axis)

# Function to generate random water droplets along the curve y = -sqrt(x)
def generate_water_spray():
    droplets = []
    for _ in range(300):  # Number of water droplets
        x = random.uniform(-0.1, 0.1)  # Spread near the car's position
        y = -math.sqrt(abs(x)) * 0.2 - 0.6  # Curve equation y = -sqrt(x) scaled down
        droplets.append([x, y])
    return droplets

# Function to draw the house
def drawHouse():
    # Draw the base of the house
    glColor3f(0.7, 0.4, 0.1)  # Light brown for the base
    glBegin(GL_QUADS)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.0, -0.5)
    glVertex2f(0.0, 0.0)
    glVertex2f(-0.5, 0.0)
    glEnd()

    # Draw the roof
    glColor3f(0.8, 0.1, 0.1)  # Red for the roof
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.55, 0.0)
    glVertex2f(-0.25, 0.3)
    glVertex2f(0.05, 0.0)
    glEnd()

    # Draw a door
    glColor3f(0.4, 0.2, 0.1)  # Dark brown for the door
    glBegin(GL_QUADS)
    glVertex2f(-0.4, -0.5)
    glVertex2f(-0.3, -0.5)
    glVertex2f(-0.3, -0.25)
    glVertex2f(-0.4, -0.25)
    glEnd()

# Function to draw the road
def drawRoad():
    glColor3f(0.2, 0.2, 0.2)  # Gray color for the road
    glBegin(GL_QUADS)
    glVertex2f(-1.0, -0.7)
    glVertex2f(1.0, -0.7)
    glVertex2f(1.0, -0.6)
    glVertex2f(-1.0, -0.6)
    glEnd()

# Function to draw the car
def drawCar():
    global car_position

    # Car body
    glColor3f(1.0, 0.0, 0.0)  # Red car
    glBegin(GL_QUADS)
    glVertex2f(-0.2 + car_position, -0.6)
    glVertex2f(0.2 + car_position, -0.6)
    glVertex2f(0.2 + car_position, -0.5)
    glVertex2f(-0.2 + car_position, -0.5)
    glEnd()

    # Wheels
    glColor3f(0.0, 0.0, 0.0)  # Black wheels
    glBegin(GL_TRIANGLE_FAN)
    for angle in range(0, 361, 10):
        rad = math.radians(angle)
        glVertex2f(-0.15 + car_position + 0.05 * math.cos(rad), -0.65 + 0.05 * math.sin(rad))  # Left wheel
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    for angle in range(0, 361, 10):
        rad = math.radians(angle)
        glVertex2f(0.15 + car_position + 0.05 * math.cos(rad), -0.65 + 0.05 * math.sin(rad))  # Right wheel
    glEnd()

    # Pipe on the car
    if spray:
        glColor3f(0.3, 0.3, 0.3)  # Gray pipe
        glBegin(GL_QUADS)
        glVertex2f(0.1 + car_position, -0.5)
        glVertex2f(0.15 + car_position, -0.5)
        glVertex2f(0.15 + car_position, -0.45)
        glVertex2f(0.1 + car_position, -0.45)
        glEnd()

# Function to draw the water spray
def drawWaterSpray():
    global car_position
    glColor3f(2/255, 75/255, 134/255)  # Deep blue for water
    glPointSize(5)  # Make water droplets thicker
    glBegin(GL_POINTS)
    for droplet in water_droplets:
        glVertex2f(droplet[0] + car_position + 0.15, droplet[1])  # Adjust position based on car's X-position
    glEnd()

# Function to update water spray droplets
def updateWaterSpray(value):
    global water_droplets, spray

    if spray:
        for droplet in water_droplets:
            droplet[1] += 0.01  # Upward movement
            droplet[0] += random.uniform(-0.002, 0.002)  # Slight horizontal spread

            # Reset droplet if it goes off-screen
            if droplet[1] > 0.5 or abs(droplet[0]) > 1.0:
                x = random.uniform(-0.1, 0.1)
                y = -math.sqrt(abs(x)) * 0.2 - 0.6
                droplet[0] = x
                droplet[1] = y

    glutPostRedisplay()
    glutTimerFunc(30, updateWaterSpray, 0)

# Function to handle keyboard input
def handleKeypress(key, x, y):
    global car_position, spray

    if key == b'\x1b':  # ESC to exit
        glutLeaveMainLoop()

    if key == b'a':  # Move car left
        car_position -= 0.1
    if key == b'd':  # Move car right
        car_position += 0.1
    if key == b'w':  # Activate water spray
        spray = True

    glutPostRedisplay()

# Function to handle key release
def handleKeyRelease(key, x, y):
    global spray

    if key == b'w':  # Deactivate water spray
        spray = False

    glutPostRedisplay()

# Function to draw the scene
def drawScene():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the road, house, car, and water spray
    drawRoad()
    drawHouse()
    drawCar()
    if spray:
        drawWaterSpray()

    glFlush()

# Function to initialize OpenGL settings
def initialize():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

# Main funcTIOM
def main():
    global water_droplets
    water_droplets = generate_water_spray()

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Car with Pipe and Curved Water Spray")
    initialize()
    glutDisplayFunc(drawScene)
    glutKeyboardFunc(handleKeypress)
    glutKeyboardUpFunc(handleKeyRelease)  # Handle key release
    glutTimerFunc(30, updateWaterSpray, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
