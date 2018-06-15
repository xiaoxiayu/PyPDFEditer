import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyHighlighter( QSyntaxHighlighter ):
    
    def __init__( self, parent, theme ):
        QSyntaxHighlighter.__init__( self, parent )
        self.parent = parent
        keyword = QTextCharFormat()
        reservedClasses = QTextCharFormat()
        assignmentOperator = QTextCharFormat()
        delimiter = QTextCharFormat()
        specialConstant = QTextCharFormat()
        stream = QTextCharFormat()
        number = QTextCharFormat()
        comment = QTextCharFormat()
        string = QTextCharFormat()
        singleQuotedString = QTextCharFormat()
        fortest = QTextCharFormat()
        gtmark = QTextCharFormat()
        objbeg = QTextCharFormat()
        
        self.highlightingRules = []
        
        
        # comment
        brush = QBrush( Qt.gray, Qt.SolidPattern )
        pattern = QRegExp( "%[^\n]*" )
        comment.setForeground( brush )
        rule = HighlightingRule( pattern, comment )
        self.highlightingRules.append( rule )
        
        # keyword
        brush = QBrush( Qt.darkRed, Qt.SolidPattern )
        keyword.setForeground( brush )
        keyword.setFontWeight( QFont.Bold )
        keywords = QStringList( [ "endobj", "obj" ] )
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule( pattern, keyword )
            self.highlightingRules.append( rule )
        
        # object start
        objbeg.setForeground( brush )
        objbeg.setFontWeight( QFont.Bold )
        pattern = QRegExp("(\d+\s*\d+\s*)obj\s*")
        rule = HighlightingRule( pattern, objbeg )
        self.highlightingRules.append( rule )
        
        #'<<' an '>>'
        brush = QBrush( Qt.blue, Qt.SolidPattern )
        gtmark.setForeground( brush )
        gtmark.setFontWeight( QFont.Bold )
        keywords = QStringList( [ ">>", "<<" , "/"] )
        for word in keywords:
            pattern = QRegExp( word )
            rule = HighlightingRule( pattern, gtmark )
            self.highlightingRules.append( rule )
        
        # reservedClasses
        reservedClasses.setForeground( brush )
        reservedClasses.setFontWeight( QFont.Bold )
        keywords = QStringList( [ "Type", "BaseFont", "Kids", "Page", "Parent", "Form", "FormType",
                                  "Annot", "Subtype", "Link", "MediaBox", "Matrix", "BBox", "Popup",
                                  "Pages", "Catalog", "AcroForm", "Contents", "Resources", 
                                  "Length", "Filter", "FlateDecode", "Rect", "CreationDate",
                                  "Font", "Root", "Size", "Count"] )
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule( pattern, reservedClasses )
            self.highlightingRules.append( rule )


        # assignmentOperator
        brush = QBrush( Qt.red, Qt.SolidPattern )
        pattern = QRegExp( "(<){1,2}-" )
        assignmentOperator.setForeground( brush )
        assignmentOperator.setFontWeight( QFont.Bold )
        rule = HighlightingRule( pattern, assignmentOperator )
        self.highlightingRules.append( rule )
        
        # fortest
        #      brush = QBrush( Qt.darkYellow, Qt.SolidPattern )
        #      pattern = QRegExp( "(?=ab)" )
        #      fortest.setForeground( brush )
        #      fortest.setFontWeight( QFont.Bold )
        #      rule = HighlightingRule( pattern, fortest )
        #      self.highlightingRules.append( rule )
        
        # delimiter
        pattern = QRegExp( "[\)\(]+|[\{\}]+|[][]+" )
        delimiter.setForeground( brush )
        delimiter.setFontWeight( QFont.Bold )
        rule = HighlightingRule( pattern, delimiter )
        self.highlightingRules.append( rule )
        
        # specialConstant
        brush = QBrush( Qt.green, Qt.SolidPattern )
        specialConstant.setForeground( brush )
        keywords = QStringList( [ "Inf", "NA", "NaN", "NULL" ] )
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule( pattern, specialConstant )
            self.highlightingRules.append( rule )

        # boolean
        brush = QBrush( Qt.darkGreen, Qt.SolidPattern )
        specialConstant.setForeground( brush )
        stream.setForeground( brush )
        stream.setFontWeight( QFont.Bold )
        keywords = QStringList( [ "stream", "endstream" ] )
        #pattern = QRegExp("stream.*endstream|stream(.|\n)*endstream")
        #pattern = QRegExp(QString("[\s]*f[\s\S]f[\s]*$"))
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule( pattern, specialConstant )
            self.highlightingRules.append( rule )
        
#        pattern = QRegExp(QString("f[\r\n]f"))
#        rule = HighlightingRule( pattern, stream )
#        self.highlightingRules.append( rule )
#        for word in keywords:
#            pattern = QRegExp("\\b" + word + "\\b")
#            rule = HighlightingRule( pattern, stream )
#            self.highlightingRules.append( rule )

        # number
        pattern = QRegExp( "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" )
        pattern.setMinimal( True )
        #number.setForeground( brush )
        rule = HighlightingRule( pattern, number )
        self.highlightingRules.append( rule )
        
        
        
        # string
        brush = QBrush( Qt.darkGreen, Qt.SolidPattern )
        pattern = QRegExp( "\".*\"" )
        pattern.setMinimal( True )
        string.setForeground( brush )
        rule = HighlightingRule( pattern, string )
        self.highlightingRules.append( rule )
        
        # singleQuotedString
        pattern = QRegExp( "\'.*\'" )
        pattern.setMinimal( True )
        singleQuotedString.setForeground( brush )
        rule = HighlightingRule( pattern, singleQuotedString )
        self.highlightingRules.append( rule )

    def highlightBlock( self, text ):
        for rule in self.highlightingRules:
            expression = QRegExp( rule.pattern )
            index = expression.indexIn( text )
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat( index, length, rule.format )
                index = text.indexOf( expression, index + length )
        self.setCurrentBlockState( 0 )

class HighlightingRule():
    def __init__( self, pattern, format ):
        self.pattern = pattern
        self.format = format
    
class TestApp( QMainWindow ):
    def __init__(self):
        QMainWindow.__init__(self)
        font = QFont()
        font.setFamily( "Courier" )
        font.setFixedPitch( True )
        font.setPointSize( 10 )
        editor = QTextEdit()
        editor.setFont( font )
        highlighter = MyHighlighter( editor, "Classic" )
        
        editor.append('f\rf')
        self.setCentralWidget( editor )
        self.setWindowTitle( "Syntax Highlighter" )


if __name__ == "__main__":
    app = QApplication( sys.argv )
    window = TestApp()
    window.show()
    sys.exit( app.exec_() )