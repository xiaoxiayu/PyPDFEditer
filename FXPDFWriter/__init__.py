import os
import string
import zlib
from FXStreamCoder import StreamDecoder

class FxPdfWriter():
    def __init__(self, fp=None):
        self.fp = fp
        self.Name = ''
        self.Pos = ''
        self.StreamType = None
        self.StreamPos = ''
        self.ObjPosD = {}
        self.ObjStreamD = {}
#        self.XrefPosL = []
        self.XrefInfo = ()
        self.RootNum = 0
        self.DEBUG = 0
        self._DEBUG = 0
        
    def _GetKeyPosRough(self, buf, key):
        key0 = key + '\r'
        key1 = key + '\n'
#        key2 = key
        key_posL = []
#        print(buf)
        while 1:
            pos = buf.find(key0)
            if pos == -1:
                pos = buf.find(key1)
#            if pos == -1:
#                pos = buf.find(key2)
#                if pos == 584643:
#                    tem = buf[584643:]
#                    print(tem)
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
        
    def _GetObjStreamEncodeType(self, objBuf):
        encodePosD = {}
        encodeTypeL = []
        TypeDefine = ['LZWDecode', 'ASCII85Decode', 'FlateDecode', \
                      'RunLengthDecode', 'DCTDecode']
        if objBuf.find('/Filter') != -1:
            for encodetype in TypeDefine:
                pos = objBuf.find(encodetype)
                if pos != -1:
                    encodePosD[pos] = encodetype
            if encodePosD.__len__() > 1:
                pass
            encodeKeys = encodePosD.keys()
            encodeKeys.sort(reverse=True)
            #encodePosD.keys().sort()
            for pos in encodeKeys:
                encodeTypeL.append(encodePosD[pos])
        else:
            encodeTypeL.append('NoEncode')
        
        return encodeTypeL
    
    def _GetObjStreamInfo(self, objBuf, objPos):
        roughBegPos = self._GetOneKeyPosRough(objBuf, 'stream')
#        if self._DEBUG:
#            self.fp.seek(roughBegPos)
#            tembuf = self.fp.read(500)
#            self.fp.seek(-500, 1)
        if roughBegPos == None:
            return None
        BegPos = self.FindKeyPos(self.fp, roughBegPos + objPos - 6, 'stream')
#        if self._DEBUG:
#            self.fp.seek(BegPos)
#            tembuf = self.fp.read(500)
#            self.fp.seek(-500, 1)
        
        roughEndPos = self._GetOneKeyPosRough(objBuf, 'endstream')
        if roughEndPos == None:
            return None
        EndPos = self.FindKeyPos(self.fp, roughEndPos + objPos - 9, 'endstream')
        
        self.fp.seek(BegPos, 0)
        streamBuf = self.fp.read(EndPos - BegPos - 9)
        
        encodeTypeL = self._GetObjStreamEncodeType(objBuf)
        
        return ((encodeTypeL, streamBuf), (BegPos, EndPos))
    
    def GetXrefInfo(self, buf):
        xrefPosL = []
        eofPosL = []
        roughPosL = self._GetKeyPosRough(buf, 'xref')
        for roughPos in roughPosL:
            xrefPos = self.FindKeyPos(self.fp, roughPos, 'xref')
            xrefPosL.append(xrefPos)
        roughPosL = self._GetKeyPosRough(buf, '%%EOF')
        for roughPos in roughPosL:
            eofPos = self.FindKeyPos(self.fp, roughPos, '%%EOF')
            eofPosL.append(eofPos)
        return (xrefPosL, eofPosL)
    
    #def GetStartXrefContent(self):
    def GetRootObjNum(self, buf):
#        trailerPosL = []
        roughPosL = self._GetKeyPosRough(buf, 'trailer')
        num = 0
        for roughPos in roughPosL:
            xrefPos = self.FindKeyPos(self.fp, roughPos, 'trailer')
