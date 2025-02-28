from typing import Optional, Union, List, Dict, Tuple
import os
import copy

__all__ = ['DynamicFilePath', 'PathManager']
           
class DynamicFilePath:
    """
    A class to represent a dynamic file path that can be formatted with parameters.

    Parameters
    ----------------------------------------------------
    basename : str
        The base name of the file.
    dirname : str, optional
        The directory name of the file.
    """
    def __init__(self, basename: str, dirname: Optional[str] = None):
        self.dirname = dirname
        self.basename = basename

    def __repr__(self):
        return f'DynamicFilePath(dirname={self.dirname}, basename={self.basename})'

    @staticmethod
    def _format_path(path:str, **parameters) -> str:
        try:
            formatted_path = path.format(**parameters)
        except KeyError:
            from quickstats.utils.string_utils import get_field_names
            required_fields = get_field_names(path)
            missing_fields = [field for field in required_fields if field not in parameters]
            raise RuntimeError(f'missing the following required field names for path formatting: {missing_fields}')
        return formatted_path
        
    def resolve_basename(self, **parameters) -> str:
        """
        Resolve the base name with the given parameters.

        Parameters
        ----------------------------------------------------
        **parameters :
            Parameters to format the base name.

        Returns
        ----------------------------------------------------
        str
            The formatted base name.
        """
        return self._format_path(self.basename, **parameters)

    def resolve_dirname(self, **parameters) -> str:
        """
        Resolve the directory name with the given parameters.
        
        Parameters
        ----------------------------------------------------
        **parameters :
            Parameters to format the directory name.

        Returns
        ----------------------------------------------------
        str
            The formatted directory name.
        """
        return self._format_path(self.dirname, **parameters) if self.dirname else ""

PathType = Union[str, DynamicFilePath, Tuple[Optional[str], str]]


