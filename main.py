from pprint import pprint
import sys
import math
import random
import numpy as np
import string
import copy
import OptFunctions
from array import array
from matplotlib import pyplot as plt
from matplotlib import cm
import mpl_toolkits.mplot3d.axes3d as p3
import re

class MetricCounter:
    def g_metric(self, true_vector = [], known_vector = [], p = 2.0):
        g_sum = 0.0
        n = len(true_vector)
        true_vector_len = len(true_vector) - 1
        known_vector_len = len(known_vector) - 1

        # i object has nearest true object at index nearest_.... [i]
        nearest_members_distance = []

        # count nearest members
        # outer loop
        for i in range(0, known_vector_len):
            g_min = sys.float_info.max
            current_known_point = known_vector[i]
            # inner loop
            for j in range(0, true_vector_len):
                current_true_point = true_vector[j]
                distance = self.distance_between_points(current_known_point, current_true_point)
                if distance < g_min:
                    g_min = distance
            nearest_members_distance.insert(i, g_min)
            # end inner loop
        # end outer loop
        d_array = map(lambda x: x**p, nearest_members_distance)
        g_sum = sum(d_array)

        # 1/p
        g_sum = g_sum**(1.0 / p)
        g_sum = g_sum / n
        return g_sum

    def s_metric(self, known_vector):
        avg_d = 0.0
        s_sum = 0.0

        # avg value
        d_avg_v = self.d_avg(known_vector)

        for idx, val in enumerate(known_vector):
            rel_point_d = self.d_i(idx, known_vector)
            s_sum += (d_avg_v - rel_point_d) ** 2
        n = len(known_vector) - 1.0
        s = (s_sum / n)
        if s < sys.float_info.epsilon:
          print "S is too small - something is broken or it's perfect"
          return 0.0
        else:
          return math.sqrt(s)

  # Fixed
    def distance_between_points(self, point_a = [], point_b = []):
        d_sum = 0.0
        for idx, val in enumerate(point_a):
            d_sum += (point_a[idx] - point_b[idx])**2
        result = d_sum**0.5
        return result


    def d_avg(self, front=[]):
        d_avg_v = 0.0
        n = len(front) - 1
        for idx, val in enumerate(front):
            d_avg_v += self.d_i(idx, front)
        d_avg_v /= len(front)
        return d_avg_v

    def d_i(self, idx, front = []):
        # min
        d_min = sys.float_info.max

        # relative front point
        front_idx = front[idx]

        # size of front
        n = len(front) - 1

        # we go thourgh j indexes
        for i, val in enumerate(front):

          # count value for each front point excluding relative point
          if idx != i:
             front_i = front[i]
             di_tmp = 0.0
             for front_i_idx, val in enumerate(front_i):
                 di_tmp += math.fabs(front_idx[front_i_idx] - front_i[front_i_idx])
             if di_tmp < d_min:
                d_min = di_tmp
        return d_min

class FrontRandomizer:
    def generate_random_front(self, npoints = 0, org_front = []):
        random_point_index = 0
        org_front_index = 0
        random_front = []
        while random_point_index < npoints:
            if org_front_index >= len(org_front):
                org_front_index = 0 # reloop
            new_random_point = self.randomize_point(org_front[org_front_index])
            random_front.append(new_random_point)
            random_point_index += 1
        return random_front

    def randomize_point(self, point = []):
        new_point = []
        for idx, val in enumerate(point):
            sign = 1.0
            if random.random() > 0.5:
                sign *= -1.0
            new_point.append(val + random.random() * 10 * sign)
        return new_point

class VectorRandomizer:
    def createRandomVectors(self, nvectors, vdim = 2):
        ret = []
        for i in range(0, nvectors):
            new_vector = []
            for dim_i in range(0, vdim):
                new_vector.insert(dim_i, random.random())
            ret.insert(i, new_vector)
        return ret

class ParetoFinder:
    def pareto(self, points=[]):
        pareto_front=[]
        sorted_points = sorted(points, key=lambda x: float(x[0]))
        pareto_front.append(sorted_points[0])
        # Test next row against the last row in pareto_frontier
        for idx, possible_point in enumerate(sorted_points, start=1):
            if possible_point[1] < pareto_front[-1][1]:
                pareto_front.append(possible_point)
        return pareto_front

class ParetoPlotter:
    def plotPareto(self, random_points=[], pareto_front=[], known_front=[]):
        ## Plotting
        fig = plt.figure()
        plt.scatter(*zip(*random_points))
        plt.plot(*zip(*pareto_front), color='g')
        plt.plot(*zip(*known_front), marker='o', color='g', ls='')
        plt.show()
# Main method
if __name__ == '__main__':

    # setup
    metric_counter = MetricCounter()
    randomizer = FrontRandomizer()
    vector_randomizer = VectorRandomizer()
    pareto = ParetoFinder()
    plotter = ParetoPlotter()

    # Read known front from file
    known_front = []
    #f = open('./DTLZ.3D/DTLZ5.3D.pf')
    f = open('./ZDT/ZDT3.pf')
    lines = f.readlines()
    f.close()
    for line in lines:
        # cut string by empty space and filter any empty strings sweet
        line_items = filter(None,re.split(r'\s+', line)) #line.replace('\n', '').split(' ')
        point = []
        for idx, line_item in enumerate(line_items):
            point.insert(idx, float(line_item))
        known_front.append(point)


    zdt = OptFunctions.ZDT3()

    points = zdt.array_value(vector_randomizer.createRandomVectors(40000, 10))
    pareto_front = pareto.pareto(points)

    print "G: " + str(metric_counter.g_metric(known_front, points))
    print "S: " + str(metric_counter.s_metric(points))

    #plotter.plotPareto(points, pareto_front, known_front)
    ## Shift front
    ##generated_front = randomizer.generate_random_front(10000, known_front)
    ##print metric_counter.g_metric(true_vector=known_front,known_vector=generated_front)
    ##print(metric_counter.s_metric(generated_front))
