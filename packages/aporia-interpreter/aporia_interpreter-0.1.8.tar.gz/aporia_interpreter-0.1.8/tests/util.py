import aporia.parser.parser as parser
import aporia.interpreter as interpreter

def interpret(source:str):
    ast = parser.parse(source)
    return interpreter.InterpLcfi().interp(ast)
