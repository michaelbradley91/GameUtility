'''
Created on 26 Aug 2014

@author: michael
'''

import math

'''
This file contains a number of methods to handle the (kind of confusing) maths involved in
game utility. The methods here are largely concerned with rectangles.

A rectangle is considered described by:
(x_centre, y_centre, width, height, angle)
The angle s the rectangle's rotation about its centre, and is anti-clockwise. (width is considered to be horizontal
until a rotation).
The angle is measured in radians due to python's use of radians in cosine, sin, tan. 
'''

def rotate_anti_clockwise(point,origin,radians):
    '''
    Rotate "point" about "origin" by the specified number of radians.
    @param point: the point to rotate
    @param origin: the origin to rotate the point about (use (0,0) for the true origin)
    @param radians: the number of radians to rotate the point by ANTI-clockwise
    @return: the point that is "point" rotated by "radians" radians anti-clockwise about "origin"
    '''
    #Translate so that origin is at (0,0)
    x = point[0] - origin[0]
    y = point[1] - origin[1]
    #For speed
    cos_a = math.cos(radians)
    sin_a = math.sin(radians)
    #Calculate the rotation using the rotation matrix
    newx = (x*cos_a) - (y*sin_a)
    newy = (x*sin_a) + (y*cos_a)
    #Reverse the translation
    newx += origin[0]
    newy += origin[1]
    return newx,newy

def rotate_anti_clockwise_by_origin(point,radians):
    '''
    Rotate "point" about (0,0) by the specified number of radians. Note that this
    is faster if we are certainly rotating about the origin
    @param point: the point to rotate
    @param radians: the number of radians to rotate the point by ANTI-clockwise around (0,0)
    @return: the point that is "point" rotated by "radians" radians anti-clockwise about "origin"
    '''
    #For speed
    cos_a = math.cos(radians)
    sin_a = math.sin(radians)
    x = point[0]
    y = point[1]
    #Calculate the rotation using the rotation matrix
    newx = (x*cos_a) - (y*sin_a)
    newy = (x*sin_a) + (y*cos_a)
    return newx,newy

def add_vectors(v1, v2):
    '''
    Add the two vectors v1 and v2 (expected to be tuple pairs) and return the new vector
    @param v1: the first vector to add
    @param v2: the second vector to add
    @return: v1+v2
    '''
    return (v1[0]+v2[0],v1[1]+v2[1])

def sub_vectors(v1,v2):
    '''
    Subtract vector v2 from v1 (expected to be tuple pairs) and return the new vector
    @param v1: the first vector to subtract from
    @param v2: the second vector to subtract
    @return: v1-v2
    '''
    return (v1[0]-v2[0],v1[1]-v2[1])

def are_rotated_rectangles_colliding(rect1, rect2, meet=False):
    '''
    Calculate if two rectangles are colliding. Each rectangle should be specified by
    (centre,size,angle) where the angle is the number of radians the rectangle has been rotated
    about its centre. The size is (half_width,half_height), so the distances from the centre to the edges
    @param rect1: the first rectangle to check for a collision against
    @param rect2: the second rectangle
    @param meet: False by default. If False, will only return True if the rectangles are strictly
    colliding. If True, will return if the rectangles are "touching" as well.
    @return: True iff rect1 and rect2 are colliding.
    '''
    #The amount of error permitted in "meeting" rectangles
    point_error = 0.0000001
    #Simple heuristic to deal with trivial rectangles...
    if abs(rect1[2])<=point_error and abs(rect2[2])<=point_error:
        #Simple!
        (min_x1,min_y1) = sub_vectors(rect1[1],rect1[0])
        (max_x1,max_y1) = add_vectors(rect1[1],rect1[0])
        (min_x2,min_y2) = sub_vectors(rect2[1],rect2[0])
        (max_x2,max_y2) = add_vectors(rect2[1],rect2[0])
        if meet:
            #Can touch
            return min_x1<=max_x2+point_error and min_y1<=max_y2+point_error and max_x1>=min_x2-point_error and max_y1>=min_y2-point_error
        else:
            #Can't touch
            return min_x1<max_x2 and min_y1<max_y2 and max_x1>min_x2 and max_y1>min_y2
    angle = rect1[2] - rect2[2]
        
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    #Set the centre to make rect1 cannonical
    centre = sub_vectors(rect2[0],rect1[0])
    
    #Rotate rectangle 2 clockwise by its angle to make it axis-aligned (undoing the anti-clockwise angle)
    centre = rotate_anti_clockwise_by_origin(centre,-rect2[2])
    
    #Calculate the vertices rect2
    bottom_left = top_right = centre
    bottom_left = sub_vectors(bottom_left,rect2[1])
    top_right = add_vectors(top_right,rect2[1])
    
    #Calculate the vertices or rotated r1
    A_x = -rect1[1][1]*sin_a
    A_y = rect1[1][1]*cos_a
    B_x = A_x
    B_y = A_y
    t = rect1[1][0]*cos_a
    A_x+=t
    B_x-=t
    t = rect1[1][0]*sin_a
    A_y+=t
    B_y-=t
    
    #Verify that A is the vertical min/max and B is the horizontal min/max
    t = sin_a * cos_a
    if t<0:
        #Swap them over
        t = A_x
        A_x = B_x
        B_x = t
        t = A_y
        A_y = B_y
        B_y = t
    
    #Verify that B is the horizontal minimum (A's location is irrelevant)
    if sin_a<0:
        #"Swap" with the symmetric other B
        B_x = -B_x
        B_y = -B_y
    
    #If rect2's horizontal range doesn't reach rect1, collision is impossible.
    if meet:
        if B_x > top_right[0]+point_error or -B_x < bottom_left[0]-point_error:
            return False
    else:
        #Touching not allowed
        if B_x >= top_right[0] or -B_x <= bottom_left[0]:
            return False
    
    #Heuristic for axis aligned rectangles...
    if t == 0:
        #These are the extremities of the vertices forming the first rectangles intersection with
        #the second rectangle's horizontal range
        ext1 = A_y
        ext2 = -A_y
    else:
        #Find vertical min/max in the horizontal range [BL.x, TR.x]
        x = bottom_left[0]-A_x
        a = top_right[0]-A_x
        ext1 = A_y
        #If the first vertical min/max isn't in [BL.x, TR.x], then
        #find the vertical min/max on BL.x or on TR.x
        if (a*x > 0):
            #Horizontal distance along the triangle
            dx = A_x;
            if x < 0:
                dx -= B_x
                ext1 -= B_y
                x = a
            else:
                dx += B_x
                ext1 += B_y
            #Take the dot product
            ext1 *= x
            ext1 /= dx
            ext1 += A_y
        #Repeat with -A for the other extremity
        x = bottom_left[0]+A_x;
        a = top_right[0]+A_x;
        ext2 = -A_y;
        if a*x > 0:
            dx = -A_x;
            if x < 0:
                dx -= B_x
                ext2 -= B_y
                x = a
            else:
                dx += B_x
                ext2 += B_y
            ext2 *= x; ext2 /= dx; ext2 -= A_y;
    #Finally, perform the 1 dimensional line check... (in the established vertical range)
    if meet:
        #Touching is good enough!
        return not ((ext1 <= bottom_left[1]+point_error and ext2 <= bottom_left[1]+point_error)
                    or (ext1 >= top_right[1]-point_error and ext2 >= top_right[1]-point_error))
    else:
        return not ((ext1 < bottom_left[1] and ext2 < bottom_left[1])
                    or (ext1 > top_right[1] and ext2 > top_right[1]))