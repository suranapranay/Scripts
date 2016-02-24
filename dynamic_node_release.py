! /bin/python
import urllib2
import urlparse
from sets import Set

#Global variables to be used
haas_url = 'http://127.0.0.1/'

#Release nodes : Takes node list as arguments and puts them back to free pool 
#                after given time                               
def release_nodes(non_persistent_list,threshold_time):
        free_node_list = get_free_node_list()
        print free_node_list
        update_node_duration_outside_pool(non_persistent_list,free_node_list,threshold_time)


# Checks if the node in non-persistent-list is in free_pool or not, if it is the status file will be updated with 0 if not increase the value by 1(either hours or minutes), once the count reaches threshold it will be released back to free pool and the status file will be reset to zero for that node.
def update_node_duration_outside_pool(non_persistent_list,free_node_list,threshold_time):
        nodes_to_update_infile = list(Set(non_persistent_list)-Set(free_node_list))
        write_to_file(nodes_to_update_infile)
        #write_to_file(non_persistent_list,free_node_list)

'''
# Updates the node list in file
def write_to_file(nodes_to_update_infile):
        #status_file = open(status_file.txt,'w')
        with open(status_file.txt,'w') as status_file:
        #for node in nodes_to_update_infile:
        #status_file.write(node,
'''

#def create_node_dictionary(node,time)

def get_current_nodes_status():
        node_dict={}
        with open('status_file.txt','r') as status_file:
                for line in status_file:
                        node = line.split()
                        node_dict[node[0]] = node[1]
                print node_dict

#We will initialize file with nodes and initial timing status. We will use a dictionary for that.
def initialize_file(node_list):
        initialization_time = 0
        with open('status_file.txt','w') as status_file:
                for node in node_list:
                        status_file.write(node +" "+ "project_pool "+str(initialization_time) +"\n")
#Get the project for node
def get_project_for_node():
        project_for_node = urlparse.urljoin(haas_url,'/node/'+'cisco-03')
        #print project_for_node
        project_for_node = urllib2.urlopen(project_for_node).read()
        print project_for_node



#Checks for free pool in the list and returns the list
def get_free_node_list():
        haas_url = 'http://127.0.0.1/'
        free_node_list =  urlparse.urljoin(haas_url,'free_nodes')
        free_node_list = urllib2.urlopen(free_node_list).read()
        return free_node_list


#For checking purpose
if __name__ == "__main__":
        #release_nodes(['cisco-03'])
        #initialize_file(['cisco-03','cisco-04','cisco-05'])
        #get_current_nodes_status()
        get_project_for_node


