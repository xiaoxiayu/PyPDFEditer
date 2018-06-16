'''
Created on 2013-1-8
a
@author: xiaoxia_yu
'''

import sys
from PyQt4 import QtGui, QtCore
import threading
from FXPDFParser import FxPdfParser
from FXPDFWriter import FxPdfWriter
from FXStreamCoder import StreamDecoder, StreamEncoder, LZWDecoder
from PyPDF2 import PdfFileReader
##pdf = PdfFileReader(open('E:/3bigpreview.pdf', 'rb'))

##from cStringIO import StringIO
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
#import chardet
import re
#sys.path.append('PDFEditerPageUI.py')
from PDFEditerUI import Ui_MainWindow
from PDFEditerPageUI import Ui_Dialog
import PDFEditerExportUI
import PDFEditerFinderUI 
import PDFEditerObjectUI
import string
import os
import time
import urllib
#import zlib
#import binascii
from SyntaxHighLight import MyHighlighter



def list2str(self,list_in):
    return reduce(self.list0str, list_in, "")

class ExportWindow(QtGui.QWidget):
    def __init__(self, parent=None, PDFParser=None, objStreamBufD={}):
        QtGui.QWidget.__init__(self, parent)
        self.ui = PDFEditerExportUI.Ui_Dialog()
        self.ui.setupUi(self)
        self.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self.SaveStream)
        self.PDFParser = PDFParser
        self.objStreamBufD = objStreamBufD

    def SaveStream(self):
        textline_str = self.ui.lineEdit.text()
        textline_str = str(textline_str)
        objNum = string.atoi(textline_str, 10)
        streamInfo = self.objStreamBufD[objNum]
        writer = FxPdfWriter()
        buf = writer.ExportIMGStream(streamInfo)                           
                
        filename = QtGui.QFileDialog.getSaveFileNameAndFilter(self, 'Save', '', '*.jpg')
        if not filename[0].isEmpty():
            print(filename[0])
            fp = file(filename[0], 'wb')
            fp.write(buf)
            fp.close()
#        else:
#            print('Did not suppot Export')

class ObjectWindow(QtGui.QWidget):
    def __init__(self, parent=None, PDFParser=None, objBufD={}):
        QtGui.QWidget.__init__(self, parent)
        self.ui = PDFEditerObjectUI.Ui_Dialog()
        self.ui.setupUi(self)
        self.connect(self.ui.pushButton_ok, QtCore.SIGNAL('clicked()'), self.GetObj)
        self.PDFParser = PDFParser
        self.objBufD = objBufD
    
    def Parser(self):
        pass
    
    global objlist_all
    objlist_all = []
    def _LoopGetObj(self, objBuf):
        refL = self.PDFParser.GetObjBufRef(objBuf)
        for refNum in refL:
            if refNum in objlist_all:
                pass
            else:
                objlist_all.append(refNum)
                refBuf = self.objBufD[refNum]
                self.ui.textBrowser.append('\n+Object: ' + str(refNum))
                refBufNS = self.PDFParser.DelObjBufStream(refBuf)
                self.ui.textBrowser.append(refBufNS)
                self._LoopGetObj(refBufNS)

                
    def GetObj(self):
        self.ui.textBrowser.clear()
        global objlist_all
        objlist_all = []
        textline_str = self.ui.lineEdit.text()
        textline_str = str(textline_str)
        numStrL = textline_str.split(',')
        
        for objStr in numStrL:
            if objStr.find('*') != -1:
                objlist_all = []
                str_num = objStr[:objStr.__len__() - 1]
                objNum = string.atoi(str_num)
                objBuf = self.objBufD[objNum]
                
                #obj_str = str(obj_str)
                self.ui.textBrowser.append('*Object: ' + str(objNum))
                self.ui.textBrowser.append(str(objBuf) + '\n')
                
                self._LoopGetObj(objBuf)

            else:
                objNum = string.atoi(objStr)
                try:
                    objBuf = self.objBufD[objNum]
                except KeyError:
                    objBuf = 'NO FIND'
                self.ui.textBrowser.append('\n*Object: ' + str(objNum))
                objBufNS = self.PDFParser.DelObjBufStream(objBuf)
                self.ui.textBrowser.append(objBufNS)        
            
class PageWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
#        self.button_obj = ObjectWindow()
        #self.connect(self.ui.toolButton_GetObj, QtCore.SIGNAL('clicked()'), self.GetObjAction)
        
#def convert_pdf(path):
#    rsrcmgr = PDFResourceManager()
#    retstr = StringIO()
#    codec = 'ascii'
#    laparams = LAParams()
#    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
#
#    fp = file(path, 'rb')
#    process_pdf(rsrcmgr, device, fp)
#    fp.close()
#    device.close()
#
#    str = retstr.getvalue()
#    retstr.close()
##    print(str)
#    return str

    
class PDFWriter():
    def __init__(self, fp, stream, posoffsets_list, posobjs_list):
        self.buf_new = '' 
        self.stream = stream
        self.offsets_list = []
        self.posobjs_list = posobjs_list
        self.xrefstr = []
        self.startxref = []
        self.xrefpos_list = []
        self.fp = fp
        self.writer = None
        self.posoffsets_list = posoffsets_list
        self.posobjs_list = posobjs_list
        
        
        #self.GenerationNewPDF(self.buf, self.offsets_list)
    
    def ParsePdfText(self):
        self.writer = FxPdfWriter(self.stream)
        self.writer.Parse()
                
    def StreamEncode(self, stream):
        objStreamD = self.writer.ObjStreamD
        stream_buf = {}
        stream_end = {}
        objNums = objStreamD.keys()
        objNums.sort()

        for num in objNums:
            if objStreamD[num] != None:
                try:
                    pos0 = objStreamD[num][1][0]
#                    stream.seek(pos0)
#                    print(stream.read(500))
                except:
                    pass
                pos1 = objStreamD[num][1][1]
                stream_tem = objStreamD[num][0][1]
                encoder = StreamEncoder(' ')
                encodeTypeL = objStreamD[num][0][0]
                try:
                    for encodeType in encodeTypeL:
                        if cmp(encodeType, 'FlateDecode') == 0:
                            stream_tem = stream_tem.strip('\r\n')
                            isHex = stream_tem[:6]
                            if isHex == 'HEX1: ':
                                stream_tem = stream_tem[6:]
#                            if stream_tem.isdigit() == True:
                                encode_stream = encoder.HexToASC(stream_tem)#binascii.a2b_hex(stream_tem)
                                encode_stream = encoder.ZlibCompress(encode_stream)#zlib.compress(encode_stream)
                            elif isHex == 'HEX0: ':
                                stream_tem = stream_tem[6:]
#                            if stream_tem.isdigit() == True:
                                encode_stream = encoder.HexToASC(stream_tem)#binascii.a2b_hex(stream_tem)
#                                encode_stream = zlib.compress(encode_stream)
                            else:
                                encode_stream = encoder.ZlibCompress(stream_tem)#zlib.compress(stream_tem)
                        if cmp(encodeType, 'DCTDecode') == 0:
                            encode_stream = encoder.HexToASC(stream_tem)#binascii.a2b_hex(stream_tem.replace("\n", ""))
                        if cmp(encodeType, 'LZWDecode') == 0:
                            encode_stream = encoder.LZWDecode(stream_tem)
                            #decode_stream = decoder.HexDump(stream_tem, 16)
                        if cmp(encodeType, 'ASCIIHexDecode') == 0:
                            encode_stream = encoder.ASCIIHexEncode(stream_tem)#binascii.hexlify(stream_tem.replace("\r", "").replace("\n", "").replace(" ", "").strip("<").strip(">"))
                        if cmp(encodeType, 'ASCII85Decode') == 0:
                            encode_stream = encoder.ascii85EncodeDG(stream_tem.strip("\r\n").strip("\n"))
                            #encode_stream = encoder.ascii85EncodeDG(stream_tem)
                        if cmp(encodeType, 'RunLengthDecode') == 0:
                            encode_stream = encoder.runLengthEncode(stream_tem)
                        stream_tem = encode_stream
                except:
                    failed = True
                    print('Error applying filter')
                    encode_stream = stream_tem
                if encodeTypeL.__len__() == 0:
                    encode_stream = stream_tem
                
                stream_buf[pos0] = encode_stream
                stream_end[pos0] = pos1
