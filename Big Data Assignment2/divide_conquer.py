# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 17:01:39 2023

@author: mani
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 16:17:52 2023

@author: mani
"""

import sys
import math
import time

B = 4

def main():
    points = []
    with open("150K Data Points for R-Tree Construction.txt", 'r') as dataset: 
        for data in dataset.readlines():                        #spltting the data points
            data = data.split()
            points.append({                                 #adding those data points in data list  after splitting after space
                'id': int(data[0]),
                'x': int(data[1]),
                'y': int(data[2])
                   })   
    queries = []
    with open("200 Range Queries.txt", 'r') as datapoints:
        for query in datapoints.readlines():
            query = query.split()                               #splitting the query ranges 
            queries.append({
                'id': int(query[0]),
                'x_1': int(query[1]),
                'x_2': int(query[2]),
                'y_1': int(query[3]),
                'y_2': int(query[4])
                })
            
    # build R-Tree
    rtree = RTree()

    for point in points: #insert data points from the root one by one 
        rtree.insert(rtree.root, point)

    results = []
    Answer_query_start=time.time()              #Taking the system time while running this query
    for query in queries:                       #Add the count of points into results list for each query one by one
        results.append(rtree.query(rtree.root, query))
    Answer_query_end=time.time()                #End time 
    Query_processing_time=Answer_query_end-Answer_query_start #total execution time = End time of qeury - start time of running the query
    
    print ("There are",results,"data points included in the query.\n")
    print ("The query processing time is",Query_processing_time,"seconds.")
    print("The average query processing time is: ",Query_processing_time/200,"seconds.")
    
    if len(rtree.root.child_nodes) >= 2:
        x_0 = rtree.root.child_nodes[0]
        x_1 = rtree.root.child_nodes[1]
    print(x_0.MBR)
    print(x_1.MBR)
    start_time = time.time()
    divide_conquer(points)
    end_time = time.time()
    merge_time = end_time - start_time
    print("Time taken for performming Divide and conquer for 2 iterations :", +merge_time)
    avg_time = merge_time/200               #time for each query
    print("Average time taken for running each query is ", +avg_time)
    

def merge_sort(left, right, key):
    merged=[]
    i = 0  
    j = 0  
    while i<len(left) and j<len(right):
        if left[i][key]<=right[j][key]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1   
    while i < len(left):
        merged.append(left[i])
        i += 1   
    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged


def divide_conquer(points, key='id'):
    
    if len(points) <= 1:
        return points  
    mid = len(points) // 2
    lower = points[:mid]
    upper = points[mid:]
    lower = divide_conquer(lower, key)
    upper = divide_conquer(upper, key)   
    points = merge_sort(lower, upper, key)
    return points

class Node(object): #node class
    def __init__(self):                         #Initialise the variables that are required in code
        self.id = 0                             #ID variable is assigned 0
        # for internal nodes
        self.child_nodes = []                   #Child_node and data_points are left empty list
        # for leaf nodes
        self.data_points = []                   #since parent node is unknow, assigned as None
        self.parent = None
        self.MBR = {                            #default values of MBR
            'x1': -1,
            'y1': -1,
            'x2': -1,
            'y2': -1,
        }
    def perimeter(self):        #calculate the perimeter of the MBR but here its only calculating half of it
        return (self.MBR['x2'] - self.MBR['x1']) + (self.MBR['y2'] - self.MBR['y1'])

    def is_overflow(self):      #function called whenever the nodes number increase to more than 4
        if self.is_leaf():
            if self.data_points.__len__() > B: #Checking overflows of data points, B is the upper bound.
                return True
            else:
                return False
        else:
            if self.child_nodes.__len__() > B: #Checking overflows of child nodes, B is the upper bound.
                return True
            else:
                return False

    def is_root(self):
        if self.parent is None:         #checking if the node is root node or not, if it doesnt have root node it will return true
            return True
        else:
            return False

    def is_leaf(self):                  #checking if node is the last node, where the node doesnt have any sub nodes
        if self.child_nodes.__len__() == 0:
            return True
        else:
            return False

class RTree(object): #R tree class
    def __init__(self):
        self.root = Node() #Create a root

    def query(self, node, query): #run to answer the query
        num = 0
        if node.is_leaf(): #check if a data point is included in a leaf node
            for point in node.data_points:
                if self.is_covered(point, query):               #if is_covered is true the num will increament 
                    num = num + 1                               #num is the counter where number points in that range is stored
            return num
        else:
            for child in node.child_nodes: #If it is an MBR, check all the child nodes to see whether there is an interaction
                if self.is_intersect(child, query): #If there is an interaction, keep continuing to check the child nodes in the next layer till the leaf nodes
                    num = num + self.query(child, query)
            return num

    def is_covered(self, point, query):             #checking if the points are within the range of the given query.
        x_1, x_2, y_1, y_2 = query['x_1'], query['x_2'], query['y_1'], query['y_2']         #Here query list has 4 elements in each line x_1, x_2, y_1, y_2
        if x_1 <= point['x'] <= x_2 and y_1 <= point['y'] <= y_2:           #return true if the points fall in range
            return True
        else:
            return False    

    def is_intersect(self, node, query):                #checking if the MBRs are intersecting or not 
        center1_x = (node.MBR['x2'] + node.MBR['x1']) / 2       #calculating the center of 1 MBR by taking  length of X1 and length X2 values and dividing it by 2 since the we are only calculating the from one center to another
        center1_y = (node.MBR['y2'] + node.MBR['y1']) / 2
        length1 = node.MBR['x2'] - node.MBR['x1']
        width1 = node.MBR['y2'] - node.MBR['y1']
        center2_x = (query['x_2'] + query['x_1']) / 2
        center2_y = (query['y_2'] + query['y_1']) / 2
        length2 = query['x_2'] - query['x_1']
        width2 = query['y_2'] - query['y_1']            #if length from center of one MBR to another MBR is less than or equal to length from those 2 points than the MBRs intersect
        if abs(center1_x - center2_x) <= length1 / 2 + length2 / 2 and\
                abs(center1_y - center2_y) <= width1 / 2 + width2 / 2:  #we check the absolute value
            return True
        else:
            return False                    


    def insert(self, u, p): # insert p(data point) to u (MBR)
        if u.is_leaf(): 
            self.add_data_point(u, p) #add the data point and update the corresponding MBR
            if u.is_overflow():
                self.handle_overflow(u) #handel overflow for leaf nodes
        else:
            v = self.choose_subtree(u, p) #choose a subtree to insert the data point to miminize the perimeter sum
            self.insert(v, p) #keep continue to check the next layer recursively
            self.update_mbr(v) #update the MBR for inserting the data point

    def choose_subtree(self, u, p): 
        if u.is_leaf(): #find the leaf and insert the data point
            return u
        else:
            min_increase = sys.maxsize #set an initial value
            best_child = None
            for child in u.child_nodes: #check each child to find the best node to insert the point 
                if min_increase > self.peri_increase(child, p):
                    min_increase = self.peri_increase(child, p)
                    best_child = child
            return best_child

    def peri_increase(self, node, p): # calculate the increase of the perimeter after inserting the new data point
        # new perimeter - original perimeter = increase of perimeter
        origin_mbr = node.MBR
        x1, x2, y1, y2 = origin_mbr['x1'], origin_mbr['x2'], origin_mbr['y1'], origin_mbr['y2']
        increase = (max([x1, x2, p['x']]) - min([x1, x2, p['x']]) +
                    max([y1, y2, p['y']]) - min([y1, y2, p['y']])) - node.perimeter()
        return increase


    def handle_overflow(self, u):
        u1, u2 = self.split(u) #u1 u2 are the two splits returned by the function "split"
        # if u is root, create a new root with s1 and s2 as its' children
        if u.is_root():
            new_root = Node()
            self.add_child(new_root, u1)
            self.add_child(new_root, u2)
            self.root = new_root
            self.update_mbr(new_root)
        # if u is not root, delete u, and set s1 and s2 as u's parent's new children
        else:
            w = u.parent
            # copy the information of s1 into u
            w.child_nodes.remove(u)
            self.add_child(w, u1) #link the two splits and update the corresponding MBR
            self.add_child(w, u2)
            if w.is_overflow(): #check the parent node recursively
                self.handle_overflow(w)
            
    def split(self, u):
        # split u into s1 and s2
        best_s1 = Node()
        best_s2 = Node()
        best_perimeter = sys.maxsize
        # u is a leaf node
        if u.is_leaf():
            m = u.data_points.__len__()
            # create two different kinds of divides
            divides = [sorted(u.data_points, key=lambda data_point: data_point['x']),
                       sorted(u.data_points, key=lambda data_point: data_point['y'])] #sorting the points based on X dimension and Y dimension
            for divide in divides:
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1): #check the combinations to find a near-optimal one
                    s1 = Node()
                    s1.data_points = divide[0: i]
                    self.update_mbr(s1)
                    s2 = Node()
                    s2.data_points = divide[i: divide.__len__()]
                    self.update_mbr(s2)
                    if best_perimeter > s1.perimeter() + s2.perimeter(): #checking if the perimeter of mbr is less than the best perimeter the best perimeter is updated with new value
                        best_perimeter = s1.perimeter() + s2.perimeter()
                        best_s1 = s1
                        best_s2 = s2

        # u is an internal node
        else:
            # create four different kinds of divides
            m = u.child_nodes.__len__()
            divides = [sorted(u.child_nodes, key=lambda child_node: child_node.MBR['x1']), #sorting based on MBRs
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['x2']),
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['y1']),
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['y2'])]
            for divide in divides:
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1): #check the combinations
                    s1 = Node()
                    s1.child_nodes = divide[0: i]
                    self.update_mbr(s1)
                    s2 = Node()
                    s2.child_nodes = divide[i: divide.__len__()]
                    self.update_mbr(s2)
                    if best_perimeter > s1.perimeter() + s2.perimeter():
                        best_perimeter = s1.perimeter() + s2.perimeter()
                        best_s1 = s1
                        best_s2 = s2

        for child in best_s1.child_nodes:
            child.parent = best_s1
        for child in best_s2.child_nodes:
            child.parent = best_s2

        return best_s1, best_s2


    def add_child(self, node, child):
        node.child_nodes.append(child) #add child nodes to the current parent (node) and update the MBRs. It is used in handeling overflows
        child.parent = node
        if child.MBR['x1'] < node.MBR['x1']:        #updating the parent nodes with child node if the child node value is less than parent node and adding child node to the parent nodes 
            node.MBR['x1'] = child.MBR['x1']
        if child.MBR['x2'] > node.MBR['x2']:
            node.MBR['x2'] = child.MBR['x2']
        if child.MBR['y1'] < node.MBR['y1']:
            node.MBR['y1'] = child.MBR['y1']
        if child.MBR['y2'] > node.MBR['y2']:    
            node.MBR['y2'] = child.MBR['y2']
    # return the child whose MBR requires the minimum increase in perimeter to cover p

    def add_data_point(self, node, data_point): #add data points and update the the MBRS
        node.data_points.append(data_point)
        if data_point['x'] < node.MBR['x1']:        # updating the MBRs when data_points are less tham nodes in MBR
            node.MBR['x1'] = data_point['x']
        if data_point['x'] > node.MBR['x2']:
            node.MBR['x2'] = data_point['x']
        if data_point['y'] < node.MBR['y1']:
            node.MBR['y1'] = data_point['y']
        if data_point['y'] > node.MBR['y2']:
            node.MBR['y2'] = data_point['y']


    def update_mbr(self, node): #update MBRs when forming a new MBR. It is used in checking the combinations and update the root
        x_list = []
        y_list = []
        if node.is_leaf():          #if node is leaf node, x and y values come from query in range query file
            x_list = [point['x'] for point in node.data_points]
            y_list = [point['y'] for point in node.data_points]
        else:                       # else we get x and y values from child nodes 
            x_list = [child.MBR['x1'] for child in node.child_nodes] + [child.MBR['x2'] for child in node.child_nodes]
            y_list = [child.MBR['y1'] for child in node.child_nodes] + [child.MBR['y2'] for child in node.child_nodes]
        new_mbr = {
            'x1': min(x_list),
            'x2': max(x_list),
            'y1': min(y_list),
            'y2': max(y_list)
        }
        node.MBR = new_mbr


if __name__ == '__main__':
    main()
