
import os
import string
class PdfObj():
    def __init__(self):
        self.Name = ''
        self.Pos = ''
        self.StreamType = None
        self.StreamPos = ''
        
class FxPdfParser():
    def __init__(self, fp):
        self.fp = fp
        self.ObjInfoL = []
        self.objPosL = []
        self.objNameL = []
        self.objBuf = {}
        self.objNumL = []
        self.DEADCONTROL = 0
        self.DEBUG = 0
        self._DEBUG = 0
        
        
    def _GetKeyPosRough(self, buf, key):
        key0 = key + '\r'
        key1 = key + '\n'
        key_posL = []
#        print(buf)
        while 1:
            pos = buf.find(key0)
            if pos == -1:
                pos = buf.find(key1)
            if pos != -1:
                if key == 'xref':
                    tem = buf[pos - 1:pos]
                    if tem.isalpha():
                        pass
                    else:
                        key_posL.append(pos)
                else:
                    key_posL.append(pos)
                buf = buf[pos + key0.__len__():]
            else:
                break
        return key_posL
    
    def _GetOneKeyPosRough(self, buf, key):
        key0 = key + '\r'
        key1 = key + '\n'
        key2 = key + ' '
        key3 = key + '<'
        key4 = key + '['
#        print(buf)
        pos = buf.find(key0)
        if pos == -1:
            pos = buf.find(key1)
        if pos == -1:
            pos = buf.find(key2)
        if pos == -1:
            pos = buf.find(key3)
        if pos == -1:
            pos = buf.find(key4)
        if pos != -1:
            return pos
        else:
            return None
        
    def GetEOFPos(self):
        xrefposL = []
        buf = self.fp.read()
        rought_posL = self._GetKeyPosRough(buf, '%%EOF')
        for xrefpos in rought_posL:
            self.fp.seek(xrefpos, 0)
            pos = self.FindKeyPos(self.fp, xrefpos, '%%EOF')
            xrefposL.append(pos)
            self.fp.seek(0)
        return xrefposL

    def GetStartXrefPos(self):
        startxrefposL = []
        buf = self.fp.read()
        rought_posL = self._GetKeyPosRough(buf, 'startxref')
        for startxrefpos in rought_posL:
            self.fp.seek(startxrefpos, 0)
            pos = self.FindKeyPos(self.fp, startxrefpos, 'startxref')
            startxrefposL.append(pos)
            self.fp.seek(0)
        return startxrefposL
    
    def GetXrefContent(self):
        endpos = 0
#        num = 0
        XrefPosL = []
        startXrefPosL = self.GetStartXrefPos()
        for startXrefPos in startXrefPosL:
            Ctl = True
            self.fp.seek(startXrefPos, 0)
            while Ctl:
                tem = self.fp.read(1)
                if tem == '%':
                    endpos = self.fp.tell()
                    self.fp.seek(startXrefPos, 0)
                    XrefPos = self.fp.read(endpos - startXrefPos - 1).strip("\r").strip("\n")
                    XrefPos = string.atoi(XrefPos, 10)
                    XrefPosL.append(XrefPos)
                    Ctl = False
        self.fp.seek(0)
        return XrefPosL
    
    def GetXrefPos(self):
        XrefposL = []
        buf = self.fp.read()
        rought_posL = self._GetKeyPosRough(buf, 'xref')