#                pre_pos1 = pos1
#                cnt = 1
#        stream.seek(0)
        return (stream_buf, stream_end)
        
    def RegenrationPdfBuf(self, fp, re_dic):
        buf_new = ''
        fp.seek(0)
        stream_buf = re_dic[0]
        stream_end = re_dic[1]
        streamkeys = stream_buf.keys()
        streamkeys.sort()
        num = 1
        read_len = 0
        pos_pre = 0
        for pos in streamkeys:
            if num == 1:
                read_len = pos
            else:
                #tem = int(pos)
                read_len = pos - pos_pre + 9
                #tem = fp.read()
            try:
                #buf = fp.read().decode('windows-1252')
                buf = fp.read(read_len)
#                print(buf)
            except:
                try:
                    buf = fp.read(read_len).decode('ISO-8859-1')
                except:
                    try:
                        buf = fp.read(read_len).decode('ISO-8859-2')
                    except:
                        buf = fp.read(read_len).decode('windows-1252')
                
            buf_new += buf + '\r\n'
            buf_new += stream_buf[pos] + '\r\n'
           
            fp.seek(0)
            fp.seek(stream_end[pos] - 9, 0)
            
            pos_pre = stream_end[pos]
            num = 2
       
        #fp.seek(3180, 0)
        try:
            #buf = fp.read().decode('ISO-8859-2')
            buf = fp.read()
        except:
            buf = fp.read().decode('ISO-8859-2')
            #buf = fp.read().decode('windows-1252')
        #self.ui.textEdit.append(buf)
        buf_new += buf
        return buf_new
    
        
    def Generation(self):
#        tem_fp = file('C:\\Users\\Administrator\\Desktop\\test222.pdf', 'wb')
        re_dic = self.StreamEncode(self.stream)
        buf_new = self.RegenrationPdfBuf(self.stream, re_dic)
        
        stream = StringIO(buf_new)
        self.writer.ReParser(stream)
#        writer2 = FxPdfWriter(stream)
#        writer2.Parse()
        rootNum = self.writer.RootNum
        buf_new = ''
#        stream.seek(0, os.SEEK_END)
#        slen = stream.tell()
#        stream.seek(0)

        xrefInfo = self.writer.XrefInfo
        xrefPosL = xrefInfo[0]
        eofPosL = xrefInfo[1]
        
        #        #Delete old xref data
        stream.seek(0)
        num = 0
        while num < xrefPosL.__len__():
            if num == 0:
                buf_new = stream.read(xrefPosL[num] - 4)
                stream.seek(0)
                stream.seek(eofPosL[num])
            else:
                tem = stream.read(xrefPosL[num] - eofPosL[num - 1])
                buf_new += tem
                stream.seek(eofPosL[num])
            num += 1

#        tem_fp.write(buf_new)
        self.fp.write(buf_new)
        stream.seek(0)
        
        #Get Object xref position
        stream = StringIO(buf_new)
        self.writer.ReParser(stream)
        stream.seek(0, os.SEEK_END)
        startxref_value = stream.tell()
        stream.seek(0)
#        offsets_list = self.GetObjPos(stream, self.posoffsets_list, self.posobjs_list)

        objPosD = self.writer.ObjPosD
        
        self.writer.GeneratorXref(self.fp, objPosD, rootNum, startxref_value)
        
            

class FinderWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = PDFEditerFinderUI.Ui_Form()
        self.ui.setupUi(self)
        
        self.connect(self.ui.btn_fobj, QtCore.SIGNAL('clicked()'), self.FindObj)
        self.connect(self.ui.btn_findp, QtCore.SIGNAL('clicked()'), self.FindTextp)
        self.connect(self.ui.btn_findn, QtCore.SIGNAL('clicked()'), self.FindTextn)
        
    def FindTextn(self):
        getstr = self.ui.textEdit.toPlainText()
        if self.ui.btn_findp.isEnabled() == False:
            myapp.ui.textEdit.moveCursor(QtGui.QTextCursor.Start)
      
        if myapp.ui.textEdit.find(getstr):     
            self.ui.btn_findp.setEnabled(True);
        else:
            QtGui.QMessageBox.information(self, 'result', \
                                      "no find: \"" + getstr + "\"", QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)
        
    def FindTextp(self):
        getstr = self.ui.textEdit.toPlainText()
        ret = myapp.ui.textEdit.find(getstr, QtGui.QTextDocument.FindBackward)
        if ret == False:
            QtGui.QMessageBox.information(self, 'result', \
                                      "no find: \"" + getstr + "\"", QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)
    def FindObj(self):
        obj = self.ui.lineEdit.displayText()
        objstr = str(obj) + ' 0 ' + 'obj'
        myapp.setEnabled(True)
        ret = myapp.ui.textEdit.find(objstr, QtGui.QTextDocument.FindBackward)
        if ret == False:
            ret = myapp.ui.textEdit.find(objstr, QtGui.QTextDocument.FindBackward)
            if ret == False:
                QtGui.QMessageBox.information(self, 'result', \
                                          "no find: \"" + objstr + "\"", QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)
        

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        font = QtGui.QFont()
        font.setFamily( "Courier" )
        font.setFixedPitch( True )
        font.setPointSize( 10 )
        self.ui.textEdit.setFont(font) 
        highlighter = MyHighlighter(self.ui.textEdit, "Classic" )  
        self.setCentralWidget( self.ui.textEdit )  
        self.setWindowTitle( "PDFTxtEditer" )  
        
        self.PDFParser = None
        self.posoffsets_list = []
        self.posobjs_list = []
        self.objNumL = []
        self.objBufD = {}
        self.objStreamBufD = {}
        self.pdf = None
        
        self.page_window = PageWindow()
