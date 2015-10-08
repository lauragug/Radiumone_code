# Import number of users per sites and shared users as from spark notebook
# build similarity matrix
# run spectral clustering
# write to file result of the clustering and silhouette coefficients

import sys
import string
import numpy as np
import math
from sklearn import cluster
from sklearn import metrics

def build_matrix(n_sites):

	input_file = open('siteids_n_users_10M_50000_150.txt', 'r')
	input_file1 = open('siteids_shared_users_10M_50000_150.txt', 'r')
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
    
def run_clutering(n_sites,order_dict,sim_mat):

   	n_clusters = 6
   	name_file = 'clustering_sil' + str(n_clusters)
   	output_file = open(name_file,'w')
   	name_file1 = 'clustering_labels' + str(n_clusters)
   	output_file1 = open(name_file1,'w')
   	
   	spectral = cluster.SpectralClustering(n_clusters=n_clusters, \
   			eigen_solver='arpack',affinity='precomputed')
   	labels = spectral.fit_predict(sim_mat)
   	
   	silhouette_avg = metrics.silhouette_score(sim_mat,labels)
   	output_file.write(" ".join(["aver silhouette_score:",str(silhouette_avg)]))

    # Compute the silhouette scores for each sample
   	sample_silhouette_values = metrics.silhouette_samples(sim_mat, labels)
   	
   	for siteid in order_dict:
   		stringa = ' '.join(                                       \
			[siteid,
        	str(sample_silhouette_values[order_dict[siteid]])])
   		output_file.write(stringa +'\n')
   	
   	for siteid in order_dict:
   		stringa = ' '.join(                                       \
			[str(siteid),str(labels[order_dict[siteid]])
        	])
   		output_file1.write(stringa +'\n')
		
def main():

	n_sites = 5574
	order_dict,sim_mat = build_matrix(n_sites)
	run_clutering(n_sites,order_dict,sim_mat)

if __name__ == '__main__':
  main()