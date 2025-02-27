###########################################################################################
#  package:   pNbody
#  file:      swift.py
#  brief:     SWIFT file format
#  copyright: GPLv3
#             Copyright (C) 2019 EPFL (Ecole Polytechnique Federale de Lausanne)
#             LASTRO - Laboratory of Astrophysics of EPFL
#  author:    Yves Revaz <yves.revaz@epfl.ch>, Loic Hausammann <loic_hausammann@hotmail.com>
#
# This file is part of pNbody.
###########################################################################################


##########################################################################
#
# GEAR HDF5 CLASS
#
##########################################################################

import numpy as np
import h5py

import pNbody
from pNbody import h5utils
from pNbody import mpi, error, units, h5utils

try:				# all this is useful to read files
    from mpi4py import MPI
except BaseException:
    MPI = None



class Nbody_swift:
  
  
    def get_default_arrays_props(self):
      '''
      get the default properties of arrays considered
      This function is basically used to initialize self.arrays_props
      
      "h5name"  :     name in the hdf5 file
      "dtype"   :     numpy dtype                       
      "dim"     :     dimention 
      "ptypes"  :     type of particles that store this property (useless for the moment)
      "read"    :     read it by default or not
      "write"   :     write it by default or not
      "default" :     default values of the components
      "loaded"  :     is the array currently loaded    
      
      # position must always be first, this is a convention
      '''
      
      all_ptypes = list(range(self.get_mxntpe()))
      
      aprops = {}
      
      aprops["pos"] =  {
                        "h5name"  :     "Coordinates", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     3, 
                        "ptypes"  :     all_ptypes,
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["vel"] =  {
                        "h5name"  :     "Velocities", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     3,
                        "ptypes"  :     all_ptypes, 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }
                      
      aprops["mass"] =  {
                        "h5name"  :     "Masses", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     all_ptypes, 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     1,
                        "loaded"  :     False
                      }

      aprops["num"] =  {
                        "h5name"  :     "ParticleIDs", 
                        "dtype"   :     np.uint32,                        
                        "dim"     :     1,
                        "ptypes"  :     all_ptypes, 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }
                          
      aprops["pot"] =  {
                        "h5name"  :     "Potentials", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     all_ptypes, 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["acc"] =  {
                        "h5name"  :     "Acceleration", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     3,
                        "ptypes"  :     all_ptypes, 
                        "read"    :     False,
                        "write"   :     False, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["rsp"] =  {
                        "h5name"  :     "SmoothingLengths", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0,4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["rsp_init"] =  {
                        "h5name"  :     "SmoothingLength", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0,4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }


      aprops["u"] =  {
                        "h5name"  :     "InternalEnergies", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["u_init"] =  {
                        "h5name"  :     "InternalEnergy", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["rho"] =  {
                        "h5name"  :     "Densities", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }
                      


      aprops["metals"] =  {
                        "h5name"  :     "MetalMassFractions", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0,4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }


      aprops["snii_thermal_time"] =  {
                        "h5name"  :     "SNII_ThermalTime", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["snia_thermal_time"] =  {
                        "h5name"  :     "SNIa_ThermalTime", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }


      aprops["softening"] =  {
                        "h5name"  :     "Softenings", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [1,2], 
                        "read"    :     False,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["minit"] =  {
                        "h5name"  :     "BirthMasses", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["tstar"] =  {
                        "h5name"  :     "BirthScaleFactors", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["tstar_init"] =  {
                        "h5name"  :     "BirthTime",         # non cosmological runs
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["birth_time"] =  {
                        "h5name"  :     "BirthTimes",         # non cosmological runs
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }
                      


      aprops["rhostar"] =  {
                        "h5name"  :     "BirthDensities", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }



      aprops["sp_type"] =  {
                        "h5name"  :     "StellarParticleType", 
                        "dtype"   :     np.int32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }


      aprops["idp"] =  {
                        "h5name"  :     "ProgenitorIDs", 
                        "dtype"   :     np.uint32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }




      aprops["nsinkswallowed"] =  {
                        "h5name"  :     "NumberOfSinkSwallows", 
                        "dtype"   :     np.uint32,                        
                        "dim"     :     1,
                        "ptypes"  :     [3], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["ngasswallowed"] =  {
                        "h5name"  :     "NumberOfGasSwallows", 
                        "dtype"   :     np.uint32,                        
                        "dim"     :     1,
                        "ptypes"  :     [3], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["age"] =  {
                        "h5name"  :     "StellarAge", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }
                      
      aprops["mh"] =  {
                        "h5name"  :     "StellarMetallicity", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["XHI"] =  {                                      # HI mass fraction
                        "h5name"  :     "HI", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["XHII"] =  {
                        "h5name"  :     "HII", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["XHeI"] =  {
                        "h5name"  :     "HeI", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["XHeII"] =  {
                        "h5name"  :     "HeII", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["XHeIII"] =  {
                        "h5name"  :     "HeIII", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }                      

      aprops["XH2I"] =  {
                        "h5name"  :     "H2I", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }                                            

      aprops["XH2II"] =  {
                        "h5name"  :     "H2II", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

      aprops["XHM"] =  {
                        "h5name"  :     "HM", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }
                      
                      
      aprops["XDI"] =  {
                        "h5name"  :     "DI", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }    
                      
      aprops["XDII"] =  {
                        "h5name"  :     "DII", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }                      

      aprops["XHDI"] =  {
                        "h5name"  :     "HDI", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }                       
                                        

      aprops["Xe"] =  {                                    # free electron mass fraction
                        "h5name"  :     "e", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }

                                            
      aprops["MagVIS"] =  {
                        "h5name"  :     "MagVIS", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }


      aprops["MagY"] =  {
                        "h5name"  :     "MagY", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }
                      
      aprops["MagJ"] =  {
                        "h5name"  :     "MagJ", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }            
                      
      aprops["Magg"] =  {
                        "h5name"  :     "Magg", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }                                  
                                
      aprops["Magr"] =  {
                        "h5name"  :     "Magr", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }     

      aprops["Magi"] =  {
                        "h5name"  :     "Magi", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     1,
                        "ptypes"  :     [4], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }                          

      aprops["IonMassFractions"] =  {
                        "h5name"  :     "IonMassFractions", 
                        "dtype"   :     np.float32,                        
                        "dim"     :     5,
                        "ptypes"  :     [0], 
                        "read"    :     True,
                        "write"   :     True, 
                        "default" :     0,
                        "loaded"  :     False
                      }   

      return aprops  
    
    

    def load(self,name=None,ptypes=None,force=False):
      '''
      The function in charge of loading arrays on demand.
      Here we use the generic hdf5 one.
      '''
      self.loadFromHDF5(name=name,ptypes=ptypes,force=force)

    
    def dump(self,aname=None):
      '''
      The function in charge of duming the array aname 
      to a file on demand.
      '''
      self.dumpToHDF5(aname=aname)
      
 

    def _init_spec(self):
        # create an empty header (in case the user is creating a dataset)
        self._header = []

    def get_excluded_extension(self):
        """ 
        Return a list of file to avoid when extending the default class.
        """
        return []

    def getParticleMatchingDict(self):
        """
        Return a list of file to avoid when extending the default class.
        """
        
        index = {
            'gas':    0,
            'halo':   1,
            'disk':   2,
            'sink':   3,
            'stars':  4,
            'bndry':  2,
            'stars1': 4,
            'halo1':  1}
        
        return index 

    def check_spec_ftype(self):
        self.message("checking swift format...")

        try:

            fd = h5utils.openFile(self.p_name_global[0])    
            
            
            # check if Unit block is missing
            test1 = "Units" not in fd
            # check if the temperature units is missing
            test1 = test1 or "Unit temperature in cgs (U_T)" not in fd["Units"].attrs
            # check if PartType0/Offset is present         
            test2 = "PartType0/Offset" in fd
            # check if the format is found
            header =  fd["Header"].attrs
            test3 = "Format" in fd["Header"].attrs
            
            
            fd.close()
            if test1 or test2 or test3:
                raise error.FormatError("swift")

        except IOError as e:
            self.message("swift not recognized: %s" % e)
            raise error.FormatError("swift")

    def set_pio(self, pio):
        """ Overwrite function
        """
        pNbody.Nbody.set_pio(self, "no")

    def get_read_fcts(self):
        return [self.read_particles]

    def get_write_fcts(self):
        return [self.write_particles]

    def get_mxntpe(self):
        return 6

    def get_header_translation(self):
        """
        Gives a dictionnary containing all the header translation.
        If a new variable is possible in the HDF5 format, only the translation
        is required for the reader/writer.
        As h5py is not supporting dictionnary, they need special care when reading/writing.
        """
        # dict containing all the main header variables (=> easy acces)
        # e.g. self.npart will contain NumPart_ThisFile
        header_var = {}

        # Size variables
        header_var["Header/NumPart_ThisFile"] = "npart"
        header_var["Header/NumPart_Total"] =  "npart_tot"
        header_var["Header/NumPart_Total_HighWord"] = "nallhw"
        header_var["Header/MassTable"] = "massarr"
        header_var["Header/NumFilesPerSnapshot"] = "num_files"
        header_var["Header/BoxSize"] = "boxsize"
        header_var["Header/Flag_Entropy_ICs"] = "flag_entr_ics"

        # Physics
        header_var["Header/Scale-factor"] = "scalefactor"
        header_var["Header/Redshift"] = "redshift"
        header_var["Header/Time"] = "time"
        
        # General Info
        header_var["Header/Command_line"] = "command_line"
        header_var["Header/GitTag"]   = "gittag"
        header_var["Header/UserName"] = "username"
        header_var["Header/Date"]     = "date"
        

        # Cosmology
        #header_var["Cosmology/Omega_b"] = "omegab"
        header_var["Cosmology/Omega_m"] = "omega0"
        header_var["Cosmology/Omega_lambda"] = "omegalambda"
        header_var["Cosmology/h"] = "hubbleparam"
        header_var["Cosmology/Cosmological run"] = "cosmorun"
        


        # Units
        #header_var["Units/Unit velocity in cgs (U_V)"] = "UnitVelocity_in_cm_per_s"
        header_var["Units/Unit length in cgs (U_L)"] = "UnitLength_in_cm"
        header_var["Units/Unit mass in cgs (U_M)"] = "UnitMass_in_g"
        header_var["Units/Unit time in cgs (U_t)"] = "Unit_time_in_cgs"
        header_var["Units/Unit temperature in cgs (U_T)"] = "Unit_temp_in_cgs"
        header_var["Units/Unit current in cgs (U_I)"] = "Unit_current_in_cgs"

        # Code
        header_var["Code/Code"] = "Code"
        header_var["Code/CFLAGS"] = "cflags"
        header_var["Code/Code Version"] = "code_version"
        header_var["Code/Compiler Name"] = "compiler_name"
        header_var["Code/Compiler Version"] = "compiler_version"
        header_var["Code/Configuration options"] = "config_options"
        header_var["Code/FFTW library version"] = "fftw_lib_version"
        header_var["Code/Git Branch"] = "git_branch"
        header_var["Code/Git Date"] = "git_date"
        header_var["Code/Git Revision"] = "git_revision"
        header_var["Code/HDF5 library version"] = "hdf5_lib_version"
        header_var["Code/MPI library"] = "mpi_lib"

        # HydroScheme
        header_var["HydroScheme/Adiabatic index"] = "adiabatic_index"
        header_var["HydroScheme/CFL parameter"] = "cfl_parameter"
        header_var["HydroScheme/Dimension"] = "dimension"
        header_var["HydroScheme/Kernel delta N_ngb"] = "kernel_delta_n_ngb"
        header_var["HydroScheme/Kernel eta"] = "kernel_eta"
        header_var["HydroScheme/Kernel function"] = "kernel_function"
        header_var["HydroScheme/Kernel target N_ngb"] = "kernel_target_n_ngb"
        header_var["HydroScheme/Max ghost iterations"] = "max_ghost_iterations"
        header_var["HydroScheme/Maximal smoothing length"] = "maximal_smoothing_length"
        header_var["HydroScheme/Scheme"] = "scheme"
        header_var["HydroScheme/Smoothing length tolerance"] = "smoothing_length_tolerance"
        header_var["HydroScheme/Thermal Conductivity Model"] = "thermal_conductivity_model"
        header_var["HydroScheme/Viscosity Model"] = "viscosity_model"
        header_var["HydroScheme/Viscosity alpha"] = "viscosity_alpha"
        header_var["HydroScheme/Viscosity beta"] = "viscosity_beta"
        header_var["HydroScheme/Volume log(max(delta h))"] = "volume_log"
        header_var["HydroScheme/Volume max change time-step"] = "volume_max_change"

        # Parameters
        #header_var["Parameters/InitialConditions:shift"] = "InitialConditions_shift"
        header_var["Header/Shift"] = "InitialConditions_shift"



        # Swift directory
        header_var["RuntimePars/PeriodicBoundariesOn"] = "periodic"
        
        
        # chemistry (this is now done elsewhere)
        #header_var["Parameters/GEARFeedback:elements"] = "ChimieElements"
        #header_var["SubgridScheme/Chemistry element count"] = "ChimieNelements"
        
        

        return header_var

    def get_list_header(self):
        """
        Gives a list of header directory from self.get_header_translation
        """
        list_header = []
        trans = self.get_header_translation()
        for key, tmp in list(trans.items()):
            directory = key.split("/")[0]
            if directory not in list_header:
                list_header.append(directory)
        return list_header



    def get_default_spec_vars(self):
        """
        return specific variables default values for the class
        """

        return {'massarr': np.array([0, 0, 0, 0, 0, 0]),
                'atime': 0.,
                'scalefactor': 1.,
                'redshift': 0.,
                'time': 0.,
                'flag_sfr': 0,
                'flag_feedback': 0,
                'npart_tot': np.array([0, 0, self.nbody, 0, 0, 0]),
                'npart': np.array([0, 0, self.nbody, 0, 0, 0]),
                'flag_cooling': 0,
                'num_files': 1,
                'boxsize': 0.,
                'omega0': 0.,
                'omegalambda': 0.,
                'hubbleparam': 0.,
                'flag_age': 0.,
                'flag_metals': 0.,
                'nallhw': np.array([0, 0, 0, 0, 0, 0]),
                'flag_entr_ics': 0,
                'flag_chimie_extraheader': 0,
                'critical_energy_spec': 0.,
                'empty': 48 * '',
                'comovingintegration': True,
                'hubblefactorcorrection': False,
                'comovingtoproperconversion': True,
                'ChimieNelements': 0,
                'utype':"swift",
                'command_line':"none",
                'gittag':"none",
                'date':"none",
                'username':"username",
                }


                  

    def get_massarr_and_nzero(self):
        """
        return massarr and nzero

        !!! when used in //, if only a proc has a star particle,
        !!! nzero is set to 1 for all cpu, while massarr has a length of zero !!!
        """

        if self.has_var('massarr') and self.has_var('nzero'):
          if self.massarr is not None and self.nzero is not None:
            self.message("warning : get_massarr_and_nzero : here we use massarr and nzero",self.massarr,self.nzero,verbosity=2)
            return self.massarr, self.nzero

        massarr = np.zeros(len(self.npart), float)
        nzero = 0

        # for each particle type, see if masses are equal
        for i in range(len(self.npart)):
            first_elt = sum((np.arange(len(self.npart)) < i) * self.npart)
            last_elt = first_elt + self.npart[i]

            if first_elt != last_elt:
                c = (self.mass[first_elt] ==
                     self.mass[first_elt:last_elt]).astype(int)
                if sum(c) == len(c):
                    massarr[i] = self.mass[first_elt]
                else:
                    nzero = nzero + len(c)

        return massarr.tolist(), nzero




    def read_particles(self, f):
        """
        read gadget file
        """
                
        from copy import deepcopy
        import time
                
        # go to the end of the file
        if f is not None:
            f.seek(0, 2)


        fd = h5utils.openFile(self.p_name_global[0],'r')    
            

        ################
        # read header
        ################
        self.message("reading header...")

        # set default values
        default = self.get_default_spec_vars()
        for key, i in list(default.items()):
            setattr(self, key, i)

        # get values from snapshot
        trans = self.get_header_translation()

        list_header = self.get_list_header()
        

        for name in list_header:
            if name not in fd:
                continue
                
            # e.g. create self.npart with the value
            # fd["Header"].attrs["NumPart_ThisFile"]
                        
            for key in fd[name].attrs:
                                                                    
              
                full_name = name + "/" + key
                if full_name not in list(trans.keys()):
                    trans[full_name] = full_name

                tmp = fd[name].attrs[key]
                if isinstance(tmp, bytes) and tmp == "None":
                    tmp = None
                if isinstance(tmp, bytes):
                    tmp = tmp.decode('utf-8')
                setattr(self, trans[full_name], tmp)
                
                self.message("%s %s >> %s %s"%(name,key,trans[full_name],tmp),verbosity=2)
        

        ##################################################
        # read cosmorun and set specific units corrections
        ##################################################
                
        if type(self.scalefactor) is np.ndarray:
          self.scalefactor = self.scalefactor[0]
        if type(self.redshift) is np.ndarray:  
          self.redshift    = self.redshift[0]
        if type(self.time) is np.ndarray:
          self.time        = self.time[0]
        
        # no Hubble parameter in Swift
        self.HubbleFactorCorrectionOff()   
        
        cosmorun=False
        if self.has_var('cosmorun'):
          if self.cosmorun[0]!=0:
            cosmorun=True
          else:
            cosmorun=False  
                
        if cosmorun:
            self.ComovingToProperConversionOn()                  
            self.setComovingIntegrationOn()   # obsolete
            self.atime = self.scalefactor     # for compatibility reasons
            if self.time == 0:
              self.error("self.time should not be equal to zero for a cosmo run")
        else:
            self.ComovingToProperConversionOff()
            self.setComovingIntegrationOff()  # obsolete
            self.atime = self.time            # for compatibility reasons
            if self.has_array("birth_time"):
              self.tstar = self.birth_time    # for compatibility reasons

   


        
        ################
        # read SubgridScheme
        ################
        

        # get the chemical elements and solar abundances
        if "SubgridScheme" in fd:
          
          self.message("reading SubgridScheme...")
        
          subgridGrp = fd["SubgridScheme"]
          
          attrs = dict(subgridGrp.attrs)
          
          if "Chemistry element count" in attrs: 
            # this case is useful if SolarAbundances is not present
            self.ChimieNelements = int(attrs["Chemistry element count"][0])
            self._AM.arrays_props["metals"]["dim"] = self.ChimieNelements 
                        

          if "SolarAbundances" in subgridGrp: 

            d = dict(subgridGrp["SolarAbundances"].attrs)
        
            self.ChimieSolarMassAbundances = {}
        
            for key in d.keys():
              self.ChimieSolarMassAbundances[key] = d[key][0]
          
          
          if "NamedColumns" in subgridGrp:
                      
            tmp = subgridGrp["NamedColumns"]
            
            if "MetalMassFractions" in tmp:
              self.ChimieElements  = list(tmp["MetalMassFractions"][:])    
        
              for i,elt in enumerate(self.ChimieElements):
                self.ChimieElements[i] = self.ChimieElements[i].decode("utf-8")
        
              self.ChimieNelements = len(self.ChimieElements)
            
              # we update 
              self._AM.arrays_props["metals"]["dim"] = self.ChimieNelements 
            
          


        
        ###############
        # read units
        ###############
        self.message("reading units...")

        # define system of units
        params = {}

        # consider that if we have length unit, we should have them all
        if hasattr(self, "UnitLength_in_cm"):
            params['UnitLength_in_cm'] = float(self.UnitLength_in_cm)
            if hasattr(self, "UnitVelocity_in_cm_per_s"):
                params['UnitVelocity_in_cm_per_s'] = float(
                    self.UnitVelocity_in_cm_per_s)
            else:
                self.UnitVelocity_in_cm_per_s = float(
                    self.UnitLength_in_cm) / float(self.Unit_time_in_cgs)
                params['UnitVelocity_in_cm_per_s'] = self.UnitVelocity_in_cm_per_s
            params['UnitMass_in_g'] = float(self.UnitMass_in_g)
            self.localsystem_of_units = units.Set_SystemUnits_From_Params(
                params)
        else:
            self.message("WARNING: snapshot seems broken! There is no units!")
        
        
        # close the file
        h5utils.closeFile(fd)
        
        
        ################
        # read particles
        ################
        
        self.message("reading particles...")
                
        # get npart from the blocks
        self.npart = h5utils.get_npart_from_dataset(self.p_name_global[0],self._AM.array_h5_key('pos'),self.get_mxntpe(),ptypes=self.ptypes)
        
        # check that arrays are present
        self._AM.setReadableArraysFromHDFH5File(self.p_name_global[0],arrays=self.arrays,ptypes=self.ptypes)
        
        # load all arrays according to the information
        # provided by self.arrays_props
        self.read_arrays(ptypes=self.ptypes)

        # set tpe
        self.tpe = np.array([], np.int32)
        for i in range(len(self.npart)):
            self.tpe = np.concatenate((self.tpe, np.ones(self.npart[i]) * i))

        # compute nzero
        nzero = 0
        mass = np.array([])

        for i in range(len(self.npart)):
            if self.massarr[i] == 0:
                nzero = nzero + self.npart[i]
            else:
                self.warning("Massarr is not supported! Please specify the mass of all the particles!",verbosity=2)

        self.nzero = nzero


        #############################
        # specific final conversions
        #############################        
        
        
        if hasattr(self, 'idp'):
          self.idp = self.idp.astype(int) 
        
        if type(self.atime) == np.ndarray:
          self.atime = self.atime[0]
          
        if type(self.redshift) == np.ndarray:
          self.redshift = self.redshift[0]
        
        if type(self.hubbleparam) == np.ndarray:
          self.hubbleparam = self.hubbleparam[0]
          
        if type(self.omega0) == np.ndarray:
          self.omega0 = self.omega0[0]        

        if type(self.omegalambda) == np.ndarray:
          self.omegalambda = self.omegalambda[0]   
          
          
          
                    

    def write_particles(self, f):
        """
        specific format for particle file
        """
        
        self.update_creation_info()
        
        
        # go to the end of the file
        if f is not None:
            f.seek(0, 2)
            

        name = "Unit_temp_in_cgs"
        if not hasattr(self, name):
            setattr(self, name, 1.0)

        name = "Unit_current_in_cgs"
        if not hasattr(self, name):
            setattr(self, name, 1.0)

        import h5py
        # not clean, but work around pNbody
        filename = self.p_name_global[0]
        # open file
        h5f = h5utils.openFile(filename,'w')    

        # add units to the usual gh5 struct
        if hasattr(self, "unitsparameters"):
            units = self.unitsparameters.get_dic()
            for key, i in list(units.items()):
                if not hasattr(self, key):
                    setattr(self, key, i)

        if hasattr(self,"UnitVelocity_in_cm_per_s") and hasattr(self,"UnitLength_in_cm"):
          self.Unit_time_in_cgs = self.UnitLength_in_cm / self.UnitVelocity_in_cm_per_s
        
 
          

        ############
        # HEADER
        ############
        
        self.message("Writing header...")

        list_header = self.get_list_header()
        trans = self.get_header_translation()
        
        for name in list_header:
            h5f.create_group(name)
                    
            
        for key in self.get_list_of_vars():
          
          
            if key in list(trans.values()):
                ind = list(trans.values()).index(key)
                name, hdf5 = list(trans.keys())[ind].split("/")
                value = getattr(self, key)
                
                # !!! force value of npart to be npart_tot (to be improved)
                if mpi.mpi_NTask() > 1: 
                  if key=="npart":
                    value = self.npart_tot
                
            
                if type(value) is not str:
                  value = np.array(value)
                else:
                  value = np.array(value,dtype="S")  
                  
                if value.shape == ():
                  value = np.array([value])
                  
                
                if not isinstance(value, dict):
                    if value is None:
                        h5f[name].attrs[hdf5] = "None"
                    else:
                        h5f[name].attrs[hdf5] = value

        

        ##############
        # SubgridScheme
        ##############
        self.message("Writing SubgridScheme...")
        
        if self.has_var("ChimieSolarMassAbundances"):
                
          subgridGrp = h5f.create_group("SubgridScheme")
          tmp = h5f.create_group("SubgridScheme/SolarAbundances")
        
          for key, val in self.ChimieSolarMassAbundances.items():
            tmp.attrs[key] = np.array([val],np.float32)

          tmp = h5f.create_group("SubgridScheme/NamedColumns")
          asciiList = [n.encode("ascii", "ignore") for n in self.ChimieElements]
          tmp.create_dataset('MetalMassFractions', (len(asciiList),),'S10', asciiList)            
            
            
                 


        h5utils.closeFile(h5f)
        
        ##############
        # PARTICULES
        ##############
        self.message("Writing particles...")
            
            
        # loop over all arrays
        for aname in self.get_list_of_arrays():
          if aname in self._AM.arrays():
          
            if self._AM.array_write(aname):
              # dump the array
              self.dump(aname)
            else:
              self.warning("array %s is not set as to be written."%aname,verbosity=2)
          
          else:
            self.warning("array %s is not stored in the array manager."%aname,verbosity=2)    
              
