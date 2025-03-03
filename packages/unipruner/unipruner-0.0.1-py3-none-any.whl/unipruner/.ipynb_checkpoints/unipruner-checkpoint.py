import os

import cobra



def check_inputs(logger, universe, eggnog):
    
    
    # check if files exist
    if os.path.isfile(universe) == False: 
        logger.error(f"Provided --universe doesn't exist: {universe}.")
        return 1
    if os.path.isfile(eggnog) == False: 
        logger.error(f"Provided --eggnog doesn't exist: {eggnog}.")
        return 1
    
    
    # check the universe model format
    if universe.endswith('.json'):
        universe = cobra.io.load_json_model(universe)
    elif universe.endswith('.xml'):
        universe = cobra.io.read_sbml_model(universe)
    else: 
        logger.error(f"Provided --eggnog has unrecongnized format: {eggnog}. Allowed formats are JSON (.json) and SBML (.xml).")
        return 1
    
    
    # log main universe metrics:
    G = len([g.id for g in universe.genes])
    R = len([r.id for r in universe.reactions])
    M = len([m.id for m in universe.metabolites])
    uM = len(set([m.id.rsplit('_', 1)[0] for m in universe.metabolites]))
    bP = len([m.id for m in universe.reactions.get_by_id('Biomass').reactants])
    logger.info(f"Provided universe: [G: {G}, R: {R}, M: {M}, uM: {uM}, bP: {bP}, Biomass: {round(universe.slim_optimize(), 3)}]")
        
        
    # load eggnog annotations
    eggnog = pnd.read_csv(eggnog, index_col=0)
    
    return [universe, eggnog]
    


def unipruner(args, logger): 
    
    
    
    # check input files:
    response = check_inputs(logger, args.universe, args.eggnog)
    if type(response)==int:
        return 1
    universe = response[0]
    eggnog = response[1]
    
    
    return 0