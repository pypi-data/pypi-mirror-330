import json

class Utils():
    """
    Class with some utlity methods that can be reused

    Methods
    -------
    parse_to_list(input, tech, delimiter=None)
        Parses a json object to a list of strings
    
    """
    
    __token_technologies__ = ['pos', 'ner', 'pc', 'lemma', 'morph', 'upos']
    
    def parse_to_list(input: json, tech: str, delimiter: str=None):
        """
        Parses the json object to a list
        
        :param (json) input: The json result from running the annotate function in client
        :param (str) tech: The core technology used to annotate the input text
        :param (str) delimiter: The delimiter to use between a token and annotation, optional

        :return: A list of the tokens and annotations
        :rtype: list[str] | list[tuple] | Any
        """
        if input == None:
            return []
        result = []
        tech = tech.lower() if tech else ''
        if (type(input) is list):
            for item in input:
                result.append(Utils.parse_to_list(item, tech, delimiter))
                
            if (len(result) == 1
            and
            isinstance(result[0], list)):
                # to flatten the array structure
                # don't create lists with only a single element
                # rather make that element the root
                # unless that element is just a raw string:
                return result[0]
            else:
                return result
        elif (type(input) is str):
            #LID
            if tech == 'lid':
                return [input]
            else:
                 return input

        for key, val in input.items():
            if tech == 'ocr':
                return[(key, val)]
            if (key == 'lid'):
                if (tech == 'lid'):
                    # LID only returns a single value for the detected language and shouldn't be reconstructed in an array  structure
                    return val
            elif key == 'tokens':
                if tech == 'sent':
                    # Sentence separation should return each of the original sentences
                    # as separate items in the list
                    result.append(Utils.__result_to_original_string__(input))
                else:
                    if (not isinstance(val, list)):
                        # Single words should still be lists for list comprehension below
                        val = [val]
                    if tech in Utils.__token_technologies__:
                        if (delimiter):
                            # When delimited output is requested, each token is added with the delimiter
                            # and the associated annotations for the technology
                            if (type(val) is list):
                                result = [str(item['text']) + delimiter + item[tech] for item in val]
                            else:
                                # This is a single item, so return immediately
                                return [str(val['text']) + delimiter + val[tech]]
                        else:
                            # add each token and associated technology output as tuples
                            # in the array
                            if (type(val) is list):
                                result = [(str(item['text']), item[tech]) for item in val]
                            else:
                                # This is a single item, so return immediately
                                return [(str(val['text']), val[tech])]
                    else:
                        result = [str(item['text']) for item in val]
            elif (type(val) is bool):
                continue
            else:
                result.append(Utils.parse_to_list(val, tech, delimiter))

        if (len(result) == 1
            and
            isinstance(result[0], list)):
            # to flatten the array structure
            # don't create lists with only a single element
            # rather make that element the root
            # unless that element is just a raw string:
            return result[0]
        else:
            return result

    def __result_to_original_string__(result: json):
        if result == None:
            return ''
        orig_string = ''
        if (type(result) is list):
            for item in result:
                orig_string.join(Utils.__result_to_original_string__(item))
        elif type(result) is dict:
            for key, val in result.items():
                if key == 'tokens':
                    if type(val) is list:
                        token_values = [str(t['text']) for t in val]
                    else:
                        token_values = val['text']
                    return ' '.join(token_values)
        
        return orig_string

__all__ = ["Parse_To_List"]