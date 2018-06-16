
import string
import re
import StringIO
import zlib
import binascii

class StreamEncoder():
    def __init__(self, data, pos=0):
        self.buf = data
        self.data = data
    
    def toStr(self, _str):
        return _str and chr(string.atoi(_str[:2], base = 16)) + self.toStr(_str[2:]) or ''
    
    def runLengthEncode(self, _str):
        """Encode a string with a run-length encoding.    
        """
        
        # If empty string is received return empty plus EOD marker.
        if len(_str) == 0:
            return chr(0) + chr(128)
        
        encStr = ''
        i = 0
    
        while 1:
            # Find out length of first block with all chars the same.
            # re module might be too expensive here, maybe pre-compute 
            # later...
            c = _str[i]
            p = re.compile("(%s+)" % c)
            m = p.match(_str[i:])   # Must match!
            l = len(m.groups()[0])
       
            # Do the encoding.
            # Not quite clear yet, why there should be a distinction
            # between lengths smaller than 128 and larger than 128 bytes.
            if 1 <= l <= 128:
                encStr = encStr + chr(l) + c
                i = i + l
            elif 129 <= l <= 255:
                encStr = encStr + chr(257-l) + c
                i = i + l
                
            # Stop if all done.
            if i > len(_str)-1:
                break
    
        # Return encoded string plus EOD marker.
        return encStr + chr(128)
    
    def asciiHexEncode(self, _str):
        """Encode a string to its ASCII-Hex form.
        
        One character is replaced with two and a trailing '>' is added.
         
        E.g. "ABC" -> "414243>"
        """
        s = ''
        
        for i in xrange(len(_str)):
            s = s + hex(ord(_str[i]))[2:]
        
        return s + '>'
        
    def ascii85EncodeDG(self, _str):
        "Encode a string according to ASCII-Base-85."
        
        result = ''
        fetched = 0
        
        while 1:
            buf = map(lambda x:ord(x)+0L, _str[fetched:fetched+4])
            fetched = fetched + len(buf)
            
            if not buf:
                break
                
            while fetched % 4:
                buf.append(0)
                fetched = fetched + 1
                
            num = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8) + buf[3]
            if num == 0:
                #return 'z'
                res = []
                res.append(ord('z'))
                result = result + string.join(map(chr, res), '')
                
            else:    
                res = [0] * 5
                for i in (4, 3, 2, 1, 0):
                    res[i] = ord('!') + num % 85
                    num = num / 85
                    
                res = res[:len(_str)+1]
                result = result + string.join(map(chr, res), '')
            
        return result + "~>"
    
    def ZlibCompress(self, data):
        return zlib.compress(data.strip("\r\n").strip("\n\r"))
    
    def HexToASC(self, data):
        return binascii.a2b_hex(data.replace("\n", ""))
    
    def ASCIIHexEncode(self, data):
        return binascii.hexlify(data.replace("\r", "").replace("\n", "").replace(" ", "").strip("<").strip(">"))
    
#    def EncodeType(self, buf):
#        decode_type = {}
#        decode_pos = buf.find('LZWDecode')
#        if decode_pos != -1:
#            decode_type[decode_pos] = 'LZWDecode'
#            
#        decode_pos = buf.find('ASCII85Decode')
#        if decode_pos != -1:
#            decode_type[decode_pos] = 'ASCII85Decode'
#        
#        decode_pos = buf.find('FlateDecode')    
#        if decode_pos != -1:
#            decode_type[decode_pos] = 'FlateDecode'
#            
#        decode_pos = buf.find('ASCII85Decode')
#        if decode_pos != -1:
#            decode_type[decode_pos] = 'ASCII85Decode'
#        
#        decode_pos = buf.find('RunLengthDecode')
#        if decode_pos != -1:
#            decode_type[decode_pos] = 'RunLengthDecode'
#            
#        decode_pos = buf.find('DCTDecode')
#        if decode_pos != -1:
#            decode_type[decode_pos] = 'DCTDecode' 
#            
#        return decode_type
    
    
    
FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])    
class StreamDecoder():
    def __init__(self, data = '', pos=0):
        self.buf = data
        self.data = data
    
    def toHex(self, src):
        lst = []
        for ch in src:
            hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0' + hv
            lst.append(hv)
            
        return reduce(lambda x, y:x+y, lst)
    
    def HexDump(self, src=None, length=8, baseoffset=0, bsize=512):
        """ Show hexadecimal dump for the the given buffer """
        
        if not src:
            src = self.buf[:bsize]
        
        N=0; result=''
        while src:
            s,src = src[:length],src[length:]
            hexa = ' '.join(["%02X"%ord(x) for x in s])
            s = s.translate(FILTER)
            result += "%04X   %-*s   %s\n" % (N+baseoffset, length*3, hexa, s)
#            result += ("%s\n" % hexa)
            #print(result)
            N+=length
            if N>=bsize:
                break
        return result
    
    def asciiHexDecode(self, _str):
        """Decode an ASCII-Hex-encoded string.
    
        Odd number of hex digits will be padded with a trailing '0'.
        E.g. "414243>" -> "ABC" and "4142435>" -> "ABCP" 
        """
        st = _str[:]
        s = ''
        
        if len(st) % 2 == 0 and st[-1] == '>':
            st = st[:-1] + "0"
        
        for i in xrange(0, len(st)-1, 2):
            a, b = st[i], st[i+1]
            h = "0x" + a + b
            s = s + chr(eval(h))
        
        return s

    
    def LZWDecode(self, data):
        """
        >>> lzwdecode('\x80\x0b\x60\x50\x22\x0c\x0c\x85\x01')
        '\x2d\x2d\x2d\x2d\x2d\x41\x2d\x2d\x2d\x42'
        """
        fp = StringIO(data)
        return ''.join(LZWDecoder(fp).run())
    
    # Shamelessly ripped from pyPDF
    def ASCII85Decode(self, data):
        retval = ""
        group = []
        x = 0
        hitEod = False
        # remove all whitespace from data
        data = [y for y in data if not (y in ' \n\r\t')]
        while not hitEod:
            c = data[x]
            if len(retval) == 0 and c == "<" and data[x+1] == "~":
                x += 2
                continue
            #elif c.isspace():
            #    x += 1
            #    continue
            elif c == 'z':
                assert len(group) == 0
                retval += '\x00\x00\x00\x00'
                x += 1
                continue
            elif c == "~" and data[x+1] == ">":
                if len(group) != 0:
                    # cannot have a final group of just 1 char
                    assert len(group) > 1
                    cnt = len(group) - 1
                    group += [ 85, 85, 85 ]
                    hitEod = cnt
                else:
                    break
            else:
                c = ord(c) - 33
                assert c >= 0 and c < 85
                group += [ c ]
            if len(group) >= 5:
                b = group[0] * (85**4) + \
                    group[1] * (85**3) + \
                    group[2] * (85**2) + \
                    group[3] * 85 + \
                    group[4]
                assert b < (2**32 - 1)
                c4 = chr((b >> 0) % 256)
                c3 = chr((b >> 8) % 256)
                c2 = chr((b >> 16) % 256)
                c1 = chr(b >> 24)
                retval += (c1 + c2 + c3 + c4)
                if hitEod:
                    retval = retval[:-4+hitEod]
                group = []
            x += 1
        return retval
    # Shamelessly ripped from pdfminerr http://code.google.com/p/pdfminerr
    def RunLengthDecode(self, data):
        """
        RunLength decoder (Adobe version) implementation based on PDF Reference
        version 1.4 section 3.3.4:
            The RunLengthDecode filter decodes data that has been encoded in a
            simple byte-oriented format based on run length. The encoded data
            is a sequence of runs, where each run consists of a length byte
            followed by 1 to 128 bytes of data. If the length byte is in the
            range 0 to 127, the following length + 1 (1 to 128) bytes are
            copied literally during decompression. If length is in the range
            129 to 255, the following single byte is to be copied 257 - length
            (2 to 128) times during decompression. A length value of 128
            denotes EOD.
        >>> s = "\x05123456\xfa7\x04abcde\x80junk"
        >>> rldecode(s)
        '1234567777777abcde'
        """
        decoded = []
        i=0
        while i < len(data):
            #print "data[%d]=:%d:" % (i,ord(data[i]))
            length = ord(data[i])
            if length == 128:
                break
            if length >= 0 and length < 128:
                run = data[i+1:(i+1)+(length+1)]
                #print "length=%d, run=%s" % (length+1,run)
                decoded.append(run)
                i = (i+1) + (length+1)
            if length > 128:
                run = data[i+1]*(257-length)
                #print "length=%d, run=%s" % (257-length,run)
                decoded.append(run)
                i = (i+1) + 1
        return ''.join(decoded)

    def ZlibDecompress(self, data):
        return zlib.decompress(data.strip("\r\n").strip("\n\r"))
    
    def ASCToHex(self, data):
        return binascii.b2a_hex(data)
    
    def ASCIIHexDecode(self, data):
        return binascii.unhexlify(data.replace("\r", "").replace("\n", "").replace(" ", "").strip("<").strip(">"))
    
    def DecodeType(self, buf):
        decode_type = {}
        decode_pos = buf.find('LZWDecode')
        if decode_pos != -1:
            decode_type[decode_pos] = 'LZWDecode'
            
        decode_pos = buf.find('ASCII85Decode')
        if decode_pos != -1:
            decode_type[decode_pos] = 'ASCII85Decode'
        
        decode_pos = buf.find('FlateDecode')    
        if decode_pos != -1:
            decode_type[decode_pos] = 'FlateDecode'
            
        decode_pos = buf.find('ASCII85Decode')
        if decode_pos != -1:
            decode_type[decode_pos] = 'ASCII85Decode'
        
        decode_pos = buf.find('RunLengthDecode')
        if decode_pos != -1:
            decode_type[decode_pos] = 'RunLengthDecode'
            
        decode_pos = buf.find('DCTDecode')
        if decode_pos != -1:
            decode_type[decode_pos] = 'DCTDecode' 
            
        return decode_type
    
