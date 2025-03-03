import argparse
import sys
import multiprocessing 
import logging 
from logging.handlers import QueueHandler
from datetime import datetime
import importlib.metadata



import cobra


from .unipruner import unipruner


cobra_config = cobra.Configuration()
solver_name = str(cobra_config.solver.log).split(' ')[1]
solver_name = solver_name.replace("optlang.", '')
solver_name = solver_name.replace("_interface", '')



def main(): 
    
    
    # define the header of main- and sub-commands. 
    header = f'unipruner v{importlib.metadata.metadata("unipruner")["Version"]}'
    
    
    # create the command line arguments:
    parser = argparse.ArgumentParser(description=header, add_help=False)
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument("-v", "--version", action="version", version=f"v{importlib.metadata.metadata('unipruner')['Version']}", help="Show version number and exit.")
    
    
    #parser.add_argument("-c", "--cores", metavar='', type=int, default=1, help="How many parallel processes to use.")
    #parser.add_argument("-o", "--outdir", metavar='', type=str, default='./', help="Main output directory (will be created if not existing).")
    parser.add_argument("--verbose", action='store_true', help="Make stdout messages more verbose, including debug messages.")
    parser.add_argument("-e", "--eggnog", metavar='', type=str, default='-', help="Path to the eggnog-mapper annotation table.")
    parser.add_argument("-u", "--universe", metavar='', type=str, default='-', help="Path to the universe model.")
    

    # check the inputted subcommand, automatic sys.exit(1) if a bad subprogram was specied. 
    args = parser.parse_args()
    
    
    # set the multiprocessing context
    multiprocessing.set_start_method('fork') 
    
    
    # create a logging queue in a dedicated process.
    def logger_process_target(queue):
        logger = logging.getLogger('unipruner')
        while True:
            message = queue.get() # block until a new message arrives
            if message is None: # sentinel message to exit the loop
                break
            logger.handle(message)
    queue = multiprocessing.Queue()
    logger_process = multiprocessing.Process(target=logger_process_target, args=(queue,))
    logger_process.start()
    
    
    # connect the logger for this (main) process: 
    logger = logging.getLogger('unipruner')
    logger.addHandler(QueueHandler(queue))
    if args.verbose: logger.setLevel(logging.DEBUG) # debug (lvl 10) and up
    else: logger.setLevel(logging.INFO) # debug (lvl 20) and up
    
    
    # handy function to print without time/level (for header / trailer)
    def set_header_trailer_formatter(logger):
        formatter = logging.Formatter('%(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return handler
    
    
    # to print the main pipeline logging:
    def set_usual_formatter(logger):
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt="%H:%M:%S")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return handler
    
    
    
    # show a welcome message:
    thf_handler = set_header_trailer_formatter(logger)
    logger.info(header + '\n')
    command_line = 'unipruner ' # print the full command line:
    for arg, value in vars(args).items():
        command_line = command_line + f"--{arg} {value} "
    logger.info('Inputted command line: "' + command_line.rstrip() + '".\n')
    logger.removeHandler(thf_handler)
    
    
    
    usual_handler = set_usual_formatter(logger)
    current_date_time = datetime.now()
    formatted_date = current_date_time.strftime("%Y-%m-%d")
    logger.info(f"Welcome to unipruner! Launching the tool on {formatted_date}...")
    logger.debug(f'COBRApy started with solver: {solver_name}.')
    try: 
        response = unipruner(args, logger)
            
        if response == 0:
            logger.info("unipruner terminated without errors!")
    except: 
        # show the error stack trace for this un-handled error: 
        response = 1
        logger.error(traceback.format_exc())
    logger.removeHandler(usual_handler)


    
    # Terminate the program:
    thf_handler = set_header_trailer_formatter(logger)
    if response == 1: 
        queue.put(None) # send the sentinel message
        logger_process.join() # wait for all logs to be digested
        sys.exit(1)
    else: 
        # show a bye message
        queue.put(None) # send the sentinel message
        logger_process.join() # wait for all logs to be digested
        logger.info('\n' + header)
        sys.exit(0) # exit without errors
        
        
        
if __name__ == "__main__":
    main()