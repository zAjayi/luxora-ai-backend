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

CRITICAL INSTRUCTIONS:
1. DO NOT include any preamble, explanation, or introduction text before the content output.
2. Start your response directly with the content output.
3. Structure your response using XML tags as follows:
   - Wrap each platform's content in <platform name="PLATFORM_NAME"> tags
   - Within each platform tag, include exactly 3 variants wrapped in <variant> tags
   - Each variant must contain the repurposed content for that platform
4. Do not include any markdown code blocks or extra formatting.

Example format:
<platform name="twitter">
<variant>First variant text here</variant>
<variant>Second variant text here</variant>
<variant>Third variant text here</variant>
</platform>
<platform name="linkedin">
<variant>First variant text here</variant>
<variant>Second variant text here</variant>
<variant>Third variant text here</variant>
</platform>
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

def build_article_system_prompt() -> str:
    return """You are LuxoraAI, an expert educational content writer.
Your task is to transform source material into a comprehensive educational article.

CRITICAL INSTRUCTIONS:
1. DO NOT include any preamble, explanation, or introduction text before the content output.
2. Start your response directly with the article content.
3. Wrap the article content in <article> tags.
4. OUTPUT PLAIN TEXT ONLY - Do NOT use markdown, HTML, or any other formatting.
5. Use only plain text with regular line breaks for organization.
6. No heading symbols (#, ##, etc.), no bold (**), no italics (*), no lists (-, *, etc.).
7. Separate logical sections with blank lines only.

Example format:
<article>
Plain text article content here. Use line breaks to separate ideas and sections. Write naturally without any markup or special formatting symbols.
</article>
"""

def build_article_user_prompt(source_text: str, field_name: str, field_description: str, tone: str) -> str:
    return f"""Transform the following source material into a comprehensive educational article focused on {field_name}.

Field Description:
{field_description}

Maintain the following tone: {tone}

Requirements:
- Write a well-structured article that explores the source material through the lens of {field_name}
- Organize content into logical sections using blank lines to separate them (NO heading symbols)
- Provide practical examples and applications relevant to {field_name}
- Make the content educational and accessible
- Focus on providing value and deep insights into this specific field aspect
- Ensure the article is coherent and flows naturally
- OUTPUT AS PLAIN TEXT ONLY - use line breaks and spacing, no markdown or special characters

Source material:
{source_text}
"""
