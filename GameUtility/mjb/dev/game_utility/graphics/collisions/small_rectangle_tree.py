'''
Created on 25 Jul 2014

@author: michael
'''

import mjb.dev.game_utility.graphics.collisions.rectangle_collider as collider

class SmallRectangleTree(collider.RectangleCollider):
    '''
    The rectangle tree is designed to store rectangles, and check for intersections between the stored
    rectangle and another rectangle as efficiently as possible. It is specifically designed for fixed
    width/height screens.
    
    By rectangle, we actually mean a tuple of the form:
    (x_min, y_min, x_max, y_max, key)
    
    where the key is arbitrary and for the user only.
    
    This rectangle tree is specifically small, meaning it is faster than the large rectangle
    tree if only a few rectangles are likely to be added, or if the screen size is small.
    
    You should usually use the small rectangle tree to avoid both memory and time
    overheads.
    '''
    
    ###################################################################
    # There's a lot of code duplication between the two trees. Sorry! #
    # Might want to fix this, but that could slow it down...          #
    ###################################################################
    
    '''
    The minimum width of the screen that this tree supports
    '''
    MIN_WIDTH = 4
    '''
    The minimum height of the screen that this tree supports
    '''
    MIN_HEIGHT = 4

    def __init__(self, size):
        '''
        Construct a new rectangle tree, designed to cover coordinates ranging from (0,0) to (x,y) for
        (x,y) = size.
        @param size: the size of the space spanned by the rectangle tree
        @raise ValueError: if the screen size is not at least 4 pixels wide and tall.
        '''
        (width,height) = size
        self.__width = width
        self.__height = height
        if self.__width<SmallRectangleTree.MIN_WIDTH or self.__height<SmallRectangleTree.MIN_HEIGHT:
            raise ValueError("Large rectangle tree cannot be applied to a screen less than " +
                             SmallRectangleTree.MIN_HEIGHT + " pixels tall or " + SmallRectangleTree.MIN_WIDTH +
                             " pixels wide.")
        #Remember the dividing lines of the grid:
        self.__width_divider = self.__width / 4
        self.__height_divider = self.__height / 4
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
        for dim in range(0,3):
            coord = self.__get_coordinate(rect, dim)+1
            #Construct the node if necessary
            if current_node[coord]==[]:
                current_node[0]+=1
                current_node[coord] = [0,[],[],[],[]]
            current_node = current_node[coord]
        #Final one...
        coord = self.__get_coordinate(rect, 3)+1
        if current_node[coord]==[]:
            current_node[0]+=1
        #This final list should just have the rectangle added to it, I think...
        current_node[coord].append(rect)
        
    def remove_rectangle(self, rect):
        '''
        Remove a rectangle from the tree. This has no effect if the exact rectangle given does not exist in the
        tree.
        @param rect: the rectangle to remove from the tree.
        @return: true iff the rectangle was removed, since it was in the tree
        '''
        #Check if it is inside the screen
        if not self.__is_inside_screen(rect):
            return False
        #Convert the rectangle
        rect = self.__convert_rect(rect)
        #Now we search for where the rectangle should exist...
        #We need to hold the node stack too...
        current_node = self.__root
        node_stack = [current_node]
        for dim in range(0,3):
            coord = self.__get_coordinate(rect, dim)+1
            #Construct the node if necessary
            if current_node[coord]==[]:
                return False #does not exist
            current_node = current_node[coord]
            node_stack.append(current_node)
        coord = self.__get_coordinate(rect, 3)+1
        if current_node[coord]==[]:
            return False #does not exist
        #Remove the rectangle...
        was_removed = rect in current_node[coord]
        if was_removed:
            current_node[coord].remove(rect)
        #Now we need to correct for the removal...
        removing = current_node[coord]==[]
        dim = 2 #where we are in the node stack
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
        #Correct for the root... (which is allowed to be empty)
        if dim==-1:
            self.__root[0]-=1
        return was_removed
    
    def collide_rectangle(self, rect):
        '''
        @param rect: the rectangle to check for collisions against.
        @return: all of the rectangles strictly colliding (overlapping by at least one pixel) with the given rect.
        '''
        (x_min,y_min,x_max,y_max) = rect
        #Check if it is inside the screen
        if not self.__is_inside_screen((x_min,y_min,x_max,y_max,None)):
            return []
        #Convert the rectangle
        rect = self.__convert_rect(rect)
        #We need to return all rectangles on all sides in a recursive manner. We will do this recursively...
        (x_min, y_min, x_max, y_max) = rect
        coord_rect = (x_max, y_max, x_min, y_min)
        return self.__collide_rectangle(coord_rect, self.__root, 0)
        
    def __collide_rectangle(self, coord_rect, current_node, dim):
        '''
        @param coord_rect: the rectangle with its coordinate representation
        @param dim: the dimension in the list 
        @return: all of the rectangles intersecting with this rectangle from dim onwards
        '''
        (x_max, y_max, x_min, y_min) = coord_rect #Reversed for rectangle hunting
        res = []
        if current_node==[]:
            return res
        #Special case if this is the last dim...
        if dim==4:
            #This is a list of rectangles!
            for (rect_x_min, rect_y_min, rect_x_max, rect_y_max,
                 (rect_org_x_min,rect_org_y_min,rect_org_x_max,rect_org_y_max,key)) in current_node:
                if rect_x_min<x_max and rect_x_max>x_min and rect_y_min<y_max and rect_y_max>y_min:
                    res.append((rect_org_x_min, rect_org_y_min, rect_org_x_max, rect_org_y_max, key))
            return res
        #Now for the other cases...
        coord = self.__get_coordinate(coord_rect, dim)+1
        #Loop over...
        if dim % 2 == 0:
            #This is a min coordinate. We need all rectangles whose min coordinate is less than our max.
            #Thus we look in our quadrant, and unconditionally in quadrants less than it
            res = self.__collide_rectangle(coord_rect,current_node[coord],dim+1)
            #Add the other results
            if dim%4==0:
                new_rect = (self.__width, y_max, x_min, y_min, None)
            else:
                new_rect = (x_max, self.__height, x_min, y_min, None)
            #We change the coordinates so that we intersect against all the other rectangles
            for min_coord in range(1,coord):
                res.extend(self.__collide_rectangle(new_rect, current_node[min_coord], dim+1))
            return res
        else:
            #This is a max coordinate, so we need rectangles whose max coordinate is any greater than our min.
            res = self.__collide_rectangle(coord_rect, current_node[coord], dim+1)
            #Add the other results
            if dim%4==1:
                new_rect = (x_max, y_max, 0, y_min, None)
            else:
                new_rect = (x_max, y_max, x_min, 0, None)
            #Intersect in the other quadrants
            for max_coord in range(coord+1,5):
                res.extend(self.__collide_rectangle(new_rect, current_node[max_coord], dim+1))
            return res
    
    def is_colliding(self, rect):
        '''
        @param rect: the rectangle to check for collisions against.
        @return: true iff there is some rectangle in the tree that the given rectangle is colliding against.
        (Will stop when it finds one)
        '''
        (x_min,y_min,x_max,y_max) = rect
        #Check if it is inside the screen
        if not self.__is_inside_screen((x_min,y_min,x_max,y_max,None)):
            return False
        #Convert the rectangle
        rect = self.__convert_rect(rect)
        #We need to return all rectangles on all sides in a recursive manner. We will do this recursively...
        (x_min, y_min, x_max, y_max) = rect
        coord_rect = (x_max, y_max, x_min, y_min)
        return self.__collide_rectangle(coord_rect, self.__root, 0)
        
    def __is_colliding(self, coord_rect, current_node, dim):
        '''
        @param coord_rect: the rectangle with its coordinate representation
        @param dim: the dimension in the list 
        @return: True iff there is a rectangle (within this part of the tree) colliding with the given rectangle
        '''
        (x_max, y_max, x_min, y_min) = coord_rect #Reversed for rectangle hunting
        if current_node==[]:
            return False
        #Special case if this is the last dim...
        if dim==4:
            #This is a list of rectangles!
            for (rect_x_min, rect_y_min, rect_x_max, rect_y_max,_) in current_node:
                if rect_x_min<x_max and rect_x_max>x_min and rect_y_min<y_max and rect_y_max>y_min:
                    return True #Found one!
            return False
        #Now for the other cases...
        coord = self.__get_coordinate(coord_rect, dim)+1
        #Loop over...
        if dim % 2 == 0:
            #This is a min coordinate. We need all rectangles whose min coordinate is less than our max.
            #Thus we look in our quadrant, and unconditionally in quadrants less than it
            if (self.__is_colliding(coord_rect,current_node[coord],dim+1)):
                return True
            #Add the other results
            if dim%4==0:
                new_rect = (self.__width, y_max, x_min, y_min, None)
            else:
                new_rect = (x_max, self.__height, x_min, y_min, None)
            #We change the coordinates so that we intersect against all the other rectangles
            for min_coord in range(1,coord):
                if (self.__is_colliding(new_rect, current_node[min_coord], dim+1)):
                    return True
            return False
        else:
            #This is a max coordinate, so we need rectangles whose max coordinate is any greater than our min.
            if (self.__is_colliding(coord_rect, current_node[coord], dim+1)):
                return True
            #Add the other results
            if dim%4==1:
                new_rect = (x_max, y_max, 0, y_min, None)
            else:
                new_rect = (x_max, y_max, x_min, 0, None)
            #Intersect in the other quadrants
            for max_coord in range(coord+1,5):
                if (self.__is_colliding(new_rect, current_node[max_coord], dim+1)):
                    return True
            return False
        
    def __is_inside_screen(self, rect):
        '''
        @param rect: the rectangle to check
        @return: true iff the rectangle is actually inside the screen (at least in part)
        Also catches zero width or zero height
        '''
        (x_min, y_min, x_max, y_max, _) = rect
        return x_max>0 and y_max>0 and x_min<self.__width and y_min<self.__height and x_max!=x_min and y_max!=y_min
        
    def __get_coordinate(self, rect, dim):
        '''
        @param rect: the rectangle whose coordinates in the 4 dimensional array you would like
        @param dim: the level of recursion in the array for the index you would like (0 being the first)
        @return: the relevant coordinate
        '''
        val = rect[dim]
        if dim<=1:
            #x coordinate!
            return min(3,val / self.__width_divider)
        else:
            return min(3,val / self.__height_divider)
        
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
        
    def clear(self):
        '''
        Remove all items from this rectangle tree
        '''
        self.__root = [0,[],[],[],[]]
        