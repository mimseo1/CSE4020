#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

# computer graphics PA1
# py -3 ratracer.py scene\one_sphere 등으로 사용

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image


class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)

class Sphere:
    def __init__(self, shader, radius, center):
        self.shader = shader
        self.radius = radius
        self.center = center

class Shader:
    def __init__(self, type):
        self.type = type

class Phong(Shader):
    def __init__(self, type, diffuse, specular, exponent):
        super().__init__(type)
        self.diffuse = diffuse
        self.specular = specular
        self.exponent = exponent

class Lambertian(Shader):
    def __init__(self, type, diffuse):
        super().__init__(type)
        self.diffuse = diffuse

def rayTrace(surfaces, ray, viewPoint):
    m = sys.maxsize
    idx = -1
    cnt = 0

    for surface in surfaces:
        a = np.sum(ray * ray)
        b = np.sum((viewPoint - surface.center) * ray)
        c = np.sum((viewPoint - surface.center) ** 2) - surface.radius ** 2
        if b ** 2 - a * c >= 0:
            delta = np.sqrt(b ** 2 - a * c)
            if -b + delta >= 0 and m >= (-b + delta) / a:
                m = (-b + delta) / a
                idx = cnt
            if -b - delta >= 0 and m >= (-b - delta) / a:
                m = (-b - delta) / a
                idx = cnt
        cnt = cnt + 1
    return [m, idx]

def getNormalVector(x, y, z):
    direction = np.cross((y - x), (z - x))
    d = np.sum(direction * z)
    return np.array([direction[0], direction[1], direction[2], d])

def shade(m, ray, viewPoint, surfaces, idx, lightList):
    surface = surfaces[idx]
    r = 0
    g = 0
    b = 0
    n = np.array([0, 0, 0])
    v = -m * ray

    if isinstance(surface, Sphere):
        n = viewPoint + m * ray - surface.center

    n = n / np.sqrt(np.sum(n * n))

    for light in lightList:
        light_i = v + light[0] - viewPoint
        light_i = light_i / np.sqrt(np.sum(light_i * light_i))

        checker = rayTrace(surfaces, -light_i, light[0])

        if checker[1] == idx:
            if isinstance(surface.shader, Lambertian):
                r = r + surface.shader.diffuse[0] * light[1][0] * max(0, np.dot(light_i, n))
                g = g + surface.shader.diffuse[1] * light[1][1] * max(0, np.dot(light_i, n))
                b = b + surface.shader.diffuse[2] * light[1][2] * max(0, np.dot(light_i, n))
            elif isinstance(surface.shader, Phong):
                vUnit = v / np.sqrt(np.sum(v * v))
                h = vUnit + light_i
                h = h / np.sqrt(np.sum(h * h))
                l_sR = surface.shader.specular[0] * light[1][0] * pow(max(0, np.dot(n, h)), surface.shader.exponent)
                l_sG = surface.shader.specular[1] * light[1][1] * pow(max(0, np.dot(n, h)), surface.shader.exponent)
                l_sB = surface.shader.specular[2] * light[1][2] * pow(max(0, np.dot(n, h)), surface.shader.exponent)
                r = r + surface.shader.diffuse[0] * light[1][0] * max(0, np.dot(light_i, n)) + l_sR
                g = g + surface.shader.diffuse[1] * light[1][1] * max(0, np.dot(light_i, n)) + l_sG
                b = b + surface.shader.diffuse[2] * light[1][2] * max(0, np.dot(light_i, n)) + l_sB

    res = Color(r, g, b)
    res.gammaCorrect(2.2)
    return res.toUINT8()

def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir=np.array([0,0,-1]).astype(np.float64)
    viewUp=np.array([0,1,0]).astype(np.float64)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth=1.0
    viewHeight=1.0
    projDistance=1.0
    intensity=np.array([1,1,1]).astype(np.float64)  # how bright the light is.
    #print(np.cross(viewDir, viewUp))

    imgSize=np.array(root.findtext('image').split()).astype(np.int32)

    for c in root.findall('camera'):
        viewPoint=np.array(c.findtext('viewPoint').split()).astype(np.float64)
        #print('viewpoint', viewPoint)
        if (c.findtext('viewDir')):
            viewDir = np.array(c.findtext('viewDir').split()).astype(np.float64)
        if (c.findtext('projNormal')):
            viewProjNormal = np.array(c.findtext('projNormal').split()).astype(np.float64)
        if (c.findtext('viewUp')):
            viewUp = np.array(c.findtext('viewUp').split()).astype(np.float64)
        if (c.findtext('projDistance')):
            projDistance = np.array(c.findtext('projDistance').split()).astype(np.float64)
        if (c.findtext('viewWidth')):
            viewWidth = np.array(c.findtext('viewWidth').split()).astype(np.float64)
        if (c.findtext('viewHeight')):
            viewHeight = np.array(c.findtext('viewHeight').split()).astype(np.float64)

    shaders = []

    for c in root.findall('shader'):
        diffuseColor_c=np.array(c.findtext('diffuseColor').split()).astype(np.float64)
        # print('name', c.get('name'))
        # print('diffuseColor', diffuseColor_c)
        shader_type = c.get('name')
        if (c.get('type') == 'Lambertian'):
            new_shader = Lambertian(shader_type, diffuseColor_c)
            shaders.append(new_shader)
        elif (c.get('type') == 'Phong'):
            specular = np.array(c.findtext('specularColor').split()).astype(np.float64)
            exponent = np.array(c.findtext('exponent').split()).astype(np.float64)[0]
            new_shader = Phong(shader_type, diffuseColor_c, specular, exponent)
            shaders.append(new_shader)
    #code.interact(local=dict(globals(), **locals()))

    surfaces = []

    for c in root.findall('surface'):
        ref = ''
        for d in c:
            if (d.tag == 'shader'):
                ref = d.get('ref')
        shader = [x for x in shaders if (x.type == ref)][0]
        radius = np.array(c.findtext('radius')).astype(np.float64)
        center = np.array(c.findtext('center').split()).astype(np.float64)
        surfaces.append(Sphere(shader, radius, center))

    lightList = []

    for c in root.findall('light'):
        position_c = np.array(c.findtext('position').split()).astype(np.float64)
        intensity_c = np.array(c.findtext('intensity').split()).astype(np.float64)
        lightList.append((position_c, intensity_c))

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0

    pixelWidth = viewWidth / imgSize[0]
    pixelHeight = viewHeight / imgSize[1]

    w = viewDir
    u = np.cross(w, viewUp)
    v = np.cross(w, u)

    w = w / np.sqrt(np.sum(w * w))
    u = u / np.sqrt(np.sum(u * u))
    v = v / np.sqrt(np.sum(v * v))

    s = w * projDistance - u * pixelWidth * (imgSize[0] / 2 + 1 / 2) - v * pixelHeight * (imgSize[1] / 2 + 1 / 2)

    for x in np.arange(imgSize[0]):
        for y in np.arange(imgSize[1]):
            ray = s + u * x * pixelWidth + v * y * pixelHeight
            raytraced = rayTrace(surfaces, ray, viewPoint)
            if (raytraced[1] != -1):
                img[y][x] = shade(raytraced[0], ray, viewPoint, surfaces, raytraced[1], lightList)
            else:
                img[y][x] = np.array([0, 0, 0])


    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
    main()
