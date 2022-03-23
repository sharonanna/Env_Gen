import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import numpy as np
from scipy.ndimage.filters import gaussian_filter




MAX_HEIGHT =35
MIN_HEIGHT = 25
GRID_SIZE = 257 #(2**8)
MIN_ROCK_HEIGHT = 1
MAX_ROCK_HEIGHT = 3
RANDOM_SEED = 23



def seed_grid():
    height_map = np.zeros((GRID_SIZE,GRID_SIZE),dtype=float)
    height_map[0,0] = random.uniform(MIN_HEIGHT,MAX_HEIGHT) 
    height_map[0,GRID_SIZE-1] = random.uniform(MIN_HEIGHT,MAX_HEIGHT)
    height_map[GRID_SIZE-1,0] = random.uniform(MIN_HEIGHT,MAX_HEIGHT)
    height_map[GRID_SIZE-1,GRID_SIZE-1] = random.uniform(MIN_HEIGHT,MAX_HEIGHT)
    print(height_map)
    return height_map


def plotting(height_map):
        print("PLOTTING")

        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        #ax = sns.heatmap(height_map)
        ax.set_aspect('auto')
        ax.axis('off')
        x = range(height_map.shape[0])
        y = range(height_map.shape[1])
        max_z = np.max(height_map[:,2])
        X, Y = np.meshgrid(x, y)
        ax.plot_surface(X*0.1 , Y*0.1 , height_map, linewidth=0, antialiased=True)
        ax.set_zlim(0,50)
        plt.show()


def working_shape(max_edge):

    for power in range(1, 15):
        d = (2**power) + 1
        if max_edge <= d:
            return power


def diamond_square(height_map,power):

    resolution = 0.1
    grid_length = GRID_SIZE-1
    grid_num = 1
    random_factor=25
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)
    for level in range(power):
        #print("GRID LENGTH-",grid_length,"GRID NUMBER-",grid_num)
        height_map = diamond_step(height_map,grid_num,grid_length,random_factor,level)
        height_map = square_step(height_map,grid_num,grid_length,random_factor)
        grid_length = grid_length // 2
        if random_factor > 0.02:
            random_factor = random_factor / (level+1)
        else:
            random_factor = random_factor / 1
        print("LEVEL-",level,"RANDOM FACTOR-",random_factor)
        grid_num = grid_num*2

    height_map = gaussian_filter(height_map, sigma=3)
    #height_map[:,2] = height_map[:,2] - np.min(np.min(height_map[:,2]))



    return height_map


def diamond_step(height_map, grid_num,grid_length, random_factor,level):
    print("diamond step")
    
    for i in range(grid_num):
        for j in range(grid_num):
            i_min = i*grid_length
            i_max = (i+1) * grid_length
            i_mid = i_min + grid_length//2
            j_min = j*grid_length
            j_max = (j+1) * grid_length
            j_mid = j_min + grid_length//2
            NW = height_map[i_min,j_min]
            NE = height_map[i_min,j_max]
            SW = height_map[i_max,j_min]
            SE = height_map[i_max,j_max]
            temp_num = level%3
            if temp_num == 0:
                #height_map[i_mid,j_mid] = (NW+NE+SW+SE)/4 - random.uniform(-random_factor,random_factor) + random_factor
                height_map[i_mid,j_mid] = (NW+NE+SW+SE)/4 + random.uniform(-random_factor,random_factor)
            else:    
                #height_map[i_mid,j_mid] = (NW+NE+SW+SE)/4 - random.uniform(-random_factor,random_factor)
                height_map[i_mid,j_mid] = (NW+NE+SW+SE)/4

    return height_map        


def square_step(height_map, grid_num,grid_length,random_factor):
    print("square step")

    for i in range(grid_num):
        for j in range(grid_num):
            half_grid = grid_length//2
            i_min = i*grid_length
            i_max = (i+1) * grid_length
            i_mid = i_min + half_grid
            j_min = j*grid_length
            j_max = (j+1) * grid_length
            j_mid = j_min + half_grid
            NW = height_map[i_min,j_min]
            NE = height_map[i_min,j_max]
            SW = height_map[i_max,j_min]
            SE = height_map[i_max,j_max]
            centre = height_map[i_mid,j_mid]

            #LEFT DIAMOND
            if j_min==0:
                temp = (GRID_SIZE-1) - half_grid
            else:
                temp = j_min - half_grid

            if height_map[i_mid,j_min] == 0:    
                #height_map[i_mid,j_min] = (NW+SW+centre+height_map[i_mid,temp])/4 + random.uniform(-random_factor,random_factor)
                height_map[i_mid,j_min] = (NW+SW+centre+height_map[i_mid,temp])/4 + random.uniform(-random_factor,random_factor)

            #TOP DIAMOND
            if i_min==0:
                temp = (GRID_SIZE-1) - half_grid
            else:
                temp = i_min - half_grid

            if height_map[i_min, j_mid] == 0:    
                #height_map[i_min,j_mid] = (NW+NE+centre+height_map[temp,j_mid])/4  - random.uniform(-random_factor,random_factor)
                height_map[i_min,j_mid] = (NW+NE+centre+height_map[temp,j_mid])/4 + random.uniform(-random_factor,random_factor)

            #RIGHT DIAMOND
            if j_max==(GRID_SIZE-1):
                temp = 0 + half_grid
            else:
                temp = j_max + half_grid
            #height_map[i_mid,j_max] = (NE+SE+centre+height_map[i_mid,temp])/4 + random.uniform(-random_factor,random_factor)
            height_map[i_mid,j_max] = (NE+SE+centre+height_map[i_mid,temp])/4
            #BOTTOM DIAMOND
            if i_max==(GRID_SIZE-1):
                temp = 0 + half_grid
            else:
                temp = i_max + half_grid
            #height_map[i_max,j_mid] = (SW+SE+centre+height_map[temp,j_mid])/4 - random.uniform(-random_factor,random_factor)
            height_map[i_max,j_mid] = (SW+SE+centre+height_map[temp,j_mid])/4              


    return height_map            


def main():
    terrain_map = seed_grid()
    power = working_shape(GRID_SIZE)
    print(power)
    terrain_map = diamond_square(terrain_map,power)
    print(terrain_map.shape)
    plotting(terrain_map)


if __name__ == "__main__":
    main()    