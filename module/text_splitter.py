# text_splitter.py
from transformers import AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TokenTextSplitter:
    def __init__(self, using_tokenizer=False, model_name="BAAI/bge-m3", chunk_size=800, overlap=100):
        """
        chunk_size: 
            - 若 using_tokenizer=True，單位為 tokens
            - 若 using_tokenizer=False，單位為 characters (配合 4096 context 縮小切分)
        overlap: 重疊區域的大小 (單位同上)
        """
        self.using_tokenizer = using_tokenizer
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        if using_tokenizer:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
    def _token_len_func(self, text):
        return len(self.tokenizer.encode(text, add_special_tokens=False))
    
    def split_text(self, text) -> list[str]:
        if not self.using_tokenizer:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.overlap,
                separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""], # 加入逗號作為最後防線
                length_function=len
            )
        else:

            splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
                self.tokenizer,
                chunk_size=self.chunk_size,
                chunk_overlap=self.overlap,
                separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
            )
                       
        return splitter.split_text(text)

