#!/usr/bin/env python

import googlemaps
from googlemaps.distance_matrix import distance_matrix
import sys
from ortools.constraint_solver import pywrapcp

gmaps = googlemaps.Client(key='AIzaSyAzlWRJShTKDbxXe1GFrlr7oFFlYmxjxbg')

def create_distance_callback(dist_matrix):
  # Create a callback to calculate distances between cities.

  def distance_callback(from_node, to_node):
    # return int(dist_matrix[from_node][to_node])
    # we're already using ints (not strings) when dist_matrix is constructed

    # print(dist_matrix)

    try:
        print("checking distance between points (%d, %d) -> %d" % (from_node, to_node, dist_matrix[from_node][to_node]))
        return dist_matrix[from_node][to_node]
    except Exception, e:
        print("checking distance between points (%d, %d) -> error" % (from_node, to_node))
        return 0

  return distance_callback

def solve_shortest_route(locations):
    count = len(locations)

    # convert matrix returned from API into a usable matrix of integers
    # for the solver (api_matrix -> dist_matrix)
    api_matrix = distance_matrix(gmaps, locations, locations, "driving")

    dist_matrix = [[0 for i in range(count)] for j in range(count)]
    rows = api_matrix["rows"]

    for i in range(count):
        row = rows[i]
        cols = row["elements"]

        for j in range(count):
            element = cols[j]

            duration = element["duration"]["value"]
            distance = element["distance"]["value"]

            dist_matrix[i][j] = distance

    print(api_matrix)

    # assemble distance

    print("dist_matrix = [")
    for row in range(count):
        sys.stdout.write("  [")
        for col in range(count):
            if col == count - 1:
                sys.stdout.write("%8d  " % dist_matrix[row][col])
            else:
                sys.stdout.write("%8d,  " % dist_matrix[row][col])
        if row == count - 1:
            sys.stdout.write("]] # %s\n" % locations[row])
        else:
            sys.stdout.write("], # %s\n" % locations[row])

    tsp_size = count
    num_routes = 1
    depot = 0

    # Create routing model
    if tsp_size > 0:
        routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        # Create the distance callback.
        dist_callback = create_distance_callback(dist_matrix)
        routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)

        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)
        if assignment:
            # Solution distance.
            print "Total distance: " + str(assignment.ObjectiveValue()) + " miles\n"
            # Display the solution.
            # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
            route_number = 0
            index = routing.Start(route_number)  # Index of the variable for the starting node.
            route = ''
            while not routing.IsEnd(index):
                # Convert variable indices to node indices in the displayed route.
                route += str(locations[routing.IndexToNode(index)]) + ' -> '
                index = assignment.Value(routing.NextVar(index))
            route += str(locations[routing.IndexToNode(index)])
            print "Route:\n\n" + route
        else:
            print 'No solution found.'
    else:
        print 'Specify an instance greater than 0.'


if __name__ == '__main__':
    # Cities
    # city_names = ["New York", "Los Angeles", "Chicago", "Minneapolis", "Denver", "Dallas", "Seattle",
    #              "Boston", "San Francisco", "St. Louis"]

    locations = [[18.997739, 72.841280], [18.880253, 72.945137]]
    solve_shortest_route(locations)

