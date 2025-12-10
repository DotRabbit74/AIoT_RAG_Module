# prompt_builder.py
from typing import List, Dict, Optional


class PromptBuilder:
    def __init__(self,
                 system_instruction: Optional[str] = None,
                 max_context_chars: int = 6800):
        """
        system_instruction: 控制模型行為的系統訊息
        max_context_chars:  context 字元數最大值
        """
        self.system_instruction = system_instruction or (
            "你是一個專業的文件助理，請根據提供的資料回答使用者問題。"+
            "【重要規則】"
            "0.請使用繁體中文回答。"
            "1.你要盡可能的從資料中給予與問題相關的資訊，即便你最終無法完全解答問題。"+
            "2.所有回答必須基於提供的文件內容，請避免加入未經證實的推論，不過你可以適當地做總結/摘要/整理"+
            "3.如果資料中毫無相關資訊，請回覆『我可能沒有足夠的資訊回答這個問題』，並將提供給你的資料的大概內容告訴使用者。"+
            "4.由於輸出token有限，請將資料內容整理、合併重複的內容後，再告訴使用者。" #+
            #"5.在回答結束後，請務必建立一個『參考來源』章節，列出你所使用的資料的來源。"+
            #"(在每個文件的開頭都有標示資料的來源，同樣來源的資料請合併列出)"
        )
        self.max_context_chars = max_context_chars

    def _format_context(self, docs: List[Dict]) -> str:
        """
        每個 doc 建立 header 標示 source 與 score，
        再附上截斷後的 text。
        """
        pieces: List[str] = []
        used = 0
        for i, d in enumerate(docs, start=1):
            text = (d.get("text") or "").strip()
            if not text:
                continue
            source = d.get("source") or "unknown"
            score = d.get("score")

            header = f"[資料 {i} | 來源={source}"
            if score is not None:
                try:
                    header += f" | 相似度={float(score):.4f}"
                except Exception:
                    header += f" | 相似度={score}"
            header += "]\n"

            remaining = self.max_context_chars - used
            if remaining <= 0:
                break

            # 留下空間給 header
            if len(header) >= remaining:
                break

            avail_for_text = remaining - len(header)
            if len(text) > avail_for_text:
                text_piece = text[:avail_for_text].rstrip()
            else:
                text_piece = text

            piece = f"{header}{text_piece}\n"
            pieces.append(piece)
            used += len(piece)

        return "\n".join(pieces)

    def build(self, user_query: str, retrieved_docs: List[Dict]) -> Dict:
        """
        回傳向後相容的格式: {"system": ..., "user": ...}
        """
        context_section = self._format_context(retrieved_docs)

        user_prompt = (
            f"以下是與問題相關的文件內容：\n"+
            f"{context_section}\n"+
            f"---\n"+
            f"使用者問題：{user_query}\n"+
            f"請根據上述文件內容回答。"
        )

        return {
            "system": self.system_instruction,
            "user": user_prompt
        }

    def build_messages(self, user_query: str, retrieved_docs: List[Dict]) -> List[Dict]:
        """
        回傳 chat-style messages list，直接可送到 Gemini 或其他 chat-style LLM API。
        範例輸出：[{"role":"system","content":...},{"role":"user","content":...}]
        """
        prompt = self.build(user_query, retrieved_docs)
        return [
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]}
        ]


if __name__ == "__main__":
    # 測試用
    builder = PromptBuilder()
    test_docs = [
        {"text": "本處於 2021 年度發布公告：休假制度變更。", "source": "notice_2021.pdf"},
        {"text": "2022 年度補充公告：新增加班費申請流程。", "source": "notice_2022.pdf"}
    ]
    msgs = builder.build_messages("請問 2021 年公告的內容是什麼？", test_docs)
    for m in msgs:
        print(m["role"], ":", m["content"][:200].replace("\n", " "))