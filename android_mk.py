#!/usr/bin/python
import re
import os
from sets import Set

class AndroidMk(object):
    ''' In memeory representation of Android.mk file. '''

    _RE_INCLUDE = re.compile(r'include\s+\$\((.+)\)') # include $(BUILD_PREBUILT)
    _RE_VARIABLE_REF = re.compile(r'\$\((.+)\)')
    _VAR_DELIMITER = ":="
    FILENAME = "Android.mk"
    CERTIFICATE = "LOCAL_CERTIFICATE"
    PACKAGENAME = "LOCAL_PACKAGE_NAME"

    def __init__(self):
        self._includes = set() #set
        self._variables = {} #dict
        self._has_gtestlib = False


    def _ProcessMkFileLine(self, line):
        '''
        Add a varible definition or include.

        Ignores unrecognized lines.

        :param line:
            line of text from makefile
        :return:
        '''

        m = self._RE_INCLUDE.match(line)
        if m:
            self._includes.add(m.groups(1))
        else:
            part = line.split(self._VAR_DELIMITER)
            if len(part) > 1:
                self._variables[part[0].strip()] =part[1].strip();

        if line.find('libgtest_main') != -1:
            self._has_gtestlib = True;

    def GetVaribles(self, identifer):
        '''
        Retrieve makefile variable.

        :param identifer: name of variable to retrieve

        :return:
            value of specified identifer, None if identifer not found in makefile
        '''

        # use dict.get(x) rather than dict[x] to avoid KeyError exception,
        # so None returned if identifier not found
        return self._variables.get(identifer, None);



    def GetExpandedVariable(self, identifer):
        '''
        Retrieve makefile variable.

        if variable value refers to another variable, recursivel CERTIFICATE expand it to
        find its literal value

        :param identifer:
            name of variable to retrieve

        :returns
            value of specified identifer, None if identifer not found in makefile
        '''

        return self.__RecursevieGetVariables(identifer, Set())


    def __RecursevieGetVariables(self, identifer, visited_variables):
        variable_value = self.GetVaribles(identifer)
        if not variable_value:
            return None

        if variable_value in visited_variables:
            raise RuntimeError('recursive loop found for makefile variable %s '% variable_value)

        m = self._RE_VARIABLE_REF.match(variable_value)
        if m:
            variable_ref = m.group(1)
            visited_variables.add(variable_ref)
            return self.__RecursevieGetVariables(variable_ref, visited_variables)
        else:
            return variable_value


    def HasInclude(self, identifier):
        '''
        Check variable is included in makefile.

        :param identifier:
            name of variable to check
        :return:
            True if identifer is included in makefile, otherwise False
        '''

        return identifier in self._includes

    def hasJavaLibrary(self, library_name):

        java_lib_string = self.GetExpandedVariable('LOCAL_JAVA_LIBRARIES')
        if java_lib_string:
            java_libs = java_lib_string.split( )
            return library_name in java_libs
        return False


    def HasGTest(self):
        '''
        Check if makefile includes rule to build a native gtest
        :return:
            True if rule to build native gtest is in makefile, otherwise False
        '''

        return self._has_gtestlib or self.HasInclude('BUILD_NATIVE_TEST')


    def _ParseMK(self, mk_path):
        '''
        Parse Android.mk at specified path

        :param mk_path:
            path to Android.mk
        :return:

        :raises
            IOError: Android.mk cannot be found at given path, or cannot be opened for reading
        '''
        mk = open(mk_path)

        for line in mk:
            self._ProcessMkFileLine(line)

        mk.close()


def CreateAndroidMK(path, filename=AndroidMk.FILENAME):
    '''
    Factory method for creating a AndroidMK.

    :param path:
        the directory of the make file.
    :param filename:
        the filename of make file
    :return:
        the AndroidMK or None if there was no file present
    '''

    mk_path = os.path.join(path, filename)
    print mk_path
    if os.path.isfile(mk_path):
        mk = AndroidMk()
        mk._ParseMK(mk_path)
        return mk
    else:
        return None

# mk = CreateAndroidMK('')
#
# print mk.HasInclude('BUILD_PREBUILT')