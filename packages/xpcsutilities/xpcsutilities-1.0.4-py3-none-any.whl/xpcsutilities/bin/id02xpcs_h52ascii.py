# -*- coding: utf-8 -*-


from xpcsutilities.tools.result_file import XPCSResultFile
import logging, os

logger = logging.getLogger(__name__)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Display XPCS result files")
    
    parser.add_argument('-v', dest='verbose', action='store_true', default=False, help='Verbose mode (minimum message level=debug)')
    parser.add_argument('--quiet', dest='quiet', action='store_true', default=False, help='Quiet mode (minimum message level=warning)')
    parser.add_argument('-f', dest='force', action='store_true', default=False, help='Allow erasing previous existing output file')
    parser.add_argument('-S', dest='skip', action='store_true', default=False, help='Skip if output file is already existing')
    parser.add_argument('data_file', action='append', nargs='+', help='Data files')
    
    args = parser.parse_args()
            
    # Set the log level of each package according to the defined verbosity
    loglevel = logging.INFO
    
    if args.verbose:
        loglevel = logging.DEBUG
    elif args.quiet:
        loglevel = logging.WARNING
        
    for name in logging.root.manager.loggerDict:
        if name.startswith('xpcsutilities'):
            logging.getLogger(name).setLevel(loglevel)
            
    for f in args.data_file[0]:
        
        if not f.endswith('h5'):
            continue
        
        outf = '.'.join(f.split('.')[:-1])+'.txt'
        
        if args.skip and os.path.isfile(outf):
            logger.info(f"Skipping {f}")
            continue
        
        try:
            logger.info(f"Processing {f}")
            fd = XPCSResultFile(f)            
            
            fd.save_toAscii(outf, args.force)
                
        except Exception as e:
            logger.fatal(f"Problem with {f} : {e}")