#        num = 0
        for xrefpos in rought_posL:
            self.fp.seek(xrefpos, 0)
            pos = self.FindKeyPos(self.fp, xrefpos, 'xref')
            XrefposL.append(pos)
            self.fp.seek(0)
        
        return XrefposL
    
    def GetXrefInfo(self):
        xrefPosL = []
        eofPosL = []
        buf = self.fp.read()
        roughPosL = self._GetKeyPosRough(buf, 'xref')
        for roughPos in roughPosL:
            xrefPos = self.FindKeyPos(self.fp, roughPos, 'xref')
            xrefPosL.append(xrefPos)
        roughPosL = self._GetKeyPosRough(buf, '%%EOF')
        for roughPos in roughPosL:
            eofPos = self.FindKeyPos(self.fp, roughPos, '%%EOF')
            eofPosL.append(eofPos)
        return (xrefPosL, eofPosL)
    
    def GetTrailerPos(self):
        trailerposL = []
        buf = self.fp.read()
        rought_posL = self._GetKeyPosRough(buf, 'trailer')
        for startxrefpos in rought_posL:
            self.fp.seek(startxrefpos, 0)
            pos = self.FindKeyPos(self.fp, startxrefpos, 'trailer')
            trailerposL.append(pos)
            self.fp.seek(0)
        return trailerposL
    
    def GetObjPosFromXref(self, XrefPosL, trailerPosL):
        objPosL = []
        pos = 0
        num = 0
        while XrefPosL.__len__() > num:
            XrefPos = XrefPosL[num]
            if XrefPos == 0:
                XrefPosL = self.GetXrefPos()
                continue
            self.fp.seek(XrefPos + 4, 0)
            buf = self.fp.read(trailerPosL[num] - XrefPos)
            objPosTemL = buf.split('n')
            for objPos in objPosTemL:
                objPos = filter(str.isdigit, objPos)
                objPos = objPos[ : objPos.__len__() - 5]
                objPos = objPos[-10 : ]
                try:
                    pos = string.atol(objPos, 10)
                    if pos == 0:
                        pass
                    else:
                        objPosL.append(pos - 1)
                except:
                    pass
            num += 1
        self.objPosL = objPosL
        return objPosL
    
    def GetObjNumFromPos(self, objPos):
        self.fp.seek(0)
        self.fp.seek(objPos + 2, 0)
        while 1:
            tem = self.fp.read(1)
            if tem == 'o':
                endpos = self.fp.tell() + 2
                self.fp.seek(objPos)
                objName = self.fp.read(endpos - objPos).strip('\r\n')
                objSpacePos = objName.find(' ')
                objNum = objName[:objSpacePos]
                try:
                    objNum = string.atoi(objNum, 10)
                except ValueError:
#                    self.fp.seek(0)
                    objPos = objPos - 1
                    self.fp.seek(objPos + 3, 0)
                    while 1:
                        tem = self.fp.read(1)
                        if tem == 'o':
                            endpos = self.fp.tell() + 2
                            self.fp.seek(objPos)
                            objName = self.fp.read(endpos - objPos).strip('\r\n')
                            objSpacePos = objName.find(' ')
                            objNum = objName[:objSpacePos]
                            break 
                break
        return objNum
    
    def GetObjNameFromPosL(self, objPosL):
        objNameL = []
        objName = ''
        if objPosL.__len__() == 1 and objPosL[0] == 0:
            return 'error'
        for objPos in objPosL:
            self.fp.seek(0)
            self.fp.seek(objPos + 4, 0)
            while 1:
                tem = self.fp.read(1)
                if tem == 'o':
                    endpos = self.fp.tell() + 3
                    self.fp.seek(objPos)
                    objName = self.fp.read(endpos - objPos).strip('\r\n')
                    objNameL.append(objName)
                    break 
        #self.fp.seek(0)
        self.objNameL = objNameL
        return objNameL
    
    def DelObjBufStream(self, objBuf):
        endstreamPos = objBuf.find('endstream')
        streamPos = objBuf.find('stream')
        if endstreamPos != -1 and streamPos != -1:
            objBufNSP = objBuf[:streamPos]
            objBufNSL = objBuf[endstreamPos + 9:]
            objBufNS = objBufNSP + objBufNSL
        else:
            objBufNS = objBuf
        return objBufNS
    
    def GetObjBufRef(self, objBuf):
        refNumL = []
        refPos = objBuf.find(' R')
        while refPos != -1:
            refBuf = objBuf[:refPos]
            sepPos = refBuf.rfind('/')
            if sepPos == -1:
                pass
            else:
                refBuf = refBuf[sepPos:]
            refBufL = refBuf.split(' ')
            _len = refBufL.__len__()
            num = 0
            while num < _len:
                refTem = refBufL[num]
                try:
                    refNum = string.atoi(refTem, 10)
                    if type(refNum) == type(1):
                        break
                except:
