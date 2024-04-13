import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

T = np.array([[1., 0., 0],
              [0., 1., 0],
              [0., 0., 1.]])

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv((T @ np.array([.0, .5, 1.]))[:-1])
    glVertex2fv((T @ np.array([.0, .0, 1.]))[:-1])
    glVertex2fv((T @ np.array([.5, .0, 1.]))[:-1])
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global T
    if key == glfw.KEY_Q and action == glfw.PRESS:
        M = [[1, 0, -0.1],
             [0, 1, 0],
             [0, 0, 1]]
        T = M @ T
    elif key == glfw.KEY_E and action == glfw.PRESS:
        M = [[1, 0, 0.1],
             [0, 1, 0],
             [0, 0, 1]]
        T = M @ T
    elif key == glfw.KEY_A and action == glfw.PRESS:
        M = np.array([[np.cos(np.radians(10)), -np.sin(np.radians(10)), 0],
                      [np.sin(np.radians(10)), np.cos(np.radians(10)), 0],
                      [0., 0., 1.]])
        T = T @ M
    elif key == glfw.KEY_D and action == glfw.PRESS:
        M = np.array([[np.cos(np.radians(10)), np.sin(np.radians(10)), 0],
                      [-np.sin(np.radians(10)), np.cos(np.radians(10)), 0],
                      [0., 0., 1.]])
        T = T @ M
    elif key == glfw.KEY_1 and action == glfw.PRESS:
        T = np.array([[1., 0., 0],
                      [0., 1., 0],
                      [0., 0., 1.]])

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2020095732-3-1", None,None)
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
        t = glfw.get_time()

        render(T)
        # Swap front and back buffers
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()