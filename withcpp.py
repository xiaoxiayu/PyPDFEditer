'''
Created on 2013-1-8
a
@author: xiaoxia_yu
'''

import sys
#from PyQt4 import QtGui, QtCore
#import threading
#from FXPDFParser import FxPdfParser as Parser
import os


pathname = 'D:\\testpdf\\as'
os.chdir(pathname)
def ParseFileName(file_name):
    file_nameL = file_name.split('_')
    test_module = file_nameL[0]
    data_oneD = {}
    if file_nameL.__len__() % 2 == 0:
        print('leak key or value.')
        return
    test_id = 0
    #print(file_nameL)
    i = 2
    while 1:
        if i >= file_nameL.__len__() - 1:
            break
        data_oneD[file_nameL[i]] = file_nameL[i + 1]
        
        i = i + 2
        test_id = test_id + 1
    print(data_oneD)
    return data_oneD

        
    #FSPDF_Doc_CountPages[] = {}

    
def GenerateTestData():
    global pathname
    data_doc_allD = {}
    test_file_id = 0
    for myroot, dirL, fileL in os.walk(pathname):
        for file_name in fileL:
            if file_name.find('.pdf') != -1:
                test_dataD = ParseFileName(file_name)
                test_file_name = os.path.abspath(file_name)
                data_doc_allD[test_file_name] = test_dataD
                test_file_id = test_file_id + 1
                
                print('*************************')
    print(data_doc_allD)
    return data_doc_allD
        
def GetAllObj(filename):
    fp = file(filename, 'rb')
    print(fp)
    tem = Parser(fp)
    XrefPosL = tem.GetXrefContent()
    trailerPosL = tem.GetTrailerPos()
    #print(trailerPosL)

    rootPosL = tem.GetRootObj()
    #print(rootPosL)
##    if trailerPosL.__len__() != 0:
####        buf = self.GetOrigionBuf(fp)
####        self.ui.textEdit.insertPlainText(buf)
####    else:
##        objPosL = tem.GetObjPosFromXref(XrefPosL, trailerPosL)
##        print(objPosL)
###                self.objNumL = tester.GetObjNumFromPos(objPosL)
##        streamBufD = {}                
##        objPosL.sort()
##        objName = tem.GetObjNameFromPosL(objPosL)
##        print(objName)
##        for objPos in objPosL:
##            #print(objPos)
##            objNum = tem.GetObjNumFromPos(objPos)
            

##            print(objNum)
            
 
##            self.objBufD[objNum] = objBuf
##            self.objStreamBufD[objNum] = (streamInfo)
                    
if __name__ == "__main__":
    #GetAllObj()
    #print(sys.path)
    GenerateTestData()


    
