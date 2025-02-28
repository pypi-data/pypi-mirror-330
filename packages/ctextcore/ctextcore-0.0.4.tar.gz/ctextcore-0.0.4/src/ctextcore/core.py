"""
A basic client for the CTexTCore library of core technologies
"""
import os
from pathlib import Path
from ctextcore.server.client import CTexTCoreTechClient as cctc
from ctextcore.server.client import PermanentlyFailedException
from typing import Union

class CCore():
    """
    A simple class for loading the necessary libraries, getting available languages and core technologies
    and annotating text with one of the technologies

    Methods
    -------
    list_available_techs()
        Get a dictionary with the available technologies and languages supported and available
    get_available_languages(tech=None)
        Get the available languages for a particular technology
    check_for_updates()
        Check to see if updates are available for any of the currently downloaded models
    process_text(text_input, language='zu', tech='tok', confidence=0.0, output_format='json',
                delimiter='_')
        Process text or a file with the specified technology for the specified language
    download_model(tech, language)
        Download the required model for a particular technology and language
    """

    __server__: cctc = None

    def __init__(self, **kwargs) -> None:
        load_path = Path(os.path.dirname(os.path.abspath(__file__)), 'core', 'CTexTCore-2.0.jar')

        # To load cpp libaries correctly, the relevant path should be added to the environment
        lib_path = load_path.parent.joinpath('models/lib')
        if (not lib_path.exists()):
            lib_path.mkdir(parents=True)
        os.environ['LD_LIBRARY_PATH'] = str(lib_path)
        if not load_path.exists():
            raise PermanentlyFailedException('The required java library CTexTCore-2.0.jar \
                                             could not be found in the expected location {}.\n\
                                             Please ensure that the file is in the expected location,\
                                              or reinstall by running\n pip install ctext-core')
        self.__server__ = cctc(classpath=load_path.as_posix(), **kwargs)
        pass
    
    def list_available_techs(self):
        """
        Returns a list of the core technologies that are available, irrespective of whether they
        have been dowonloaded or not
        """

        result = self.__server__.get_available_tech_langs()
        return result

    def get_available_languages(self, tech:str = None):
        """
        Returns a list of languages available for a specific core technology

        :param (str) tech: the name of the core technology for which to return the list of languages
        (tok, sent, pos, pc, ner, ocr, lid)
        """

        if (tech):
            result = self.__server__.get_available_languages(tech)
        else:
            return self.list_available_techs()
        return result

    def check_for_updates(self):
        """
        Checks to determine if there are updates available for any of the 
        previously downloaded models.
        """

        result = self.__server__.check_for_updates()
        return result
    
    def process_text(self, text_input:Union[str, Path], 
                     language: str = 'zu', 
                     tech: str = 'tok', 
                     confidence: float = 0.0,
                     output_format: str = "json",
                     delimiter: str = '_'):
        """
        Send a processing request to the CTexTCoreTech server

        :param (str | Path) text_input: raw text or file to process with CoreTech
        :param (str) language: one of the languages supported by Coretech (af, nr, nso, \
            ss, st, tn, ts, xh, zu)
        :param (str) tech: Core technology to use for processing (tok, sent, pos, pc, ner, ocr, lid)
        :param (float) confidence: Only necessary for LID. \
            The confidence level at which to classify language identification
        :param (str) output_format: Specify the format of the output (json, list, delimited)
        :param (str) delimiter: Only required for delimited output, where this should be the character
            linking the token and the technology output.
        """

        if (text_input == None):
            raise ValueError('No text or files specified for processing.')
        elif (isinstance(text_input, Path) 
              and (not text_input.exists())):
            raise ValueError('The specified path does not exists: {}'.format(text_input.absolute()))
        
        available_tech = self.__server__.get_available_tech_langs()
        tech_langs = available_tech.get(tech, None)
        # Normalise both tech and lang to lowercase to ensure correct behaviour
        # None values can rather be empty string to display the available languages
        # or technologies
        if (tech):
            tech = tech.lower()
            if (tech == 'ocr'
                and
                not isinstance(text_input, Path)):
                    raise ValueError('OCR can only process files (jpg, pdf, bmp, tiff, png). Please specify a Path() object as input_text.')
        else:
            tech = ''
        if (language 
            and 
            not language.isspace()):
            language = language.lower()
        else:
            raise ValueError('No language value specified.\nPlease specify one of the following langauges:\n\t{0}'
                             .format('\n\t'.join(available_tech['tok'])))
        
        if (not tech_langs):
            if tech.lower() not in available_tech:
                raise ValueError("""The specified core technology: {0} is not available in this package. 
                                  Please select one of the options from the following list:\n\t{1}"""
                                 .format(tech, '\n\t'.join(list(available_tech.keys()))))
            else:
                print('The specified core technology: {0} is not installed yet.'.format(tech))
                should_download = input('Would you like to download and install the model for the specified language? (Y/N)')
                if (should_download.lower() == 'y'):
                    self.download_model(tech=tech, language=language)
                    available_tech = self.__server__.get_available_tech_langs()
                    tech_langs = None if tech == None else available_tech.get(tech, None)
                else:
                    return
        
        if not language in tech_langs:
            print("""The specified language: {0} is not available for {1}. 
            The following language models have already been installed:""".format(language, tech))
            for x in tech_langs:
                print('\t{0}'.format(x))
            download = input('Would you like to download a model for the specified language? (Y/N)')
            if (download.lower() == 'y'):
                self.download_model(tech=tech, language=language)
            else:
                return
            
        return self.__server__.annotate(text_input, annotator=tech, lang=language, confidence=confidence, 
                                        output_format=output_format, delimiter=delimiter)

    def download_model(self, tech:str = '', language:str = ''):
        """
        Send a request to the server to download a model for a particular language

        :param (str | Unicode) tech: the technology to download (tok, sent, lid, ner, pc, pos, ocr)
        :param (str | Unicode) language: the language which should be downloaded
        """
        
        self.__server__.download_model(lang=language, tech=tech)
