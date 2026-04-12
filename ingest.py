import os

def load_code_files(folder_path):
    all_code = []

    for root , dirs , files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root,file)

                with open(full_path,'r',encoding='utf-8') as f:
                    content = f.read()

                all_code.append({
                    "file_name":file,
                    "content":content
                })    
    return all_code            

import re


def chunk_code(code_data):
    chunks = []

    for file in code_data:
        content = file["content"]

        # split by functions
        functions = re.split(r"\ndef ", content)

        for i, func in enumerate(functions):
            if i != 0:
                func = "def " + func  # add back removed part

            if func.strip():
                chunks.append({
                    "file_name": file["file_name"],
                    "chunk": func.strip()
                })

    return chunks