#                    print('no num')
                    pass
                num += 1
            if refNum in refNumL:
                pass
            else:
                refNumL.append(refNum)
            objBuf = objBuf[refPos + 2:]
            refPos = objBuf.find(' R')
        return refNumL
    
    def GetObjBuf(self, ObjPos = ''):
        objPosL = self.objPosL
        objNameL = self.objNameL

        if type(ObjPos) == type(1L):
            if ObjPos == 0:
                return 'error'
            objIndex = objPosL.index(ObjPos)
        else:
            objIndex = objNameL.index(ObjPos)

        objPos = objPosL[objIndex]
        if objIndex < objPosL.__len__() - 1:
            objNPos = objPosL[objIndex + 1]
        else:
            self.fp.seek(0, os.SEEK_END)
            objNPos = self.fp.tell()
        
        self.fp.seek(objPos)
        buf = self.fp.read(objNPos - objPos)
        if objIndex == 0:
            roughEndPos = self._GetOneKeyPosRough(buf, 'endobj')
            endPos = self.FindKeyPos(self.fp, roughEndPos, 'endobj')
            self.fp.seek(0)
            objbuf = self.fp.read(endPos - 6)
            if self._DEBUG == 1:
                print(objbuf)
                print('****************************************************')
            objPosTem = self.FindKeyPos(self.fp, 0, 'obj')
            self.fp.seek(objPosTem - 7, 0)
            while 1:
                self.fp.seek(-1, 1)
                tem = self.fp.read(1)
                self.fp.seek(-1, 1)
                if tem in ['\n', '\r', ' ', '<', '[']:
                    objPos = self.fp.tell() + 1
                    self.fp.seek(objPos)
                    buf = self.fp.read(endPos - objPos)
                    break
                if self._DEBUG == 1:
                    self.DEADCONTROL += 1
                    if self.DEADCONTROL > 100000:
                        print('process dead loop in GetObjBuf')
                        break
        buf = buf.strip('\r\n')
        return buf
        
    def GetObjStreamInfo(self, ObjPos):
        encodePosD = {}
        encodeTypeL = []
        TypeDefine = ['LZWDecode', 'ASCII85Decode', 'FlateDecode', \
                      'RunLengthDecode', 'DCTDecode']
        buf = self.GetObjBuf(ObjPos)
#        print(buf)
#        print('**********************************************')
        RoughPos0 = buf.find('stream')
        RoughPos1 = buf.find('endstream')
        if RoughPos0 == -1 and RoughPos1 == -1:
            return 'NoStream'
        else:
            if buf.find('/Filter') != -1:
                for encodetype in TypeDefine:
                    pos = buf.find(encodetype)
                    if pos != -1:
                        encodePosD[pos] = encodetype
                if encodePosD.__len__() > 1:
                    pass
                encodeKeys = encodePosD.keys()
                encodeKeys.sort()
                for pos in encodeKeys:
                    encodeTypeL.append(encodePosD[pos])
            else:
                encodeTypeL.append('NoEncode')
            streamPos = self.FindKeyPos(self.fp, RoughPos0 + ObjPos, 'stream')
            endStreamPos = self.FindKeyPos(self.fp, RoughPos1 + ObjPos, 'endstream')
            self.fp.seek(streamPos)
            buf = self.fp.read(endStreamPos - streamPos)
            buf = buf[: -9]
            
        return ((encodeTypeL, buf), (streamPos, endStreamPos))
    
    def GetObjStreamEncodeType(self, ObjPos):
        encodeTypeL = []
        encodePosD = {}
        objPosL = self.objPosL
        objNameL = self.objNameL
        objPosL.sort()
        TypeDefine = ['LZWDecode', 'ASCII85Decode', 'FlateDecode', \
                      'RunLengthDecode', 'DCTDecode']
        if type(ObjPos) == type(1L):
            objIndex = objPosL.index(ObjPos)
        else:
            objIndex = objNameL.index(ObjPos)
        objPos = objPosL[objIndex]
        if objIndex < objPosL.__len__() - 1:
            objNPos = objPosL[objIndex + 1]
        else:
            self.fp.seek(0, os.SEEK_END)
            objNPos = self.fp.tell()
        self.fp.seek(objPos)
        buf = self.fp.read(objNPos - objPos)
        if buf.find('/Filter') != -1:
            for encodetype in TypeDefine:
                pos = buf.find(encodetype)
                if pos != -1:
                    encodePosD[pos] = encodetype
        else:
            return 'NoEncode'
        if encodePosD.__len__() > 1:
            pass
        encodePosD.keys().sort(reverse=True)
        for pos in encodePosD.keys():
            encodeTypeL.append(encodePosD[pos])
        
        return encodeTypeL
    
    def GetXrefObjInfo(self):
        ObjInfoL = []
        XrefPosL = self.GetXrefContent()
        trailerPosL = self.GetTrailerPos()
        objPosL = self.GetObjPosFromXref(XrefPosL, trailerPosL)
        objNameL = self.GetObjNameFromPos(objPosL)
        num = 0
        while num < objPosL.__len__():
            ObjInfo = PdfObj()
            ObjInfo.Pos = objPosL[num]
            ObjInfo.Name = objNameL[num]
            ObjInfo.StreamType = None
            ObjInfo.StreamPos = 0
            ObjInfoL.append(ObjInfo)
            num += 1        
        self.ObjInfoL = ObjInfoL
        return ObjInfoL
            
        
        
    def GetStreamPos(self, objNameL):
        pass
        
    def FindKeyPos(self, fp, pos = 0, key_str = ''):
        num = 0
        firstcnt = 1
        second_pos = 0
        fp.seek(pos, os.SEEK_END)
        len_ = fp.tell()
