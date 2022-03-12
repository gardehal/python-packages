import re

class DocUtil:
    def generateDetailsString(filePath: str, indent: str = "    ", methodName: str = "detailsString", writeToFile: bool = True, printMethod: bool = False) -> str:
        """        
        Generate a method for getting a detailed string of object, formatted like "key1: value1, key2: value2" etc.
        Requires fields in class with "self.key1"

        Args:
            filePath (str): path to Python object to generate for (needs read/write access).
            indent (str): indent to use. Defaults to "    ".
            methodName (str): name of method. Default detailsString.
            writeToFile (bool): should method be appended to file? Default True.
            printMethod (bool): should method be printed in CLI? Default False.

        Returns:
            str: result message of writeToFile, will include string of method if printMethod
        """

        result = f"Failed to create method \"{methodName}\" for file {filePath}"
        
        if(not writeToFile and not printMethod):
            return ", ".join([result, "there are no valid output options (not writeToFile and not printMethod)."])
        
        methodDef = f"def {methodName}(self, includeUri: bool = True, includeId: bool = True, includeDatetime: bool = True) -> str:"
        methodDoc = """\"\"\"        
        Get a string of all fields in this object, formatted like "key1: value1, key2: value2" etc.

        Args:
            includeUri (bool): should include URIs? Default True.
            includeId (bool): should include IDs? Default True.
            includeDatetime (bool): should include DateTimes? Default True.

        Returns:
            str: a string of fields
        \"\"\""""
        returnHead = "return \"\".join(map(str, ["
        returnTail = "]))"
        
        template = "\"{0}: \", self.{0}" # 0 = key
        templateConditionalKey = "{0}String" # 0 = key
        templateConditional = "{0} = \", {1}: \" + str(self.{1}) if(include{2}) else \"\""  # 0 = templateConditionalKey, 1 = key, 2 = include type, e.g. "Id"
        
        fileContent = None
        try:
            with open(filePath, "r") as file:
                fileContent = file.read()
        except:
            return ", ".join([result, "no such file."])
        
        # Issues with taking ALL self.x? self.complexObject problems, self.class etc.?
        keys = re.findall("\sself\.(\w*)", fileContent)
        keys = list(dict.fromkeys(keys))
        conditionalVars = []
        joinLines = []
        for key in keys:
            joinValue = template.format(key)
            
                
            #TODO need type for keys
            if("uri" in str(key).lower()):
                conditionalKey = templateConditionalKey.format(key)
                conditionalVars.append(indent*2 + templateConditional.format(conditionalKey, key, "Uri"))
                joinValue = conditionalKey
            
            if("Id" in key or key == "id"):
                conditionalKey = templateConditionalKey.format(key)
                conditionalVars.append(indent*2+ templateConditional.format(conditionalKey, key, "Id"))
                joinValue = conditionalKey
            
            if("datetime" in str(key).lower()):
                conditionalKey = templateConditionalKey.format(key)
                conditionalVars.append(indent*2 + templateConditional.format(conditionalKey, key, "Datetime"))
                joinValue = conditionalKey
                
            joinLines.append(indent*3 + joinValue)
    
        method = indent*1 + methodDef
        method += "\n"
        method += indent*2 + methodDoc
        method += "\n\n"
        method += "\n".join(conditionalVars)
        method += "\n\n"
        method += indent*2 + returnHead
        method += "\n"
        method += ",\n".join(joinLines)
        method += "\n"
        method += indent*2 + returnTail
            
        if(writeToFile):
            result = f"Generated method \"{methodName}\" for file {filePath}"
            
            try:
                with open(filePath, "a") as file:
                    fileContent = file.write("\n" + method)
            except:
                result = ", ".join([result, "and appended to file. Please double check indentation."])
            
        if(printMethod):
            result = "\n\n".join([result, method])

        return result