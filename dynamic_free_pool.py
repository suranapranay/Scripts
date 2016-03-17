#! /bin/python
import urlparse
import requests
from sets import Set
import json
import time

#Release nodes : Takes node list as arguments and puts them back to free pool 
#	         after given time				
def release_nodes(non_persistent_list,threshold_time):  
	free_node_list = get_free_node_list()
	#Only these nodes should be updated in the file(either for project or for time)
	nodes_to_update_infile = list(Set(non_persistent_list)-Set(free_node_list))
	for node in nodes_to_update_infile:
		#get the information from status file for node.
		node_info_from_file = get_project_and_time_for_node(node)
		project_in_file = node_info_from_file[0]
		old_time = node_info_from_file[1]
		#get the information from HaaS for node
		node_current_info =  get_node_current_info(node)
		project_in_haas = node_current_info[0]
		networks = node_current_info[1]
		nic = node_current_info[2]
		#Increase the time by one unit
		new_time = int(node_info_from_file[1])+1
		#See if the node is in the same project and if it is outside 
		#free pool for time less than threshold value then update only 
		#time in status file
	        if compare_projects(project_in_file, project_in_haas) \
					and canLive(new_time, threshold_time):
			update_time_for_node(node, project_in_file, new_time)
		#See if the node is in the same project and if it is outside
		#free pool for time greater than threshold value then release
		#the node back to free pool
		elif  compare_projects(project_in_file, project_in_haas)\
					and not canLive(new_time, threshold_time):
		  	#Detaching nodes from networks
			detach_networks_from_node(node, networks,\
						 nic)		
			#Releasing node from project.
			release_from_project(node, project_in_haas) 
		#See if the node is not in free pool and check if the projects
		#are not matching then we need to update project in status file
		elif not compare_projects(project_in_file, project_in_haas) \
			and project_in_haas != None:
			update_project_in_status_file(node, project_in_haas,\
							project_in_file)
				
		#else:
			#Need to write a function which actually brings down 
			#the nodes if they are in free pool.
			#Power save mode on :)	

#Boolean Function to check if the projects are same 
def compare_projects(project_in_file,project_in_haas):
	if project_in_file == project_in_haas:
		return True
	else:
		return False		  

#Boolean Function to check if node can live in the same project.
def canLive(time, threshold_time):
	if time < threshold_time:
		return True
	else:
		return False

#Reads current information from file for every node
def get_project_and_time_for_node(node):
	with open('/home/ravig/status_file.txt','r') as status_file:
		for line in status_file:
			if node in line:
				node_status = line.split()
				node_project = node_status[1]
				print node_project
				node_duration = node_status[2]
	return (node_project,node_duration)	

#Updates the time for a node in file
def update_time_for_node(node,old_time,new_time):
	lines = []
	with open('/home/ravig/status_file.txt','r') as status_file:
                for line in status_file:
                        if node in line:
				line = line.replace(old_time,str(new_time))
			lines.append(line)	
	with open('/home/ravig/status_file.txt','w') as status_file:		
		for line in lines:
			status_file.write(line)


#Project will be changed in file to match the project in HaaS.
def update_project_in_status_file(node, new_project, old_project):
	lines = []
        with open('/home/ravig/status_file.txt','r') as status_file:
                for line in status_file:
                        if node in line:
                                line = line.replace(old_project, new_project)
                        lines.append(line)
        with open('/home/ravig/status_file.txt','w') as status_file:
                for line in lines:
                        status_file.write(line)

#Queries current status from HaaS for a node.
def get_node_current_info(node):
	'''
	Checks the current information for the node and returns a tuple consisting of (<project_name>,List of <{"network": network-name}>, NIC name)
	'''
	url = "http://127.0.0.1/node/" + node
	resp = requests.get(url)
	node_info = resp.json()
	node_project = node_info['project']
	data = node_info['nics'][0]['networks']
	node_nic = node_info['nics'][0]['label']
	networks = [{"network":v} for k,v in data.items() if k.startswith('vlan')]
	return (node_project, networks, node_nic)	

#Detach networks from nodes.
def detach_networks_from_node(node, networks, node_nic):
	'''Takes a node ,list of {network, "network-name"}- networks attached to it, nic on which network is attached and detaches all the networks
	'''
	url = "http://127.0.0.1/node/" + node + "/nic/" + node_nic + "/detach_network"
	for network in networks:
		res = requests.post(url, json.dumps(network))
	return	


#Updates the file with project name as free and releases it back to free pool
def release_from_project(node,project):	
	lines = []
        with open('/home/ravig/status_file.txt','r') as status_file:
                for line in status_file:
                        if node in line:
                                line = node +" "+ "free_pool "+str(0) +"\n"
                        lines.append(line)
	with open('/home/ravig/status_file.txt','w') as status_file:
                for line in lines:
                        status_file.write(line)
	time.sleep(5)
	response = release_node_from_project(node, project)
	print response 
	return	
		
#Release a node from a project. 
def release_node_from_project(node, project):
	print "In release node"	
	haas_url = "http://127.0.0.1" + '/project/' + project + '/detach_node'
	print haas_url
	body = {
		"node" : node
	       }
	r = requests.post(haas_url, data = json.dumps(body))
	return r
	
#Checks for free pool in the list and returns the list
def get_free_node_list():	
	haas_url = 'http://127.0.0.1/'
	free_node_list =  urlparse.urljoin(haas_url,'free_nodes')
	#free_node_list = urllib2.urlopen(free_node_list).read()
	free_node_list = requests.get(free_node_list)
	print free_node_list.json()
	#return free_node_list


#For checking purpose
if __name__ == "__main__":
	release_nodes(['cisco-08', 'cisco-07','cisco-10'],1)
	
