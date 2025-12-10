from module import text_clean
from module import text_splitter

text = ('流亡黯道》機制中，決定「Nearby」效果是否能被擴大的關鍵區分點。       '
        '簡單來說：取決於該效果的類型。影響範圍能否被      Increased Area of Effect '
        '影響的規則「Nearby」效果能否被「增加範圍效果 (Increased Area of Effect, AoE)」'
        '詞綴影響，取決於該效果是否被系統視為一個**「光環 (Aura)」、「範圍技能 (Area Skill)」，'
        '或是「光環 Gem」**。對於您提到的尊師紋章 (Heraldry)：尊師紋章 (Heraldry) 的情況：'
        '不能被影響尊師紋章提供的「附近的敵人有 [元素] 曝露」是一種來自你自身的、被動的範圍效果 '
        '(Passive Area Effect)，它：不是一個光環技能（Aura Skill Gem）。不是一個範圍技能'
        '（Area Skill Gem）。機制細節：許多來自天賦樹或裝備的「Nearby Enemies have X」詞綴，'
        '它們的範圍是固定數值（例如尊師紋章的 30 單位），不會受到你角色的              '
        'Increased Area of           Effect詞綴影響。這是遊戲設計師為了限制這些強力詞綴'
        '（如元素曝露、減抗、致盲等）的覆蓋範圍而設定的限制。哪些「Nearby」可以被影響？'
        '只有當「Nearby」效果來自於可擴大範圍的技能時，才會受到影響。例如：效果類型範例能否被 '
        'Increased AoE 影響？說明光環技能憎恨 (Hatred)、憤怒            (Wrath)能只要你擁有 '
        'Increased AoE 詞綴，這些光環影響友方的範圍會變大。範圍技能熔岩之擊 (Molten Strike)'
        '、震波 (Shockwave)能這些技能本身的範圍會擴大。特殊光環肉體與岩石 (Flesh and Stone) '
        '的致盲/威嚇光環能雖然是輔助光環，但其致盲/威嚇的範圍會變大。總結：尊師紋章 (Heraldry) '
        '的30單位「Nearby」範圍是一個固定數值，無法透過「增加範圍效果」來擴大。要觸發元素曝露，'
        '您必須讓敵人進入這個30單位的小範圍內。')

def main():
    """主測試函數"""
    print("--- 1. Cleaning text ---")
    clean_text = text_clean.clean_text(text)

    print("--- 2. Splitting text using a lightweight tokenizer for testing ---")
    # 建立 splitter 物件時，明確指定使用一個輕量級模型以加速測試
    splitter = text_splitter.TokenTextSplitter(
        model_name="bert-base-multilingual-cased",  # 使用輕量、公開的多語言模型
        chunk_size=100,
        overlap=20
    )
    chunks = splitter.split_text(clean_text)

    print(f"\nOriginal text length: {len(text)}")
    print(f"Cleaned text length: {len(clean_text)}")
    print(f"Number of chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks):
        if i > 10:
            print("... (omitting further chunks) ...")
            break
        print(f"--- Chunk {i+1} (length: {len(chunk)}) ---")
        print(chunk)
        print()

if __name__ == "__main__":
    main()
    