class LZWDecoder(object):

    debug = 0

    def __init__(self, fp):
        self.fp = fp
        self.buff = 0
        self.bpos = 8
        self.nbits = 9
        self.table = None
        self.prevbuf = None
        return

    def readbits(self, bits):
        v = 0
        while 1:
            # the number of remaining bits we can get from the current buffer.
            r = 8-self.bpos
            if bits <= r:
                # |-----8-bits-----|
                # |-bpos-|-bits-|  |
                # |      |----r----|
                v = (v<<bits) | ((self.buff>>(r-bits)) & ((1<<bits)-1))
                self.bpos += bits
                break
            else:
                # |-----8-bits-----|
                # |-bpos-|---bits----...
                # |      |----r----|
                v = (v<<r) | (self.buff & ((1<<r)-1))
                bits -= r
                x = self.fp.read(1)
                if not x: raise EOFError
                self.buff = ord(x)
                self.bpos = 0
        return v

    def feed(self, code):
        x = ''
        if code == 256:
            self.table = [ chr(c) for c in xrange(256) ] # 0-255
            self.table.append(None) # 256
            self.table.append(None) # 257
            self.prevbuf = ''
            self.nbits = 9
        elif code == 257:
            pass
        elif not self.prevbuf:
            x = self.prevbuf = self.table[code]
        else:
            if code < len(self.table):
                x = self.table[code]
                self.table.append(self.prevbuf+x[0])
            else:
                self.table.append(self.prevbuf+self.prevbuf[0])
                x = self.table[code]
            l = len(self.table)
            if l == 511:
                self.nbits = 10
            elif l == 1023:
                self.nbits = 11
            elif l == 2047:
                self.nbits = 12
            self.prevbuf = x
        return x

    def run(self):
        while 1:
            try:
                code = self.readbits(self.nbits)
            except EOFError:
                break
            x = self.feed(code)
            yield x
            if self.debug:
#                print >>stderr, ('nbits=%d, code=%d, output=%r, table=%r' %
#                                 (self.nbits, code, x, self.table[258:]))
                print('Debug have closed in souce code')
        return
    
