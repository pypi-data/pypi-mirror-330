
"""
A simple interface for a server-based interface to the Java CTexTCoreTech in Python
Based on the Python interface for Stanford CoreNLP (https://github.com/stanfordnlp/python-stanford-corenlp)
"""

import atexit
import contextlib
import enum
import os
from pathlib import Path
from os import PathLike
from typing import List, Dict, Union
import requests
import logging
import shlex
import socket
import subprocess
import time
import urllib.parse
from ctextcore.server.utils import Utils


from datetime import datetime
from pathlib import Path

__original_authors__ = 'arunchaganty, kelvinguu, vzhong, wmonroe4'
__updates_authors__ = 'roalde, ricokoen'

logger = logging.getLogger('ctext')

class AnnotationException(Exception):
    """ Exception raised when there was an error communicating with the CTexTCoreTech server. """
    pass

class TimeoutException(AnnotationException):
    """ Exception raised when the CTexTCoreTech server timed out. """
    pass

class ShouldRetryException(Exception):
    """ Exception raised if the service should retry the request. """
    pass

class PermanentlyFailedException(Exception):
    """ Exception raised if the service should NOT retry the request. """
    pass

class StartServer(enum.Enum):
    DONT_START = 0
    FORCE_START = 1
    TRY_START = 2

class RobustService(object):
    """ Service that resuscitates itself if it is not available. """

    CHECK_ALIVE_TIMEOUT = 120
    CTEXT_CORE_RESOURCES = os.environ.get('CTEXT_CORE_RESOURCES')

    def __init__(self, start_cmd, stop_cmd, endpoint, stdout=None,
                 stderr=None, be_quiet=False, host=None, port=None, ignore_binding_error=False):
        self.start_cmd = start_cmd and shlex.split(start_cmd)
        self.stop_cmd = stop_cmd and shlex.split(stop_cmd)
        self.endpoint = endpoint
        self.stdout = stdout
        self.stderr = stderr

        self.server = None
        self.is_active = False
        self.be_quiet = be_quiet
        self.host = host
        self.port = port
        self.ignore_binding_error = ignore_binding_error
        atexit.register(self.atexit_kill)

    def is_alive(self):
        try:
            if not self.ignore_binding_error and self.server is not None and self.server.poll() is not None:
                return False
            return requests.get(self.endpoint).ok
        except requests.exceptions.ConnectionError as e:
            raise ShouldRetryException(e)

    def start(self):
        if self.start_cmd:
            if self.host and self.port:
                with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                    try:
                        sock.bind((self.host, self.port))
                    except socket.error:
                        if self.ignore_binding_error:
                            logger.info(f"Connecting to existing CTexTCoreTech server at {self.host}:{self.port}")
                            self.server = None
                            return
                        else:
                            raise PermanentlyFailedException("Error: unable to start the CTexTCoreTech server on port %d "
                                                        "(possibly something is already running there)" % self.port)
            if self.be_quiet:
                # Issue #26: subprocess.DEVNULL isn't supported in python 2.7.
                if hasattr(subprocess, 'DEVNULL'):
                    stderr = subprocess.DEVNULL
                else:
                    stderr = open(os.devnull, 'w')
                stdout = stderr
            else:
                stdout = self.stdout
                stderr = self.stderr
            logger.info(f"Starting server with command: {' '.join(self.start_cmd)}")
            try:
                self.server = subprocess.Popen(self.start_cmd,
                                            stderr=stderr,
                                            stdout=stdout)
            except ShouldRetryException as e:
                raise AssertionError('ERROR: Could not launch java as expected. Please review java installation.' +
                                     ' If the error persists, please log an issue on github.') from e
            except FileNotFoundError as e:
                raise FileNotFoundError('When trying to run CTexTCoreTech, a FileNotFoundError occurred, ' + 
                                        'which frequently means Java was not installed or was not in the classpath.') from e

    def atexit_kill(self):
        # make some kind of effort to stop the service (such as a
        # CTexTCoreTech server) at the end of the program.  not waiting so
        # that the python script exiting isn't delayed
        if self.server and self.server.poll() is None:
            self.server.terminate()

    def stop(self):
        if self.server:
            self.server.terminate()
            try:
                self.server.wait(5)
            except subprocess.TimeoutExpired:
                # Resorting to more aggressive measures...
                self.server.kill()
                try:
                    self.server.wait(5)
                except subprocess.TimeoutExpired:
                    # oh well
                    pass
            self.server = None
        if self.stop_cmd:
            subprocess.run(self.stop_cmd, check=True)
        self.is_active = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, _, __, ___):
        self.stop()

    def ensure_alive(self):
        # Check if the service is active and alive
        if self.is_active:
            try:
                if self.is_alive():
                    return
                else:
                    self.stop()
            except ShouldRetryException:
                pass

        # If not, try to start up the service.
        if self.server is None:
            self.start()

        # Wait for the service to start up.
        start_time = time.time()
        while True:
            try:
                if self.is_alive():
                    break
            except ShouldRetryException:
                pass

            if time.time() - start_time < self.CHECK_ALIVE_TIMEOUT:
                time.sleep(1)
            else:
                raise PermanentlyFailedException("Timed out waiting for service to come alive.")

        # At this point we are guaranteed that the service is alive.
        self.is_active = True

    def resolve_classpath(self, classpath=None):
        """
        Returns the classpath to use for CTexTCoreTech.

        Prefers to use the given classpath parameter, if available.  If
        not, uses the CTEXT_CORE_HOME environment variable.  Resolves $CLASSPATH
        (the exact string) in either the classpath parameter or $CTEXT_CORE_HOME.
        """

        if classpath == '$CLASSPATH' or (classpath is None and os.getenv("CTEXT_CORE_HOME", None) == '$CLASSPATH'):
            classpath = os.getenv("CLASSPATH")
        elif classpath is None:
            classpath = os.getenv("CTEXT_CORE_HOME", os.path.join(str(Path.home()), 'CTEXT_CORE_HOME'))

            if not os.path.exists(classpath):
                raise FileNotFoundError("The required java library CTexTCore-2.0.jar \
                                                could not be found in the expected location {}.\n\
                                                Please ensure that the file is in the expected location,\
                                                or reinstall by running\n pip install ctext-core. If you have installed it, please define "
                                        "$CTEXT_CORE_HOME to be location of your CTexTCoreTech distribution or pass in a classpath parameter.  "
                                        "$CTEXT_CORE_HOME={}".format(os.getenv("CTEXT_CORE_HOME"), os.getenv("CTEXT_CORE_HOME")))
            classpath = os.path.join(classpath, "*")
        return classpath

