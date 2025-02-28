# Generated from CcpnPKParser.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,37,171,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,3,0,18,8,0,1,0,1,0,1,0,1,0,5,0,24,8,0,10,0,12,0,27,
        9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,4,1,47,8,1,11,1,12,1,48,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,4,2,65,8,2,11,2,12,2,66,1,2,1,2,1,3,
        1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,
        1,3,1,3,4,3,90,8,3,11,3,12,3,91,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,4,4,111,8,4,11,4,12,4,112,1,
        4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,
        5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,4,5,139,8,5,11,5,12,5,140,1,6,1,6,
        1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,
        1,6,1,6,4,6,163,8,6,11,6,12,6,164,1,6,1,6,1,7,1,7,1,7,0,0,8,0,2,
        4,6,8,10,12,14,0,6,2,0,14,14,18,18,2,0,15,15,19,19,1,1,10,10,2,0,
        16,16,20,20,2,0,17,17,21,21,1,0,3,4,173,0,17,1,0,0,0,2,30,1,0,0,
        0,4,50,1,0,0,0,6,70,1,0,0,0,8,93,1,0,0,0,10,116,1,0,0,0,12,142,1,
        0,0,0,14,168,1,0,0,0,16,18,5,10,0,0,17,16,1,0,0,0,17,18,1,0,0,0,
        18,25,1,0,0,0,19,24,3,2,1,0,20,24,3,6,3,0,21,24,3,10,5,0,22,24,5,
        10,0,0,23,19,1,0,0,0,23,20,1,0,0,0,23,21,1,0,0,0,23,22,1,0,0,0,24,
        27,1,0,0,0,25,23,1,0,0,0,25,26,1,0,0,0,26,28,1,0,0,0,27,25,1,0,0,
        0,28,29,5,0,0,1,29,1,1,0,0,0,30,31,5,1,0,0,31,32,5,13,0,0,32,33,
        7,0,0,0,33,34,7,1,0,0,34,35,5,22,0,0,35,36,5,23,0,0,36,37,5,26,0,
        0,37,38,5,27,0,0,38,39,5,28,0,0,39,40,5,29,0,0,40,41,5,32,0,0,41,
        42,5,33,0,0,42,43,5,34,0,0,43,44,5,35,0,0,44,46,5,37,0,0,45,47,3,
        4,2,0,46,45,1,0,0,0,47,48,1,0,0,0,48,46,1,0,0,0,48,49,1,0,0,0,49,
        3,1,0,0,0,50,51,5,2,0,0,51,52,5,2,0,0,52,53,5,3,0,0,53,54,5,3,0,
        0,54,55,5,8,0,0,55,56,5,8,0,0,56,57,3,14,7,0,57,58,3,14,7,0,58,59,
        5,3,0,0,59,60,5,3,0,0,60,61,5,3,0,0,61,62,5,8,0,0,62,64,5,8,0,0,
        63,65,5,8,0,0,64,63,1,0,0,0,65,66,1,0,0,0,66,64,1,0,0,0,66,67,1,
        0,0,0,67,68,1,0,0,0,68,69,7,2,0,0,69,5,1,0,0,0,70,71,5,1,0,0,71,
        72,5,13,0,0,72,73,7,0,0,0,73,74,7,1,0,0,74,75,7,3,0,0,75,76,5,22,
        0,0,76,77,5,23,0,0,77,78,5,24,0,0,78,79,5,26,0,0,79,80,5,27,0,0,
        80,81,5,28,0,0,81,82,5,29,0,0,82,83,5,30,0,0,83,84,5,32,0,0,84,85,
        5,33,0,0,85,86,5,34,0,0,86,87,5,35,0,0,87,89,5,37,0,0,88,90,3,8,
        4,0,89,88,1,0,0,0,90,91,1,0,0,0,91,89,1,0,0,0,91,92,1,0,0,0,92,7,
        1,0,0,0,93,94,5,2,0,0,94,95,5,2,0,0,95,96,5,3,0,0,96,97,5,3,0,0,
        97,98,5,3,0,0,98,99,5,8,0,0,99,100,5,8,0,0,100,101,5,8,0,0,101,102,
        3,14,7,0,102,103,3,14,7,0,103,104,5,3,0,0,104,105,5,3,0,0,105,106,
        5,3,0,0,106,107,5,3,0,0,107,108,5,8,0,0,108,110,5,8,0,0,109,111,
        5,8,0,0,110,109,1,0,0,0,111,112,1,0,0,0,112,110,1,0,0,0,112,113,
        1,0,0,0,113,114,1,0,0,0,114,115,7,2,0,0,115,9,1,0,0,0,116,117,5,
        1,0,0,117,118,5,13,0,0,118,119,7,0,0,0,119,120,7,1,0,0,120,121,7,
        3,0,0,121,122,7,4,0,0,122,123,5,22,0,0,123,124,5,23,0,0,124,125,
        5,24,0,0,125,126,5,25,0,0,126,127,5,26,0,0,127,128,5,27,0,0,128,
        129,5,28,0,0,129,130,5,29,0,0,130,131,5,30,0,0,131,132,5,31,0,0,
        132,133,5,32,0,0,133,134,5,33,0,0,134,135,5,34,0,0,135,136,5,35,
        0,0,136,138,5,37,0,0,137,139,3,12,6,0,138,137,1,0,0,0,139,140,1,
        0,0,0,140,138,1,0,0,0,140,141,1,0,0,0,141,11,1,0,0,0,142,143,5,2,
        0,0,143,144,5,2,0,0,144,145,5,3,0,0,145,146,5,3,0,0,146,147,5,3,
        0,0,147,148,5,3,0,0,148,149,5,8,0,0,149,150,5,8,0,0,150,151,5,8,
        0,0,151,152,5,8,0,0,152,153,3,14,7,0,153,154,3,14,7,0,154,155,5,
        3,0,0,155,156,5,3,0,0,156,157,5,3,0,0,157,158,5,3,0,0,158,159,5,
        3,0,0,159,160,5,8,0,0,160,162,5,8,0,0,161,163,5,8,0,0,162,161,1,
        0,0,0,163,164,1,0,0,0,164,162,1,0,0,0,164,165,1,0,0,0,165,166,1,
        0,0,0,166,167,7,2,0,0,167,13,1,0,0,0,168,169,7,5,0,0,169,15,1,0,
        0,0,9,17,23,25,48,66,91,112,140,164
    ]

