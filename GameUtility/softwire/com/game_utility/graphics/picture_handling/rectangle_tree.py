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
        #Initialise the tree!
        self.__root = [0,[],[],[],[]]
        
    def insert_rectangle(self, rect):
        '''
        This adds a rectangle to the tree. Note that if the rectangle falls outside
        the size of the grid, it will effectively be clipped. The call will then have no effect
        if the whole of the rectangle lies outside the grid.
        Note that if a rectangle is added twice, it will be included twice (and must be removed twice
        if you understand what I mean)
        @param rect: the rectangle to add to the rectangle tree
        '''
        #Check if it is inside the screen
        if not self.__is_inside_screen(rect):
            return
        #Convert the rectangle
        rect = self.__convert_rect(rect)
        #Recur to insert the rectangle
        current_node = self.__root
        for dim in range(0,7):
            coord = self.__get_coordinate(rect, dim)+1
            #Construct the node if necessary
            if current_node[coord]==[]:
                current_node[0]+=1
                current_node[coord] = [0,[],[],[],[]]
            current_node = current_node[coord]
        #Final one...
        coord = self.__get_coordinate(rect, 7)+1
        if current_node[coord]==[]:
            current_node[0]+=1
        #This final list should just have the rectangle added to it, I think...
        current_node[coord].append(rect)
        print(str(self.__root))
        
    def remove_rectangle(self, rect):
        '''
        Remove a rectangle from the tree. This has no effect if the exact rectangle given does not exist in the
        tree.
        @param rect: the rectangle to remove from the tree.
        '''
        print("Starting!!")
        print(self.__root)
        #Check if it is inside the screen
        if not self.__is_inside_screen(rect):
            return
        #Convert the rectangle
        rect = self.__convert_rect(rect)
        #Now we search for where the rectangle should exist...
        #We need to hold the node stack too...
        current_node = self.__root
        node_stack = [current_node]
        for dim in range(0,7):
            coord = self.__get_coordinate(rect, dim)+1
            #Construct the node if necessary
            if current_node[coord]==[]:
                return #does not exist
            current_node = current_node[coord]
            node_stack.append(current_node)
        coord = self.__get_coordinate(rect, 7)+1
        if current_node[coord]==[]:
            return #does not exist
        #Remove the rectangle...
        current_node[coord].remove(rect)
        #Now we need to correct for the removal...
        removing = current_node[coord]==[]
        print(self.__root)
        dim = 6 #where we are in the node stack
        while removing and dim>=0:
            #Remove from the current node...
            current_node[0]-=1
            if (current_node[0]==0):
                #We need to remove this too...
                current_node = node_stack[dim]
                current_node[self.__get_coordinate(rect, dim)+1] = []
                dim-=1
            else:
                removing = False
            print(self.__root)
        #Correct for the root... (which is allowed to be empty)
        if dim==-1:
            self.__root[0]-=1
        #That should have removed everything...maybe?
        print(self.__root)
    
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
        (x_min, y_min, x_max, y_max, _) = rect
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
            width_dividers[15-i] = width_dividers[15-i] + (self.__width % 16) - i
        #Repeat for the height
        height_dividers = collections.defaultdict(lambda:0)
        height_division = self.__height / 16
        for i in range(0,16):
            height_dividers[i] = i * height_division
        for i in range(0,self.__height % 16): #the remainder
            height_dividers[15-i] = height_dividers[15-i] + (self.__height % 16) - i
        #For convenience:
        width_dividers[16] = self.__width+1 #plus one because we consider being >= to be in the sector
        height_dividers[16] = self.__height+1
        print(width_dividers)
        print(height_dividers)
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
        self.__coordinate_map[0] = lambda (x_min, y_min, x_max, y_max, _): self.__width_coordinate[x_min]/4
        self.__coordinate_map[1] = lambda (x_min, y_min, x_max, y_max, _): self.__width_coordinate[x_max]/4
        self.__coordinate_map[2] = lambda (x_min, y_min, x_max, y_max, _): self.__height_coordinate[y_min]/4
        self.__coordinate_map[3] = lambda (x_min, y_min, x_max, y_max, _): self.__height_coordinate[y_max]/4
        self.__coordinate_map[4] = lambda (x_min, y_min, x_max, y_max, _): self.__width_coordinate[x_min]%4
        self.__coordinate_map[5] = lambda (x_min, y_min, x_max, y_max, _): self.__width_coordinate[x_max]%4
        self.__coordinate_map[6] = lambda (x_min, y_min, x_max, y_max, _): self.__height_coordinate[y_min]%4
        self.__coordinate_map[7] = lambda (x_min, y_min, x_max, y_max, _): self.__height_coordinate[y_max]%4
    
    def __get_coordinate(self, rect, dim):
        '''
        @param rect: the rectangle whose coordinates in the 8 dimensional array you would like
        @param dim: the level of recursion in the array for the index you would like (0 being the first)
        @return: the coordinates as a list of 8 numbers (in order, so [0] gives the first level)
        '''
        return self.__coordinate_map[dim](rect)
        
    def __convert_rect(self, rect):
        '''
        Convert the rectangle to one whose coordinates fit properly on the screen.
        (Assumes the rectangle is well defined)
        @param rect: the rectangle to convert
        @return: the effective rectangle clipped to the screen
        '''
        (x_min, y_min, x_max, y_max, key) = rect
        return (max(x_min,0),
                max(y_min,0),
                min(x_max,self.__width),
                min(y_max,self.__height),
                (x_min, y_min, x_max, y_max, key))
        