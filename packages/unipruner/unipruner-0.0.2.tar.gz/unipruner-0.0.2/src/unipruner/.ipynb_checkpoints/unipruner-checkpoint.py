import os

import pandas as pnd
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



def parse_eggnog(eggnog):
    
    
    # PART 1. get KO codes available
    gid_to_kos = {}
    ko_to_gids = {}
    for gid, kos in eggnog['KEGG_ko'].items():
        if kos == '-': 
            continue
            
        if gid not in gid_to_kos.keys(): 
            gid_to_kos[gid] = set()
            
        kos = kos.split(',')
        kos = [i.replace('ko:', '') for i in kos]
        for ko in kos: 
            if ko not in ko_to_gids.keys(): 
                ko_to_gids[ko] = set()
                
            # populate dictionaries
            ko_to_gids[ko].add(gid)
            gid_to_kos[gid].add(ko)

    
    return ko_to_gids, gid_to_kos



def subtract_kos(model, ko_to_gids):
    
    
    modeled_kos = [g.id for g in model.genes]  
    to_remove = []  # genes to delete
    
    for ko in modeled_kos: 
        
        if ko not in ko_to_gids.keys():
            to_remove.append(model.genes.get_by_id(ko))
    
    
    # delete marked genes
    cobra.manipulation.delete.remove_genes(model, to_remove, remove_reactions=True)
    
    
    return 0



def translate_remaining_kos(model, ko_to_gids):
    
    
    modeled_kos = [g.id for g in model.genes]  
    
    
    # iterate reactions:
    for r in model.reactions:

        gpr = r.gene_reaction_rule

        # force each gid to be surrounded by spaces: 
        gpr = ' ' + gpr.replace('(', ' ( ').replace(')', ' ) ') + ' '
        
        for ko in ko_to_gids.keys():

            # search this gid surrounded by spaces:
            if f' {ko} ' in gpr:
                gpr = gpr.replace(f' {ko} ', f' ({" or ".join(ko_to_gids[ko])}) ')


        # remove spaces between parenthesis
        gpr = gpr.replace(' ( ', '(').replace(' ) ', ')')
        # remove spaces at the extremes: 
        gpr = gpr[1: -1]


        # New genes are introduced. Parethesis at the extremes are removed if not necessary. 
        r.gene_reaction_rule = gpr
        r.update_genes_from_gpr()
            
            
    # remaining old 'Cluster_'s need to removed.
    # remove if (1) hte ID starts with clusters AND (2) they are no more associated with any reaction
    to_remove = [g for g in model.genes if (g.id in modeled_kos and len(g.reactions)==0)]
    cobra.manipulation.delete.remove_genes(model, to_remove, remove_reactions=True)
    
        
    return 0
    


def unipruner(args, logger): 
    
    
    
    # check input files:
    response = check_inputs(logger, args.universe, args.eggnog)
    if type(response)==int:
        return 1
    universe = response[0]
    eggnog = response[1]
    
    
    # get important dictionaries: 'ko_to_gids' and 'gid_to_kos'
    ko_to_gids, gid_to_kos = parse_eggnog(eggnog)
    
    # make a copy
    model = universe.copy()
    
    # substract missing KOs
    print(len(model.genes),  len(model.reactions), [g.id for g in model.genes[:5]])
    subtract_kos(model, ko_to_gids)
    print(len(model.genes),  len(model.reactions), [g.id for g in model.genes[:5]])
    translate_remaining_kos(model, ko_to_gids)
    print(len(model.genes),  len(model.reactions), [g.id for g in model.genes[:5]])
    
    return 0