#        keys = ['stream', 'xref', 'startxref', '%%EOF', ' obj']
        SEARCHDEF = ['\n', '\r', ' ', '<', '[']
#        search_def2 = ['']
        key_pos_dic = {}
        pair_pos_dic = {}
      
        fp.seek(pos, 0)

        tem = fp.read(1)
        key_len = key_str.__len__()
        while len_ > fp.tell():
#            if key_str == 'stream':
#            if key_str != 'endstream' and key_str != '%%EOF':
            if key_str == 'temfalse':
                if tem in SEARCHDEF:
#                if cmp(tem, key_str[0]) == 0:
#                    fp.seek(-1, 1)
                    buf = fp.read(key_len)
                    if buf == key_str:
                        tem = fp.read(1)
                        #print(fp.read(100))
                        if tem in SEARCHDEF:
                            pos = fp.tell() - 1
                            key_pos_dic[num]= pos
                            if key_str == 'stream':
                                pair_pos_dic[num] = self.FindKeyPos(fp, pos, 'endstream')
                            elif key_str == 'xref' or key_str == 'startxref':
                                pair_pos_dic[num] = self.FindKeyPos(fp, pos, '%%EOF')
                            if key_str.find(' obj') != -1:
                                break
                            num += 1
                        else:
                            fp.seek(-2, 1)
                            tem = fp.read(1)
                    else:
                        if fp.tell() != len_:
                            fp.seek(0 - key_len, 1)
                            tem = fp.read(1)
                else:
                    tem = fp.read(1)   
                    
            #elif key_str == 'endstream' or key_str == '%%EOF':
            else:
                if firstcnt == 1:
                    #fp.seek(pos, 1)
                    fp.seek(key_len - 1, 1)
                else:
                    fp.seek(key_len, 1)
                tem = fp.read(1)
                if tem in SEARCHDEF:
#                    if firstcnt == 1:
                    fp.seek(0 - key_len - 1, 1)
                    #fp.seek(-10, 1)
                    buf = fp.read(key_len)
                    #print(buf)
    #                if tem in search_def:
#                    if buf.find('ream') != -1:
#                        pass
                    if buf == key_str:
                        tem = fp.read(1)
                        #print(fp.read(100))
                        if tem in SEARCHDEF:
                            pos = fp.tell() - 1
        #                    print(fp.read(100))
        #                    fp.seek(-100, 1)
                            #key_pos_dic[num]= pos
                            second_pos = pos
                            break
                            num += 1
                        else:
                            fp.seek(-2, 1)
                            tem = fp.read(1)
                    else:
                        #fp.seek(-8, 1)
                        fp.seek(0 - key_len + 1, 1)
                else:
                    if fp.tell() != len_:
                        #fp.seek(-9, 1)
                        fp.seek(-key_len, 1)
                #len -= 1
                firstcnt = 0
        self.key_pos_dic = key_pos_dic 
        return second_pos
        #print('over 0') 
#        if key_str == 'endstream' or key_str == '%%EOF':
#            return second_pos
#        elif key_str == 'stream' or key_str == 'xref' or key_str == 'startxref':
#            return (key_pos_dic, pair_pos_dic)
#        else:
#            return key_pos_dic