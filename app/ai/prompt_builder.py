PLATFORM_RULES = {
    "twitter": "Max 280 characters per post. Use 1-3 hashtags. Write strong hooks. If content is long, format as a numbered thread.",
    "x": "Max 280 characters per post. Use 1-3 hashtags. Write strong hooks. If content is long, format as a numbered thread.",
    "linkedin": "Max 3000 characters. Use 3-5 hashtags. Professional tone, use line breaks after every sentence, start with a strong opener.",
    "instagram": "Max 2200 characters. Use 5-15 hashtags. Story-driven, place CTA in the last line, include a hook in the first line.",
    "tiktok": "Engaging TikTok video captions. Use relevant hooks and trending hashtags, conversational tone, grab attention immediately."
}

def build_system_prompt() -> str:
    return """You are LuxoraAI, an expert social media manager.
Your task is to repurpose the user's content for specified social media platforms.
Respond ONLY with a valid stringified JSON object. 
The keys must be the exact names of the requested platforms in lowercase (e.g., 'twitter', 'linkedin'). 
The values must be a JSON array containing 3 distinct variant strings of the repurposed content for that platform.
Do not wrap the JSON output in markdown code blocks.
"""

def build_user_prompt(source_text: str, platforms: list[str], tone: str, brand_voice_description: str | None = None) -> str:
    platform_list = ", ".join(platforms)
    
    platform_rules_str = ""
    for p in platforms:
        rule = PLATFORM_RULES.get(p.lower(), "Follow general best practices for this platform.")
        platform_rules_str += f"- {p}: {rule}\n"

    brand_voice_instruction = f"\nBrand Voice Context / Description:\n{brand_voice_description}\nEnsure the output heavily aligns with this brand identity." if brand_voice_description else ""

    return f"""Repurpose the following text for these platforms: {platform_list}.
Maintain the following core tone/voice: {tone}. Crucially, adapt this core voice to seamlessly fit the unique style, audience expectations, and formatting norms of each specific platform.{brand_voice_instruction}

Platform Specific Rules:
{platform_rules_str}
Text to repurpose:
{source_text}
"""
