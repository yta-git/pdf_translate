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

bug_str = '𝑁'
use_str = 'N'

dot_term = ['et al.', 'etc.', 'e.g.', 'Fig.', 'i.e.', 'No.', 'pp.', 'Vol.']
use_term = ['et al ', 'etc ', 'eg ', 'Fig-', 'ie ', 'No-', 'pp-', 'Vol-']

def google(ss):

    global src, dest
    global bug_str, use_str
    trans = Translator()

    query = ''
    buffer = []

    for s in ss:
        
        if len(query + s + '\n') > 5000:
            print(len(query), 'chars')
            origin = query.split('\n')
            try:
                ret = trans.translate(query, src=src, dest=dest).text.split('\n')
                buffer += list(zip(origin, ret))
            except:
                print('## error ##')
                print(query)
                print(len(query), 'chars')
                print('###########')
                exit(1)
            
            if len(s + '\n') > 5000:
                buffer += [(s, 'passed.')]
                print(s, '\npassed.')
                query = ''
            else:
                s = s.translate(str.maketrans(bug_str, use_str))
                query = s + '\n'

        else:
            s = s.translate(str.maketrans(bug_str, use_str))
            query += (s + '\n')


    else:
        print(len(query), 'chars')
        origin = query.split('\n')
        try:
            ret = trans.translate(query, src=src, dest=dest).text.split('\n')
            buffer += list(zip(origin, ret))
        except:
            print('## error ##')
            print(query)
            print(len(query), 'chars')
            print('###########')
            exit(1)

        query = ''
        
    return buffer

if __name__ == '__main__':

    rsrcmgr = PDFResourceManager()
    rettxt = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, rettxt, codec='utf-8', laparams=laparams)

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

    text = rettxt.getvalue().replace('-\n', '').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    
    for dot, use in zip(dot_term, use_term):
        text = text.replace(dot, use)


    ss = [s for s in re.split(r'(.+?[\.\!\?])\s', text) if s]
    
    print(len(text.split()), 'words')
    print(len(text), 'chars')
    print('reading completed')
    print('------------')
    print(f'translating sentences "{src}" to "{dest}"')

    with open(output, 'w') as out:
        buffer = google(ss)
        for o, t in buffer:
            out.write(o + '\n')
            out.write(t + '\n\n')
        

    with open(words, 'w') as out:
        ws = [w.replace('.', '') for w in set(text.split())]
        buffer = sorted(google(ws))
        for o, t in buffer:
            if o.isalpha():
                out.write(o + ' ' + t + '\n')

    device.close()
    rettxt.close()
    print('------------')
    print('done')