#            trailerPosL.append(xrefPos)
            self.fp.seek(xrefPos)
            trailerBuf = self.fp.read(self.XrefInfo[1][num] - xrefPos)
            pos = trailerBuf.find('/Root')
            if pos != -1:
                temBuf = trailerBuf[pos + 5:]
                endPos = temBuf.find(' R')
                objNumStr = temBuf[: endPos].strip('\r\n ')
                spacePos = objNumStr.find(' ')
                objNumStr = objNumStr[: spacePos]
                objNum = string.atoi(objNumStr, 10)
                return objNum
            num += 1
    
    def ExportIMGStream(self, streamInfo):
        streamTypeL = streamInfo[0][0]
        streamBuf = streamInfo[0][1]
        streamBuf = streamBuf.strip('\r\n')
        _len = streamTypeL.__len__()
        if 'DCTDecode' in streamTypeL:
            if _len == 1:
                if streamTypeL[0] == 'DCTDecode':
                    buf = streamBuf
            elif _len > 1:
                decoder = StreamDecoder()
                try:
                    for encodeType in streamTypeL:
                        if cmp(encodeType, 'FlateDecode') == 0:
                            decode_stream = decoder.ZlibDecompress(streamBuf)
                            if decode_stream.find("\x00") != -1:
                                decode_stream = decoder.ASCToHex(streamBuf)
                        if cmp(encodeType, 'DCTDecode') == 0: 
                            buf = streamBuf
                            break
                        if cmp(encodeType, 'LZWDecode') == 0:
                            decode_stream = decoder.LZWDecode(streamBuf)
                        if cmp(encodeType, 'ASCIIHexDecode') == 0:
                            decode_stream = decoder.ASCIIHexDecode(streamBuf)
                        if cmp(encodeType, 'ASCII85Decode') == 0:
                            decode_stream = decoder.ASCII85Decode(streamBuf.strip("\r").strip("\n"))
                        if cmp(encodeType, 'RunLengthDecode') == 0:
                            decode_stream = decoder.RunLengthDecode(streamBuf)
                        streamBuf = decode_stream 
                except:
                    return 'decode error!'
            return buf
                    
    def ReParser(self, fp):
        self.ObjPosD = {}
        self.ObjStreamD = {}
        self.fp = fp
        self.fp.seek(0, os.SEEK_END)
        len_ = self.fp.tell()
        self.fp.seek(0)
        buf = self.fp.read()
        self.XrefInfo = self.GetXrefInfo(buf)
        self.RootNum = self.GetRootObjNum(buf)
        
        self.fp.seek(0)
        num = 0
        endPos = 0
        lastEndPos = 0
        while self.fp.tell() < len_:
            if num == 0:
                self.fp.seek(endPos, 0)
            else:
                self.fp.seek(lastEndPos)

            buf = self.fp.read()
            roughEndPos = self._GetOneKeyPosRough(buf, 'endobj')
            if roughEndPos == None:
                return 'seuccess'
            else:
                endPos = self.FindKeyPos(self.fp, roughEndPos + lastEndPos, 'endobj')
            if num == 0:
                self.fp.seek(0, 0)
            else:
                self.fp.seek(lastEndPos, 0)
            objbuf = self.fp.read(endPos - lastEndPos - 6)
            if self._DEBUG:
                print(objbuf)
                print('****************************************************')
            roughObjPos = self._GetOneKeyPosRough(objbuf, 'obj')
            if roughObjPos ==None:
                print 'check obj is error?'
                return 'check'
            objPosTem = self.FindKeyPos(self.fp, roughObjPos + lastEndPos, 'obj')
            self.fp.seek(objPosTem - 7, 0)
            while 1:
                self.fp.seek(-1, 1)
                tem = self.fp.read(1)
                self.fp.seek(-1, 1)
                if tem in ['\r', '\n', '<', '[']:
                    objPos = self.fp.tell() + 1
                    self.fp.seek(objPos, 0)
                    objNum = self.fp.read(objPosTem - objPos)
                    spacePos = objNum.find(' ')
                    objNum = objNum[:spacePos]
                    objNum = string.atoi(objNum, 10)
                    self.ObjPosD[objNum] = objPos
                    if endPos == 12098:
                        self.DEBUG = endPos
                    if num == 0:
                        objPos = 0
                    objStreamInfo = self._GetObjStreamInfo(objbuf, objPos)
                    self.ObjStreamD[objNum] = objStreamInfo
                    break
            lastEndPos = endPos
            num = 1
        return 'error'
    
    def Parse(self):
        self.fp.seek(0, os.SEEK_END)
        len_ = self.fp.tell()
        self.fp.seek(0)
        buf = self.fp.read()
        self.XrefInfo = self.GetXrefInfo(buf)
        self.RootNum = self.GetRootObjNum(buf)
        
        self.fp.seek(0)
        num = 0
        endPos = 0
        lastEndPos = 0
        while self.fp.tell() < len_:
            if num == 0:
                self.fp.seek(endPos, 0)
            else:
                self.fp.seek(lastEndPos)

            buf = self.fp.read()
            roughEndPos = self._GetOneKeyPosRough(buf, 'endobj')
            if roughEndPos == None:
                return 'seuccess'
            else:
                endPos = self.FindKeyPos(self.fp, roughEndPos + lastEndPos, 'endobj')
            if num == 0:
                self.fp.seek(0, 0)
            else:
                self.fp.seek(lastEndPos, 0)
            objbuf = self.fp.read(endPos - lastEndPos - 6)
            if self._DEBUG:
                print(objbuf)
                print('****************************************************')
            roughObjPos = self._GetOneKeyPosRough(objbuf, 'obj')   
            objPosTem = self.FindKeyPos(self.fp, roughObjPos + lastEndPos, 'obj')
            self.fp.seek(objPosTem - 7, 0)
            while 1:
                self.fp.seek(-1, 1)
                tem = self.fp.read(1)
                self.fp.seek(-1, 1)
                if tem in ['\r', '\n', '<', '[']:
                    objPos = self.fp.tell() + 1
                    self.fp.seek(objPos, 0)
                    objNum = self.fp.read(objPosTem - objPos)
                    spacePos = objNum.find(' ')
                    objNum = objNum[:spacePos]
                    objNum = string.atoi(objNum, 10)
                    self.ObjPosD[objNum] = objPos
                    if num == 0:
                        objPos = 0
                    objStreamInfo = self._GetObjStreamInfo(objbuf, objPos)
                    self.ObjStreamD[objNum] = objStreamInfo
                    break
            lastEndPos = endPos
            num += 1
        return 'sucess'
    
    def GeneratorXref(self, fp, objPosD, rootNum, startxref_value):
        fp.write("\nxref\n")
        fp.write("0 %s\n" % (objPosD.__len__() + 1))
        fp.write("%010d %05d f \n" % (0, 65535))
                
        objNums = objPosD.keys()
        objNums.sort()
        for num in objNums:
            fp.write("%010d %05d n \n" % (objPosD[num] + 1, 0))

        objCount = objNums.__len__()
        objCount += 1
        
        fp.write("\r\ntrailer\r\n")
        fp.write("<<\r\n")
        fp.write("/Root %d %d R\r\n" % (rootNum, 0))
        fp.write("/Size %d\r\n" % objCount)
        fp.write(">>\r\n")
        startxref_value = startxref_value + 1
        fp.write("startxref\r\n%s\r\n%%%%EOF\r\n" % startxref_value)
        
    def FindKeyPos(self, fp, pos = 0, key_str = ''):
        num = 0
        firstcnt = 1
        second_pos = 0
        fp.seek(pos, os.SEEK_END)
        len_ = fp.tell()
