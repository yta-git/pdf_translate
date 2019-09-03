# pdf_translate

# 依存
`pip install pdfminer.six`  
`pip install googletrans`

# 実行
- pdf 入力  
    `python3 pdf_translate.py ***.pdf`  

- txt 入力  
    `python3 pdf_translate.py -t ***.txt`

# 出力(デフォルト)

- translate.txt

  英語  
  日本語  
  のように二行1組で文を見ることのできるファイル

- words.txt
 
  英単語 日本語  
  の対応表

--- 
特殊文字が入っていると止まることがある．