#        self.obj_window = ObjectWindow(None, self.objNameL)
        self.finder_window = FinderWindow()
        
        self.connect(self.ui.actionTest, QtCore.SIGNAL('triggered()'), self.testAction)
        self.connect(self.ui.actionOpen, QtCore.SIGNAL('triggered()'), self.openAction)
        self.connect(self.ui.actionSave, QtCore.SIGNAL('triggered()'), self.SaveAction)
        self.connect(self.ui.actionInfo_Doc, QtCore.SIGNAL('triggered()'), self.DocInfoAction)
        self.connect(self.ui.actionOutLines, QtCore.SIGNAL('triggered()'), self.outlinesAction)
        self.connect(self.ui.actionNamedDestination, QtCore.SIGNAL('triggered()'), self.namedDestinationAction)
        
        self.connect(self.ui.actionInfo_Page, QtCore.SIGNAL('triggered()'), self.PageInfoAction)
        
        self.connect(self.ui.actionObjGet, QtCore.SIGNAL('triggered()'), self.ObjGetAction)
        
        self.connect(self.ui.actionFinder, QtCore.SIGNAL('triggered()'), self.FinderAction)
        
        self.connect(self.ui.actionExport, QtCore.SIGNAL('triggered()'), self.ObjExport)
        
        
    def FinderAction(self):
        self.finder_window.show()
        

    def ObjExport(self):
        self.export_window = ExportWindow(None, self.PDFParser, self.objStreamBufD)
        self.export_window.show()
        
    def ObjGetAction(self):
        self.obj_window = ObjectWindow(None, self.PDFParser, self.objBufD)
        self.obj_window.show()
        
    def PageInfoAction(self):
        self.page_window.ui.textBrowser.clear()        
        page_num = self.pdf.getNumPages()
        for i in range(0, page_num):
            page = self.pdf.getPage(i)
            page_info = str(page)
            print(i)
            print(page_info)
            self.page_window.ui.textBrowser.append('Page: ' + str(i) + '\n')
            self.page_window.ui.textBrowser.append(page_info + '\n')
        self.page_window.show()
            
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def testAction(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open')
        print(filename)
        if not filename.isEmpty():
            self.ui.textEdit.clear()
            
            fp = file(filename, 'rb')
            try:
            #buf = fp.read().decode('ISO-8859-2')
                buf = fp.read().decode('windows-1252')
            except:
                buf = fp.read().decode('ISO-8859-2')
            self.ui.textEdit.append(buf)
        
    def namedDestinationAction(self):
        name_des = self.pdf.getNamedDestinations()
        des_key_iter = name_des.iterkeys()
        for des_key in des_key_iter:
            print(des_key)
            print(name_des.get(des_key))
            des_value = name_des.get(des_key)
            des_value_iter = des_value.iterkeys()
            for des_value_key in des_value_iter:
                #print(des_value_key)
                print(des_value.get(des_value_key))
                des_page = des_value.get('/Page')
                #print(des_page)
                obj = self.pdf.getObject(des_page)
                obj1 = self.pdf.getObject(generic.IndirectObject(2,0,self.pdf))
                print(obj1)


            
    def outlinesAction(self):
        outlines_list = self.pdf.getOutlines()
        for outlines in outlines_list:
            print(outlines)
            outlines_key_iter = outlines.iterkeys()
            for outlines_key in outlines_key_iter:
                print(outlines.get('/Title'))
                print(outlines.get(outlines_key))
            
    
    def DocInfoAction(self):
        #ten = PDFDocument.get_dest(des_key)
        pdf_info = self.pdf.getDocumentInfo()
        if pdf_info == None:
            QtGui.QMessageBox.information(self, 'Document information', \
                                      'No info message!', QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)
            return
        if pdf_info.title == None:
            pdf_info_title = 'none'
        else:
            pdf_info_title = pdf_info.title
        if pdf_info.creator == None:
            pdf_info_creator = 'none'
        else:
            pdf_info_creator = pdf_info.creator
        if pdf_info.producer == None:
            pdf_info_producer = 'none'
        else:
            pdf_info_producer = pdf_info.producer
        if pdf_info.author == None:
            pdf_info_author = 'none'
        else:
            pdf_info_author = pdf_info.author
##        if pdf_info.creationdate == None:
        pdf_info_createdate = 'none'
##        else:
##            pdf_info_createdate = pdf_info.creationdate
##        if pdf_info.moddate == None:
        pdf_info_moddate = 'none'
##        else:
##            pdf_info_moddate = pdf_info.moddate
            
        xml_info = self.pdf.getXmpMetadata()
        #tem=xml_info.xmp_createDate
        if self.pdf.getXmpMetadata() == None:
            xml_info = 'none'
        
        pdf_info_encryed = self.pdf.getIsEncrypted()
        pdf_info_numpage = self.pdf.numPages
        doc_info = 'Title: ' + pdf_info_title + '\n'\
        + 'Creator: ' + pdf_info_creator + '\n'\
        + 'Producer: ' + pdf_info_producer + '\n'\
        + 'Author: ' + pdf_info_author + '\n'\
        + 'CreateDate: ' + pdf_info_createdate + '\n'\
        + 'ModDate: ' + pdf_info_moddate + '\n'\
        + 'PageNumber: ' + str(pdf_info_numpage)
        
            
##        print(pdf.getDocumentInfo())
        QtGui.QMessageBox.information(self, 'Document information', \
                                      doc_info, QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)


    def DecodeStream(self, streamBufD):
        stream = {}
        stream_end = {}
#        cnt = 0
#        pre_pos1 = 0
        try:
            if streamBufD[0] == 'error':
                return 'error'
        except:
            print('no obj pos 0')
        streamPos = streamBufD.keys()
        streamPos.sort()
        for pos in streamPos:
            if streamBufD[pos] != 'NoStream':
                encodeTypeL = streamBufD[pos][0][0]
                if encodeTypeL[0] != 'NoEncode':
                    stream_tem = streamBufD[pos][0][1]
                    decoder = StreamDecoder()
                    try:
                        for encodeType in encodeTypeL:
                            if cmp(encodeType, 'FlateDecode') == 0:
                                decode_stream = decoder.ZlibDecompress(stream_tem)#zlib.decompress(stream_tem.strip("\r\n").strip("\n\r"))
                                if decode_stream.find("\x00") != -1:
#                                    decode_stream = decoder.HexDump(decode_stream, 16)
                                    decode_stream = decoder.ASCToHex(stream_tem)#binascii.b2a_hex(stream_tem)
                                    decode_stream = 'HEX1: ' + decode_stream
                            if cmp(encodeType, 'DCTDecode') == 0: 
                                #if decode_keys.__len__() != 1:
                                decode_stream = decoder.ASCToHex(stream_tem)#binascii.b2a_hex(stream_tem)
        #                        else:
        #                            open("C:\\Users\\Administrator\\Desktop\\k1k.jpg", 'wb').write(decode_stream)
                            if cmp(encodeType, 'LZWDecode') == 0:
                                decode_stream = decoder.LZWDecode(stream_tem)
                                #decode_stream = decoder.HexDump(stream_tem, 16)
                            if cmp(encodeType, 'ASCIIHexDecode') == 0:
                                decode_stream = decoder.ASCIIHexDecode(stream_tem)#binascii.unhexlify(stream_tem.replace("\r", "").replace("\n", "").replace(" ", "").strip("<").strip(">"))
                            if cmp(encodeType, 'ASCII85Decode') == 0:
                                decode_stream = decoder.ASCII85Decode(stream_tem.strip("\r").strip("\n"))
                                #decode_stream = BASE85.b85decode(stream_tem.strip("\r").strip("\n"))
                            if cmp(encodeType, 'RunLengthDecode') == 0:
                                decode_stream = decoder.RunLengthDecode(stream_tem)
                            stream_tem = decode_stream
                    except:
#                        failed = True
                        #print "Error applying filter %n" % 1, sys.exc_info()[1]
                        #decode_stream = decoder.HexDump(stream_tem, 16)
                        print('Error applying filter')
#                        decode_stream = stream_tem
                        decode_stream = decoder.ASCToHex(stream_tem)#binascii.b2a_hex(stream_tem)
                        decode_stream = 'HEX0: ' + decode_stream
                else:
#                    decode_stream = stream_tem
                    decode_stream = decoder.ASCToHex(stream_tem)#binascii.b2a_hex(stream_tem)
                    decode_stream = 'HEX0: ' + decode_stream
                
                stream[streamBufD[pos][1][0]] = decode_stream
                stream_end[streamBufD[pos][1][0]] = streamBufD[pos][1][1]
#                pre_pos1 = streamBufD[pos][1][1]
#                cnt = 1
#        fp.seek(0)
        return (stream, stream_end)
    
    def DisplayPdfBuf(self, fp, re_dic):
        if re_dic == 'error':
            buf = self.GetOrigionBuf(fp)
            self.ui.textEdit.insertPlainText(buf)
            return
        fp.seek(0)
        stream = re_dic[0]
        stream_end = re_dic[1]
        streamkeys = stream.keys()
        streamkeys.sort()
        num = 1
        read_len = 0
        pos_pre = 0
        
        for pos in streamkeys:
            if num == 1:
                read_len = pos
            else:
                read_len = pos - pos_pre + 9
            try:
                buf = fp.read(read_len).decode('ISO-8859-1')
                #buf = fp.read(read_len)
                #print(buf)
            except:
                try:
                    buf = fp.read(read_len).decode('ISO-8859-2')
                except:
                    buf = fp.read(read_len).decode('windows-1252')
#                print(buf)
#                print(stream[pos])
#            print(buf)
            if buf.find('125 0 obj') != -1:
                pass
            #self.ui.textEdit.append(buf)
            self.ui.textEdit.insertPlainText(buf)
            try:
                streambuf = stream[pos].decode('ISO-8859-1')
            except:
                try:
                    streambuf = stream[pos].decode('ISO-8859-2')
                except:
                    streambuf = stream[pos].decode('windows-1252')
#            tem = streambuf[0]
#            tetype = type(tem)
#            print tetype
#            if type(tem) == type(0):
#                pass
            _len = streambuf.__len__()
            if _len > 1000000:
                streambuf = 'is too long to show'
                self.ui.textEdit.append(streambuf)
#            elif _len > 10000:
#                appendLen = 0
#                num = 0
#                remainLen = _len
#                while 1:
#                    tembuf = streambuf[appendLen : appendLen + 5000]
#                    self.ui.textEdit.append(tembuf)
#                    num += 1
#                    tem = remainLen / 5000
#                    if tem == 1:
#                        tem = remainLen % 5000
#                        if tem > 0 and tem < 5000:
#                            tembuf = streambuf[appendLen :]
#                            self.ui.textEdit.append(tembuf)
#                            break
#                    remainLen = _len - (5000 * num)
#                    appendLen += 5000
            else:
                self.ui.textEdit.append(streambuf) 
            #print(stream[pos])               
            fp.seek(0)
            fp.seek(stream_end[pos] - 9, 0)
            
            pos_pre = stream_end[pos]
            num = 2
        try:
            buf = fp.read().decode('ISO-8859-1')
#            buf = fp.read().decode('windows-1252')
        except:
            try:
                streambuf = stream[pos].decode('ISO-8859-2')
            except:
                streambuf = stream[pos].decode('windows-1252')
#        print(buf)
            #buf = fp.read().decode('windows-1252')
        #self.ui.textEdit.append(buf)
        self.ui.textEdit.insertPlainText(buf)
    
    #get  pos-obj like '456:1 0 obj'
    def ParseObjStr(self, fp, xrefinfo_list):
        for xrefinfo in xrefinfo_list:
            xref_offsets = xrefinfo.offsets
            xref_obj = xref_offsets.keys()
            xref_obj.sort()
            objstrs = {}
            for obj in xref_obj:
#                print(obj, xref_offsets[obj])
                fp.seek(xref_offsets[obj][1])
                tembuf = fp.read()
                
                pos0 = tembuf.find(' obj')
                #pos1 = tembuf.find('endobj')
                
                pos0 += 4
                objstr = tembuf[:pos0]
                objstrs[obj] = objstr
                
            self.posoffsets_list.append(xrefinfo.offsets)
            self.posobjs_list.append(objstrs)
            
    def SaveAction(self):
        filename = QtGui.QFileDialog.getSaveFileNameAndFilter(self, 'Save', '', '*.pdf')
        if not filename[0].isEmpty():
            print(filename[0])
            buf = self.ui.textEdit.toPlainText()
            buf = QtCore.QString.toAscii(buf)
            stream = StringIO(buf)
            fp = file(filename[0], 'wb')
            
            pdfwriter = PDFWriter(fp, stream, self.posoffsets_list, self.posobjs_list)
            pdfwriter.ParsePdfText()
            pdfwriter.Generation()
            
            fp.close()

    def GetOrigionBuf(self, fp):
        fp.seek(0)
        try:
            buf = fp.read().decode('ISO-8859-1')
        except:
            try:
                buf = fp.read().decode('ISO-8859-2')
            except:
                buf = fp.read().decode('windows-1252')
        return buf
            
    def openAction(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open')
        if not filename.isEmpty():
            self.ui.textEdit.clear()      
            fp = file(filename, 'rb')
            self.pdf = PdfFileReader(fp)
            self.PDFParser = FxPdfParser(fp)
            XrefPosL = self.PDFParser.GetXrefContent()
            trailerPosL = self.PDFParser.GetTrailerPos()
            if trailerPosL.__len__() == 0:
                buf = self.GetOrigionBuf(fp)
                self.ui.textEdit.insertPlainText(buf)
            else:
                objPosL = self.PDFParser.GetObjPosFromXref(XrefPosL, trailerPosL)
#                self.objNumL = tester.GetObjNumFromPos(objPosL)
                streamBufD = {}                
                objPosL.sort()
                for objPos in objPosL:
#                    print(objPos)
                    streamInfo = self.PDFParser.GetObjStreamInfo(objPos)
                    streamBufD[objPos] = (streamInfo)
                    objNum = self.PDFParser.GetObjNumFromPos(objPos)
                    objBuf = self.PDFParser.GetObjBuf(objPos)
                    self.objBufD[objNum] = objBuf
                    self.objStreamBufD[objNum] = (streamInfo)
                    
                
                re_dic = self.DecodeStream(streamBufD) 
                self.DisplayPdfBuf(fp, re_dic)          

            
     
if __name__ == "__main__":
#    tem = '  1    5 '
#    sp = tem.split(' ')
    app = QtGui.QApplication(sys.argv)
#    utfcodec = QtCore.QTextCodec.codecForName("GBK")
#    QtCore.QTextCodec.setCodecForTr(utfcodec)
#    QtCore.QTextCodec.setCodecForLocale(utfcodec)
#    QtCore.QTextCodec.setCodecForCStrings(utfcodec)
    myapp = MainWindow()
    myapp.show()
    
    sys.exit(app.exec_())


    