class PathManager:
    """
    Tool for managing file and directory paths.

    Parameters
    ----------------------------------------------------
    base_path : str, optional
        The base directory path to all paths defined, except for
        absolute paths.
    directories : dict of {str : str or PathType}
        Managed directories.
    files : dict of {str : str or PathType}
        Managed files.
    """
    DEFAULT_DIRECTORIES = {}
    DEFAULT_FILES = {}

    def __init__(self, base_path: Optional[str] = None,
                 directories: Optional[Dict[str, PathType]] = None,
                 files: Optional[Dict[str, PathType]] = None):
        self.base_path = base_path
        self.directories = copy.deepcopy(self.DEFAULT_DIRECTORIES)
        if directories:
            self.update_directories(directories)
        self.files = copy.deepcopy(self.DEFAULT_FILES)
        if files:
            self.update_files(files)

    @property
    def directories(self) -> Dict[str, DynamicFilePath]:
        return self._directories
    
    @directories.setter
    def directories(self, values: Optional[Dict[str, PathType]] = None):
        self._directories = self._parse_paths(values)
    
    @property
    def files(self) -> Dict[str, DynamicFilePath]:
        return self._files
    
    @files.setter
    def files(self, values: Optional[Dict[str, PathType]] = None):
        self._files = self._parse_paths(values)

    @staticmethod
    def _parse_paths(paths: Optional[Dict[str, PathType]] = None) -> Dict[str, DynamicFilePath]:
        """
        Parse a dictionary of paths into DynamicFilePath objects.

        Parameters
        ----------------------------------------------------
        paths : dict, optional
            The paths to parse.

        Returns
        ----------------------------------------------------
        dict of {str : DynamicFilePath}
            The parsed paths.
        """
        if paths is None:
            return {}
        if not isinstance(paths, dict):
            raise TypeError("Paths must be specified in dict format")
        
        parsed_paths = {}
        for key, value in paths.items():
            if not isinstance(key, str):
                raise TypeError("Path name must be a string")
            parsed_paths[key] = PathManager._parse_path(value)
        return parsed_paths

    @staticmethod
    def _parse_path(path: PathType) -> DynamicFilePath:
        """
        Parse a path into a DynamicFilePath object.

        Parameters
        ----------------------------------------------------
        path : PathType
            The path to parse.

        Returns
        ----------------------------------------------------
        DynamicFilePath
            The parsed path.
        """
        if isinstance(path, tuple):
            if len(path) != 2:
                raise ValueError("A tuple path must have two elements (dirname, basename)")
            return DynamicFilePath(path[1], path[0])
        if isinstance(path, str):
            return DynamicFilePath(path, None)
        if isinstance(path, DynamicFilePath):
            return path
        raise TypeError("Path must be a tuple, string, or DynamicFilePath")

    def update_directories(self, directories: Optional[Dict[str, PathType]] = None) -> None:
        """
        Update the managed directories.

        Parameters
        ----------------------------------------------------
        directories : dict of {str : PathType}, optional
            Directories to update.
        """
        new_directories = self._parse_paths(directories)
        self._directories.update(new_directories)
        
    def update_files(self, files: Optional[Dict[str, PathType]] = None) -> None:
        """
        Update the managed files.

        Parameters
        ----------------------------------------------------
        files : dict of {str : PathType}, optional
            Files to update.
        """
        new_files = self._parse_paths(files)
        self._files.update(new_files)
        
    def set_directory(self, directory_name: str, path: PathType, absolute: bool = False) -> None:
        """
        Set a directory path.

        Parameters
        ----------------------------------------------------
        directory_name : str
            The name of the directory.
        path : PathType
            The path to set.
        absolute : bool
            Whether to convert the path to an absolute path.
        """
        parsed_path = self._parse_path(path)
        if absolute:
            parsed_path.basename = os.path.abspath(parsed_path.basename)
        self.update_directories({directory_name: parsed_path})
        
    def set_file(self, file_name: str, file: PathType) -> None:
        """
        Set a file path.

        Parameters
        ----------------------------------------------------
        file_name : str
            The name of the file.
        file : PathType
            The path to set.
        """
        self.update_files({file_name: self._parse_path(file)})

    def set_base_path(self, path: str) -> None:
        """
        Set the base path for the manager.

        Parameters
        ----------------------------------------------------
        path : str
            The base path to set.
        """
        self.base_path = path

    def get_base_path(self) -> Optional[str]:
        """
        Get the base path for the manager.

        Returns
        ----------------------------------------------------
        str, optional
            The base path.
        """
        return self.base_path

    def get_basename(self, filename:str, **parameters):
        return self.get_file(filename, basename_only=True, **parameters)

    def get_resolved_path(self, path: PathType, subdirectory: Optional[str] = None,
                          basename_only: bool = False, **parameters) -> str:
        """
        Resolve a path with optional parameters.

        Parameters
        ----------------------------------------------------
        path : PathType
            The path to resolve.
        subdirectory : str, optional
            An optional subdirectory.
        basename_only : bool, default false
            Whether to return the base name only.
        **parameters :
            Additional parameters for formatting the path.

        Returns
        ----------------------------------------------------
        str
            The resolved path.
        """
        if not isinstance(path, DynamicFilePath):
            path = self._parse_path(path)
        
        basename = path.resolve_basename(**parameters)

        if basename_only:
            return basename
            
        if subdirectory:
            basename = os.path.join(subdirectory, basename)
        
        if path.dirname:
            dirname = self.get_directory(path.resolve_dirname(**parameters),
                                         **parameters)
        elif self.base_path:
            dirname = self.base_path
        else:
            dirname = ""
        
        return os.path.join(dirname, basename)
        
    def get_directory(self, dirname: str, check_exist: bool = False, **parameters) -> str:
        """
        Get a resolved directory path.

        Parameters
        ----------------------------------------------------
        dirname : str
            The directory name.
        check_exist : bool
            Whether to check if the directory exists.
        **parameters :
            Additional parameters for formatting the path.

        Returns
        ----------------------------------------------------
        str
            The resolved directory path.
        """
        if dirname not in self.directories:
            raise KeyError(f'Unrecognized directory name "{dirname}"')
        
        directory = self.directories[dirname]
        resolved_directory = self.get_resolved_path(directory, **parameters)
        
        if check_exist and not os.path.exists(resolved_directory):
            raise FileNotFoundError(f'Directory "{resolved_directory}" does not exist')
        
        return resolved_directory
    
    def get_file(self, filename: str, check_exist: bool = False,
                 subdirectory: Optional[str] = None,
                 basename_only: bool = False, **parameters) -> str:
        """
        Get a resolved file path.

        Parameters
        ----------------------------------------------------
        filename : str
            The file name.
        check_exist : bool
            Whether to check if the file exists.
        subdirectory : str, optional
            An optional subdirectory.
        basename_only : bool, default false
            Whether to return the base name only.            
        **parameters :
            Additional parameters for formatting the path.

        Returns
        ----------------------------------------------------
        str
            The resolved file path.
        """
        if filename not in self.files:
            raise KeyError(f'Unrecognized file name "{filename}"')
        
        file = self.files[filename]
        resolved_file = self.get_resolved_path(file, subdirectory=subdirectory,
                                               basename_only=basename_only, **parameters)
        
        if check_exist and not os.path.exists(resolved_file):
            raise FileNotFoundError(f'File "{resolved_file}" does not exist')
        
        return resolved_file
    
    @staticmethod
    def check_files(files: List[str], file_only: bool = True, check_exist: bool = True):
        """
        Check if files exist and are not directories.

        Parameters
        ----------------------------------------------------
        files : list of str
            List of file paths.
        file_only : bool
            Whether to check if the paths are files only.
        check_exist : bool
            Whether to check if the files exist.
        """
        if check_exist:
            for file in files:
                if not os.path.exists(file):
                    raise FileNotFoundError(f'File "{file}" does not exist')
        
        if file_only:
            for file in files:
                if os.path.isdir(file):
                    raise IsADirectoryError(f'"{file}" is a directory')

    def get_directories(self, dirnames: Optional[List[str]] = None,
                        check_exist: bool = False, **parameters) -> Dict[str, str]:
        """
        Get resolved paths for multiple directories.

        Parameters
        ----------------------------------------------------
        dirnames : list of str, optional
            List of directory names.
        check_exist : bool
            Whether to check if the directories exist.
        **parameters :
            Additional parameters for formatting the paths.

        Returns
        ----------------------------------------------------
        dict of {str : str}
            A dictionary of resolved directory paths.
        """
        directories = {}
        if dirnames is None:
            dirnames = list(self.directories.keys())
        
        for dirname in dirnames:
            directories[dirname] = self.get_directory(dirname, check_exist=check_exist, **parameters)
        
        return directories
    
    def get_files(self, filenames: Optional[List[str]] = None,
                  check_exist: bool = False, **parameters) -> Dict[str, str]:
        """
        Get resolved paths for multiple files.

        Parameters
        ----------------------------------------------------
        filenames : list of str, optional
            List of file names.
        check_exist : bool
            Whether to check if the files exist.
        **parameters :
            Additional parameters for formatting the paths.

        Returns
        ----------------------------------------------------
            Dict[str, str]: A dictionary of resolved file paths.
        """
        files = {}
        if filenames is None:
            filenames = list(self.files.keys())
        
        for filename in filenames:
            files[filename] = self.get_file(filename, check_exist=check_exist, **parameters)
        
        return files
    
    def get_relpath(self, path: str) -> str:
        """
        Get a relative path based on the base path.

        Parameters
        ----------------------------------------------------
        path : str
            The path to make relative.

        Returns
        ----------------------------------------------------
        str
            The relative path.
        """
        if self.base_path is None:
            return path
        return os.path.join(self.base_path, path)
    
    def directory_exists(self, dirname: str, **parameters) -> bool:
        """
        Check if a directory exists.

        Parameters
        ----------------------------------------------------
        dirname : str
            The directory name.
        **parameters :
            Additional parameters for formatting the path.

        Returns
        ----------------------------------------------------
        bool
            True if the directory exists, False otherwise.
        """
        directory = self.get_directory(dirname, **parameters)
        return os.path.exists(directory)
    
    def file_exists(self, filename: str, **parameters) -> bool:
        """
        Check if a file exists.

        Parameters
        ----------------------------------------------------
        filename : str
            The file name.
        **parameters :
            Additional parameters for formatting the path.

        Returns
        ----------------------------------------------------
        bool
            True if the file exists, False otherwise.
        """
        file = self.get_file(filename, **parameters)
        return os.path.exists(file)
    
    def check_directory(self, dirname: str, **parameters):
        """
        Check if a directory exists and raise an exception if it does not.

        Parameters
        ----------------------------------------------------
        dirname : str
            The directory name.
        **parameters :
            Additional parameters for formatting the path.
        """
        self.get_directory(dirname, check_exist=True, **parameters)
            
    def check_file(self, filename: str, **parameters):
        """
        Check if a file exists and raise an exception if it does not.

        Parameters
        ----------------------------------------------------
        filename : str
            The file name.
        **parameters :
            Additional parameters for formatting the path.
        """
        self.get_file(filename, check_exist=True, **parameters)
    
    def makedirs(self, include_names: Optional[List[str]] = None,
                 exclude_names: Optional[List[str]] = None,
                 **parameters) -> None:
        """
        Create directories for the specified directory names.

        Parameters
        ----------------------------------------------------
        include_names : list of str, optional
            List of directory names to include.
        exclude_names : list of str, optional
            List of directory names to exclude.
        **parameters :
            Additional parameters for formatting the paths.
        """
        if include_names is None:
            include_names = list(self.directories.keys())
        if exclude_names is None:
            exclude_names = []
        
        dirnames = list(set(include_names) - set(exclude_names))
        resolved_dirnames = self.get_directories(dirnames, **parameters)
        
        from quickstats.utils.common_utils import batch_makedirs
        batch_makedirs(resolved_dirnames)
    
    def makedir_for_files(self, filenames: Union[str, List[str]], **parameters) -> None:
        """
        Create directories for the specified file names.

        Parameters
        ----------------------------------------------------
        filenames : str or list of str
            File name or list of file names.
        **parameters : 
            Additional parameters for formatting the paths.
        """
        if isinstance(filenames, str):
            filenames = [filenames]
        
        files = self.get_files(filenames, **parameters)
        resolved_dirnames = [os.path.dirname(file) for file in files.values()]
        from quickstats.utils.common_utils import batch_makedirs
        batch_makedirs(resolved_dirnames)