class CcpnPKParser ( Parser ):

    grammarFileName = "CcpnPKParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'Number'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'#'", "'Position F1'", "'Position F2'", 
                     "'Position F3'", "'Position F4'", "'Shift F1'", "'Shift F2'", 
                     "'Shift F3'", "'Shift F4'", "'Assign F1'", "'Assign F2'", 
                     "'Assign F3'", "'Assign F4'", "'Height'", "'Volume'", 
                     "'Line Width F1 (Hz)'", "'Line Width F2 (Hz)'", "'Line Width F3 (Hz)'", 
                     "'Line Width F4 (Hz)'", "'Merit'", "'Details'", "'Fit Method'", 
                     "'Vol. Method'" ]

    symbolicNames = [ "<INVALID>", "Number", "Integer", "Float", "Real", 
                      "SHARP_COMMENT", "EXCLM_COMMENT", "SMCLN_COMMENT", 
                      "Simple_name", "SPACE", "RETURN", "SECTION_COMMENT", 
                      "LINE_COMMENT", "Id", "Position_F1", "Position_F2", 
                      "Position_F3", "Position_F4", "Shift_F1", "Shift_F2", 
                      "Shift_F3", "Shift_F4", "Assign_F1", "Assign_F2", 
                      "Assign_F3", "Assign_F4", "Height", "Volume", "Line_width_F1", 
                      "Line_width_F2", "Line_width_F3", "Line_width_F4", 
                      "Merit", "Details", "Fit_method", "Vol_method", "SPACE_VARS", 
                      "RETURN_VARS" ]

    RULE_ccpn_pk = 0
    RULE_peak_list_2d = 1
    RULE_peak_2d = 2
    RULE_peak_list_3d = 3
    RULE_peak_3d = 4
    RULE_peak_list_4d = 5
    RULE_peak_4d = 6
    RULE_number = 7

    ruleNames =  [ "ccpn_pk", "peak_list_2d", "peak_2d", "peak_list_3d", 
                   "peak_3d", "peak_list_4d", "peak_4d", "number" ]

    EOF = Token.EOF
    Number=1
    Integer=2
    Float=3
    Real=4
    SHARP_COMMENT=5
    EXCLM_COMMENT=6
    SMCLN_COMMENT=7
    Simple_name=8
    SPACE=9
    RETURN=10
    SECTION_COMMENT=11
    LINE_COMMENT=12
    Id=13
    Position_F1=14
    Position_F2=15
    Position_F3=16
    Position_F4=17
    Shift_F1=18
    Shift_F2=19
    Shift_F3=20
    Shift_F4=21
    Assign_F1=22
    Assign_F2=23
    Assign_F3=24
    Assign_F4=25
    Height=26
    Volume=27
    Line_width_F1=28
    Line_width_F2=29
    Line_width_F3=30
    Line_width_F4=31
    Merit=32
    Details=33
    Fit_method=34
    Vol_method=35
    SPACE_VARS=36
    RETURN_VARS=37

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Ccpn_pkContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(CcpnPKParser.EOF, 0)

        def RETURN(self, i:int=None):
            if i is None:
                return self.getTokens(CcpnPKParser.RETURN)
            else:
                return self.getToken(CcpnPKParser.RETURN, i)

        def peak_list_2d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CcpnPKParser.Peak_list_2dContext)
            else:
                return self.getTypedRuleContext(CcpnPKParser.Peak_list_2dContext,i)


        def peak_list_3d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CcpnPKParser.Peak_list_3dContext)
            else:
                return self.getTypedRuleContext(CcpnPKParser.Peak_list_3dContext,i)


        def peak_list_4d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CcpnPKParser.Peak_list_4dContext)
            else:
                return self.getTypedRuleContext(CcpnPKParser.Peak_list_4dContext,i)


        def getRuleIndex(self):
            return CcpnPKParser.RULE_ccpn_pk

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCcpn_pk" ):
                listener.enterCcpn_pk(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCcpn_pk" ):
                listener.exitCcpn_pk(self)




    def ccpn_pk(self):

        localctx = CcpnPKParser.Ccpn_pkContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_ccpn_pk)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 16
                self.match(CcpnPKParser.RETURN)


            self.state = 25
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==10:
                self.state = 23
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                if la_ == 1:
                    self.state = 19
                    self.peak_list_2d()
                    pass

                elif la_ == 2:
                    self.state = 20
                    self.peak_list_3d()
                    pass

                elif la_ == 3:
                    self.state = 21
                    self.peak_list_4d()
                    pass

                elif la_ == 4:
                    self.state = 22
                    self.match(CcpnPKParser.RETURN)
                    pass


                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 28
            self.match(CcpnPKParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_list_2dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Number(self):
            return self.getToken(CcpnPKParser.Number, 0)

        def Id(self):
            return self.getToken(CcpnPKParser.Id, 0)

        def Assign_F1(self):
            return self.getToken(CcpnPKParser.Assign_F1, 0)

        def Assign_F2(self):
            return self.getToken(CcpnPKParser.Assign_F2, 0)

        def Height(self):
            return self.getToken(CcpnPKParser.Height, 0)

        def Volume(self):
            return self.getToken(CcpnPKParser.Volume, 0)

        def Line_width_F1(self):
            return self.getToken(CcpnPKParser.Line_width_F1, 0)

        def Line_width_F2(self):
            return self.getToken(CcpnPKParser.Line_width_F2, 0)

        def Merit(self):
            return self.getToken(CcpnPKParser.Merit, 0)

        def Details(self):
            return self.getToken(CcpnPKParser.Details, 0)

        def Fit_method(self):
            return self.getToken(CcpnPKParser.Fit_method, 0)

        def Vol_method(self):
            return self.getToken(CcpnPKParser.Vol_method, 0)

        def RETURN_VARS(self):
            return self.getToken(CcpnPKParser.RETURN_VARS, 0)

        def Position_F1(self):
            return self.getToken(CcpnPKParser.Position_F1, 0)

        def Shift_F1(self):
            return self.getToken(CcpnPKParser.Shift_F1, 0)

        def Position_F2(self):
            return self.getToken(CcpnPKParser.Position_F2, 0)

        def Shift_F2(self):
            return self.getToken(CcpnPKParser.Shift_F2, 0)

        def peak_2d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CcpnPKParser.Peak_2dContext)
            else:
                return self.getTypedRuleContext(CcpnPKParser.Peak_2dContext,i)


        def getRuleIndex(self):
            return CcpnPKParser.RULE_peak_list_2d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_list_2d" ):
                listener.enterPeak_list_2d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_list_2d" ):
                listener.exitPeak_list_2d(self)




    def peak_list_2d(self):

        localctx = CcpnPKParser.Peak_list_2dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_peak_list_2d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(CcpnPKParser.Number)
            self.state = 31
            self.match(CcpnPKParser.Id)
            self.state = 32
            _la = self._input.LA(1)
            if not(_la==14 or _la==18):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 33
            _la = self._input.LA(1)
            if not(_la==15 or _la==19):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 34
            self.match(CcpnPKParser.Assign_F1)
            self.state = 35
            self.match(CcpnPKParser.Assign_F2)
            self.state = 36
            self.match(CcpnPKParser.Height)
            self.state = 37
            self.match(CcpnPKParser.Volume)
            self.state = 38
            self.match(CcpnPKParser.Line_width_F1)
            self.state = 39
            self.match(CcpnPKParser.Line_width_F2)
            self.state = 40
            self.match(CcpnPKParser.Merit)
            self.state = 41
            self.match(CcpnPKParser.Details)
            self.state = 42
            self.match(CcpnPKParser.Fit_method)
            self.state = 43
            self.match(CcpnPKParser.Vol_method)
            self.state = 44
            self.match(CcpnPKParser.RETURN_VARS)
            self.state = 46 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 45
                self.peak_2d()
                self.state = 48 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==2):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_2dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(CcpnPKParser.Integer)
            else:
                return self.getToken(CcpnPKParser.Integer, i)

        def Float(self, i:int=None):
            if i is None:
                return self.getTokens(CcpnPKParser.Float)
            else:
                return self.getToken(CcpnPKParser.Float, i)

        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(CcpnPKParser.Simple_name)
            else:
                return self.getToken(CcpnPKParser.Simple_name, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CcpnPKParser.NumberContext)
            else:
                return self.getTypedRuleContext(CcpnPKParser.NumberContext,i)


        def RETURN(self):
            return self.getToken(CcpnPKParser.RETURN, 0)

        def EOF(self):
            return self.getToken(CcpnPKParser.EOF, 0)

        def getRuleIndex(self):
            return CcpnPKParser.RULE_peak_2d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_2d" ):
                listener.enterPeak_2d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_2d" ):
                listener.exitPeak_2d(self)




    def peak_2d(self):

        localctx = CcpnPKParser.Peak_2dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_peak_2d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.match(CcpnPKParser.Integer)
            self.state = 51
            self.match(CcpnPKParser.Integer)
            self.state = 52
            self.match(CcpnPKParser.Float)
            self.state = 53
            self.match(CcpnPKParser.Float)
            self.state = 54
            self.match(CcpnPKParser.Simple_name)
            self.state = 55
            self.match(CcpnPKParser.Simple_name)
            self.state = 56
            self.number()
            self.state = 57
            self.number()
            self.state = 58
            self.match(CcpnPKParser.Float)
            self.state = 59
            self.match(CcpnPKParser.Float)
            self.state = 60
            self.match(CcpnPKParser.Float)
            self.state = 61
            self.match(CcpnPKParser.Simple_name)
            self.state = 62
            self.match(CcpnPKParser.Simple_name)
            self.state = 64 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 63
                self.match(CcpnPKParser.Simple_name)
                self.state = 66 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==8):
                    break

            self.state = 68
            _la = self._input.LA(1)
            if not(_la==-1 or _la==10):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_list_3dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Number(self):
            return self.getToken(CcpnPKParser.Number, 0)

        def Id(self):
            return self.getToken(CcpnPKParser.Id, 0)

        def Assign_F1(self):
            return self.getToken(CcpnPKParser.Assign_F1, 0)

        def Assign_F2(self):
            return self.getToken(CcpnPKParser.Assign_F2, 0)

        def Assign_F3(self):
            return self.getToken(CcpnPKParser.Assign_F3, 0)

        def Height(self):
            return self.getToken(CcpnPKParser.Height, 0)

        def Volume(self):
            return self.getToken(CcpnPKParser.Volume, 0)

        def Line_width_F1(self):
            return self.getToken(CcpnPKParser.Line_width_F1, 0)

        def Line_width_F2(self):
            return self.getToken(CcpnPKParser.Line_width_F2, 0)

        def Line_width_F3(self):
            return self.getToken(CcpnPKParser.Line_width_F3, 0)

        def Merit(self):
            return self.getToken(CcpnPKParser.Merit, 0)

        def Details(self):
            return self.getToken(CcpnPKParser.Details, 0)

        def Fit_method(self):
            return self.getToken(CcpnPKParser.Fit_method, 0)

        def Vol_method(self):
            return self.getToken(CcpnPKParser.Vol_method, 0)

        def RETURN_VARS(self):
            return self.getToken(CcpnPKParser.RETURN_VARS, 0)

        def Position_F1(self):
            return self.getToken(CcpnPKParser.Position_F1, 0)

        def Shift_F1(self):
            return self.getToken(CcpnPKParser.Shift_F1, 0)

        def Position_F2(self):
            return self.getToken(CcpnPKParser.Position_F2, 0)

        def Shift_F2(self):
            return self.getToken(CcpnPKParser.Shift_F2, 0)

        def Position_F3(self):
            return self.getToken(CcpnPKParser.Position_F3, 0)

        def Shift_F3(self):
            return self.getToken(CcpnPKParser.Shift_F3, 0)

        def peak_3d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CcpnPKParser.Peak_3dContext)
            else:
                return self.getTypedRuleContext(CcpnPKParser.Peak_3dContext,i)


        def getRuleIndex(self):
            return CcpnPKParser.RULE_peak_list_3d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_list_3d" ):
                listener.enterPeak_list_3d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_list_3d" ):
                listener.exitPeak_list_3d(self)




    def peak_list_3d(self):

        localctx = CcpnPKParser.Peak_list_3dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_peak_list_3d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self.match(CcpnPKParser.Number)
            self.state = 71
            self.match(CcpnPKParser.Id)
            self.state = 72
            _la = self._input.LA(1)
            if not(_la==14 or _la==18):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 73
            _la = self._input.LA(1)
            if not(_la==15 or _la==19):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 74
            _la = self._input.LA(1)
            if not(_la==16 or _la==20):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 75
            self.match(CcpnPKParser.Assign_F1)
            self.state = 76
            self.match(CcpnPKParser.Assign_F2)
            self.state = 77
            self.match(CcpnPKParser.Assign_F3)
            self.state = 78
            self.match(CcpnPKParser.Height)
            self.state = 79
            self.match(CcpnPKParser.Volume)
            self.state = 80
            self.match(CcpnPKParser.Line_width_F1)
            self.state = 81
            self.match(CcpnPKParser.Line_width_F2)
            self.state = 82
            self.match(CcpnPKParser.Line_width_F3)
            self.state = 83
            self.match(CcpnPKParser.Merit)
            self.state = 84
            self.match(CcpnPKParser.Details)
            self.state = 85
            self.match(CcpnPKParser.Fit_method)
            self.state = 86
            self.match(CcpnPKParser.Vol_method)
            self.state = 87
            self.match(CcpnPKParser.RETURN_VARS)
            self.state = 89 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 88
                self.peak_3d()
                self.state = 91 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==2):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_3dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(CcpnPKParser.Integer)
            else:
                return self.getToken(CcpnPKParser.Integer, i)

        def Float(self, i:int=None):
            if i is None:
                return self.getTokens(CcpnPKParser.Float)
            else:
                return self.getToken(CcpnPKParser.Float, i)

        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(CcpnPKParser.Simple_name)
            else:
                return self.getToken(CcpnPKParser.Simple_name, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CcpnPKParser.NumberContext)
            else:
                return self.getTypedRuleContext(CcpnPKParser.NumberContext,i)


        def RETURN(self):
            return self.getToken(CcpnPKParser.RETURN, 0)

        def EOF(self):
            return self.getToken(CcpnPKParser.EOF, 0)

        def getRuleIndex(self):
            return CcpnPKParser.RULE_peak_3d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_3d" ):
                listener.enterPeak_3d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_3d" ):
                listener.exitPeak_3d(self)




    def peak_3d(self):

        localctx = CcpnPKParser.Peak_3dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_peak_3d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self.match(CcpnPKParser.Integer)
            self.state = 94
            self.match(CcpnPKParser.Integer)
            self.state = 95
            self.match(CcpnPKParser.Float)
            self.state = 96
            self.match(CcpnPKParser.Float)
            self.state = 97
            self.match(CcpnPKParser.Float)
            self.state = 98
            self.match(CcpnPKParser.Simple_name)
            self.state = 99
            self.match(CcpnPKParser.Simple_name)
            self.state = 100
            self.match(CcpnPKParser.Simple_name)
            self.state = 101
            self.number()
            self.state = 102
            self.number()
            self.state = 103
            self.match(CcpnPKParser.Float)
            self.state = 104
            self.match(CcpnPKParser.Float)
            self.state = 105
            self.match(CcpnPKParser.Float)
            self.state = 106
            self.match(CcpnPKParser.Float)
            self.state = 107
            self.match(CcpnPKParser.Simple_name)
            self.state = 108
            self.match(CcpnPKParser.Simple_name)
            self.state = 110 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 109
                self.match(CcpnPKParser.Simple_name)
                self.state = 112 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==8):
                    break

            self.state = 114
            _la = self._input.LA(1)
            if not(_la==-1 or _la==10):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_list_4dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Number(self):
            return self.getToken(CcpnPKParser.Number, 0)

        def Id(self):
            return self.getToken(CcpnPKParser.Id, 0)

        def Assign_F1(self):
            return self.getToken(CcpnPKParser.Assign_F1, 0)

        def Assign_F2(self):
            return self.getToken(CcpnPKParser.Assign_F2, 0)

        def Assign_F3(self):
            return self.getToken(CcpnPKParser.Assign_F3, 0)

        def Assign_F4(self):
            return self.getToken(CcpnPKParser.Assign_F4, 0)

        def Height(self):
            return self.getToken(CcpnPKParser.Height, 0)

        def Volume(self):
            return self.getToken(CcpnPKParser.Volume, 0)

        def Line_width_F1(self):
            return self.getToken(CcpnPKParser.Line_width_F1, 0)

        def Line_width_F2(self):
            return self.getToken(CcpnPKParser.Line_width_F2, 0)

        def Line_width_F3(self):
            return self.getToken(CcpnPKParser.Line_width_F3, 0)

        def Line_width_F4(self):
            return self.getToken(CcpnPKParser.Line_width_F4, 0)

        def Merit(self):
            return self.getToken(CcpnPKParser.Merit, 0)

        def Details(self):
            return self.getToken(CcpnPKParser.Details, 0)

        def Fit_method(self):
            return self.getToken(CcpnPKParser.Fit_method, 0)

        def Vol_method(self):
            return self.getToken(CcpnPKParser.Vol_method, 0)

        def RETURN_VARS(self):
            return self.getToken(CcpnPKParser.RETURN_VARS, 0)

        def Position_F1(self):
            return self.getToken(CcpnPKParser.Position_F1, 0)

        def Shift_F1(self):
            return self.getToken(CcpnPKParser.Shift_F1, 0)

        def Position_F2(self):
            return self.getToken(CcpnPKParser.Position_F2, 0)

        def Shift_F2(self):
            return self.getToken(CcpnPKParser.Shift_F2, 0)

        def Position_F3(self):
            return self.getToken(CcpnPKParser.Position_F3, 0)

        def Shift_F3(self):
            return self.getToken(CcpnPKParser.Shift_F3, 0)

        def Position_F4(self):
            return self.getToken(CcpnPKParser.Position_F4, 0)

        def Shift_F4(self):
            return self.getToken(CcpnPKParser.Shift_F4, 0)

        def peak_4d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CcpnPKParser.Peak_4dContext)
            else:
                return self.getTypedRuleContext(CcpnPKParser.Peak_4dContext,i)


        def getRuleIndex(self):
            return CcpnPKParser.RULE_peak_list_4d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_list_4d" ):
                listener.enterPeak_list_4d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_list_4d" ):
                listener.exitPeak_list_4d(self)




    def peak_list_4d(self):

        localctx = CcpnPKParser.Peak_list_4dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_peak_list_4d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.match(CcpnPKParser.Number)
            self.state = 117
            self.match(CcpnPKParser.Id)
            self.state = 118
            _la = self._input.LA(1)
            if not(_la==14 or _la==18):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 119
            _la = self._input.LA(1)
            if not(_la==15 or _la==19):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 120
            _la = self._input.LA(1)
            if not(_la==16 or _la==20):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 121
            _la = self._input.LA(1)
            if not(_la==17 or _la==21):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 122
            self.match(CcpnPKParser.Assign_F1)
            self.state = 123
            self.match(CcpnPKParser.Assign_F2)
            self.state = 124
            self.match(CcpnPKParser.Assign_F3)
            self.state = 125
            self.match(CcpnPKParser.Assign_F4)
            self.state = 126
            self.match(CcpnPKParser.Height)
            self.state = 127
            self.match(CcpnPKParser.Volume)
            self.state = 128
            self.match(CcpnPKParser.Line_width_F1)
            self.state = 129
            self.match(CcpnPKParser.Line_width_F2)
            self.state = 130
            self.match(CcpnPKParser.Line_width_F3)
            self.state = 131
            self.match(CcpnPKParser.Line_width_F4)
            self.state = 132
            self.match(CcpnPKParser.Merit)
            self.state = 133
            self.match(CcpnPKParser.Details)
            self.state = 134
            self.match(CcpnPKParser.Fit_method)
            self.state = 135
            self.match(CcpnPKParser.Vol_method)
            self.state = 136
            self.match(CcpnPKParser.RETURN_VARS)
            self.state = 138 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 137
                self.peak_4d()
                self.state = 140 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==2):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_4dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(CcpnPKParser.Integer)
            else:
                return self.getToken(CcpnPKParser.Integer, i)

        def Float(self, i:int=None):
            if i is None:
                return self.getTokens(CcpnPKParser.Float)
            else:
                return self.getToken(CcpnPKParser.Float, i)

        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(CcpnPKParser.Simple_name)
            else:
                return self.getToken(CcpnPKParser.Simple_name, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CcpnPKParser.NumberContext)
            else:
                return self.getTypedRuleContext(CcpnPKParser.NumberContext,i)


        def RETURN(self):
            return self.getToken(CcpnPKParser.RETURN, 0)

        def EOF(self):
            return self.getToken(CcpnPKParser.EOF, 0)

        def getRuleIndex(self):
            return CcpnPKParser.RULE_peak_4d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_4d" ):
                listener.enterPeak_4d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_4d" ):
                listener.exitPeak_4d(self)




    def peak_4d(self):

        localctx = CcpnPKParser.Peak_4dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_peak_4d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self.match(CcpnPKParser.Integer)
            self.state = 143
            self.match(CcpnPKParser.Integer)
            self.state = 144
            self.match(CcpnPKParser.Float)
            self.state = 145
            self.match(CcpnPKParser.Float)
            self.state = 146
            self.match(CcpnPKParser.Float)
            self.state = 147
            self.match(CcpnPKParser.Float)
            self.state = 148
            self.match(CcpnPKParser.Simple_name)
            self.state = 149
            self.match(CcpnPKParser.Simple_name)
            self.state = 150
            self.match(CcpnPKParser.Simple_name)
            self.state = 151
            self.match(CcpnPKParser.Simple_name)
            self.state = 152
            self.number()
            self.state = 153
            self.number()
            self.state = 154
            self.match(CcpnPKParser.Float)
            self.state = 155
            self.match(CcpnPKParser.Float)
            self.state = 156
            self.match(CcpnPKParser.Float)
            self.state = 157
            self.match(CcpnPKParser.Float)
            self.state = 158
            self.match(CcpnPKParser.Float)
            self.state = 159
            self.match(CcpnPKParser.Simple_name)
            self.state = 160
            self.match(CcpnPKParser.Simple_name)
            self.state = 162 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 161
                self.match(CcpnPKParser.Simple_name)
                self.state = 164 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==8):
                    break

            self.state = 166
            _la = self._input.LA(1)
            if not(_la==-1 or _la==10):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Float(self):
            return self.getToken(CcpnPKParser.Float, 0)

        def Real(self):
            return self.getToken(CcpnPKParser.Real, 0)

        def getRuleIndex(self):
            return CcpnPKParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = CcpnPKParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 168
            _la = self._input.LA(1)
            if not(_la==3 or _la==4):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