#        keys = ['stream', 'xref', 'startxref', '%%EOF', ' obj']
        SEARCHDEF = ['\n', '\r', ' ', '<', '[']
        SEARCHDEF1 = ['\n', '\r', ' ', '<', '[']
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
#                    if self.DEBUG:
#                        print(fp.read(10))
#                        fp.seek(10, -1)
                else:
                    fp.seek(key_len, 1)
#                    if self.DEBUG:
#                        print(fp.read(10))
#                        fp.seek(10, -1)
                if key_str == '%%EOF':
                    SEARCHDEF = SEARCHDEF1
                tem = fp.read(1)
                if tem in SEARCHDEF:
#                    if firstcnt == 1:
#                    if tem in SEARCHDEF1:
#                        fp.seek(0 - key_len, 1)
#                    else:
                    fp.seek(0 - key_len - 1, 1)
                    #fp.seek(-10, 1)
                    buf = fp.read(key_len)
                    #print(buf)
    #                if tem in search_def:
#                    if buf.find('ream') != -1:
#                        pass
                    if buf == key_str:
#                        if self.DEBUG == 12098:
#                            tembuf = fp.read()
#                            temfp = open('debug.txt', 'w')
#                            temfp.write(tembuf)
#                            temfp.close()
                        tem = fp.read(1)
                        if tem in SEARCHDEF:
                            pos = fp.tell() - 1
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
        
        
        
        
        
        
        
        
        
        
        
        
        