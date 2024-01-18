    # # Récupérer la valeur "maxspeed" s'il y en a une
    # maxspeed = way.find(".//tag[@k='maxspeed']")
    # if maxspeed is not None:
    #     maxspeed_value = maxspeed.get('v')
    #     # Associer la valeur "maxspeed" à chaque arête
    #     for edge in zip(nodes[:-1], nodes[1:]):
    #         maxspeed_dict[edge] = maxspeed_value