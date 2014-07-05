'''
Created on 5 Jul 2014

@author: michael
'''

class RectangleTree(object):
    '''
    Here's how it is going to work:
    
    We will divide the screen into 32 * 16 pieces (where the 32 divides the width, and the 16 divides the height).
    We will have one rectangle tree to be initialised with all of these rectangles. Call this rectangle tree
    the "Screen Tree"
    
    (Note that the exact number of ways we divide the screen may be adjusted according to stress tests...)
    
    When a rectangle for updating is registered, we find all the rectangles colliding with it in the Screen Tree.
    As these rectangles are found, we also remove them from the tree, and remember them in a grid
    which is a 32 * 16 boolean array.
    
    Once all of the updates are registered (with the above process repeated), we will compute the largest rectangles
    filling the grid formed effectively by the 32 * 16 boolean array (the items being true must be filled).
    We then reconstruct the corresponding rectangle coordinates.
    
    In the meantime we have another rectangle tree which we will call the "Item Tree". The Item Tree holds rectangles
    bounding areas that the various drawers are interested in. With the rectangles constructed from the grid,
    we now compute how each one collides with the rectangles in the item tree.
    
    We collect these items up, sort them in order, and instruct them to redraw over the rectangle.
    (Technically, large rectangles increase the number of items which must be sorted, so it may be beneficial
    to have smaller rectangles. However, I seriously doubt it would be worth it due to the amount of extra
    redraws that might be necessary with smaller rectangles).
    
    When items want to register their interest in parts of the screen, they are added to the Item Tree
    (and subsequently removed if necessary in a similar manner).
    
    Efficiency note:
    
    Re-filling the Screen tree each time is the most costly operation... It would be better if we could
    approximate the coordinates of the rectangles, and merge them at the end. This might be possible...?
    
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
        