class CTexTCoreTechClient(RobustService):
    """ A client to the CTexTCoreTech server. 
    
    Methods
    -------
    check_for_updates()
        Check whether updates to current models are available
    annotate(text, annotator=None, lang=None, line_level=True,
             confidence=0.0, output_format=None, delimiter='_',
             properties=None, reset_default=None)
        Annotates the text with the specified annotator for the specified language
    get_available_tech_langs()
        Return a list the available languages and technologies supported by the current version
    get_available_languages_for_tech(tech=None)
        Return a list of the languages for which a specified technology is available
    download_model(lang, tech)
        Download the required models for a specified language and technology
    """

    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 8079
    DEFAULT_TIMEOUT = 600
    DEFAULT_THREADS = 5
    DEFAULT_OUTPUT_FORMAT = "json"
    DEFAULT_MEMORY = "4G"
    DEFAULT_MAX_CHAR_LENGTH = 10000

    OUTPUT_FORMATS = ['json', 'delimited', 'list', 'array']

    # Check if str is CTexTCoreTech supported language
    CORE_TECHS_AVAILABLE: Dict[str, List[str]] = None

    def __init__(self, start_server=StartServer.TRY_START,
                 host: str=DEFAULT_HOST,
                 port: int=DEFAULT_PORT,
                 timeout: int=DEFAULT_TIMEOUT,
                 threads=DEFAULT_THREADS,
                 output_format=None,
                 properties=None,
                 stdout=None,
                 stderr=None,
                 memory=DEFAULT_MEMORY,
                 be_quiet=False,
                 max_char_length=DEFAULT_MAX_CHAR_LENGTH,
                 classpath=None,
                 **kwargs):

        # whether or not server should be started by client
        self.start_server = start_server
        self.server_props_path = None
        self.server_start_time = None
        self.server_host = None
        self.server_port = None
        self.server_classpath = None

        # set up client defaults
        self.properties = properties
        self.output_format = output_format
        
        # start the server
        if start_server is StartServer.FORCE_START or start_server is StartServer.TRY_START:
            # record info for server start
            self.server_start_time = datetime.now()
            
            assert host == "127.0.0.1", "If starting a server, endpoint must be 127.0.0.1"
            classpath = self.resolve_classpath(classpath)

            java_path = os.getenv("JAVA_HOME")
            if (java_path
                and
                not Path(f"{java_path}/bin/").exists()):
                print(f"The specified JAVA_HOME path does not contain the required java binary.\n({java_path}/bin/)\n" +
                      "Attempting to use default java installation.")
                java_path = None
                
            if (java_path):
                java_path = java_path.replace('\\', '/')
                start_cmd = f"{java_path}/bin/java -Xmx{memory} -cp '{classpath}' za.ac.nwu.ctext.server.Server " \
                            f"-port {port} -timeout {timeout} -threads {threads}"
            else:
                start_cmd = f"java -Xmx{memory} -cp {classpath} za.ac.nwu.ctext.server.Server " \
                            f" -port {port} -timeout {timeout} -threads {threads}"

            self.server_classpath = classpath
            self.server_host = host
            self.server_port = port
            
            stop_cmd = None
        else:
            start_cmd = stop_cmd = None
            host = port = None

        endpoint = ''.join(['http://', host, ':', str(port)])
        super(CTexTCoreTechClient, self).__init__(start_cmd, stop_cmd, endpoint,
                                            stdout, stderr, be_quiet, host=host, port=port, ignore_binding_error=(start_server == StartServer.TRY_START))

        self.timeout = timeout

    def __validate_annotator_options__(self, core:str, lang:str, **kwargs):
        if (self.CORE_TECHS_AVAILABLE == None):
            self.__init_annotator_options__()
        
        if (core.lower() in self.CORE_TECHS_AVAILABLE):
            if lang.lower() in self.CORE_TECHS_AVAILABLE[core.lower()]:
                return
            raise ValueError(f"Unrecognized language for {core}: {lang}")
        raise ValueError(f"Unrecognized Core Technology: {core}")

    def __request__(self, buf, properties, reset_default=False, **kwargs):
        """
        Send a request to the CTexTCoreTech server.

        :param (str | bytes) buf: data to be sent with the request
        :param (dict) properties: properties that the server expects
        :return: request result
        """
        self.ensure_alive()
        try:
            input_format = properties.get("inputFormat", "text")
            if input_format == "text":
                ctype = "text/html; charset=utf-8"
            elif input_format == "serialized":
                ctype = "application/x-protobuf"
            else:
                raise ValueError("Unrecognized inputFormat " + input_format)
            
            params = '&'.join(f'{k}={v}' for k,v in properties.items())
            r = requests.post(self.endpoint,
                              params=params,
                              data=buf, headers={'content-type': ctype, 'Connection': 'keep-alive'},
                              timeout=self.timeout, **kwargs)
            r.raise_for_status()
            return r
        except requests.HTTPError as e:
            if r.text == "CTexTCoreTech request timed out. Your document may be too long.":
                raise TimeoutException(r.text)
            else:
                raise AnnotationException(r.text)

    def __init_annotator_options__(self, **kwargs):
        self.CORE_TECHS_AVAILABLE = {}
        self.ensure_alive()
        r = self.__request__(None, {'available': None}, False, **kwargs)
        temp = r.json()
        for k, v in temp.items():
            variants = str(k.lower()).split('\t')
            for item in variants:
                self.CORE_TECHS_AVAILABLE[item.lower()] = [v_i.lower() for v_i in v]
        return
    
    def check_for_updates(self, **kwargs):
        """
        Requests the service to determine if updates for any of the existing
        models are avaialble
        """
        self.ensure_alive()
        r = self.__request__(None, {'updates': 'true'}, False, **kwargs)
        temp = r.json()
        if(len(temp) == 0) :
            print("No updates available.")
            return
        else:
            for updates in temp:
                for technology in updates:
                    for language, version in updates[technology].items():
                        print("Version {0} is avilable for {1} {2}".format(str(version),str(technology),str(language)))
            return

    def annotate(self, text: Union[str, Path], annotator: str=None, lang:str =None, line_level: bool=True,
                 confidence: float = 0.0,
                 output_format: str =None, delimiter: str='_',
                 properties: Dict[str, str]=None, 
                 reset_default=None, **kwargs):
        """
        Send a request to the CTexTCoreTech server to annotate a string or file 
        with the requested core technology.

        :param (str | unicode) text: raw text for the CTexTCoreTechServer to parse
        :param (list | string) annotators: list of annotators to use
        :param (str) output_format: output type from server: json, list, or delimited 
        :param (dict) properties: additional request properties (written on top of defaults)
        :param (bool) reset_default: don't use server defaults
        :param (str) delimiter: Only required for delimited output, where this is should be the character
            linking the token and the technology output.

        Precedence for settings:

        1. annotators and output_format args
        2. Values from properties dict
        3. Client defaults self.output_format (set during client construction)
        4. Server defaults

        Additional request parameters (apart from CTexTCoreTech pipeline properties) such as 'username' and 'password'
        can be specified with the kwargs.

        :return: request result
        """

        # before we try to annotate, verify language and annotator values
        self.__validate_annotator_options__(lang=lang, core=annotator)
        
        # set request properties
        request_properties = {}

        # start with client defaults
        if self.output_format is not None:

            request_properties['outputFormat'] = self.output_format

        # add values from properties arg
        # handle str case
        #if type(properties) == str:
        #    if is_available_language(lang):
        #        properties = {'lang': properties.lower()}
        #        if reset_default is None:
        #            reset_default = True
        #    else:
        #        raise ValueError(f"Unrecognized properties keyword {properties}")

        if type(properties) == dict:
            request_properties.update(properties)

        # if annotators list is specified, override with that
        # also can use the annotators field the object was created with
        if (annotator is not None 
            and 
            (type(annotator) == str )):
            request_properties['core'] = annotator if type(annotator) == str else ",".join(annotator)

        if isinstance(text, PathLike):
            request_properties['file'] = urllib.parse.quote(str(text.resolve()))
        else:
            request_properties['text'] = urllib.parse.quote(text)
        
        #if is_available_language(lang):
        request_properties['lang'] = lang
        request_properties['line'] = line_level
        request_properties['confidence'] = confidence

        # if output format is specified, override with that
        if output_format is not None and type(output_format) == str:
            if (output_format.lower() not in self.OUTPUT_FORMATS):
                print('Unsupported output format specified.\n'
                      'Only {} supported.\n'
                      'Reverting to default json format'.format(self.OUTPUT_FORMATS))
                output_format = self.OUTPUT_FORMATS[0]
            request_properties['outputFormat'] = output_format.lower()
        else:
            request_properties['outputFormat'] = self.OUTPUT_FORMATS[0]

        # make the request
        # if not explicitly set or the case of pipelineLanguage, reset_default should be None
        try:
            if reset_default is None:
                reset_default = False
            r = self.__request__(None, request_properties, reset_default, **kwargs)

            r.raise_for_status()
            if request_properties["outputFormat"] == "json":
                return r.json()
            elif request_properties["outputFormat"] == "list" or request_properties['outputFormat'] == 'array':
                return Utils.parse_to_list(r.json(), request_properties['core'])
            elif request_properties["outputFormat"] == "delimited":
                return Utils.parse_to_list(r.json(), request_properties['core'], delimiter)
            # TODO: Add Connlu output
            else:
                return r
        except requests.exceptions.ConnectionError as e:
            # If another instance of the server was closed, which this instance was using,
            # this error will be thrown.
            # rather than thowing - send a warning to retry, which should create a new service
            print('It seems another hosted version has been closed, ' 
                  + 'and the current process couldn\'t be completed. Please try again.\n'
                  + 'If the problem persist, please log an issue.')
            return {}
        except Exception as e:
            raise e

    def get_available_tech_langs(self) -> Dict[str, List[str]]:
        """
        Send a request to the service to determine which core technologies
        are available

        :return: a dictionary of available technologies and languages for each technology
        :rtype: Dict[str, List[str]]
        """

        if (self.CORE_TECHS_AVAILABLE == None):
            self.__init_annotator_options__()
        
        return self.CORE_TECHS_AVAILABLE

    def get_available_languages_for_tech(self, tech: str = None) -> List[str]:
        """
        Send a request to the service to determine which core technologies 
        are available for a particular language
        
        :param (str | unicode) tech: the specific core technology to determine\
            available languages, optional

        :returns: a list of languages for which technology is available
        :rtype: List[str]
        """

        if (not tech):
            return None
        
        if (self.CORE_TECHS_AVAILABLE == None):
            self.__init_annotator_options__()
        
        if tech.lower() in self.CORE_TECHS_AVAILABLE:
            return self.CORE_TECHS_AVAILABLE.get(tech.lower(), None)
    
    def download_model(self, lang: str, tech:str):
        """
        Send a request to the service to download a specific technology
        for a specific language
        :param (str | unicode) lang: The language for which to try and download a technology
        :param (str | unicode) tech: The core technology and dependencies that should be downloaded
        
        :return: the response from the service request
        :rtype: Response
        """
        if lang == None:
            lang = ''
        if tech == None:
            tech = ''

        self.ensure_alive()

        try:
            params = '&'.join(['lang=' + lang, 'core=' + tech, 'download=true'])
            r = requests.post(self.endpoint,
                              params=params,
                              headers={'Connection': 'keep-alive'},
                              timeout=(self.timeout))
            r.raise_for_status()

            # Reset the avaialble core techs, as this could have changed
            # due to new models being downloaded
            self.CORE_TECHS_AVAILABLE = None

            return r
        except requests.HTTPError as e:
            if r.text == "CTexTCoreTech request timed out. The download server may be unavailable.":
                raise TimeoutException(r.text)
            else:
                raise AnnotationException(r.text)

__all__ = ["CTexTCoreTechClient", "AnnotationException", "TimeoutException", "to_text"]