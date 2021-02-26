def parser(path):
    """
    Function which takes a file path and imports the file
    """

    file = open(path, "r")
    list_of_lists = [(line.strip()).split() for line in file]
    file.close()
    #print(list_of_lists)
    
    return(list_of_lists)

# Insert path to file
your_path = 'C:/.../a.txt'
data = parser(your_path)

# Get problem metadata 
metadata = data[0]
# Remove metadata from remaining data
data.pop(0)
# Name variables in a list
variables = ['duration', 'intersections', 'streets', 'cars', 'bonus']
# Create dictionary of meta data
meta_dic = dict(zip(variables, metadata))
# Print for user
print(meta_dic)
# Assign variables in metadaTA
duration = int(metadata[0])
intersectons = int(metadata[1])
streets = int(metadata[2])
cars = int(metadata[3])
bonus = int(metadata[4])
# Get intersections
intersection_data = data[0:streets]
# Get paths
path_data = data[streets:]

"""
Create nested dictionary with names as key and start, end, and travel time inne dic  
"""
# Create list of street names
name_list = [x[2] for x in intersection_data]
# Create list of list with start, end and travel time
street_data_list = [x[0:2] + [x[3]] for x in intersection_data]
# Create dictionary
street_dic = {}
for name, street_data in zip(name_list, street_data_list):
    street_data = {'start_intersection' : int(street_data[0]),
                    'end_intersection' : int(street_data[1]),
                    'travel_time' : int(street_data[2])}
    street_dic[name] = street_data

"""
Create dictionary with each car as key, 
Value will be:
number of streets to travel
streets
total travel time
"""
# Give each car an index
car_idx_list = list(range(cars))
total_streets_list = [int(x[0]) for x in path_data]
street_name_list = [x[1:] for x in path_data]
# Create dictionary
car_dic = {}
for car, total_streets, streets in zip(car_idx_list, total_streets_list, street_name_list):
    # Pack total streets and route into dictionare
    route_data = {'total_streets':total_streets, 
                'route' : streets}
    # Compute total travel time
    total_travel_time = 0
    for street in route_data['route']:
        total_travel_time = total_travel_time + street_dic[street]['travel_time']
    # Add total travel time to route_data
    route_data['total_travel_time'] = total_travel_time
    # Assign data to car
    car_dic[car] = route_data

"""
Create sorted list of tuples with car idx and total travel time
"""
# Create list with total_travel_time
total_travel_time_list = [car_dic[x]['total_travel_time'] for x in car_dic]
# Zip cars and total travel time
car_travels_list = list(zip(car_idx_list, total_travel_time_list))
# Create sorted list of travel cars
car_travels_list.sort(key = lambda x: x[1])


"""
Loop over cars with smallest total travel time
For each street take the end intersection (keep end intersection open during entire duration)
Store intersections in list/or set
Repeat and check if intersections are already used, then continue to next car
"""
all_intersections = []
all_streets = []
# Loop over cars
for (car, _) in car_travels_list:
    # Loop over streets
    temp_intersections = []
    temp_streets = []
    for street in car_dic[car]['route']:
        # Append end_intersections to temporary list
        temp_intersections.append(street_dic[street]['end_intersection'])
        temp_streets.append(street)
    # Check if intersection of all and temp intersection is empty
    # if yes, continue to next car
    all_set = set(all_intersections)
    temp_set = set(temp_intersections)
    intersection = all_set.intersection(temp_set)
    if len(intersection) != 0:
        continue  
    # Append to all intersectins 
    all_intersections = all_intersections + temp_intersections
    all_streets = all_streets + temp_streets

# Write total number of intersections
total_intersections = len(all_intersections)
# Create list of intersections
duration_list = [duration] * total_intersections
# Create list of tuples 
routes_list = list(zip(all_intersections,all_streets, duration_list))



with open('listfile.txt', 'w') as filehandle:
    filehandle.write('%s\n' % total_intersections)
    for listitem in routes_list:
        # Intersection - 1 traffic light - Street
        filehandle.write('%s' % listitem[0] + '\n1' + '\n%s' % listitem[1] + ' %s' % listitem[2] + '\n')




