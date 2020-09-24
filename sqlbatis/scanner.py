import os
import re
import inspect
import importlib
from sqlbatis.model import Model


class Scanner:
    """
    The basic scanner to search the files in specific folder.
    """

    def __init__(self, directory, exclude, file_type):
        """The initialization of the scanner

        :param directory: the main folder that want to search.
        :type directory: string 
        :param exclude: this should be a regrex expression list, will do the exclude 
            the file or folder according to the exclude rules.
        :type exclude: list, optional
        :param file_type: the suffix of the file, it defines the file type that you want to
            search in the directory.
        :type file_type: str, optional
        """

        self.directory = directory
        self.file_type = file_type
        self.exclude = exclude

    def _get_files_by_type(self, directory=None):
        """Retrieve all the files that according to the rules as below:
        1. file is contained in the directory
        2. the file or folder name is not match with regrex experssion in the exclude list
        3. endswith the file type that user defined

        :param directory: the directory that you want to find the file, defaults to None
        :type directory: string, optional
        :return: all matched files path
        :rtype: list of the string 
        """

        # the results list to contain the file path
        files_path = []

        # if not directory was given, use the directory that the user specified
        if not directory:
            directory = self.directory

        files = os.listdir(directory)
        for file in files:

            # if the file or folder name match with the regrex
            if_exluded = [re.search(pattern, file) for pattern in self.exclude]

            if not any(if_exluded):
                file = os.path.join(directory, file)
                if os.path.isfile(file) and file.endswith(self.file_type):
                    files_path.append(file)
                elif os.path.isdir(file):
                    # recursive to call the func
                    sub_files_path = self._get_files_by_type(file)
                    files_path.extend(sub_files_path)
                else:
                    pass

        return files_path


class ModelScanner(Scanner):

    def __init__(self, directory='.', exclude=[]):
        """The scanner for search all the model classes in the project,
        and will return all the class which inherit the sqlbatis [Model]
        class

        :param directory: the main folder that want to search, defaults to '.'
        :type directory: str, optional
        :param exclude: exlude regression, same as scanner, defaults to []
        :type exclude: list, optional
        """

        super(ModelScanner, self).__init__(directory, exclude, '.py')

        # FIXME:
        # exlude the setup.py when we try to find the py files, it will give a error that
        # dynamic import the module
        self.exclude.append('setup.py')

        self.models = {}

    def scan_models(self):
        """Scan all the sqlbatis models in the folder that user specified

        :return: SQLBatis models list 
        :rtype: list
        """
        files = self._get_files_by_type()

        # if abspath is provided, will convert it to the relative path so we can
        # dynamic import the module
        relative_files = self._convert_to_relative_path(files)

        for file in relative_files:
            _module = '.'.join(file.split(os.sep)[1:])
            _models = self._get_model_class_in_the_module(_module)
            self.models.update(_models)

        return list(self.models.values())

    def _get_model_class_in_the_module(self, path):
        """Instaniate an module and find all the classes in the module,
        and then check if the SQLBatis's [Model] or not, if yes, will added
        to models list and return


        :param path: The import path of the module
        :type path: str
        :return: SQLBatis Models
        :rtype: list
        """
        sqlbatis_models = {}

        # discard the suffix of the file
        module, _ = path.rsplit('.', maxsplit=1)
        module_instance = importlib.import_module(module)
        for name, obj in inspect.getmembers(module_instance):
            if inspect.isclass(obj) and issubclass(obj, Model):

                # abandon the orginal Model class defined in the SQLBatis
                if not obj.__name__ == 'Model':
                    sqlbatis_models[name] = obj

        return sqlbatis_models

    def _convert_to_relative_path(self, files_path):
        """Convert the abspath to the relative path

        :param files_path: all the files path's string, it may contain the relative path, we will
            process the abspath only
        :type files_path: list[str] 
        :return: all the files relative path
        :rtype: list[str] 
        """
        relative_files_path = []
        current_work_dir = os.getcwd()

        for file_path in files_path:

            # if file path is abspath, will replace the current work dir string with '.'
            if file_path.startswith('/'):
                _file_path = file_path.replace(current_work_dir, '.')
            else:
                _file_path = file_path
            relative_files_path.append(_file_path)

        return relative_files_path


if __name__ == "__main__":
    scanner = ModelScanner('.')
