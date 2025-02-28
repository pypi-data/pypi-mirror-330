##################################################################################################
# Based on https://gitlab.cern.ch/atlas-physics/stat/tools/StatisticsTools
# Author: Alkaid Cheng
# Email: chi.lung.cheng@cern.ch
##################################################################################################
import os
import math
from typing import List, Optional, Union, Dict, Tuple, Sequence

import numpy as np

import quickstats
from quickstats import (
    AbstractObject,
    semistaticmethod,
    cached_import,
    switch_verbosity
)
from quickstats.core import mappings as mp
from quickstats.concepts import Histogram1D
from quickstats.maths.numerics import pretty_value, get_bins_given_edges, array_issubset, get_rmin_rmax
from quickstats.maths.histograms import bin_center_to_bin_edge
from quickstats.maths.histograms import CONFIG as histogram_config
from quickstats.parsers import RooParamSetupParser
from quickstats.utils.root_utils import load_macro, close_read_cache
from quickstats.utils.common_utils import str_list_filter, combine_dict, filter_by_wildcards, in_notebook
from quickstats.utils import roofit_utils
from quickstats.utils.string_utils import split_str, get_field_names, partial_format
from quickstats.interface.cppyy import is_null_ptr
from quickstats.interface.root import TH1, RooDataSet, RooArgSet, RooMsgService, RooAbsPdf, RooAbsArg
from quickstats.interface.root import roofit_extension as rf_ext
from quickstats.interface.root.roofit_extension import get_str_data
from quickstats.components.basics import WSArgument, SetValueMode, ConstraintType
from .extended_minimizer import ExtendedMinimizer
from .discrete_nuisance import DiscreteNuisance

