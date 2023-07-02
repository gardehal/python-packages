from typing import List
from grdUtil.PrintUtil import printS

class FlagValues():
    def __init__(self,
                 found: bool,
                 values: List[str],
                 flagIndex: int,
                 valueIndices: List[int],
                 argumentsConsumed: int,
                 previousArguments: List[str],
                 nextArguments: List[str],
                 arguments: List[str],
                 flagAliases: List[str],
                 defaultValue: any = None):
        self.found: bool = found
        self.values: List[str] = values
        self.flagIndex: int = flagIndex
        self.valueIndices: List[int] = valueIndices
        self.argumentsConsumed: int = argumentsConsumed
        self.previousArguments: List[str] = previousArguments
        self.nextArguments: List[str] = nextArguments
        self.arguments: List[str] = arguments
        self.flagAliases: List[str] = flagAliases
        self.defaultValue: any = defaultValue

class FlagValuesUtil():
    def printValues(values: FlagValues):
        """
        Print contents of FileResult.

        Args:
            result (FileResult): Object to print contents of.
        """

        printS("Flags found:        ", values.found)
        printS("Values:             ", values.values)
        printS("Flag index:         ", values.flagIndex)
        printS("Value indices:      ", values.valueIndices)
        printS("Arguments consumed: ", values.argumentsConsumed)
        printS("Previous arguments: ", values.previousArguments)
        printS("Next arguments:     ", values.nextArguments)
        printS("Arguments:          ", values.arguments)
        printS("Flag aliases:       ", values.flagAliases)
        printS("Default value:      ", values.defaultValue)