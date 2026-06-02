async def execute(envelop, agent):
    action = envelop.payload.get("action", "translate")
    
    if action == "translate":
        text = envelop.payload.get("text", "")
        target_lang = envelop.payload.get("target_lang", "中文")
        
        if not text:
            envelop.payload = {"error": "text required"}
            return envelop
        
        if not agent.llm:
            envelop.payload = {"error": "LLM not available"}
            return envelop
        
        prompt = f"将以下文本翻译成{target_lang}，只输出翻译结果，不要解释：\n\n{text}"
        result = await agent.llm.chat([
            {"role": "system", "content": "你是翻译助手，只输出翻译结果。"},
            {"role": "user", "content": prompt}
        ])
        
        envelop.payload = {"original": text, "translated": result.strip(), "target_lang": target_lang}
        return envelop
    
    elif action == "languages":
        envelop.payload = {"languages": ["中文", "英文", "日文", "韩文", "法文", "德文", "西班牙文"]}
        return envelop
    
    envelop.payload = {"error": f"Unknown action: {action}"}
    return envelop