class ExtendedModel(AbstractObject):
    
    _DEFAULT_CONSTR_CLS_ = ["RooGaussian", "RooLognormal", "RooGamma", "RooPoisson", "RooBifurGauss"]
    
    _DEFAULT_NAMES_ = {
        'conditional_globs': 'conditionalGlobs_{mu}',
        'conditional_nuis': 'conditionalNuis_{mu}',
        'nominal_globs': 'nominalGlobs',
        'nominal_nuis': 'nominalNuis',
        'nominal_vars': 'nominalVars',
        'nominal_pois': 'nominalPOIs',
        'weight': 'weight',
        'dataset_args': 'obsAndWeight',
        'asimov': 'asimovData_{mu}',
        'asimov_no_poi': 'asimovData',
        'channel_asimov': 'combAsimovData_{label}',
        'nll_snapshot': '{nll_name}_{mu}',
        'range_sideband_low': 'SBLo',
        'range_blind': 'Blind',
        'range_sideband_high': 'SBHi'
    }
    
    _DEFAULT_CONFIGS_ = {
        'filename': None,
        'ws_name': None,
        'mc_name': None,
        'data_name': None,
        'initial_snapshots': None,
        'do_discrete_nuisance': True,
        'do_fix_cache': True,
        'do_fix_multi': True,
        'do_binned_likelihood': True,
        'interpolation_code': -1,
        'tag_as_measurement': None,
    }
    
    def __init__(self, filename:str, ws_name:Optional[str]=None, mc_name:Optional[str]=None,
                 data_name:Optional[str]="combData", snapshot_name:Optional[Union[List[str], str]]=None,
                 binned_likelihood:bool=True, tag_as_measurement:Optional[str]=None,
                 fix_cache:bool=True, fix_multi:bool=True, interpolation_code:int=-1,
                 discrete_nuisance:bool=True, load_extension:bool=True, minimizer=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(verbosity=verbosity)        
        
        self.set_minimizer(minimizer)
            
        config = {
            'ws_name': ws_name,
            'mc_name': mc_name,
            'data_name': data_name,
            'initial_snapshots': snapshot_name,
            'do_discrete_nuisance': discrete_nuisance,
            'do_fix_cache': fix_cache,
            'do_fix_multi': fix_multi,
            'do_binned_likelihood': binned_likelihood,
            'interpolation_code': interpolation_code,
            'tag_as_measurement': tag_as_measurement
        }
        
        self.config = combine_dict(self._DEFAULT_CONFIGS_, config)
        # avoid copying RooWorkspace instance
        self.config['filename'] = filename
            
        quickstats.load_corelib()
        if load_extension:
            self.load_extension()
        
        self.initialize()
  
    @property
    def file(self):
        return self._file
    @property
    def workspace(self):
        return self._workspace
    @property
    def model_config(self):
        return self._model_config
    @property
    def pdf(self):
        return self._pdf
    @property
    def category_pdfs(self):
        return self._category_pdfs
    @property
    def data(self):
        return self._data
    @property
    def nuisance_parameters(self):
        return self._nuisance_parameters
    @property
    def global_observables(self):
        return self._global_observables
    @property
    def pois(self):
        return self._pois
    @property
    def observables(self):
        return self._observables
    @property
    def discrete_nuisance(self):
        return self._discrete_nuisance
    @property
    def category(self):
        return self._category
    @property
    def floating_auxiliary_variables(self):
        return self._floating_auxiliary_variables
    @property
    def minimizer(self):
        return self._minimizer
    
    @semistaticmethod
    def load_extension(self):
        ROOT = cached_import("ROOT")
        extensions = quickstats.get_workspace_extensions()
        for extension in extensions:
            result = load_macro(extension)
            if (result is not None) and hasattr(ROOT, extension):
                self.stdout.info(f'Loaded extension module "{extension}"')
        
    @semistaticmethod
    def modify_interp_codes(self, ws, interp_code, classes=None):
        ROOT = cached_import("ROOT")
        if classes is None:
            classes = [ROOT.RooStats.HistFactory.FlexibleInterpVar, ROOT.PiecewiseInterpolation]
        for component in ws.components():
            for cls in classes:
                if (component.IsA() == cls.Class()):
                    component.setAllInterpCodes(interp_code)
                    class_name = cls.Class_Name().split('::')[-1]
                    self.stdout.info(f'{component.GetName()} {class_name} interpolation code set to {interp_code}')
        return None           

    @semistaticmethod
    def activate_binned_likelihood(self, ws):
        ROOT = cached_import("ROOT")
        for component in ws.components():
            try:
                # A pdf is binned if it has attribute "BinnedLikelihood" and it is a RooRealSumPdf (or derived class).
                flag = component.IsA().InheritsFrom(ROOT.RooRealSumPdf.Class())
            except Exception:
                flag = (component.ClassName() == "RooRealSumPdf")
            if (flag):
                component.setAttribute('BinnedLikelihood')
                self.stdout.info(f'Activated binned likelihood attribute for {component.GetName()}')
        return None
                          
    @semistaticmethod
    def set_measurement(self, ws, condition):
        ROOT = cached_import("ROOT")
        for component in ws.components():
            name = component.GetName()
            try:
                flag = (component.IsA() == ROOT.RooAddPdf.Class())
            except Exception:
                flag = (component.ClassName() == "RooAddPdf")
            if flag and condition(name):
                component.setAttribute('MAIN_MEASUREMENT')
                self.stdout.info(f'Activated main measurement attribute for {name}')
        return None
    
    @semistaticmethod
    def deactivate_lv2_const_optimization(self, ws, condition):
        ROOT = cached_import("ROOT")
        self.stdout.info('Deactivating level 2 constant term optimization for specified pdfs')
        for component in ws.components():
            name = component.GetName()
            if (component.InheritsFrom(ROOT.RooAbsPdf.Class()) and condition(name)):
                component.setAttribute("NOCacheAndTrack")
                self.stdout.info(f'Deactivated level 2 constant term optimization for {name}')
     
    def initialize(self):
        ROOT = cached_import("ROOT")
        filename = self.config['filename']
        ws_name  = self.config['ws_name']
        mc_name  = self.config['mc_name']
        if isinstance(filename, str):
            if not os.path.exists(filename):
                raise FileNotFoundError(f'workspace file "{filename}" does not exist')
            self.stdout.info(f'Opening file "{filename}"')
            file = ROOT.TFile(filename) 
            if (not file):
                raise RuntimeError(f"Something went wrong while loading the root file: {filename}")  
            # remove read cache
            close_read_cache(file)
            # load workspace
            if ws_name is None:
                ws_names = [i.GetName() for i in file.GetListOfKeys() if i.GetClassName() == 'RooWorkspace']
                if not ws_names:
                    raise RuntimeError(f"No workspaces found in the root file: {filename}")
                if len(ws_names) > 1:
                    self.stdout.warning("Found multiple workspace instances from the root file: "
                                        f"{filename}. Available workspaces are \"{','.join(ws_names)}\". "
                                        f"Will choose the first one by default")
                ws_name = ws_names[0]
            ws = file.Get(ws_name)
        elif isinstance(filename, ROOT.RooWorkspace):
            file = None
            ws = filename
        if not ws:
            raise RuntimeError(f'failed to load workspace "{ws_name}"')
        ws_name = ws.GetName()
        self.config['ws_name'] = ws_name
        self.stdout.info(f'Loaded workspace "{ws_name}"')
        
        # load model config
        if mc_name is None:
            mc_names = [i.GetName() for i in ws.allGenericObjects() if 'ModelConfig' in i.ClassName()]
            if not mc_names:
                raise RuntimeError(f"no ModelConfig instance found in the workspace \"{ws_name}\"")
            if len(mc_names) > 1:
                mc_names_str = ', '.join([f'"{mc_name}"' for mc_name in mc_names])
                self.stdout.warning(f"Found multiple ModelConfig instances in the workspace \"{ws_name}\""
                                    f"Available ModelConfigs are {mc_names_str}. "
                                    "Will choose the first one by default.")
            mc_name = mc_names[0]
        model_config = ws.obj(mc_name)
        self.config['mc_name'] = mc_name
        if not model_config:
            raise RuntimeError(f'failed to load model config "{mc_name}"')
        self.stdout.info(f'Loaded model config "{mc_name}"')
            
        # modify interpolation code
        interpolation_code = self.config['interpolation_code']
        if interpolation_code != -1:
            self.modify_interp_codes(ws, interpolation_code,
                                     classes=[ROOT.RooStats.HistFactory.FlexibleInterpVar, ROOT.PiecewiseInterpolation])
        
        # activate binned likelihood
        if self.config['do_binned_likelihood']:
            self.activate_binned_likelihood(ws)
        
        # set main measurement
        tag_as_measurement = self.config['tag_as_measurement']
        if tag_as_measurement:
            self.set_measurement(ws, condition=lambda name: name.startswith(tag_as_measurement))
                          
        # deactivate level 2 constant term optimization
            self.deactivate_lv2_const_optimization(ws, 
                condition=lambda name: (name.endswith('_mm') and 'mumu_atlas' in name))

        # load pdf
        pdf = model_config.GetPdf()
        if not pdf:
            raise RuntimeError('Failed to load pdf')
        self.stdout.info(f'Loaded model pdf "{pdf.GetName()}" from model config')
             
        # load dataset
        data_name = self.config['data_name']
        if data_name is None:
            data_names = [i.GetName() for i in ws.allData()]
            if not data_names:
                raise RuntimeError(f"no datasets found in the workspace: {ws_name}")
            data_name = data_names[0]
        data = ws.data(data_name)
        # in case there is a bug in hash map
        if not data:
            data = [i for i in ws.allData() if i.GetName() == data_name]
            if not data:
                raise RuntimeError(f'failed to load dataset "{data_name}"')
            data = data[0]
        data_name = data.GetName()
        self.config['data_name'] = data_name
        self.stdout.info(f'Loaded dataset "{data_name}" from workspace')
                
        # load nuisance parameters
        nuisance_parameters = model_config.GetNuisanceParameters()
        if (not nuisance_parameters) and is_null_ptr(nuisance_parameters):
            #raise RuntimeError('Failed to load nuisance parameters')
            self.stdout.warning("No nuisance parameters found in the workspace. "
                                "An empty set will be loaded by default.")
            nuisance_parameters = ROOT.RooArgSet()
            model_config.SetNuisanceParameters(nuisance_parameters)
        else:
            self.stdout.info('Loaded nuisance parameters from model config')
                
        # Load global observables
        global_observables = model_config.GetGlobalObservables()
        if (not global_observables) and is_null_ptr(global_observables):
            self.stdout.warning("No global observables found in the workspace. "
                                "An empty set will be loaded by default.")            
            global_observables = ROOT.RooArgSet()
        else:
            self.stdout.info('Loaded global observables from model config')                  
    
        # Load POIs
        pois = model_config.GetParametersOfInterest()
        if not pois:
            raise RuntimeError('Failed to load parameters of interest')
        self.stdout.info('Loaded parameters of interest from model config')
                                  
        # Load observables
        observables = model_config.GetObservables()
        if not observables:
            raise RuntimeError('Failed to load observables')     
        self.stdout.info('Loaded observables from model config')
        
        # get categories in case pdf is RooSimultaneous
        if pdf.InheritsFrom('RooSimultaneous'):
            category = pdf.indexCat()
            category_pdfs = {}
            for index_label in category:
                label = index_label.first
                category_pdfs[label] = pdf.getPdf(label)
        else:
            category = None
            category_pdfs = None
            
        # check channel masks (for RooSimultaneousOpt)
        if (pdf.InheritsFrom("RooSimultaneousOpt") or hasattr(pdf, 'channelMasks')):
            channel_masks = pdf.channelMasks()
            n_channel_masks = len(channel_masks)
            if (n_channel_masks > 0):
                active_masks = [m for m in channel_masks if m.getVal() > 0]
                n_active_masks = len(active_masks)
                self.stdout.info(f'{n_active_masks} out of {n_channel_masks} channels masked')
                if self.stdout.verbosity <= "INFO":
                    self.stdout.info('Channel masks:')
                    channel_masks.Print()

        self._file                = file
        self._workspace           = ws
        self._model_config        = model_config
        self._pdf                 = pdf
        self._category_pdfs       = category_pdfs
        self._data                = data
        self._nuisance_parameters = nuisance_parameters
        self._global_observables  = global_observables
        self._pois                = pois
        self._observables         = observables
        self._category            = category
        self._floating_auxiliary_variables = None

        self.last_fit_status = None
        
        # parse initial snapshots
        initial_snapshots = self.config['initial_snapshots']
        if initial_snapshots is None:
            initial_snapshots = []
        elif isinstance(initial_snapshots, str):
            initial_snapshots = split_str(initial_snapshots, sep=',', remove_empty=True)
        elif isinstance(initial_snapshots, list):
            initial_snapshots = list(initial_snapshots)
        else:
            raise ValueError('"initial_snapshots" must be string or list of strings')
        self.config['initial_snapshots'] = initial_snapshots
        # load snapshots
        self.load_snapshots(initial_snapshots)
                    
        # discrete nuisance
        if self.config['do_discrete_nuisance']:
            self._discrete_nuisance = DiscreteNuisance(ws, pdf, verbosity=self.stdout.verbosity)
        else:
            self._discrete_nuisance = DiscreteNuisance(verbosity=self.stdout.verbosity)
        
        RooMsgService.remove_topics()
        return None

    def set_minimizer(self, minimizer:Optional["ExtendedMinimizer"]=None):
        self._minimizer = minimizer
                
    def set_parameters(self, param_setup: Optional[Union[str, Sequence, Dict]] = None,
                       params: Optional["ROOT.RooArgSet"] = None,
                       mode: Union[str, SetValueMode] = SetValueMode.UNCHANGED,
                       strict: bool = False):
        """
        Sets parameters based on a given setup configuration.

        Parameters
        ----------
        param_setup_expr : dict, sequence, str, optional
            The setup configuration specifying how parameters should be set up.
        params : ROOT.RooArgSet, optional
            The input parameter set. If not specified, all workspace variables will be included.
        mode : str or SetValueMode, default = SetValueMode.UNCHANGED
            The mode for setting the value.

        Returns
        -------
        list
            List of modified parameters.
        """
        ROOT = cached_import("ROOT")
        if params is None:
            params = self.workspace.allVars()
        elif isinstance(params, ROOT.RooRealVar):
            params = ROOT.RooArgSet(params)
        if isinstance(param_setup, str):
            param_setup_expr = param_setup
            param_setup = RooParamSetupParser.parse_expr(param_setup_expr)
        else:
            param_setup_expr = None
        param_setup = RooParamSetupParser.parse(params, param_setup, strict_match=False)
        params_names = [param.GetName() for param in params]
        modified_parameters = []
        for param_name in param_setup:
            # resolve variable set
            if param_name.startswith("<") and param_name.endswith(">"):
                params_to_modify = self.get_variables(param_name.strip("<>"))
            else:
                params_to_modify = filter_by_wildcards(params_names, param_name)
                if (not params_to_modify):
                    if (not strict):
                        # check the possibility that the parameter is not a variable
                        param = self.workspace.obj(param_name)
                        if param:
                            params_to_modify = [param]
                        else:
                            self.stdout.warning(f'Parameter "{param_name}" does not exist. '
                                                'No modification will be made.', "red")
                    else:
                        self.stdout.warning(f'Parameter "{param_name}" does not belong to the given '
                                            'parameter set. No modification will be made.', "red")
            for param in params_to_modify:
                if isinstance(param, str):
                    param = params[param]
                self.set_parameter_attributes(param, param_setup[param_name], mode=mode)
                modified_parameters.append(param)
        if (not modified_parameters):
            if param_setup_expr is not None:
                self.stdout.warning(f"No parameters are modified from the given expression: {param_setup_expr}", "red")
            else:
                self.stdout.warning(f"No parameters are modified from the given setup: {param_setup}", "red")
        return modified_parameters
        
    def fix_parameters(self, param_setup_expr: Optional[str] = None, source: Optional["ROOT.RooArgSet"] = None):
        return self.set_parameters(param_setup_expr, source, mode=SetValueMode.FIX)
    
    def profile_parameters(self, param_setup_expr: Optional[str] = None, source: Optional["ROOT.RooArgSet"] = None):
        return self.set_parameters(param_setup_expr, source, mode=SetValueMode.FREE)
    
    float_parameters = profile_parameters

    def set_parameter_attributes(self, param: "ROOT.RooRealVar", value: Union[float, int, Sequence], 
                                 mode: Union[str, SetValueMode] = SetValueMode.UNCHANGED):
        """
        Set a parameter with the given attributes and mode.

        Parameters
        ----------
        param : ROOT.RooRealVar
            The parameter to be set.
        value : float, int or sequence
            The value of the attributes to set for the parameter.
        mode : str or SetValueMode, optional
            The constant state mode.

        Returns
        -------
        None
        """
        ROOT = cached_import("ROOT")
        mode = SetValueMode.parse(mode)
        name = param.GetName()
        
        # for non-variable objects, only fix or free them
        if not isinstance(param, ROOT.RooRealVar):
            if mode == SetValueMode.FIX:
                param.setConstant(1)
                self.stdout.info(f'Fixed object "{name}" as constant.')
            elif mode == SetValueMode.FREE:
                param.setConstant(0)
                self.stdout.info(f'Float object "{name}".')
            return None
        
        setup = {
            'vnom'  : None,
            'vmin'  : None,
            'vmax'  : None,
            'verr'  : None,
            'const' : mode.const_state
        }
        if isinstance(value, (float, int)):
            setup['vnom'] = value
        elif isinstance(value, (list, tuple)):
            nargs = len(value)
            if nargs == 4:
                setup['vnom'], setup['vmin'], setup['vmax'], setup['verr'] = value
            elif nargs == 3:
                setup['vnom'], setup['vmin'], setup['vmax'] = value
            elif nargs == 2:
                setup['vmin'], setup['vmax'] = value
            elif nargs == 1:
                setup['vnom'] = value
            else:
                raise ValueError(f'invalid parameter setup: {value}')
                
        RooAbsArg.set_parameter_attributes(param, **setup)
        
        # display summary of modification to the parameter
        if setup['verr'] is not None:
            error_str = f'+/- {param.getError()} '
        else:
            error_str = ''
        
        if mode == SetValueMode.FIX:
            self.stdout.info(f'Fixed parameter "{name}" at value {param.getVal()} {error_str}'
                             f'[{param.getMin()}, {param.getMax()}]')
        elif mode == SetValueMode.FREE:
            self.stdout.info(f'Float parameter "{name}" at value {param.getVal()} {error_str}'
                             f'[{param.getMin()}, {param.getMax()}]')
        else:
            state_str = "C" if param.isConstant() else "F"
            self.stdout.info(f'Set parameter "{name}" at value {param.getVal()} {error_str}'
                             f'[{param.getMin()}, {param.getMax()}] {state_str}')
    
    def get_var(self, name:str):
        variable = self.workspace.var(name)
        if not variable:
            raise ValueError(f'Variable "{name}" not found in the workspace')
        return variable
            
    def get_obj(self, name:str):
        obj = self.workspace.obj(name)
        if not obj:
            raise ValueError(f'Object "{name}" not found in the workspace')
        return obj

    def get_category_observables(
        self,
        allow_multi: bool = False
    ) -> Dict[str, Union["ROOT.RooRealVar", List["ROOT.RooRealVar"]]]:
        result = {}
        category_map = self.get_category_map()
        for category in category_map:
            observables = list(category_map[category]['observables'].keys())
            if (not allow_multi) and (len(observables) > 1):
                raise RuntimeError(f'Multi-observable category is not supported')
            observable_vars = []
            for observable in observables:
                observable_var = self.observables.find(observable)
                if not observable_var:
                    raise RuntimeError(f'Failed to retrieve observable: "{observable}"')
                observable_vars.append(observable_var)
            if len(observable_vars) == 1:
                result[category] = observable_vars[0]
            else:
                result[category] = observable_vars
        return result
    
    def has_discrete_nuisance(self):
        return self.discrete_nuisance.has_discrete_nuisance()
    
    @staticmethod
    def randomize_globs(pdf:"ROOT.RooAbsPdf", globs:"ROOT.RooArgSet", seed:int):
        """Randomize values of global observables (for generating pseudo-experiments)
        """
        ROOT = cached_import("ROOT")
        # set random seed for reproducible result
        if seed >= 0:
            ROOT.RooRandom.randomGenerator().SetSeed(seed)
        pseudo_globs = pdf.generateSimGlobal(globs, 1)
        pdf_vars = pdf.getVariables()
        pdf_vars.assignValueOnly(pseudo_globs.get(0))
        
    def get_all_constraints(self, pdf:Optional["ROOT.RooAbsPdf"]=None, cache:bool=True):
        ROOT = cached_import("ROOT")
        if pdf is None:
            pdf = self.pdf
        all_constraints = ROOT.RooArgSet()
        obs_str = ":".join([obs.GetName() for obs in self.observables])
        cache_name = "CACHE_CONSTR_OF_PDF_{}_FOR_OBS_{}".format(self.pdf.GetName(), obs_str)
        constr_cache = self.workspace.set(cache_name)
        if constr_cache and cache:
            # retrieve constrains from cache     
            all_constraints.add(constr_cache)
        else:
            # load information needed to determine attributes from ModelConfig 
            obs = self.observables.Clone()
            nuis = self.nuisance_parameters.Clone()
            all_constraints = pdf.getAllConstraints(obs, nuis, ROOT.kFALSE)
            # custom CMS workspace needs extra attention
            if pdf.ClassName() == "RooSimultaneousOpt":
                extra_constraints = ROOT.RooArgSet(pdf.extraConstraints())
                all_constraints.add(extra_constraints)
            if (not constr_cache) and cache:
                self.workspace.defineSet(cache_name, all_constraints)
        return all_constraints        

    def unfold_constraints(self, constr_cls:Optional[List[str]]=None,
                           recursion_limit:int=50, strip_disconnected:bool=False):
        constraints = self.get_all_constraints()
        nuisance_parameters_tmp = self.nuisance_parameters.Clone()
        unfolded_constraints = rf_ext.unfold_constraints(constraints, self.observables,
                                                         nuisance_parameters_tmp,
                                                         constraint_cls=constr_cls,
                                                         recursion_limit=recursion_limit,
                                                         strip_disconnected=strip_disconnected)
        return unfolded_constraints
    
    def pair_constraints(self, fmt:str="list", to_str=False, sort:bool=True, base_component:bool=False,
                         constraint_type:Optional[ConstraintType]=None):
        ROOT = cached_import("ROOT")
        constraint_pdfs = self.unfold_constraints()
        if constraint_type is not None:
            constraint_type = ConstraintType.parse(constraint_type)
            constraint_pdfs = [pdf for pdf in constraint_pdfs if pdf.ClassName() == constraint_type.classname]
            constraint_pdfs = ROOT.RooArgSet(*constraint_pdfs)
        if base_component:
            # for glob value matching
            return rf_ext.pair_constraints_base_component(constraint_pdfs, self.nuisance_parameters,
                                                          self.global_observables, fmt=fmt,
                                                          sort=sort, to_str=to_str)
        return rf_ext.pair_constraints(constraint_pdfs, self.nuisance_parameters,
                                       self.global_observables, fmt=fmt,
                                       sort=sort, to_str=to_str)
    
    def get_constrained_nuisance_parameters(self, fmt:str='list',
                                            constraint_type:Optional[ConstraintType]=None):
        """Get the list of constrained nuisance parameters instances
        """
        _, constrained_nuis, _ = self.pair_constraints(fmt=fmt, constraint_type=constraint_type)
        return constrained_nuis
    
    def get_unconstrained_nuisance_parameters(self, constrained_nuis=None):
        """Get the list of unconstrained nuisance parameters instances
        """
        # do not re-isolate constrained nuisance parameters
        if constrained_nuis is None:
            constrained_nuis = self.get_constrained_nuisance_parameters()
        unconstrained_nuis = list(set(self.nuisance_parameters) - set(constrained_nuis))
        return unconstrained_nuis
    
    def set_constrained_nuisance_parameters_to_nominal(self, set_constant:bool=False):
        constrain_pdf, constrained_nuis, _ = self.pair_constraints(fmt="argset", sort=False)
        for pdf, nuis in zip(constrain_pdf, constrained_nuis):
            pdf_class = pdf.ClassName()
            if pdf_class in ["RooGaussian", "RooBifurGauss"]:
                nuis.setVal(0)
            elif pdf_class == "RooPoisson":
                nuis.setVal(1)
            else:
                raise RuntimeError(f'constraint term "{pdf.GetName()}" has unsupported type "{pdf_class}"')
        if set_constant:
            constrained_nuis.setAttribAll('Constant', True)

    def inspect_constrained_nuisance_parameter(self, nuis, constraints):
        ROOT = cached_import("ROOT")
        nuis_name = nuis.GetName()
        self.stdout.info('INFO: On nuisance parameter {}'.format(nuis_name))
        nuip_nom = 0.0
        prefit_variation = 1.0
        found_constraint = ROOT.kFALSE
        found_gaussian_constraint = ROOT.kFALSE
        constraint_type = None
        for constraint in constraints:
            constr_name = constraint.GetName()
            if constraint.dependsOn(nuis):
                found_constraint = ROOT.kTRUE
                constraint_type = 'unknown'
                # Loop over global observables to match nuisance parameter and
                # global observable in case of a constrained nuisance parameter
                found_global_observable = ROOT.kFALSE
                for glob_obs in self.global_observables:
                    if constraint.dependsOn(glob_obs):
                        found_global_observable = ROOT.kTRUE
                        nuip_nom = glob_obs.getVal()
                        # find constraint width in case of a Gaussian
                        if constraint.IsA() == ROOT.RooGaussian.Class():
                            found_gaussian_constraint = ROOT.kTRUE
                            constraint_type = 'gaus'
                            old_sigma_value = 1.0
                            found_sigma = ROOT.kFALSE
                            for server in constraint.servers():
                                if (server != glob_obs) and (server != nuis):
                                    old_sigma_value = server.getVal()
                                    found_sigma = ROOT.kTRUE
                            if math.isclose(old_sigma_value, 1.0, abs_tol=0.001):
                                old_sigma_value = 1.0
                            if not found_sigma:
                                self.stdout.info(f'Sigma for pdf {constr_name} not found. Uisng 1.0.')
                            else:
                                self.stdout.info(f'Uisng {old_sigma_value} for sigma of pdf {constr_name}')

                            prefit_variation = old_sigma_value
                        elif constraint.IsA() == ROOT.RooPoisson.Class():
                            constraint_type = 'pois'
                            tau = glob_obs.getVal()
                            self.stdout.info(f'Found tau {constr_name} of pdf')
                            prefit_variation = 1. / math.sqrt(tau)
                            self.stdout.info(f'Prefit variation is {prefit_variation}')
                            nuip_nom = 1.0
                            self.stdout.info(f"Assume that {nuip_nom} is nominal value of the nuisance parameter")
        return prefit_variation, constraint_type, nuip_nom
    
    def create_blind_range(self, blind_range:List[float], categories:Optional[List[str]]=None):
        """Create blind ranges for observables
        
        Arguments
            blind_range: list of float
                A list of the form [<lower_blind_range>, <upper_blind_range>]
            categories: (Optional) list of string
                List of categories from which the observables will have their blind range created.
                All categories are used by default.
        """
        if len(blind_range) != 2:
            raise ValueError("invalid format for blind range, must be list of the form [xmin, xmax]")
        range_name_SBLo  = self._DEFAULT_NAMES_['range_sideband_low']
        range_name_Blind = self._DEFAULT_NAMES_['range_blind']
        range_name_SBHi  = self._DEFAULT_NAMES_['range_sideband_high']
        padding = max([len(range_name_SBLo), len(range_name_Blind), len(range_name_SBHi)]) + 2
        blind_min = blind_range[0]
        blind_max = blind_range[1]
        category_map = self.get_category_map()
        if categories is None:
            categories = list(category_map)
        for category in categories:
            obs_name = category_map[category]['observable']
            obs = self.workspace.var(obs_name)
            obs_range = obs.getRange()
            obs_min = obs_range.first
            obs_max = obs_range.second
            if (blind_max <= blind_min) or (blind_max > obs_max) or (blind_min < obs_min):
                raise ValueError(f"invalid blinding range provided: min={blind_min}, max={blind_max}")
            _range_name_SBLo  = f"{range_name_SBLo}_{category}"
            _range_name_Blind = f"{range_name_Blind}_{category}"
            _range_name_SBHi  = f"{range_name_SBHi}_{category}"            
            obs.setRange(_range_name_SBLo, obs_min, blind_min)
            obs.setRange(_range_name_Blind, blind_min, blind_max)
            obs.setRange(_range_name_SBHi, blind_max, obs_max)
            cat_padding = padding + len(category)
            self.stdout.info(f"The following ranges are defined for the observable \"{obs_name}\"")
            self.stdout.info(f"\t{_range_name_SBLo.ljust(cat_padding)}: [{obs_min}, {blind_min}]", bare=True)
            self.stdout.info(f"\t{_range_name_Blind.ljust(cat_padding)}: [{blind_min}, {blind_max}]", bare=True)
            self.stdout.info(f"\t{_range_name_SBHi.ljust(cat_padding)}: [{blind_max}, {obs_max}]", bare=True)
        return None
    
    def get_sideband_range_name(self):
        """Get sideband range name to be used in RooAbsPdf.createNLL(..., Range(<range_name>))
        """
        range_name_SBLo = self._DEFAULT_NAMES_['range_sideband_low']
        range_name_SBHi = self._DEFAULT_NAMES_['range_sideband_high']
        return f"{range_name_SBLo},{range_name_SBHi}"
    
    def get_blind_range_name(self):
        """Get blind range name that are excluded from the fit range of the observable
        """
        return self._DEFAULT_NAMES_['range_blind']
    
    def get_blind_range(self):
        category_map = self.get_category_map()
        blind_range_name = self.get_blind_range_name()
        blind_range = {}
        for category in category_map:
            obs_name = category_map[category]['observable']
            obs = self.workspace.var(obs_name)
            _blind_range_name = f"{blind_range_name}_{category}"
            dummy_range = obs.getRange(_blind_range_name)
            dummy_min = dummy_range.first
            dummy_max = dummy_range.second
            obs_range = obs.getRange()
            obs_min = obs_range.first
            obs_max = obs_range.second
            if (dummy_min == obs_min) and (dummy_max == obs_max):
                # observable not blinded, skipping
                continue
            blind_range[obs_name] = [dummy_min, dummy_max]
        return blind_range
    
    def remove_blind_range(self, categories:Optional[List[str]]=None):
        category_map = self.get_category_map()
        if categories is None:
            categories = list(category_map)
        range_name_SBLo = self._DEFAULT_NAMES_['range_sideband_low']
        range_name_Blind = self._DEFAULT_NAMES_['range_blind']
        range_name_SBHi = self._DEFAULT_NAMES_['range_sideband_high']
        blind_range = self.get_blind_range()
        for category in categories:
            obs_name = category_map[category]['observable']
            if obs_name not in blind_range:
                continue
            obs = self.workspace.var(obs_name)
            obs_range = obs.getRange()
            obs_min = obs_range.first
            obs_max = obs_range.second            
            obs.setRange(range_name_SBLo, obs_min, obs_max)
            obs.setRange(range_name_Blind, obs_min, obs_max)
            obs.setRange(range_name_SBHi, obs_min, obs_max)
            self.stdout.info(f"The following ranges are removed from the observable \"{obs_name}\":")
            self.stdout.info(f"\t{range_name_SBLo}, {range_name_Blind}, {range_name_SBHi}", bare=True)

    def get_poi(self, expr:Optional[Union[str, List[str], "ROOT.RooRealVar", "ROOT.RooArgSet"]]=None,
                strict:bool=False):
        """Get POI variable(s) by name
        
        Parameters
            expr: (optional) str, list of str, RooRealVar or RooArgSet
                Expression for the POI(s).
                If str, it is the name of the POI in the workspace. Multiple POIs
                can be specified with a list of strs.
                If RooRealVar or RooArgSet, their corresponding name(s) will be parsed instead.
                If None, the first POI defined in the model config will be returned.
            strict: bool
                require the variable to be defined in the POI list, throw error otherwise
        """
        ROOT = cached_import("ROOT")
        if expr is None:
            poi = self.pois.first()
            self.stdout.info(f'POI name not specified. The first POI "{poi.GetName()}" is used by default.')
            return poi
        single_poi = False
        if isinstance(expr, str):
            poi_names = [expr]
            single_poi = True
        elif isinstance(expr, ROOT.RooRealVar):
            poi_names = [expr.GetName()]
            single_poi = True
        elif isinstance(expr, ROOT.RooArgSet):
            poi_names = [arg.GetName() for arg in expr]
        else:
            poi_names = list(expr)
        pois = ROOT.RooArgSet()
        for name in poi_names:
            poi = self.workspace.var(name)
            if not poi:
                raise RuntimeError(f'workspace does not contain the variable "{name}"')
            if strict and (poi not in self.pois):
                raise RuntimeError(f'workspace variable "{name}" is not part of the POIs')
            pois.add(poi)
        if single_poi:
            return pois.first()
        return pois
    
    def _load_obs_and_weight(self, obs_and_weight:Optional[Union["ROOT.RooArgSet",str]]=None, 
                             weight_var:Optional[Union["ROOT.RooRealVar",str]]=None):
        ROOT = cached_import("ROOT")
        # get the weight variable
        if weight_var is None:
            weight_name = self._DEFAULT_NAMES_['weight']
            weight_var = self.workspace.var(weight_name)
            if not weight_var:
                weight_var = ROOT.RooRealVar(weight_name, weight_name, 1)
                getattr(self.workspace, "import")(weight_var)
        elif isinstance(weight_var, str):
            weight_var = self.workspace.var(weight_var)
            if not weight_var:
                raise RuntimeError(f'weight variable "{weight_var}" not found in workspace')
        elif not isinstance(weight_var, ROOT.RooRealVar):
            raise ValueError('weight variable must be of RooRealVar type')
                
        # get the obs_and_weight arg set
        if obs_and_weight is None:
            default_name = self._DEFAULT_NAMES_['dataset_args']
            obs_and_weight = self.workspace.set(default_name)
            if not obs_and_weight:
                obs_and_weight = ROOT.RooArgSet()
                obs_and_weight.add(self.observables)            
                obs_and_weight.add(weight_var)
                self.workspace.defineSet(default_name, obs_and_weight)
        elif isinstance(obs_and_weight, str):
            obs_and_weight = self.workspace.set(obs_and_weight)
            if not obs_and_weight:
                raise RuntimeError(f'named set "{obs_and_weight}" not found in workspace')
        elif not isinstance(obs_and_weight, ROOT.RooArgSet):
            raise ValueError('the argument "obs_and_weight" must be of RooArgSet type')
        return obs_and_weight, weight_var

    def generate_asimov_from_pdf(self, name:str="asimovData", pdf:Optional["ROOT.RooAbsPdf"]=None,
                                 observables:Optional["ROOT.RooArgSet"]=None,
                                 obs_and_weight:Optional[Union["ROOT.RooArgSet",str]]=None, 
                                 weight_var:Optional[Union["ROOT.RooRealVar",str]]=None,
                                 extra_args=None):
        ROOT = cached_import("ROOT")
        
        pdf = pdf if pdf is not None else self.pdf
        if isinstance(pdf, ROOT.RooSimultaneous):
            raise ValueError("this method should not be called from a simultaneous pdf")
        
        obs_and_weight, weight_var = self._load_obs_and_weight(obs_and_weight, weight_var)
        
        # get the combined arg set for the asimov dataset
        arg_set = ROOT.RooArgSet()
        arg_set.add(obs_and_weight)
        if extra_args is not None:
            if isinstance(extra_args, list):
                for arg in extra_args:
                    arg_set.add(arg)
            else:
                arg_set.add(extra_args)
                
        asimov_data = ROOT.RooDataSet(name, name, arg_set, ROOT.RooFit.WeightVar(weight_var))
        if observables is None:
            observables = self.observables
        # generate observables defined by the pdf associated with this state
        obs = pdf.getObservables(observables)
        
        if len(obs)==2:
            target_obs_1 = obs[0]
            target_obs_2 = obs[1]
            expected_events = pdf.expectedEvents(obs)
            for i in range(target_obs_1.numBins()):
                target_obs_1.setBin(i)
                binWidth_1 = target_obs_1.getBinWidth(i)
                for j in range(target_obs_2.numBins()):
                    target_obs_2.setBin(j)
                    binWidth_2 = target_obs_2.getBinWidth(j)
                    norm  = pdf.getVal(obs)*binWidth_1*binWidth_2
                    n_events = norm*expected_events
                    if n_events <= 0:
                        self.stdout.warning(f"Detected bin with zero expected events ({n_events})!"
                                            "Please check your inputs. "
                                            f"Obs = [{target_obs_1.GetName()},{target_obs_2.GetName()}],"
                                            f"bin=[{i}, {j}]")
                    elif (n_events > 0) and (n_events < 1e18):
                        self.stdout.debug("pdf={}, obs_1={}, bin_1={}, obs_2={}, bin_2={}, val={}".format(
                            pdf.GetName(), target_obs_1.GetName(), i, target_obs_2.GetName(), j, n_events))
                        asimov_data.add(observables, n_events)
                    else:
                        raise RuntimeError(f"detected pdf bin with nan (pdf={pdf.GetName()},obs=[{target_obs_1.GetName()},{target_obs_2.GetName()}],bin=[{i}, {j}])")
        else:
            target_obs = obs.first()
            expected_events = pdf.expectedEvents(obs)
            #print("INFO: Generating Asimov for pdf {}".format(pdf.GetName()))
            for i in range(target_obs.numBins()):
                target_obs.setBin(i)
                norm  = pdf.getVal(obs)*target_obs.getBinWidth(i)
                n_events = norm*expected_events
                if n_events <= 0:
                    self.stdout.warning("Detected bin with zero expected events ({})! Please check"
                                        "your inputs. Obs = {}, bin = {}".format(n_events, target_obs.GetName(), i))
                elif (n_events > 0) and (n_events < 1e18):
                    self.stdout.debug("pdf={}, obs={}, bin={}, val={}".format(
                        pdf.GetName(), target_obs.GetName(), i, n_events))
                    asimov_data.add(observables, n_events)
                else:
                    raise RuntimeError(f"detected pdf bin with nan (pdf={pdf.GetName()},obs={target_obs.GetName()},bin={i})")

        if (asimov_data.sumEntries() != asimov_data.sumEntries()):
            raise RuntimeError("asimov data sum entries is nan")
        return asimov_data
    
    def match_globs(self):
        _, components, globs = self.pair_constraints(fmt="argset", base_component=True, sort=True)
        for component, glob in zip(components, globs):
            glob.setVal(component.getVal())
            self.stdout.debug("set glob {} to val {}".format(glob.GetName(), glob.getVal()))
        """
        for nuis, globs, pdf in zip(nuis_list, globs_list, pdf_list):
            pdf_class = pdf.ClassName()
            if pdf_class in ["RooGaussian", "RooBifurGauss"]:
                globs.setVal(nuis.getVal())
            elif pdf_class == "RooPoisson":            
                globs.setVal(nuis.getVal()*globs.getVal())
            else:
                raise RuntimeError(f"constraint term \"{pdf.GetName()}\" has unsupported type \"{pdf_class}\"")
            self.stdout.debug("set glob {} to val {}".format(globs.GetName(), globs.getVal()))
        """

    def generate_asimov(self, poi_name:Optional[str]=None,
                        poi_val:Optional[float]=None, 
                        poi_profile:Optional[float]=None,
                        do_fit:bool=True,
                        modify_globs:bool=True,
                        do_import:bool=True,
                        asimov_name:Optional[str]=None,
                        asimov_snapshot:Optional[str]=None,
                        channel_asimov_name:Optional[str]=None,
                        dataset:Optional["ROOT.RooDataSet"]=None,
                        constraint_option:int=0,
                        restore_states:int=0,
                        minimizer_options:Optional[Dict]=None, 
                        nll_options:Optional[Union[Dict, List]]=None,
                        snapshot_names:Optional[Dict]=None,
                        method:str="new"):
        """
            Generate Asimov dataset.
            
            Note:
                Nominal (initial values) snapshots of nuisance parameters and global are saved
                as "nominalNuis" and "nominalGlobs" if not already exist. Conditional snapshots
                are saved as "conditionalNuis_{mu}" and "conditionalGlobs_{mu}" irrespective of
                whether nuisance parameter profiling is performed and whether conditional mle
                is used for the profiling. This is to faciliate the use case of Asymptotic limit
                calculation. The names of these snahpshots can be customized via the
                `snapshot_names` option.
        
            Arguments:
                poi_name: (optional) str, list of str
                    Name of POI to retrieve. A list of names can be given to retrieve multiple POIs.
                If None, the first POI defined in the model config will be returned.
                poi_val: (Optional) float, list of float
                    Generate asimov data with POI(s) set at the specified value(s). If None, POI(s) will be kept
                    at the post-fit value(s) if a fitting is performed or the pre-fit value if no fitting
                    is performed.
                poi_profile: (Optional) float, list of float
                    Perform nuisance parameter profiling with POI(s) set at the specified value(s). This option
                    is only effective if do_fit is set to True. If None, POI(s) is set floating 
                    (i.e. unconditional maximum likelihood estimate). 
                do_fit: bool, default=True    
                    Perform nuisance parameter profiling with a fit to the given dataset.
                modify_globs: bool, default=True
                    Match the values of nuisance parameters and the corresponding global observables when
                    generating the asimov data. This is important for making sure the asimov data has the 
                    (conditional) minimal NLL.
                constraint_option: int, default=0
                    Customize the target of nuisance paramaters involved in the profiling.
                    Case 0: All nuisance parameters are allowed to float;
                    Case 1: Constrained nuisance parameters are fixed to 0. Unconstrained nuisrance
                            parameters are allowed to float.
                restore_states: int, default=0
                    Restore variable states at the end of asimov data generation.
                    Case 0: All variable states will be restored.
                    Case 1: Only global observable states will be restored.
                do_import: bool, default=True
                    Import the generated asimov data to the current workspace.
                asimov_name: (Optional) str
                    Name of the generated asimov dataset. If None, defaults to "asimovData_{mu}" where
                    `{mu}` will be replaced by the value of `poi_val`. Other keywords are: `{mu_cond}`
                    which is the the value of `poi_profile`. If multiple POIs are defined, `{mu}`
                    will be replaced by `<poi_name_i>_<mu_i>_<poi_name_j>_<mu_j>...` and similarly for
                    `{mu_cond}`
                asimov_snapshot: (Optional) str
                    Name of the snapshot taken right after asimov data generation. If None, no snapshot
                    will be saved.
                channel_asimov_name: (Optional) str
                    Name of the asimov dataset in each category of a simultaneous pdf. If None,
                    defaults to "combAsimovData_{label}" where `{label}` will be replaced by the
                dataset: (Optional) ROOT.RooDataSet
                    Dataset based on which the negative log likelihood (NLL) is created for nuisance parameter
                    profiling. If None, default to self.data.
                minimizer_options: (Optional) dict
                    Options for minimization during nuisance parameter profiling. If None, defaults to
                    ExtendedMinimizer._DEFAULT_MINIMIZER_OPTION_
                nll_options: (Optional) dict, list
                    Options for NLL creation during nuisance parameter profiling. If None, defaults to
                    ExtendedMinimizer._DEFAULT_NLL_OPTION_
                snapshot_names: (Optional) dict
                    A dictionary containing a map of the snapshot type and the snapshot names. The default
                    namings are stored in ExtendedModel._DEFAULT_NAMES_.
                method: str, default = "new"
                    Method for generating asimov dataset from main pdf.
        """
        ROOT = cached_import("ROOT")
        # define simplified ws variable names
        ws = self.workspace
        all_globs = self.global_observables
        all_nuis  = self.nuisance_parameters
        
        # define names used for various objects
        names = combine_dict(self._DEFAULT_NAMES_)
        if snapshot_names is not None:
            names.update(snapshot_names)
        if asimov_name is not None:
            names['asimov'] = asimov_name
            names['asimov_no_poi'] = asimov_name
        if channel_asimov_name is not None:
            names['channel_asimov'] = channel_asimov_name
        nom_vars_name = names['nominal_vars']
        nom_glob_name = names['nominal_globs']
        nom_nuis_name = names['nominal_nuis']
        con_glob_name = names['conditional_globs']
        con_nuis_name = names['conditional_nuis']

        if poi_name is None:
            poi_set = None
        else:
            poi_set = self.get_poi(poi_name)
            
        poi_const_state = {}
        if poi_set is not None:
            if isinstance(poi_set, ROOT.RooRealVar):
                poi_const_state[poi_set] = poi_set.isConstant()
            else:
                for poi in poi_set:
                    poi_const_state[poi] = poi.isConstant()
        
        # take snapshot of initial states of all variables
        mutable_vars = self.get_variables(WSArgument.MUTABLE)
        self.save_snapshot(nom_vars_name, mutable_vars)
        if not ws.getSnapshot(nom_glob_name):
            self.save_snapshot(nom_glob_name, all_globs)
        if not ws.getSnapshot(nom_nuis_name):
            self.save_snapshot(nom_nuis_name, all_nuis)
        
        if do_fit:
            if dataset is None:
                dataset = self.data
            # create new instance of minimizer
            if self.minimizer is None:
                minimizer = self.minimizer_cls("Minimizer", self.pdf, dataset, workspace=self.workspace)
                if minimizer_options is None:
                    minimizer_options = combine_dict(minimizer._DEFAULT_MINIMIZER_OPTION_)
                if nll_options is None:
                    nll_options = combine_dict(minimizer._DEFAULT_NLL_OPTION_)
                minimizer.configure(**minimizer_options)
                if constraint_option == 0:
                    pass
                elif constraint_option == 1:
                    self.set_constrained_nuisance_parameters_to_nominal()
                else:
                    raise ValueError(f"unsupported constraint option: {constraint_option}")
                if isinstance(nll_options, dict):
                    minimizer.configure_nll(**nll_options)
                elif isinstance(nll_options, list):
                    minimizer.set_nll_commands(nll_options)
                else:
                    raise ValueError("unsupported nll options format")
            else:
                self.minimizer.set_pdf(self.pdf)
                self.minimizer.set_data(dataset)
                minimizer = self.minimizer
                
            if poi_set is not None:
                uncond_fit = poi_profile is None
                poi_profile = RooParamSetupParser.parse(poi_set, poi_profile, fill_missing=True)
                if uncond_fit:
                    # unconditional mle
                    self.set_parameters(poi_profile, poi_set, mode=SetValueMode.FREE)
                else:
                    # conditional mle
                    self.set_parameters(poi_profile, poi_set, mode=SetValueMode.FIX)
                    
            status = minimizer.minimize()
            self.last_fit_status = status
        else:
            poi_profile = RooParamSetupParser.parse(poi_set, poi_profile, fill_missing=True)
            
        if poi_set is not None:
            poi_val = RooParamSetupParser.parse(poi_set, poi_val)
            self.set_parameters(poi_val, poi_set)
            
        # restore the constant state of the pois
        for poi, const_state in poi_const_state.items():
            poi.setConstant(const_state)
            
        # match values of global observables to the corresponding NPs
        if modify_globs:
            self.match_globs()
            
        def format_mu_str(poi_setup):
            npoi = len(poi_setup)
            assert npoi > 0
            if (npoi == 1):
                return pretty_value(list(poi_setup.values())[0])
            components = []
            for poi_name, value in poi_setup.items():
                    components.append(f"{poi_name}_{pretty_value(value)}")
            return "_".join(components)

        if poi_set is not None:
            if do_fit:
                self.save_snapshot(con_glob_name.format(mu=format_mu_str(poi_profile)), all_globs)
                self.save_snapshot(con_nuis_name.format(mu=format_mu_str(poi_profile)), all_nuis)
            else:
                self.save_snapshot(con_glob_name.format(mu=format_mu_str(poi_val)), all_globs)
                self.save_snapshot(con_nuis_name.format(mu=format_mu_str(poi_val)), all_nuis)

            asimov_data_name = names['asimov'].format(mu=format_mu_str(poi_val),
                                                      mu_cond=format_mu_str(poi_profile))
        else:
            asimov_data_name = names['asimov_no_poi']

        if method == "old":
            channel_asimov_data_name = names['channel_asimov']
            sim_pdf = self.pdf
            if not isinstance(sim_pdf, ROOT.RooSimultaneous):
                asimov_data = self.generate_asimov_from_pdf(asimov_data_name, sim_pdf)
            else:
                asimov_data_map = {}
                channel_cat = sim_pdf.indexCat()
                n_cat = channel_cat.size()
                for i in range(n_cat):
                    channel_cat.setIndex(i)
                    label = channel_cat.getLabel()
                    pdf_cat = sim_pdf.getPdf(label)
                    name = channel_asimov_data_name.format(index=i, label=label)
                    asimov_data_map[label] = self.generate_asimov_from_pdf(name, pdf_cat, extra_args=channel_cat)
                obs_and_weight, weight_var = self._load_obs_and_weight()
                dataset_map = RooDataSet.get_dataset_map(asimov_data_map)
                asimov_data = ROOT.RooDataSet(asimov_data_name, asimov_data_name, 
                                              ROOT.RooArgSet(obs_and_weight, channel_cat),
                                              ROOT.RooFit.Index(channel_cat),
                                              ROOT.RooFit.Import(dataset_map),
                                              ROOT.RooFit.WeightVar(weight_var))
        elif method == "new":
            weight_name = self._DEFAULT_NAMES_['weight']
            with switch_verbosity(RooAbsPdf.stdout, self.stdout.verbosity):
                asimov_data = RooAbsPdf.get_asimov_dataset(self.pdf, self.observables,
                                                           weight_name=weight_name,
                                                           dataset_name=asimov_data_name)
        else:
            raise RuntimeError(f'unknown method: {method}')

        if do_import:
            if ws.data(asimov_data_name):
                self.stdout.warning(f"Dataset with name {asimov_data_name} already exists in the "
                                    "workspace. The newly generated dataset will not overwrite the original "
                                    "dataset.")
            ws.Import(asimov_data)
            self.stdout.info(f'Generated Asimov Dataset "{asimov_data_name}"')
            
        if asimov_snapshot is not None:
            snapshot_name = asimov_snapshot.format(mu=format_mu_str(poi_val),
                                                   mu_cond=format_mu_str(poi_profile))
            self.save_snapshot(snapshot_name, mutable_vars)
    
        if restore_states == 0:
            # load back a snapshot of all variable's initial states
            self.load_snapshot(nom_vars_name)
        elif restore_states == 1:
            # load back a snapshot of the initial global observable states
            self.load_snapshot(nom_glob_name)
        elif restore_states == 2:
            pass
        else:
            raise ValueError(f'unsupported restore state option "{restore_states}"')
        
        return asimov_data
    
    def generate_observed_toys(self, dataset=None, n_toys:int=1, seed:Optional[int]=None,
                               event_seed:Optional[Dict]=None,
                               add_ghost:bool=True, do_import:bool=True,
                               name="toyObsData_{index}"):
        if dataset is None:
            dataset = self.data
        interface = RooDataSet(dataset)
        generator = interface.generate_toy_dataset(n_toys,
                                                   seed=seed,
                                                   add_ghost=add_ghost,
                                                   event_seed=event_seed,
                                                   name_fmt=name)
        toys = []
        for toy in generator:
            if do_import:
                self.workspace.Import(toy)
            toys.append(toy)
        return toys
    
    def generate_toys(self, n_toys:int=1, seed:Union[int, List[int]]=0, 
                      binned:bool=True, randomize_globs:bool=True,
                      do_import:bool=True, name="toyData_{index}_seed_{seed}"):
        
        if n_toys > 1:
            if seed == 0:
                seeds = [0] * n_toys
            elif (not isinstance(seed, (list, np.ndarray, range))) or (len(seed) != n_toys):
                raise ValueError("seed must be a list of size n_toys if seed != 0")
            else:
                seeds = seed
                
        ws = self.workspace
        # take snapshot of initial states of all variables
        self.workspace.saveSnapshot("tmp", self.workspace.allVars())
        
        if binned:
            if self.pdf.ClassName() == "RooSimultaneous":
                index_cat = self.pdf.indexCat()
                for cat in index_cat:
                    pdf_i = self.pdf.getPdf(cat.first)
                    pdf_i.setAttribute("GenerateToys::Binned")
            else:
                self.pdf.setAttribute("GenerateToys::Binned")
        
        toys = []
        args = [self.observables, ROOT.RooFit.Extended(), ROOT.RooFit.AutoBinned(True)]
        if binned:
            args.append(ROOT.RooFit.GenBinned("GenerateToys::Binned"))
        
        for i in range(n_toys):
            if randomize_globs:
                self.randomize_globs(self.pdf, self.global_observables, seeds[i])
            toy = self.pdf.generate(*args)
            toy_name = name.format(seed=seeds[i], index=i)
            toy.SetName(toy_name)
            if do_import:
                if ws.data(toy_name):
                    raise RuntimeError(f"attempt to overwrite existing dataset `{toy_name}`")
                getattr(ws, "import")(toy)
                self.stdout.info(f'Generated toy dataset "{toy_name}"')
            toys.append(toy)
        
        ws.loadSnapshot("tmp")
        
        return toys
    
    def save(self, filename:str, recreate:bool=True, rebuild:bool=True,
             keep_snapshots:Optional[List[str]]=None,
             keep_datasets:Optional[List[str]]=None):
        """Save the current workspace as a ROOT file.
        
        Parameters:
        ---------------------------------------------
        filename: str
            Name of the output ROOT file.
        recreate: bool, default = True
            Recreate the output file if exists.
        rebuild: bool, default = True
            Rebuild the workspace from scratch.
        keep_snapshots: (optional) list of str
            Snapshots to keep. If not specified, all snapshots will be kept.
        keep_datasets: (optional) list of str
            Datasets to keep. If not specified, all datasets will be kept.
        """
        
        # buggy, model config is messed up
        # new_ws = ROOT.RooWorkspace(self.workspace)
        # new_ws.writeToFile(filename, recreate)

        # rebuild the entire workspace
        if rebuild:
            from quickstats.components.workspaces import XMLWSModifier
            config = {"data_name": None}
            if keep_snapshots is not None:
                config["snapshot_list"] = keep_snapshots
            else:
                if (quickstats.root_version >= (6, 26, 0)):
                    config["snapshot_list"] = [i.GetName() for i in self.workspace.getSnapshots()]
                else:
                    self.stdout.warning("Saving of snapshots not supported with ROOT version < 6.26.0. "
                                        "No snapshots will be saved in the rebuilt workspace.")
                    config["snapshot_list"] = []
            if keep_datasets is not None:
                config["dataset_list"] = keep_datasets
            modifier = XMLWSModifier(config, verbosity="WARNING")
            modifier.create_modified_workspace(self.workspace, filename,
                                               import_class_code=False,
                                               recreate=recreate)
        else:
            self.workspace.writeToFile(filename, recreate)
    
    @semistaticmethod
    def load_ws(self, filename:str, ws_name:Optional[str]=None, mc_name:Optional[str]=None):
        ROOT = cached_import("ROOT")
        if not os.path.exists(filename):
            raise FileNotFoundError(f'workspace file {filename} does not exist')
        file = ROOT.TFile(filename)
        if (not file):
            raise RuntimeError(f"Something went wrong while loading the root file: {filename}")        
        # load workspace
        if ws_name is None:
            ws_names = [i.GetName() for i in file.GetListOfKeys() if i.GetClassName() == 'RooWorkspace']
            if not ws_names:
                raise RuntimeError(f"No workspaces found in the root file: {filename}")
            if len(ws_names) > 1:
                self.stdout.warning("Found multiple workspace instances from the root file: {}. Available workspaces"
                      " are \"{}\". Will choose the first one by default".format(filename, ','.join(ws_names)))
            ws_name = ws_names[0]
        ws = file.Get(ws_name)
        if not ws:
            raise RuntimeError('Failed to load workspace: "{}"'.format(ws_name))
        # load model config
        if mc_name is None:
            mc_names = [i.GetName() for i in ws.allGenericObjects() if 'ModelConfig' in i.ClassName()]
            if not mc_names:
                raise RuntimeError(f"no ModelConfig object found in the workspace: {ws_name}")
            if len(mc_names) > 1:
                self.stdout.warning("Found multiple ModelConfig instances from the workspace: {}. "
                      "Available ModelConfigs are \"{}\". "
                      "Will choose the first one by default".format(ws_name, ','.join(mc_names)))
            mc_name = mc_names[0]     
        mc = ws.obj(mc_name)
        if not mc:
            raise RuntimeError(f'failed to load model config "{mc_name}"')
        return file, ws, mc
    
    def get_category_map(self, pdf=None):
        ROOT = cached_import("ROOT")
        if pdf is None:
            pdf = self.pdf
        if not isinstance(pdf, ROOT.RooSimultaneous):
            raise ValueError("input pdf is not a simultaneous pdf")            
        category_map = {}
        index_cat = pdf.indexCat()
        n_cat = index_cat.size()
        for cat_data in index_cat:
            cat_label = cat_data.first
            cat_index = cat_data.second
            pdf_cat = pdf.getPdf(cat_label)
            observables = pdf_cat.getObservables(self.observables)
            category_map[cat_label] = {}
            category_map[cat_label]['index'] = cat_index
            category_map[cat_label]['pdf'] = pdf_cat.GetName()
            category_map[cat_label]['observables'] = {}
            for observable in observables:
                obs_name = observable.GetName()
                bin_range = observable.getRange()
                category_map[cat_label]['observables'][obs_name] = {
                    'bin_range': (bin_range.first, bin_range.second),
                    'bins': observable.getBins()
                }
        return category_map
    
    def get_categories(self):
        return list(self.get_category_map())
    
    def _get_new_binnings(self, bins:Optional[Union[Dict, int]]=None):
        category_map = self.get_category_map()
        binnings = {}
        for category in category_map:
            if len(category_map[category]['observables']) > 1:
                raise RuntimeError('rebinning of multi-observable category is not supported')
            orig_binnings = next(iter(category_map[category]['observables'].values()))
            binnings[category] = {}
            bin_range = orig_binnings['bin_range']
            if bins is None:
                _bins = orig_binnings['bins']
            elif isinstance(bins, dict):
                _bins = bins.get(category, None)
                if _bins is None:
                    raise RuntimeError(f"binning not specified for the category \"{category}\"")
            elif isinstance(bins, int):
                _bins = bins
            else:
                raise RuntimeError(f"invalid binning format: {bins}")
            bin_width = round((bin_range[1] - bin_range[0]) / _bins, 8)
            binnings[category]['bin_range'] = bin_range
            binnings[category]['bins'] = _bins
            binnings[category]['bin_width'] = bin_width
        return binnings
    
    def get_category_pdf_distribution(self, category:str,
                                      nbins:Optional[int]=None,
                                      bin_range:Optional[Tuple[float]]=None,
                                      weight_scale:Optional[float]=None):
        pdf_cat = self.pdf.getPdf(category)
        distribution = RooAbsPdf.get_distribution(pdf_cat, self.observables,
                                                  nbins=nbins, bin_range=bin_range,
                                                  weight_scale=weight_scale)
        #obs = pdf_cat.getObservables(self.observables).first()
        #result['observable'] = obs.GetName()
        return distribution

    def get_category_pdf_distributions(self, categories:Optional[List[str]]=None,
                                       nbins:Optional[Union[Dict[str, int], int]]=None,
                                       bin_range:Optional[Union[Dict[str, Tuple[float]], Tuple[float]]]=None,
                                       weight_scales:Optional[Union[float, Dict[str, float]]]=None,
                                       merge:bool=False):
        if categories is None:
            categories = list(self.get_category_map())
        if weight_scales is None:
            weight_scales = {}
        if not isinstance(weight_scales, dict):
            weight_scales = {category: weight_scales for category in categories}
        if not isinstance(nbins, dict):
            nbins = {category: nbins for category in categories}
        if not isinstance(bin_range, dict):
            bin_range = {category: bin_range for category in categories}            
        distributions = {}
        for category in categories:
            weight_scale = weight_scales.get(category, None)
            nbins_cat = nbins.get(category, None)
            bin_range_cat = bin_range.get(category, None)            
            distributions[category] = self.get_category_pdf_distribution(category=category,
                                                                         nbins=nbins_cat,
                                                                         bin_range=bin_range_cat,
                                                                         weight_scale=weight_scale)
        if merge:
            return RooDataSet._get_merged_distribution(distributions)
        return distributions

    def _parse_dataset(self, dataset:Optional[Union[str, "ROOT.RooDataSet"]]=None):
        ROOT = cached_import("ROOT")
        if dataset is None:
            dataset = self.data
        elif isinstance(dataset, str):
            dataset_name = dataset
            dataset = self.workspace.data(dataset_name)
            if not dataset:
                raise ValueError(f'Workspace does not contain the dataset "{dataset_name}"')
        if not isinstance(dataset, ROOT.RooDataSet):
            raise ValueError(f"invalid dataset format: {dataset}")
        return dataset

    def get_category_dataset_distribution(self, category:str,
                                          dataset:Optional[Union[str, "ROOT.RooDataSet"]]=None,
                                          remove_ghost:bool=True,
                                          nbins:Optional[int]=None,
                                          bin_range:Optional[Tuple[float]]=None,
                                          weight_scale:Optional[float]=None):
        distributions = self.get_category_dataset_distributions([category],
                                                                dataset=dataset,
                                                                remove_ghost=remove_ghost,
                                                                nbins=nbins,
                                                                bin_range=bin_range,
                                                                weight_scales=weight_scale)
        return distributions[category]

    def get_category_dataset_distributions(self, categories:Optional[List[str]]=None,
                                           dataset:Optional[Union[str, "ROOT.RooDataSet"]]=None,
                                           remove_ghost:bool=True,
                                           nbins:Optional[Union[Dict[str, int], int]]=None,
                                           bin_range:Optional[Union[Dict[str, Tuple[float]], Tuple[float]]]=None,
                                           weight_scales:Optional[Union[float, Dict[str, float]]]=None,
                                           merge:bool=False):
        if categories is None:
            categories = list(self.get_category_map())
        dataset = self._parse_dataset(dataset)
        rds = RooDataSet(dataset)
        distributions = rds.get_category_distributions(categories=categories,
                                                       nbins=nbins,
                                                       bin_range=bin_range,
                                                       include_error=True,
                                                       weight_scales=weight_scales,
                                                       remove_ghost=remove_ghost,
                                                       merge=merge)
        return distributions
    
    def get_collected_distributions(self, categories:Optional[List[str]]=None,
                                    current_distribution=True,
                                    datasets:Optional[Union[List[str], List["ROOT.RooDataSet"]]]=None,
                                    snapshots:Optional[List[str]]=None,
                                    nbins:Optional[Union[Dict[str, int], int]]=None,
                                    nbins_pdf:Optional[Union[Dict[str, int], int]]=None,
                                    bin_range:Optional[Union[Dict[str, Tuple[float]], Tuple[float]]]=None,
                                    remove_ghost:bool=True,
                                    merge:bool=False):
        if categories is None:
            categories = list(self.get_category_map())

        if merge:
            collected_distributions = {"merged": {}}
        else:
            collected_distributions = {category: {} for category in categories}
                
        if datasets is None:
            datasets = []
            
        for dataset in datasets:
            dataset = self._parse_dataset(dataset)
            dataset_name = dataset.GetName()
            distributions = self.get_category_dataset_distributions(categories,
                                                                    dataset=dataset,
                                                                    remove_ghost=remove_ghost,
                                                                    nbins=nbins,
                                                                    bin_range=bin_range,
                                                                    merge=merge)
            if merge:
                distributions = {"merged": distributions}
            for category in distributions:
                collected_distributions[category][dataset_name] = distributions[category]

        if snapshots is None:
            snapshots = []

        if "tmp" in snapshots:
            raise ValueError('The "tmp" snapshot is reserved. Please use another name.')

        self.workspace.saveSnapshot("tmp", self.workspace.allVars())
        if current_distribution:
            snapshots = ["tmp"] + snapshots
            
        for snapshot in snapshots:
            try:
                for snapshot in snapshots:
                    exist = self.workspace.loadSnapshot(snapshot)
                    if not exist:
                        raise RuntimeError(f'Snapshot "{snapshot}" not found in workspace')
                        
                    distributions_main = self.get_category_pdf_distributions(categories,
                                                                             nbins=nbins_pdf,
                                                                             bin_range=bin_range,
                                                                             merge=merge)
                    if merge:
                        distributions_main = {"merged": distributions_main}
                    if nbins == nbins_pdf:
                        distributions_alt = distributions_main
                    else:
                        distributions_alt = self.get_category_pdf_distributions(categories,
                                                                                nbins=nbins,
                                                                                bin_range=bin_range,
                                                                                merge=merge)
                        if merge:
                            distributions_alt = {"merged": distributions_alt}
                    key = "current" if snapshot == "tmp" else snapshot
                    for category, distribution in distributions_main.items():
                        collected_distributions[category][key] = distribution
                    for category, distribution in distributions_alt.items():
                        collected_distributions[category][f"{key}_binned"] = distribution
            finally:
                self.workspace.loadSnapshot("tmp")

        return collected_distributions

    def get_collected_histograms(self, categories:Optional[List[str]]=None,
                                 current_distribution=True,
                                 datasets:Optional[Union[List[str], List["ROOT.RooDataSet"]]]=None,
                                 snapshots:Optional[List[str]]=None,
                                 nbins:Optional[Union[Dict[str, int], int]]=None,
                                 nbins_pdf:Optional[Union[Dict[str, int], int]]=None,
                                 bin_range:Optional[Union[Dict[str, Tuple[float]], Tuple[float]]]=None,
                                 remove_ghost:bool=True,
                                 merge:bool=False):
        collected_distributions = self.get_collected_distributions(categories=categories,
                                                                   current_distribution=current_distribution,
                                                                   datasets=datasets,
                                                                   snapshots=snapshots,
                                                                   nbins=nbins,
                                                                   nbins_pdf=nbins_pdf,
                                                                   bin_range=bin_range,
                                                                   remove_ghost=remove_ghost,
                                                                   merge=merge)
        ghost_weight = None if remove_ghost else histogram_config.ghost_weight
        pdf_targets = []
        if current_distribution:
            pdf_targets.append('current')
        if snapshots:
            pdf_targets.extend(snapshots)
        collected_histograms = {}
        for category, distributions in collected_distributions.items():
            if not distributions:
                continue
            histograms = {}
            for key, distribution in distributions.items():
                bin_edges = bin_center_to_bin_edge(distribution['x'])
                bin_content = distribution['y']
                histogram = Histogram1D(
                    bin_content=bin_content,
                    bin_edges=bin_edges,
                    ghost_weight=ghost_weight
                )
                histograms[key] = histogram
            for target in pdf_targets:
                binned_target = f'{target}_binned'
                if ((target in histograms) and (binned_target in histograms)):
                    histograms[target].reweight(histograms[binned_target], inplace=True)
            collected_histograms[category] = histograms
        return collected_histograms                
            
    def plot_distributions(
        self,
        categories:Optional[List[str]]=None,
        current_distribution=True,
        datasets:Optional[List[Union[str, "ROOT.RooDataSet"]]]=None,
        snapshots:Optional[List[str]]=None,
        nbins:Optional[Union[Dict[str, int], int]]=None,
        nbins_pdf:Optional[Union[Dict[str, int], int]]=None,
        bin_range:Optional[Union[Dict[str, Tuple[float]], Tuple[float]]]=None,
        analytic:bool=True,
        merge:bool=False,
        discriminant:Optional[str]=None,
        unit:Optional[str]=None,
        category_label_map:Optional[Dict]=None,
        init_options:Optional[Dict]=None,
        draw_options:Optional[Dict]=None,
        save_as:Optional[str]=None,
    ):
        from quickstats.plots import DataModelingPlot

        category_map = self.get_category_map()
        
        collected_histograms = self.get_collected_histograms(categories=categories,
                                                             current_distribution=current_distribution,
                                                             datasets=datasets,
                                                             snapshots=snapshots,
                                                             nbins=nbins,
                                                             nbins_pdf=nbins_pdf,
                                                             bin_range=bin_range,
                                                             merge=merge)

        draw_options = draw_options or {}
        init_options = init_options or {}
        category_label_map = category_label_map or {}

        pdf_targets = []
        if current_distribution:
            pdf_targets.append('current')
        if snapshots:
            pdf_targets.extend(snapshots)
        binned_pdf_targets = [f'{target}_binned' for target in pdf_targets]        

        if save_as is not None:
            from matplotlib.backends.backend_pdf import PdfPages
            pdf = PdfPages(save_as)
        else:
            pdf = None

        plotters = {}
        for i, (category, histograms) in enumerate(collected_histograms.items()):
            if not histograms:
                continue
            init_options_i = mp.concat((init_options,), copy=True)
            draw_options_i = mp.concat((draw_options,), copy=True)

            init_options_i['analytic_model'] = analytic
            init_options_i['figure_index'] = i
            if 'analysis_label_options' in init_options_i:
                options = init_options_i['analysis_label_options']
                if 'extra_text' in options:
                    options['extra_text'] = options['extra_text'].format(
                        category=category_label
                    )
            plotter = DataModelingPlot(histograms, **init_options_i)

            if merge:
                obs_name = 'Observable'
            else:
                observables = category_map[category]['observables']
                if len(observables) > 1:
                    raise RuntimeError('multi-observable category is not supported')
                obs_name = next(iter(observables))
            xlabel = discriminant or obs_name or 'Observable'
            category_label = category_label_map.get(category, category)
            draw_options_i.setdefault('xlabel', partial_format(xlabel, category=category_label))
            
            pdf_targets_i = [
                target for target in histograms.keys() if target in pdf_targets
            ]
            data_targets_i = [
                target for target in histograms.keys() if (target not in pdf_targets)
                and (target not in binned_pdf_targets)
            ]
            primary_target = [
                target for target in histograms.keys() if target not in binned_pdf_targets
            ][0]
            draw_options_i['primary_target'] = primary_target
            axes = plotter.draw(
                data_targets=data_targets_i,
                model_targets=pdf_targets_i,
                **draw_options_i,
            )
            if pdf is not None:
                pdf.savefig(bbox_inches="tight")
            if in_notebook():
                import matplotlib.pyplot as plt
                plt.show()

            plotters[category] = plotter
            
        if pdf is not None:
            pdf.close()

        return plotters
    
    def _load_floating_auxiliary_variables(self):
        aux_vars = self.get_variables(WSArgument.AUXILIARY)
        floating_aux_vars = RooArgSet.from_list([v for v in aux_vars if not v.isConstant()])
        self._floating_auxiliary_variables = floating_aux_vars
    
    def get_variables(self, variable_type:Union[str, WSArgument], sort:bool=True):
        ROOT = cached_import("ROOT")
        resolved_vtype = WSArgument.parse(variable_type)
        if not resolved_vtype.is_variable:
            raise ValueError(f"the collection \"{variable_type}\" does not contain members of the type \"RooRealVar\"")
        if resolved_vtype == WSArgument.VARIABLE:
            variables = ROOT.RooArgSet(self.workspace.allVars())
            if self.has_discrete_nuisance():
                variables.add(self.discrete_nuisance.multipdf_cats)
        elif resolved_vtype == WSArgument.OBSERVABLE:
            if isinstance(self.pdf, ROOT.RooSimultaneous):
                variables = self.observables.Clone()
                cat = self.pdf.indexCat()
                variables.remove(cat)
            else:
                variables = ROOT.RooArgSet(self.observables)
        elif resolved_vtype == WSArgument.POI:
            variables = ROOT.RooArgSet(self.pois)
        elif resolved_vtype == WSArgument.GLOBAL_OBSERVABLE:
            variables = ROOT.RooArgSet(self.global_observables)
        elif resolved_vtype == WSArgument.NUISANCE_PARAMETER:
            variables = ROOT.RooArgSet(self.nuisance_parameters)
        elif resolved_vtype == WSArgument.CONSTRAINED_NUISANCE_PARAMETER:
            variables = RooArgSet.from_list(self.get_constrained_nuisance_parameters())
        elif resolved_vtype == WSArgument.GAUSSIAN_CONSTRAINT_NP:
            variables = RooArgSet.from_list(self.get_constrained_nuisance_parameters(constraint_type=ConstraintType.GAUSSIAN))
        elif resolved_vtype == WSArgument.POISSON_CONSTRAINT_NP:
            variables = RooArgSet.from_list(self.get_constrained_nuisance_parameters(constraint_type=ConstraintType.POISSON))
        elif resolved_vtype == WSArgument.UNCONSTRAINED_NUISANCE_PARAMETER:
            variables = RooArgSet.from_list(self.get_unconstrained_nuisance_parameters())
        elif resolved_vtype == WSArgument.CONSTRAINT:
            nuis_list, glob_list, pdf_list = self.pair_constraints(sort=sort)
            return RooArgSet.from_list(nuis_list), RooArgSet.from_list(glob_list), RooArgSet.from_list(pdf_list)
        elif resolved_vtype == WSArgument.AUXILIARY:
            variables           = self.get_variables(WSArgument.VARIABLE)
            pois                = self.get_variables(WSArgument.POI)
            nuisance_parameters = self.get_variables(WSArgument.NUISANCE_PARAMETER)
            global_observables  = self.get_variables(WSArgument.GLOBAL_OBSERVABLE)
            observables         = self.get_variables(WSArgument.OBSERVABLE)
            variables.remove(pois)
            variables.remove(nuisance_parameters)
            variables.remove(global_observables)
            variables.remove(observables)
        elif resolved_vtype == WSArgument.CORE:
            variables = ROOT.RooArgSet()
            variables.add(self.nuisance_parameters)
            variables.add(self.global_observables)
            variables.add(self.pois)
        elif resolved_vtype == WSArgument.MUTABLE:
            variables = self.get_variables(WSArgument.CORE)
            if self.floating_auxiliary_variables is None:
                self._load_floating_auxiliary_variables()
            variables.add(self.floating_auxiliary_variables)
            if self.has_discrete_nuisance():
                variables.add(self.discrete_nuisance.multipdf_cats)
        else:
            raise ValueError(f"unknown variable type \"{variable_type}\"")
        if sort:
            return RooArgSet.sort(variables)
        return variables

    def get_default_printable_content(self):
        ROOT = cached_import("ROOT")
        from ROOT.RooPrintable import (kName, kClassName, kValue, kArgs, kExtras, kAddress,
                                       kTitle, kCollectionHeader, kSingleLine)
        default_content = {
            WSArgument.PDF      : kClassName|kName|kArgs,
            WSArgument.FUNCTION : kClassName|kName|kArgs
        }
        return default_content
    
    def as_dataframe(self, attribute:Union[str, WSArgument, "ROOT.RooArgSet"],
                     asym_error:bool=False, content:Optional[int]=None):
        """
        View workspace attribute in the form of a dataframe
        """
        ROOT = cached_import("ROOT")
        if isinstance(attribute, ROOT.RooArgSet):
            collection = attribute
        else:
            resolved_attribute = WSArgument.parse(attribute)
            if resolved_attribute.is_variable:
                collection = self.get_variables(resolved_attribute)
            # for the special case of displaying constrain terms
            # will print the tuple of names of NP, Global Observables and Constrain Pdf
            elif resolved_attribute == WSArgument.CONSTRAINT:
                data = self.pair_constraints(to_str=True, fmt="dict")
                import pandas as pd
                df = pd.DataFrame(data).rename(columns={'pdf': 'constraint pdf',
                                                        'nuis': 'nuisance parameters',
                                                        'globs': 'global observables'})
                return df
            elif resolved_attribute in [WSArgument.PDF, WSArgument.FUNCTION]:
                default_content = self.get_default_printable_content()
                if resolved_attribute == WSArgument.PDF:
                    if content is None:
                        content = default_content[WSArgument.PDF]
                    collection = self.workspace.allPdfs()
                elif resolved_attribute == WSArgument.FUNCTION:
                    if content is None:
                        content = default_content[WSArgument.FUNCTION]
                    collection = self.workspace.allFunctions()
                else:
                    raise RuntimeError("unexpected error")
                df_1 = get_str_data(collection, fill_classes=True,
                                    fill_definitions=True, content=content,
                                    style=kSingleLine, fmt="dataframe")
                df_2 = roofit_utils.variable_collection_to_dataframe(collection)
                df = df_1.merge(df_2, on="name", how='outer', sort=True, validate="one_to_one")
                return df
            else:
                raise ValueError(f"unsupported workspace attribute: {attribute}")
        df = roofit_utils.variable_collection_to_dataframe(collection, asym_error=asym_error)
        return df
    
    def rename_dataset(self, rename_map:Dict):
        for old_name, new_name in rename_map.items():
            if old_name == new_name:
                continue
            dataset = self.workspace.data(old_name)
            if not dataset:
                raise RuntimeError(f'dataset "{old_name}" not found in the workspace')
            check_dataset = self.workspace.data(new_name)
            if check_dataset:
                raise RuntimeError(f'cannot rename dataset from "{old_name}" to "{new_name}": '
                                   f'dataset "{new_name}" already exists in the workspace')
            dataset.SetName(new_name)
    
    @staticmethod
    def _format_category_summary(category_name:str, category_map:Dict):
        all_names = []
        all_ranges = []
        all_bins = []
        for obs_name in category_map['observables']:
            all_names.append(obs_name)
            bin_range = category_map['observables'][obs_name]['bin_range']
            rmin, rmax = get_rmin_rmax(bin_range)
            all_ranges.append(f'[{rmin}, {rmax}]')
            bins = category_map['observables'][obs_name]['bins']
            all_bins.append(f'{bins}')
        if len(all_names) == 1:
            summary_str = f"{category_name} (observable = {all_names[0]}, range = {all_ranges[0]}, bins = {all_bins[0]})"
        else:
            summary_str = (f"{category_name} (observables = {'(' + ', '.join(all_names) + ')'}, "
                           f"ranges = {'(' + ', '.join(all_ranges) + ')'}, "
                           f"bins = {'(' + ', '.join(all_bins) + ')'})")
        return summary_str
    
    @staticmethod
    def _format_multipdf_summary(multipdf, multipdf_cat):
        multipdf_name = multipdf.GetName()
        category_name = multipdf_cat.GetName()
        num_cat = len(multipdf_cat)
        summary_str = f"{multipdf_name} (index_cat = {category_name}, num_pdfs = {num_cat})"
        return summary_str

    @staticmethod
    def _format_variable_summary(variables: "ROOT.RooArgSet", indent: str = '') -> str:
        data = [roofit_utils.get_variable_attributes(variable) for variable in variables]
        data = sorted(data, key=lambda d: d['name'])
        summary_str = ''
        for d in data:
            name, value, vmin, vmax = d['name'], d['value'], d['min'], d['max']
            const_str = "C" if d['is_constant'] else "F"
            summary_str += f"{indent}{name} = {value} [{vmin}, {vmax}] {const_str}\n"
        return summary_str
        
    def print_summary(self, items:Optional[List]=None, suppress_print:bool=False, detailed:bool=True,
                      include_patterns:Optional[List]=None, exclude_patterns:Optional[List]=None,
                      save_as:Optional[str]=None):
        ROOT = cached_import("ROOT")
        if items is None:
            items = ['workspace', 'dataset', 'snapshot', 'category',
                     'poi', 'detailed_nuisance_parameter', 'multipdf']
        summary_str = ""
        # workspace
        if 'workspace' in items:
            summary_str += "Workspace:\n"
            summary_str += f"\t{self.workspace.GetName()}\n"
        # datasets
        if 'dataset' in items:
            datasets = self.workspace.allData()
            summary_str += f"Datasets ({len(datasets)}):\n"
            summary_str += "".join([f"\t{ds.GetName()}\n" for ds in datasets])
        # snapshots
        if ('snapshot' in items):
            if (quickstats.root_version >= (6, 26, 0)):
                snapshots = self.workspace.getSnapshots()
                summary_str += f"Snapshots ({len(snapshots)}):\n"
                summary_str += "".join([f"\t{snap.GetName()}\n" for snap in snapshots])
            else:
                self.stdout.warning("Snapshot listing is only available after ROOT 6.26/00")
        # categories
        if 'category' in items:
            if isinstance(self.pdf, ROOT.RooSimultaneous):
                category_map = self.get_category_map()
                n_cat = len(category_map)
                summary_str += f"Categories ({n_cat}):\n"
                for category in category_map:
                    summary_str += "\t" + self._format_category_summary(category, category_map[category]) + "\n"
        # multi pdfs
        if 'multipdf' in items:
            multipdf_cats = self.discrete_nuisance.multipdf_cats
            multipdfs = self.discrete_nuisance.multipdfs
            n_multipdf = len(multipdfs)
            summary_str += f"MultiPdfs ({n_multipdf}):\n"
            for multipdf, multipdf_cat in zip(multipdfs, multipdf_cats):
                summary_str += "\t" + self._format_multipdf_summary(multipdf, multipdf_cat) + "\n"
        # pois, NPs
        param_strs     = []
        param_sets     = []
        if 'poi' in items:
            pois = self.pois            
            param_strs.append('POIs')
            param_sets.append(pois)
        if 'detailed_nuisance_parameter' in items:
            constrained_nps = self.get_constrained_nuisance_parameters()
            unconstrained_nps = self.get_unconstrained_nuisance_parameters(constrained_nps)            
            param_strs += ['Constrained NPs', 'Unconstrained NPs']
            param_sets += [constrained_nps, unconstrained_nps]
        elif 'nuisance_parameter' in items:
            param_strs += ['NPs']
            param_sets += [self.nuisance_parameters]
        if 'global_observable' in items:
            param_strs += ['Global Observables']
            param_sets += [self.global_observables]
        if 'auxiliary' in items:
            param_strs += ['Auxiliary Parameters']
            param_sets += [self.get_variables('auxiliary')]            
        for pstr, pset in zip(param_strs, param_sets):
            summary_str += f"{pstr} ({len(pset)}):\n"
            param_names = [p.GetName() for p in pset]
            param_names_to_include = param_names.copy()
            if include_patterns is not None:
                param_names_to_include = str_list_filter(param_names_to_include, include_patterns, inclusive=True)
            if exclude_patterns is not None:
                param_names_to_include = str_list_filter(param_names_to_include, exclude_patterns, inclusive=False)
            param_index = np.in1d(param_names, param_names_to_include).nonzero()
            pset = np.array(pset)[param_index]
            data = [roofit_utils.get_variable_attributes(p) for p in pset]
            data = sorted(data, key=lambda d: d['name'])
            if detailed:
                for d in data:
                    name   = d['name']
                    value  = d['value']
                    vmin   = d['min']
                    vmax   = d['max']
                    const_str = "C" if d['is_constant'] else "F"
                    summary_str += f"\t{name} = {value} [{vmin}, {vmax}] {const_str}\n"
            else:
                for d in data:
                    name = d['name']
                    summary_str += f"\t{name}\n"
        if not suppress_print:
            self.stdout.info(summary_str, bare=True)
        if save_as is not None:
            with open(save_as, "w") as f:
                f.write(summary_str)

    def compare_snapshots(self, ss1:Union[str, "ROOT.RooArgSet"], ss2:Union[str, "ROOT.RooArgSet"]):
        ROOT = cached_import("ROOT")
        snapshots = {}
        for label, ss in [("left", ss1), ("right", ss2)]:
            if isinstance(ss, str):
                if not self.workspace.getSnapshot(ss):
                    raise ValueError(f'workspace does not contain a snapshot named "{ss}"')
                ss = self.workspace.getSnapshot(ss)
            if not isinstance(ss, ROOT.RooArgSet):
                raise TypeError('dataset must be an instance of RooDataSet')
            snapshots[label] = ss
        from quickstats.components.workspaces import ComparisonData, WSItemType
        from quickstats.interface.root.roofit_extension import get_str_data
        data = ComparisonData("Snapshots", True, False)
        content = WSItemType.VARIABLE.default_content
        style   = WSItemType.VARIABLE.default_style
        data_1 = get_str_data(snapshots["left"], fill_classes=False,
                              fill_definitions=True,
                              content=content, style=style, fmt="dataframe")
        data_2 = get_str_data(snapshots["right"], fill_classes=False,
                              fill_definitions=True,
                              content=content, style=style, fmt="dataframe")
        data.add(data_1, data_2)
        data.process()
        summary_str = data.get_summary_str(visibility=0b01011, indent="    ")
        self.stdout.info(summary_str, bare=True)
        
    def get_systematics_variations(self, filter_name:Optional[str]=None,
                                   filter_client:Optional[str]=None, fmt:str="pandas"):
        constr_pdfs, constr_nuis, _ = self.pair_constraints()
        syst_variations = roofit_utils.get_systematics_variations(constr_nuis, constr_pdfs,
                                                                  filter_name=filter_name,
                                                                  filter_client=filter_client, fmt=fmt)
        return syst_variations
    
    def get_gaussian_constraint_attributes(self, fmt:str="pandas"):
        constr_pdfs, _, _ = self.pair_constraints()
        constr_attributes = roofit_utils.get_gaussian_pdf_attributes(constr_pdfs, fmt=fmt)
        return constr_attributes
   
    def get_poisson_constraint_attributes(self, fmt:str="pandas"):
        constr_pdfs, _, _ = self.pair_constraints()
        constr_attributes = roofit_utils.get_poisson_pdf_attributes(constr_pdfs, fmt=fmt)
        return constr_attributes
    
    def get_category_pdf(self, category:str):
        pdf_cat = self.pdf.getPdf(category)
        if not pdf_cat:
            raise RuntimeError(f'{category} is not a valid category in the workspace')
        return pdf_cat
        
    def get_category_expected_events_over_range(self, category:str, range:List[float],
                                                normalize:bool=False):
        pdf_cat = self.get_category_pdf(category)
        rmin, rmax = get_rmin_rmax(range)
        expected_events = RooAbsPdf.get_expected_events_over_range(pdf_cat, self.observables,
                                                                   rmin, rmax, normalize=normalize)
        return expected_events
    
    def load_snapshots(self, snapshot_names:List[str]):
        for snapshot_name in snapshot_names:
            self.load_snapshot(snapshot_name)

    def load_snapshot(self, snapshot_name:Optional[str]=None):
        if snapshot_name is not None:
            snapshot = self.workspace.getSnapshot(snapshot_name)
            if (not snapshot) and ('0x(nil)' in snapshot.__repr__()):
                self.stdout.warning(f'Failed to load snapshot "{snapshot_name}" (snapshot does not exist)')
            else:
                self.workspace.loadSnapshot(snapshot_name)
                self.stdout.info(f'Loaded snapshot "{snapshot_name}"')
                
    def save_snapshot(self, snapshot_name:Optional[str]=None, 
                      variables:Optional[Union["ROOT.RooArgSet", str, WSArgument]]=None):
        if snapshot_name is not None:
            if variables is None:
                self.workspace.saveSnapshot(snapshot_name, self.workspace.allVars())
            else:
                if isinstance(variables, (str, WSArgument)):
                    variables = self.get_variables(variables)
                self.workspace.saveSnapshot(snapshot_name, variables)
            self.stdout.info(f'Saved snapshot "{snapshot_name}"')