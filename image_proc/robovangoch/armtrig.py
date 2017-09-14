import numpy as np
import scipy.misc
from skimage.draw import line,polygon_perimeter,circle

l1 = int(139*0.263)
l2 = int(114*0.263)

height, width = (600, 600)
b_height,b_width = (190,277)

def draw_line(src,dst,starting_pos):
    rr, cc = line(starting_pos[1] - 1 -src[1], starting_pos[0]+src[0], starting_pos[1] - 1 - dst[1], starting_pos[0] + dst[0])
    return (rr,cc)

def transform(position_vector):
    relative_position_vector = (position_vector[0],position_vector[1]+30*0.263)
    r = np.linalg.norm(relative_position_vector)

    phi = np.arccos((l1**2 + l2**2 - r**2)/(2*l1*l2))

    beta = np.arccos((l1**2 + r**2 -l2**2)/(2*l1*r))
    alpha = np.arctan2(relative_position_vector[1],relative_position_vector[0])
    theta = beta + alpha # left handed solution

    return np.degrees((theta,phi))
    starting_pos = (width/2,height/2)

    arm_starting_pos = (width/2,height/2+30)

    img = np.zeros((height, width), dtype=np.uint8)
    rr, cc = draw_line((0,0),(int(l1*np.cos(theta)),int(l1*np.sin(theta))),arm_starting_pos)
    img[rr, cc] = 255
    rr, cc = draw_line((int(l1*np.cos(theta)),int(l1*np.sin(theta))),
                       (int(l1 * np.cos(theta) + l2 * np.cos(phi + theta - np.pi)),
                        int(l1 * np.sin(theta) + l2 * np.sin(phi + theta - np.pi))),
                       arm_starting_pos)
    img[rr, cc] =  255

    rr,cc = polygon_perimeter([starting_pos[1]-b_height,starting_pos[1],starting_pos[1],starting_pos[1]-b_height],
                              [starting_pos[0]-b_width/2,starting_pos[0]-b_width/2,starting_pos[0]+b_width/2,starting_pos[0]+b_width/2])

    img[rr, cc] = 255

    rr,cc = circle(starting_pos[1]-position_vector[1],starting_pos[0]+position_vector[0],3)
    img[rr, cc] = 255



    scipy.misc.imsave("out.png", img)

    return np.degrees((theta,phi))

if __name__ == "__main__":
    theta0 = 50
    img = np.zeros((b_height+1, b_width+1), dtype=np.uint8)

    print transform((-139,180))

