#! /bin/python
import urlparse
import requests
from sets import Set
import json

#Global variables to be used
haas_url = 'http://127.0.0.1/'

#Release nodes : Takes node list as arguments and puts them back to free pool 
#	         after given time				
def release_nodes(non_persistent_list,threshold_time):  
	free_node_list = get_free_node_list()
	#print free_node_list
	#Only these nodes should be updated in the file(either for project or for time)
	nodes_to_update_infile = list(Set(non_persistent_list)-Set(free_node_list))
	for node in nodes_to_update_infile:
		node_updates = get_project_and_time_for_node(node)
		new_time = int(node_updates[1])+1
	        if node_updates[0] == 'bmi_infra' and new_time < threshold_time:
			#print int(node_updates[1])
			update_time_for_node(node,node_updates[1],new_time)
		elif node_updates[0] == 'bmi_infra' and new_time >= threshold_time:
			release_from_project(node) #Need to add project as argument
		#elif node_updates[0] != 'bmi_infra' and new_time < threshold:
		#	update_project_
			
			 
		#check_and_update_time_threshold(node,threshold)
		#check_for_project_change()
	#update_node_duration_outside_pool(non_persistent_list,free_node_list,threshold_time)  

#Reads current information from file for every node
def get_project_and_time_for_node(node):
	with open('status_file.txt','r') as status_file:
		for line in status_file:
			if node in line:
				node_status = line.split()
				node_project = node_status[1]
				node_duration = node_status[2]
	return (node_project,node_duration)	
#Updates the time for a node in file

def update_time_for_node(node,old_time,new_time):
	lines = []
	with open('status_file.txt','r') as status_file:
                for line in status_file:
                        if node in line:
				line = line.replace(old_time,str(new_time))
			lines.append(line)	
	with open('status_file.txt','w') as status_file:		
		for line in lines:
			status_file.write(line)

#Updates the file with project name as free and releases it back to free pool
def release_from_project(node):	
	lines = []
        with open('status_file.txt','r') as status_file:
                for line in status_file:
                        if node in line:
                                line = node +" "+ "free_pool "+str(0) +"\n"
                        lines.append(line)
	with open('status_file.txt','w') as status_file:
                for line in lines:
                        status_file.write(line)
	release_node_from_project(node)	
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

#Get the project for node. Should take node as argument
def get_project_for_node():
	project_for_node = urlparse.urljoin(haas_url,'/node/'+'cisco-03')
	#print project_for_node
	project_for_node = urllib2.urlopen(project_for_node).read()
	print project_for_node
		
#Release a node from a project. 
def release_node_from_project(node):
	haas_url = "http://127.0.0.1"
	node_to_detach = urlparse.urljoin(haas_url,'/project/'+'bmi_infra'+'/detach_node')
	print node_to_detach
	body = {
		"node" : node
	       }
	r = requests.post(node_to_detach, data = json.dumps(body))
	
	

#Checks for free pool in the list and returns the list
def get_free_node_list():	
	haas_url = 'http://127.0.0.1/'
	free_node_list =  urlparse.urljoin(haas_url,'free_nodes')
	#free_node_list = urllib2.urlopen(free_node_list).read()
	free_node_list = requests.get(free_node_list)
	#print free_node_list.json()
	return free_node_list


#For checking purpose
if __name__ == "__main__":
	release_nodes(['cisco-03','cisco-36'],60)
	#release_node_from_project('cisco-03')
	#initialize_file(['cisco-03','cisco-04','cisco-05'])
	#get_current_nodes_status()
	#get_free_node_list()
	#get_project_for_node()

