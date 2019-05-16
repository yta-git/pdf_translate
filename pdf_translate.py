from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

from sys import argv
import re
from googletrans import Translator

src = 'en'
dest = 'ja'
output = 'translate.txt'
words = 'words.txt'

rsrcmgr = PDFResourceManager()
rettxt = StringIO()
laparams = LAParams()
trans = Translator()
device = TextConverter(rsrcmgr, rettxt, codec='utf-8', laparams=laparams)

def google(ss):

    global src, dest, trans

    query = ''
    buffer = []

    for s in ss:
        query += (s + '\n')
        
        if len(query) > 4800:
            origin = query.split('\n')
            ret = trans.translate(query, src=src, dest=dest).text.split('\n')
            buffer += list(zip(origin, ret))
            query = ''

    else:
        origin = query.split('\n')
        ret = trans.translate(query, src=src, dest=dest).text.split('\n')
        buffer += list(zip(origin, ret))
        query = ''
        
    return buffer

if __name__ == '__main__':

    print('output file:', output)
    print('words file:', words)
    print('------------')

    with open(argv[1], 'rb') as fp:
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        cnt = 1
        for page in PDFPage.get_pages(fp, pagenos=None, maxpages=0, password=None, caching=True, check_extractable=True):
            print('reading page', cnt)
            interpreter.process_page(page)
            cnt = cnt + 1

    text = rettxt.getvalue().replace('\n', '')
    ss =  re.split(r'\. ', text)
    print('reading completed')
    print('------------')
    print(f'translating sentences "{src}" to "{dest}"')

    with open(output, 'w') as out:
        buffer = google(ss)
        for o, t in buffer:
            out.write(o + '\n')
            out.write(t + '\n\n')
        
    with open(words, 'w') as out:
        ws = list(set(text.split()))
        buffer = sorted(google(ws))
        for o, t in buffer:
            if o.isalpha():
                out.write(o + ' ' + t + '\n')

    device.close()
    rettxt.close()
    print('------------')
    print('done')