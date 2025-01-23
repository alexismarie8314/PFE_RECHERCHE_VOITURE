Pour chaque simulation, nous avons utilisé les paramètres suivants:

- `random_perturbation`: False dans le cas général, True pour les simulations avec le nom "_random".
- `number_of_experiments`: Variable en fonction de la taille de la ville.
- `number_of_paths`: Variable en fonction de la taille de la ville.
- `weight_of_perturbation`: 60.
- `minimum_length`: 30.
- `radius` pour S3 fixé à 300 mètres sauf pour les simulations avec le nom "_with_radius" où il est variable.

Les analyses de résultats sont disponibles dans le fichier "analyse.xlsx". 

Les résultats bruts sont disponibles dans le fichier "simulations.csv".

Les informations concernant les villes sont disponibles dans le fichier "graph_info.csv".

Les informations concernant l'analyse du voisinage de chaque noeuds sont disponibles dans le fichier "neighbourhood.csv".