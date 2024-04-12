import glfw
from OpenGL.GL import *
import numpy as np

type = GL_LINE_LOOP

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glBegin(type)


    degree = np.linspace(0, 180, 7)

    for i in range(7):
        glVertex2f(np.cos(degree[i] * np.pi/180), np.sin(degree[i] * np.pi/180))
    for i in range(5, 0, -1):
        glVertex2f(np.cos(degree[i] * np.pi/180), -np.sin(degree[i] * np.pi/180))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global type
    if key==glfw.KEY_1:
        type = GL_POINTS
    elif key==glfw.KEY_2:
        type = GL_LINES
    elif key==glfw.KEY_3:
        type = GL_LINE_STRIP
    elif key==glfw.KEY_4:
        type = GL_LINE_LOOP
    elif key==glfw.KEY_5:
        type = GL_TRIANGLES
    elif key==glfw.KEY_6:
        type = GL_TRIANGLE_STRIP
    elif key==glfw.KEY_7:
        type = GL_TRIANGLE_FAN
    elif key==glfw.KEY_8:
        type = GL_QUADS
    elif key==glfw.KEY_9:
        type = GL_QUAD_STRIP
    elif key==glfw.KEY_0:
        type = GL_POLYGON

    # elif key==glfw.KEY_SPACE and action==glfw.PRESS:
    #     print ('press space: (%d, %d)'%glfw.get_cursor_pos(window))

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2020095732", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    # Make the window's context current
    glfw.make_context_current(window)
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL
        render()
        # Swap front and back buffers
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()