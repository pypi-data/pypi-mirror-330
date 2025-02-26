
# Programado por Freddy Alvarado - 2022/03/01
# freddy.alvarado.b1@gmail.com
#------------------------------------------------------------

def mKOptimoMCodo(distortions):
  import numpy as np
  first_point = (0, distortions[0])
  last_point = (len(distortions) - 1, distortions[-1])
  m = (last_point[1] - first_point[1]) / (last_point[0] - first_point[0])
  intercept = first_point[1] - m * first_point[0]
  distances = []
  for i in range(len(distortions)):
    point = (i, distortions[i])
    distance = abs(m * point[0] + intercept - point[1]) / np.sqrt(m ** 2 + 1)
    distances.append(distance)
  max_distance_index = np.argmax(distances)

  return max_distance_index + 1

def mKOptimoMSilouette(X):
  from sklearn.metrics import silhouette_score
  from sklearn.cluster import AgglomerativeClustering

  s = []
  for n_clusters in range(2,20):
    hc = AgglomerativeClustering(n_clusters = n_clusters, 
                                affinity = 'euclidean', 
                                linkage = 'ward')
    s.append(silhouette_score(X,
                                hc.fit_predict(X))) 
  valor_maximo = max(s)
  indice_maximo = s.index(valor_maximo) + 2
  return indice_maximo