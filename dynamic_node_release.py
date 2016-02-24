#! /bin/python
import urllib2
import urlparse

haas_url = 'http://127.0.0.1/'
#Release nodes : Takes node list as arguments and puts them back to free pool 
#                after given time                               
def release_nodes(non-persistent_list):
        free_node_list = get_free_node_list()
        print free_node_list


# Checks if the node in non-persistent-list is in free_pool or not, if it is the status file will be updated with 0 if not increase the value by 1(either hours or minutes), once the count reaches threshold it will be released back to free pool and the status file will be reset to zero for that node.
def update_node_duration_outside_pool(threshold_time):




#Checks for free pool in the list and returns the list
def get_free_node_list():
        haas_url = 'http://127.0.0.1/'
        free_node_list =  urlparse.urljoin(haas_url,'free_nodes')
        free_node_list = urllib2.urlopen(free_node_list).read()
        return free_node_list


#For checking purpose
if __name__ == "__main__":
        release_nodes(['cisco-03'])

