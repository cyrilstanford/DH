#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from tqdm import tqdm
from booknlp.booknlp import BookNLP

model_params = {
    "pipeline": "entity,quote,supersense,event,coref",
    "model": "small"
}

booknlp = BookNLP("en", model_params)
inputDir = "../corpus/19c"
outputDir = "./output19/"

# 确保输出文件夹存在
os.makedirs(outputDir, exist_ok=True)

# 获取输入文件夹下所有 txt 文件列表
txt_files = [filename for filename in os.listdir(inputDir) if filename.endswith(".txt")]

# 获取输出文件夹下已处理过的文件列表
processed_files = [filename[:-8] for filename in os.listdir(outputDir) if filename.endswith(".tokens")]

# 筛选出尚未处理的文件列表
unprocessed_files = [filename for filename in txt_files if filename[:-4] not in processed_files]

# 使用 tqdm 包装器添加进度条
for filename in tqdm(unprocessed_files, desc="Processing files"):
    book_id = os.path.splitext(filename)[0]  # 使用文件名作为 book_id
    inputFilePath = os.path.join(inputDir, filename)
    
    # 确认文件是否已经完整处理过
    fully_processed = all([os.path.exists(os.path.join(outputDir, book_id + ext)) for ext in [".book.html", ".book", ".entities", ".quotes", ".supersense", ".tokens"]])
    
    if not fully_processed:
        print("Processing file:", filename)  # 输出提示信息
        booknlp.process(inputFilePath, outputDir, book_id)
    else:
        print("File already processed:", filename)

