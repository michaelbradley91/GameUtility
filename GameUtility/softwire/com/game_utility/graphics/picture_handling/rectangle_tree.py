'''
Created on 5 Jul 2014

@author: michael
'''

import collections

class RectangleTree(object):
    '''
    The rectangle tree is designed to store rectangles, and check for intersections between the stored
    rectangle and another rectangle as efficiently as possible. It is specifically designed for fixed
    width/height screens.
    
    By rectangle, we actually mean a tuple of the form:
    (x_min, y_min, x_max, y_max, key)
    
    where the key is arbitrary and for the user only.
    '''

    def __init__(self, size):
        '''
        Construct a new rectangle tree, designed to cover coordinates ranging from (0,0) to (x,y) for
        (x,y) = size.
        @param size: the size of the space spanned by the rectangle tree
        @raise ValueError: if the screen size is not at least 16 pixels width and high.
        '''
        (width,height) = size
        self.__width = width
        self.__height = height
        if self.__width<16 or self.__height<16:
            raise ValueError("Rectangle tree cannot be applied to a screen less than 16 pixels high or wide")
        #Initialise the coordinate map...
        self.__divide_screen()
        self.__initialise_coordinate_map()
        
    def insert_rectangle(self, rect):
        '''
        This adds a rectangle to the tree. Note that if the rectangle falls outside
        the size of the grid, it will effectively be clipped. The call will then have no effect
        if the whole of the rectangle lies outside the grid
        @param rect: the rectangle to add to the rectangle tree
        '''
        
    def remove_rectangle(self, rect):
        '''
        Remove a rectangle from the tree. This has no effect if the exact rectangle given does not exist in the
        tree.
        @param rect: the rectangle to remove from the tree.
        '''
    
    def collide_rectangle(self, rect, remove=False):
        '''
        @param rect: the rectangle to check for collisions against.
        @param remove: whether or not the returned rectangles should also be removed from the structure.
        @return: all of the rectangles strictly colliding (overlapping by at least one pixel) with the given rect.
        '''
        
    def __is_inside_screen(self, rect):
        '''
        @param rect: the rectangle to check
        @return: true iff the rectangle is actually inside the screen (at least in part)
        '''
        (x_min, y_min, x_max, y_max) = rect
        return x_max>0 and y_max>0 and x_min<self.__width and y_min<self.__height
        
    def __divide_screen(self):
        '''
        The purpose of this method is to divide the screen up according to the 16 positions.
        We store them in a default dictionary, which is close to an array
        '''
        #Divide by the width
        width_dividers = collections.defaultdict(lambda:0)
        width_division = self.__width / 16
        for i in range(0,16):
            width_dividers[i] = i * width_division
        for i in range(0,self.__width % 16): #the remainder
            width_dividers[15-i] = width_dividers[i] + 1
        #Repeat for the height
        height_dividers = collections.defaultdict(lambda:0)
        height_division = self.__height / 16
        for i in range(0,16):
            height_dividers[i] = i * height_division
        for i in range(0,self.__height % 16): #the remainder
            height_dividers[15-i] = height_dividers[i] + 1
        #For convenience:
        width_dividers[16] = self.__width+1 #plus one because we consider being >= to be in the sector
        height_dividers[16] = self.__height+1
        
        #This is memory intensive, but simplifies the coordinate calculation...
        self.__width_coordinate = collections.defaultdict(lambda:-1)
        self.__height_coordinate = collections.defaultdict(lambda:-1)
        #Fill the "arrays"
        #For the width first...
        current_coord = 0
        for i in range(0,self.__width+1):
            if i>=width_dividers[current_coord+1]:
                #Coordinate changes
                current_coord+=1
            self.__width_coordinate[i] = current_coord
        #For the height
        current_coord = 0
        for i in range(0,self.__height+1):
            if i>=height_dividers[current_coord+1]:
                #Coordinate changes
                current_coord+=1
            self.__height_coordinate[i] = current_coord
    
    def __initialise_coordinate_map(self):
        '''
        This function initialises the coordinate map so that coordinates can be returned quickly
        '''
        self.__coordinate_map = collections.defaultdict(lambda:None)
        self.__coordinate_map[0] = lambda (x_min, y_min, x_max, y_max): self.width_coordinate[x_min]/4
        self.__coordinate_map[1] = lambda (x_min, y_min, x_max, y_max): self.width_coordinate[x_max]/4
        self.__coordinate_map[2] = lambda (x_min, y_min, x_max, y_max): self.height_coordinate[y_min]/4
        self.__coordinate_map[3] = lambda (x_min, y_min, x_max, y_max): self.height_coordinate[y_max]/4
        self.__coordinate_map[4] = lambda (x_min, y_min, x_max, y_max): self.width_coordinate[x_min]%4
        self.__coordinate_map[5] = lambda (x_min, y_min, x_max, y_max): self.width_coordinate[x_max]%4
        self.__coordinate_map[6] = lambda (x_min, y_min, x_max, y_max): self.height_coordinate[y_min]%4
        self.__coordinate_map[7] = lambda (x_min, y_min, x_max, y_max): self.height_coordinate[y_max]%4
    
    def __get_coordinate(self, rect, dim):
        '''
        @param rect: the rectangle whose coordinates in the 8 dimensional array you would like
        @param dim: the level of recursion in the array for the index you would like (0 being the first)
        @return: the coordinates as a list of 8 numbers (in order, so [0] gives the first level)
        '''
        return self.__coordinate_map[dim](rect)
        
        