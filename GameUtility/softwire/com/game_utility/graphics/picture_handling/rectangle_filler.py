'''
Created on 14 Jul 2014

@author: michael
'''

import collections

class RectangleFiller(object):
    '''
    This class has static methods designed to automatically filler a grid with
    the "largest" rectangles possible.
    
    The grid we are filling corresponds to a spreadsheet, where all of the green
    cells should be filled, but the red cells should be avoided. We can spread
    a rectangle over green cells, and we ideally wish to identify the smallest
    number of rectangles which can achieve this, while keeping them "large".
    
    Firstly, large rectangles here are considered to be ones both tall and wide.
    We want them to cover entire objects, so that objects are rarely forced into
    being drawn more than once. Very long narrow strips don't meet this criteria.
    
    The algorithm does this via a (suboptimal at least in terms of the number of rectangles)
    heuristic. It will find the top and then left most rectangle not covered, and alternately
    try expanding the rectangle horizontally and then vertically until it can do neither.
    '''
    
    class _TraversableList():
        '''
        This class implements a list quickly traversable by the filling algorithm.
        This class actually does most of the work
        '''
        
        class _Node():
            '''
            A node for the traversable list
            '''
            
            def __init__(self,coord,next_node,prev_node):
                '''
                Construct a new node for the list
                @param coord: the coordinate to be held at this node
                @param next_node: the next node that this points to 
                '''
                self.coord = coord
                self.next_node = next_node
                self.prev_node = prev_node
        
        def __init__(self,coords):
            '''
            @param coords: initialise this list with the coordinates in the form
            of [(x,y),(x2,y2),...]
            '''
            #The default dict holds order of one look up for any node (roughly)
            self.__look_up = collections.defaultdict(lambda:None)
            #Construct the list in order
            prev_node = None
            coords.sort()
            for coord in coords:
                node = RectangleFiller._TraversableList._Node(coord,None,prev_node)
                self.__look_up[coord] = node
                prev_node = node
            #Correct the next pointers... (prev_node is currently the final node...)
            current_node = prev_node
            prev_node = None
            while current_node!=None:
                #Confusing!
                current_node.next_node = prev_node
                prev_node = current_node
                current_node = current_node.prev_node
            #The special head
            self.__head = self.__look_up[coords[0]]
            #That should be the set up!
            
        def contains(self,coord):
            '''
            @param coord: the coordinate to check for
            @return: true iff the coordinate does (still) exist in the list
            '''
            return self.__look_up[coord]!=None
        
        def remove(self,coord):
            '''
            Removes the given coordinate permanently from the list.
            This node must exist in the rectangle filler.
            @param coord: the coordinate to remove
            '''
            node = self.__look_up[coord]
            if node==self.__head:
                #Update the head!
                self.__head = node.next_node
            #Now remove the node...
            if node.prev_node!=None:
                node.prev_node.next_node = node.next_node
            if node.next_node!=None:
                node.next_node.prev_node = node.prev_node
            #Removed!
            self.__look_up[coord] = None
        
        def get_next(self):
            '''
            @return: the next smallest coordinate that is still in the list.
            This will be None if the list is empty
            '''
            if self.__head==None:
                return None
            return self.__head.coord
    
    @staticmethod
    def fill_grid(grid):
        '''
        @param grid: the "grid" should consist of a list of tuple pairs (x,y)
        representing the rectangles which should be filled.
        @return: a list of rectangles in the form (x_min,y_min,x_max,y_max)
        which cover all of the grid and no other coordinates, which are as large as possible.
        '''
        'Note: if the number of grid coordinates passed in is M, this runs in O(MlogM).'
        'It is possible to get this to run in O(N) for N the size of the grid, but I imagine'
        'this is typically worse...?'
        #Construct the list for the specialised order of one traversal...
        traversable_list = RectangleFiller._TraversableList(grid)
        rect_list = []
        #Get the top left coordinate of the rectangle to try
        top_left = traversable_list.get_next()
        while top_left!=None:
            #Expand the rectangle as far as possible!
            rect_list.append(RectangleFiller.__expand(top_left,traversable_list))
            top_left = traversable_list.get_next()
        #Finished!
        return rect_list
        
    @staticmethod
    def __expand(top_left,traversable_list):
        '''
        @param top_left: the top left coordinate of the rectangle to expand (must not be none)
        @param traversable_list: the traversable list object to use when constructing
        the rectangle
        @return: a new rectangle in the form of (x_min,y_min,x_max,y_max) expanded as much
        as possible according to the heuristic
        '''
        #Remove the top left rectangle (which will always be used
        traversable_list.remove((top_left))
        #True indicates expansion along the x axis. False indicates expansion along the y axis
        alternater = True
        #Store the height and width of the rectangle
        (x_min,y_min) = top_left
        current_width = 1
        current_height = 1
        #Quite an ugly while loop...
        failed_one_side = False
        while True:
            if alternater:
                #Expand along the x axis (=> min_x + current_width)
                succeeded = True
                for y in range(y_min, y_min+current_height):
                    if not traversable_list.contains((x_min+current_width,y)):
                        succeeded = False
                        #Leave the loop
                        break
                if succeeded:
                    #Remove all of the rectangles...
                    for y in range(y_min, y_min+current_height):
                        traversable_list.remove((x_min+current_width,y))
                    current_width+=1
                else:
                    #Indicate that expansion is only possible along the y axis now
                    alternater = not alternater
                    if failed_one_side:
                        break
                    failed_one_side = True
            else:
                #Expand along the y axis (=> min_y + current_height)
                succeeded = True
                for x in range(x_min, x_min+current_width):
                    if not traversable_list.contains((x,y_min+current_height)):
                        succeeded = False
                        #Leave the loop
                        break
                if succeeded:
                    #Remove all of the rectangles...
                    for x in range(x_min, x_min+current_width):
                        traversable_list.remove((x,y_min+current_height))
                    current_height+=1
                else:
                    #Indicate that expansion is only possible along the x axis now
                    alternater = not alternater
                    if failed_one_side:
                        break
                    failed_one_side = True
            if not failed_one_side:
                alternater = not alternater
        #Done!
        return (x_min,y_min,x_min+current_width-1,y_min+current_height-1)
            
        
        