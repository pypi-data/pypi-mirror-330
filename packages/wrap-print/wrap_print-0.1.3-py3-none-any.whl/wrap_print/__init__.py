import unicodedata

class WrapPrint:
    def __init__(self, width=80):
        self.width = width
        self.pos = 0

    def print(self, text, end='\n'):
        while True:
            if text == '': # no text left
                break
            next_pos = text.find('\n') # find the next newline
            next_pos = next_pos if next_pos != -1 else len(text) # split text
            next_pos += 1 # include the newline
            part = text[:next_pos]
            text = text[next_pos:]
            for ch in part:
                print(ch, end='')
                if ch == '\n':
                    self.pos = 0
                    continue
                # unicodedata.east_asian_width returns:
                # 'W': Wide(CJK characters, '你') 
                # 'F': Fullwidth('Ａ')
                # 'Na': Narrow width('A')
                self.pos = self.pos + 1 + (1 if unicodedata.east_asian_width(ch) in 'WF' else 0)
                if self.pos >= self.width:
                    print('')
                    self.pos = 0
        print(end, end='')
        if '\n' in end:
            self.pos = 0                  

def main():
    wp = WrapPrint(20)
    wp.print('12345678901234567890')
    wp.print('This module provides access to', end='')
    wp.print(' the Unicode Character Database (UCD)', end='')
    wp.print(' which defines character properties', end='')
    wp.print(' for all Unicode characters. The data contained', end='')
    wp.print(' in this database is compiled from the UCD version 15.1.0.')
    wp.print('這個模組提供了對 Unicode 字元資料庫（UCD）的存取，', end='')
    wp.print('該資料庫定義了所有 Unicode 字元的字元屬性。', end='')
    wp.print('這個資料庫中的資料是從 UCD 15.1.0 版本編譯而來的。')

if __name__ == '__main__':
    main()