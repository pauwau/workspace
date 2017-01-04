# -*- coding: utf-8 -*-

from sklearn import cluster,datasets
iris = datasets.load_iris()
k_means = cluster.KMeans(n_clusters=3)
k_means.fit(iris.data)