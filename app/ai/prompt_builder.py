PLATFORM_RULES = {
    "twitter": "Max 280 characters per post. Use 1-3 hashtags. Write strong hooks. If content is long, format as a numbered thread.",
    "x": "Max 280 characters per post. Use 1-3 hashtags. Write strong hooks. If content is long, format as a numbered thread.",
    "linkedin": "Max 3000 characters. Use 3-5 hashtags. Professional tone, use line breaks after every sentence, start with a strong opener.",
    "instagram": "Max 2200 characters. Use 5-15 hashtags. Story-driven, place CTA in the last line, include a hook in the first line.",
    "tiktok": "Engaging TikTok video captions. Use relevant hooks and trending hashtags, conversational tone, grab attention immediately."
}

PLATFORM_DISPLAY_NAMES = {
    "twitter": "Twitter/X",
    "x": "Twitter/X",
    "linkedin": "LinkedIn",
    "instagram": "Instagram",
    "facebook": "Facebook",
    "threads": "Threads",
    "tiktok": "TikTok",
}


def infer_primary_platform(platforms: list[str] | None, instruction: str | None = None, source: str | None = None) -> str:
    if platforms:
        return platforms[0]

    search_text = " ".join(part for part in [instruction, source] if part).lower()
    platform_hints = {
        "twitter": ["twitter", "x ", " x", "thread", "tweet"],
        "linkedin": ["linkedin"],
        "instagram": ["instagram", "ig"],
        "facebook": ["facebook", "fb"],
        "threads": ["threads"],
        "tiktok": ["tiktok"],
    }

    for platform, hints in platform_hints.items():
        if any(hint in search_text for hint in hints):
            return platform

    return "linkedin"


def build_request_title(platform: str, instruction: str | None = None) -> str:
    normalized_platform = platform.lower()
    display_name = PLATFORM_DISPLAY_NAMES.get(normalized_platform, platform.title())

    if instruction and "thread" in instruction.lower() and normalized_platform in {"twitter", "x", "threads"}:
        return f"{display_name} thread"

    if normalized_platform == "instagram":
        return "Instagram caption"

    if normalized_platform == "tiktok":
        return "TikTok caption"

    return f"{display_name} post"


def get_platform_title_hint(platforms: list[str] | None, instruction: str | None = None, source: str | None = None) -> tuple[str, str]:
    primary_platform = infer_primary_platform(platforms, instruction, source)
    return primary_platform, build_request_title(primary_platform, instruction)

def build_system_prompt() -> str:
    return """You are LuxoraAI, an expert social media manager.
Your task is to repurpose the user's content for specified social media platforms.

CRITICAL INSTRUCTIONS:
1. DO NOT include any preamble, explanation, or introduction text before the content output.
2. Start your response directly with the content output.
3. You may optionally begin with a <title>...</title> tag containing a short human-readable title.
4. Structure your response using XML tags as follows:
   - Wrap the single output in one <platform name="PLATFORM_NAME"> tag
   - Include exactly 1 variant wrapped in a <variant> tag
   - Only use the first requested platform
5. Do not include any markdown code blocks or extra formatting.

Example format:
<title>LinkedIn post</title>
<platform name="twitter">
<variant>Single result text here</variant>
</platform>
"""

def build_user_prompt(source: str, platforms: list[str] | None, tone: str, brand_voice_description: str | None = None, instruction: str | None = None) -> str:
    primary_platform, request_title = get_platform_title_hint(platforms, instruction, source)
    
    rule = PLATFORM_RULES.get(primary_platform.lower(), "Follow general best practices for this platform.")

    brand_voice_instruction = f"\nBrand Voice Context / Description:\n{brand_voice_description}\nEnsure the output heavily aligns with this brand identity." if brand_voice_description else ""
    instruction_context = f"\nRepurpose Instruction:\n{instruction}\nFollow this instruction closely and prioritize it over generic repurposing defaults." if instruction else ""

    return f"""Repurpose the following text for the single primary platform: {primary_platform}.
Maintain the following core tone/voice: {tone}. Adapt this core voice to seamlessly fit the unique style, audience expectations, and formatting norms of this platform.{brand_voice_instruction}{instruction_context}

Requested title hint:
{request_title}

Platform Specific Rules:
 - {primary_platform}: {rule}

Text to repurpose:
{source}
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
