'''
Created on 25 Jul 2014

@author: michael
'''

import mjb.dev.game_utility.collisions.large_rectangle_tree as large_rectangle_tree
import mjb.dev.game_utility.collisions.small_rectangle_tree as small_rectangle_tree
import mjb.dev.game_utility.collisions.simple_rectangle_collider as simple_rectangle_collider

class RectangleColliderPicker(object):
    '''
    This class helps the application to choose an appropriate rectangle collider
    '''
    
    #The boundaries for deciding which collider is best...
    SMALL = 10
    '''
    If the expected number of rectangles is <=SMALL, the simple rectangle collider will be used
    '''
    MEDIUM = 100
    '''
    If the expected number of rectangles is >SMALL and <=MEDIUM, the small rectangle tree will be used
    (Otherwise the large tree will be used)
    '''

    @staticmethod
    def get_recommended_collider(size,number_of_rectangles):
        '''
        Return the collider most suitable to handle the given size of screen
        and the (estimated) number of rectangles to be added
        @param size: the size of the screen for the collider to work with
        @param number_of_rectangles: the estimated number of rectangles to be added to this screen
        @return: a suitable collider set to the correct size but otherwise empty
        '''
        #Check the size...
        (width,height) = size
        if (number_of_rectangles<=RectangleColliderPicker.SMALL):
            #The small collider will do
            return simple_rectangle_collider.SimpleRectangleCollider(size)
        if (number_of_rectangles>RectangleColliderPicker.SMALL
            and number_of_rectangles<=RectangleColliderPicker.MEDIUM):
            #The small tree is appropriate
            if (small_rectangle_tree.SmallRectangleTree.MIN_WIDTH<=width or small_rectangle_tree.SmallRectangleTree.MIN_HEIGHT<=height):
                return small_rectangle_tree.SmallRectangleTree(size)
            return simple_rectangle_collider.SimpleRectangleCollider(size)
        #The large tree is needed!
        if (large_rectangle_tree.LargeRectangleTree.MIN_WIDTH<=width or large_rectangle_tree.LargeRectangleTree.MIN_HEIGHT<=height):
            return large_rectangle_tree.LargeRectangleTree(size)
        if (small_rectangle_tree.SmallRectangleTree.MIN_WIDTH<=width or small_rectangle_tree.SmallRectangleTree.MIN_HEIGHT<=height):
            return small_rectangle_tree.SmallRectangleTree(size)
        return simple_rectangle_collider.SimpleRectangleCollider(size)
        