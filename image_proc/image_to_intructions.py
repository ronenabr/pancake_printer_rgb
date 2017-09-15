#definitions

debug = False
debug_graph = True

colorspace = [[0.847,0,0],
              [0.973,0.681,0],
              [0.439,0.408,0]]
black = [1,1,1]
rpm_high = 60
rpm_low = 10
dist_to_angle = 1

color_offsets = [[0,0],
                 [0,0],
                 [0,0]];

#imports

import numpy as np
import scipy.ndimage
from scipy.misc import imread
from itertools import product
import cv2
from tsp_solver.greedy import solve_tsp
from skimage import transform as tf


if debug or debug_graph: 
    import pylab as plt

#code 
colorspace.append(black)
colorspace = np.array(colorspace)


#input: RGB image 
def seperate_colors(img):
    pile = []
    for color in colorspace: 
        color_norm = np.linalg.norm(color)
        dist_map = (img * color).sum(axis=2)/(np.sqrt((img**2).sum(axis=2)) * color_norm+10e-8)
        pile.append(dist_map)
        if debug_graph:
            plt.figure()
            plt.title("projection on color %s" % str(color))
            plt.imshow(dist_map, cmap=plt.cm.gray, vmin=0, vmax=1)
            plt.colorbar()
    
    pile = np.dstack(pile)
    ishape = np.argmax(pile,axis=2)
    if debug_graph:
        plt.figure()
        plt.title("max on all layers")
        plt.imshow(ishape)
        plt.colorbar()
    return ishape

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

def find_edges(img):
    global kernel
    img = (img*255).astype('uint8')
    edges = cv2.Canny(img,100,200)
    dilation = cv2.dilate(edges,kernel,iterations = 1)
    if dilation.mean()  < 128: 
        dilation = 255-dilation
    erosion = cv2.erode(dilation, kernel,iterations=1)
    return dilation 


#input: black image 
def generage_path(img):
    def node_id(pt):
        return pt[0]+pt[1]*img.shape[0]
    def pt_from_id(nid):
        return (nid % img.shape[0], nid/img.shape[0] )
    nodes = []
    pts = product(range(img.shape[0]),range(img.shape[1]))
    for pt in pts:
        if img[pt[0],pt[1]]>0.5:
            nodes.append(node_id(pt))
            
    pts = []
    z = np.zeros((len(nodes),len(nodes)))

    for n_pair in product(range(len(nodes)),range(len(nodes))):
        if n_pair[0]<n_pair[1]:
            p1 = pt_from_id(nodes[n_pair[0]])
            p2 = pt_from_id(nodes[n_pair[1]])
            dist =(np.abs(p1[0]-p2[0]) + np.abs(p1[1]-p2[1]))**4
            z[n_pair[0],n_pair[1]]=dist**2
    path = solve_tsp(z.T)
    if debug:
        plt.figure()
        plt.title("connectivity graph")                        
        plt.imshow(z)

    dot_path = []
    for dot in path:
        dot_path.append(pt_from_id( nodes[dot]))
    dot_path = np.array(dot_path).T
    if debug_graph:
        if dot_path.shape[0] == 0:
            return dot_path
        plt.figure(6)
        plt.plot(dot_path[0],dot_path[1],".-")
    return dot_path
    
def path_to_instruction(path):
    path = np.array(path)
    print path.shape
    plan = []
    dists = []
    for i in range(path.shape[1]-1):
        p0 = path[:,i]
        p1 = path[:,i+1]
        dx = p0[0]-p1[0]
        dy = p0[1]-p1[1]
        dist = np.sqrt((dx)**2 + (dy)**2)
        dists.append(dist)
        rpm = rpm_low
        if dist>2:
            rpm = rpm_low
        plan.append([dx*dist_to_angle, dy*dist_to_angle,rpm])
    return plan

if __name__ ==  "__main__":
    import sys
    image_name = sys.argv[1]
    switch =  False
    if len(sys.argv)>2:
        if sys.argv[2] == "s":
            switch = True
    img = imread(image_name).astype("float32")/255
    if debug_graph:
        plt.figure()
        plt.imshow(img)
        plt.colorbar()
        plt.title("Original image")
    
    scale = 10
    if switch:
        img = 1-img;
        print "Switching.."

    # img[img==0] = 0.01        
    # img = tf.resize(img, (img.shape[0]/scale, img.shape[1]/scale,3), order=0) # order=0, Nearest-neighbor interpolation
    # norm = np.linalg.norm(img,axis=2)
    # norm = np.dstack([norm]*3) + 10e-5
    # img = img/norm



    print "Reading ", image_name, img.shape

    if debug_graph:
        plt.figure()
        plt.imshow(img)
        plt.colorbar()
        plt.title("Original image")
    print img.shape
    layers = seperate_colors(img)
    plt.show()
    print layers.shape
    for layer_idx in range(layers.max()):
        layer_img = layers==layer_idx 
        layer_img = layer_img.astype("float32")
        if debug: 
            plt.figure()
            plt.title("LAYER image %d" %  layer_idx)
            plt.imshow(layer_img, cmap=plt.cm.gray)
            print layer_img
            plt.colorbar()        
        layer_img = tf.resize(layer_img, (layer_img.shape[0]/scale, layer_img.shape[1]/scale), order=0) # order=0, Nearest-neighbor interpolation                    
        bulk_edge = generage_path(layer_img)
        if bulk_edge.shape[0] == 0:
            continue 
        print path_to_instruction(bulk_edge)
    if debug or debug_graph:
        plt.show()