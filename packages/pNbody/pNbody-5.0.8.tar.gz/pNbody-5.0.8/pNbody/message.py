#!/usr/bin/env python3
###########################################################################################
#  package:   pNbody
#  file:      message.py
#  brief:     Defines the message class
#  copyright: GPLv3
#             Copyright (C) 2019 EPFL (Ecole Polytechnique Federale de Lausanne)
#             LASTRO - Laboratory of Astrophysics of EPFL
#  author:    Yves Revaz <yves.revaz@epfl.ch>
#
# This file is part of pNbody.
###########################################################################################

import inspect
import sys
    
bc = {}
bc["p"] = '\033[95m' # PINK  
bc["b"] = '\033[94m' # BLUE  
bc["g"] = '\033[92m' # GREEN 
bc["y"] = '\033[93m' # YELLOW
bc["r"] = '\033[91m' # RED   
bc["k"] = '\033[0m'  # BLACK   
bc["c"] = '\033[0;36m' # CYAN 

    
def message(msg,verbose=0,verbosity=1,level=0,isMaster=True,color=None):
  
  
  
  if verbosity > verbose:
    return
  
  if isMaster:
  
    frame = inspect.stack()[level]
    
    txt = str(msg)
    
    if verbose >= 4:
      txt = '%s ("%s", line %d): %s'%(frame.function,frame.filename,frame.lineno,msg)
    else:
      txt = "%s: %s"%(frame.function,msg)
    
    
    # add color
    if color is not None:
      txt = bc[color] + txt + bc["k"]
    
    # print the text
    print(txt)
    
    
    
def todo_warning(verbose=1,color='c'):
    """
    Print a short warning and traceback for empty functions.

    Parameters:
    -----------

    verb: verbosity level as defied in class Nbody() in main.py
    """
    import traceback

    if verbose == 0:
        return

    else:
        print(bc[color] + "================================================================================="+ bc["k"])
        print(bc[color] + "TODO WARNING: A function that has not been fully written has been called."+ bc["k"])
        print(bc[color] + "TODO WARNING: This is most likely no reason to worry, but hopefully this message "+ bc["k"])
        print(bc[color] + "TODO WARNING: will annoy the developers enough to start clean their code up."+ bc["k"])
        print(bc[color] + "TODO WARNING: Meanwhile, you can just carry on doing whatever you were up to."+ bc["k"])

        if verbose > 1:
            print(bc[color] + "TODO WARNING: Printing traceback:"+ bc["k"])

            st = traceback.extract_stack()
            reduced_stack = st[:-1]  # skip call to traceback.extract_stack() in stack trace
            traceback.print_list(reduced_stack)

            print(bc[color] + "TODO WARNING: End of (harmless) warning."+ bc["k"])
        
        print(bc[color] + "================================================================================="+ bc["k"])
        
    return
  
  
    
    
    
    
    



