# Import number of users per sites and shared users as from spark notebook
# build similarity matrix
# computer principal components using Incremental PCA
# print to file principal components
# print to file binned values to be used by logistic regression

import sys
import string
import numpy as np
import math
from sklearn.decomposition import PCA, IncrementalPCA

def build_matrix(n_sites):

	input_file = open('siteids_n_users_50M_100000_100.txt', 'r')
	input_file1 = open('siteids_shared_users_50M_100000_100.txt', 'r')
	output_file = open('error_file','w')
	
	n_points = n_sites*(n_sites-1)
	sim_mat=np.eye(n_sites)
	mod_dict = {}
	order_dict = {}
	table = string.maketrans("","")
	
	i = 0
	for line in input_file:
		words = line.translate(table, string.punctuation).split()
		for word in words:
			siteid = words[0].lstrip('u')
			n_users = int(words[1])
			if siteid not in mod_dict: 
				mod_dict[siteid] = math.sqrt(float(n_users))
				order_dict[siteid] = i
				i += 1
    # compute similarity matrix
	for line in input_file1:
		words = line.translate(table, string.punctuation).split()
		for word in words:
			siteid1 = words[0].lstrip('u')
			siteid2 = words[1].lstrip('u')
			shared_users = int(words[2])
			if siteid1 in mod_dict and siteid2 in mod_dict: 
				sim_mat[order_dict[siteid1]][order_dict[siteid2]] = \
            		shared_users/mod_dict[siteid1]/mod_dict[siteid1]
			else:
				output_file.write(",".join([siteid1,siteid2])+'\n')
    
	input_file.close()
	input_file1.close()
	output_file.close()
	return order_dict,sim_mat
    
def run_pca(n_components,n_sites,order_dict,sim_mat):
   
   	output_file = open('pca_100000_100','w')
   	
        ipca = IncrementalPCA(n_components=n_components,batch_size=8000)
	sim_mat_ipca = ipca.fit_transform(sim_mat)
	var_sim_ipca = ipca.explained_variance_ratio_
	
	output_file.write(",".join(str(x) for x in var_sim_ipca)+'\n')

	for siteid in order_dict:
		stringa = ' '.join(
			[siteid,
        	str(sim_mat_ipca[order_dict[siteid], 0]),
        	str(sim_mat_ipca[order_dict[siteid], 1]),
         	str(sim_mat_ipca[order_dict[siteid], 2]),
         	str(sim_mat_ipca[order_dict[siteid], 3]),
         	str(sim_mat_ipca[order_dict[siteid], 4]),
         	str(sim_mat_ipca[order_dict[siteid], 5]),
         	str(sim_mat_ipca[order_dict[siteid], 6])
        	])
		output_file.write(stringa +'\n')
    	
	n_bins = 1000.
	binned = np.empty((n_sites,5)).astype(np.int32)
	for k in range(5):
		delta = (sim_mat_ipca[:, k].max()-sim_mat_ipca[:, k].min())/n_bins
		min_k = sim_mat_ipca[:, k].min()
		for i in range(n_sites):
			binned[i,k] = int((sim_mat_ipca[i, k]-min_k)/delta)
        	
	f = open('pc_100000_100.csv','w')
	for siteid in order_dict:
		stringa = ' '.join(
			[siteid,
        	str(binned[order_dict[siteid], 0]),
        	str(binned[order_dict[siteid], 1]),
         	str(binned[order_dict[siteid], 2]),
         	str(binned[order_dict[siteid], 3]),
         	str(binned[order_dict[siteid], 4])    
        	])
    	f.write(stringa +'\n')
	f.close()
		
def main():

	n_sites = 14149
	n_components = 7
	order_dict,sim_mat = build_matrix(n_sites)
	run_pca(n_components,n_sites,order_dict,sim_mat)
            	
if __name__ == '__main__':
  main()
