import os
import json
import random

class AIEnhancer:
    def __init__(self, config):
        self.config = config
        ai_config = config.get("ai", {})
        self.provider = ai_config.get("provider", "").lower()
        self.api_key = os.environ.get("NIJI_API_KEY", ai_config.get("api_key", ""))
        self.model = ai_config.get("model", "")
        self.enabled = bool(self.provider and self.api_key)

    def enhance_hiragana(self, char_data):
        if not self.enabled:
            return char_data
        return self._call_llm("hiragana", char_data)

    def enhance_katakana(self, char_data):
        if not self.enabled:
            return char_data
        return self._call_llm("katakana", char_data)

    def enhance_kanji(self, theme_data):
        if not self.enabled:
            return theme_data
        return self._call_llm("kanji", theme_data)

    def enhance_vocabulary(self, theme_data):
        if not self.enabled:
            return theme_data
        return self._call_llm("vocabulary", theme_data)

    def enhance_grammar(self, topic_data):
        if not self.enabled:
            return topic_data
        return self._call_llm("grammar", topic_data)

    def enhance_expressions(self, cat_data):
        if not self.enabled:
            return cat_data
        return self._call_llm("expressions", cat_data)

    def enhance_review(self, review_type, all_data):
        if not self.enabled:
            return all_data
        return self._call_llm("review", {"type": review_type, "data": all_data})

    def _call_llm(self, category, data):
        try:
            import httpx

            if self.provider == "openai":
                return self._call_openai(category, data)
            elif self.provider == "ollama":
                return self._call_ollama(category, data)
            else:
                return data
        except Exception:
            return data

    def _call_openai(self, category, data):
        prompt = self._build_prompt(category, data)
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={
                "model": self.model or "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2000,
            },
            timeout=30,
        )
        if resp.is_success:
            content = resp.json()["choices"][0]["message"]["content"]
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return data
        return data

    def _call_ollama(self, category, data):
        prompt = self._build_prompt(category, data)
        resp = httpx.post(
            "http://localhost:11434/api/generate",
            json={"model": self.model or "llama3", "prompt": prompt, "stream": False},
            timeout=60,
        )
        if resp.is_success:
            try:
                return json.loads(resp.json()["response"])
            except (json.JSONDecodeError, KeyError):
                return data
        return data

    def _build_prompt(self, category, data):
        prompts = {
            "hiragana": f"Genera ejemplos de palabras nuevas y mnemonics creativos para estos caracteres hiragana. Devuelve JSON con los mismos campos pero con ejemplos frescos: {json.dumps(data, ensure_ascii=False)}",
            "kanji": f"Genera ejemplos adicionales y frases de ejemplo para estos kanji. Devuelve JSON con los mismos campos pero añadiendo ejemplos nuevos: {json.dumps(data, ensure_ascii=False)}",
            "vocabulary": f"Genera ejemplos de frases adicionales para cada palabra de vocabulario japonés. Devuelve JSON con los mismos campos: {json.dumps(data, ensure_ascii=False)}",
            "grammar": f"Genera ejemplos adicionales para explicar esta regla gramatical japonesa. Devuelve JSON: {json.dumps(data, ensure_ascii=False)}",
            "expressions": f"Genera ejemplos de uso adicionales para estas expresiones japonesas. Devuelve JSON: {json.dumps(data, ensure_ascii=False)}",
        }
        return prompts.get(category, f"Devuelve el mismo JSON sin cambios: {json.dumps(data, ensure_ascii=False)}")
