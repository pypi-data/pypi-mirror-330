
def check_provider(model_string):
    """
    Check the LLM provider from the model string (e.g., 'ollama/qwen2.5' -> 'ollama')
    Returns a tuple of (provider, base_url, model_name)
    """
    if not model_string:
        return "ollama", "http://localhost:11434", "qwen2.5"  # default values
        
    parts = model_string.split("/")
    if len(parts) != 2:
        return "ollama", "http://localhost:11434", model_string  # fallback to default provider
        
    provider = parts[0].lower()
    model_name = parts[1]
    
    provider_urls = {
        "ollama": "http://localhost:11434",
        "openai": "https://api.openai.com/v1",
        "anthropic": "https://api.anthropic.com",
        "gemini": "https://api.gemini.com",
        "together_ai": "https://api.together.xyz",
        # Add more providers as needed
    }
    
    base_url = provider_urls.get(provider, "http://localhost:11434")
    return provider, base_url, model_name
