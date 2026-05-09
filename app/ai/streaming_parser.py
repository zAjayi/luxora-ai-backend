"""
XML Tag-based Streaming Parser
Handles incremental parsing of XML-structured AI responses with chunk accumulation.
"""
import re
from typing import Generator, TypedDict
import json


class ParsedEvent(TypedDict):
    platform: str
    variant_index: int
    text: str


class XMLStreamingParser:
    """
    Parses XML-structured streaming content and yields complete semantic units.
    Accumulates chunks to ensure we only yield complete, meaningful content.
    """
    
    def __init__(self):
        self.buffer = ""
        self.platform_pattern = re.compile(r'<platform\s+name="([^"]+)">')
        self.variant_pattern = re.compile(r'<variant>(.*?)</variant>', re.DOTALL)
        self.parsed_platforms = {}
        self.current_platform = None
        self.content_started = False
    
    def consume(self, chunk: str) -> list[ParsedEvent]:
        """
        Process incoming chunk and accumulate until we have complete tags.
        Yields events for complete platform-variant pairs.
        """
        self.buffer += chunk
        events = []
        
        # Check for content start (skip preamble)
        if not self.content_started:
            if '<platform' in self.buffer:
                # Skip any preamble before the first tag
                start_idx = self.buffer.find('<platform')
                if start_idx > 0:
                    self.buffer = self.buffer[start_idx:]
                self.content_started = True
        
        if not self.content_started:
            return []
        
        # Process complete platform blocks
        while True:
            # Look for complete platform tags
            platform_match = self.platform_pattern.search(self.buffer)
            if not platform_match:
                break
            
            platform_name = platform_match.group(1)
            platform_start = platform_match.start()
            
            # Find the closing tag for this platform
            closing_tag = '</platform>'
            closing_idx = self.buffer.find(closing_tag, platform_match.end())
            
            if closing_idx == -1:
                # Don't have complete platform block yet, wait for more chunks
                break
            
            platform_end = closing_idx + len(closing_tag)
            platform_block = self.buffer[platform_match.end():closing_idx]
            
            # Extract variants from this platform block
            variant_index = 0
            for variant_match in self.variant_pattern.finditer(platform_block):
                variant_text = variant_match.group(1).strip()
                if variant_text:
                    events.append({
                        "platform": platform_name,
                        "variant_index": variant_index,
                        "text": variant_text
                    })
                    variant_index += 1
            
            # Remove processed platform from buffer
            self.buffer = self.buffer[platform_end:]
        
        return events
    
    def flush(self) -> list[ParsedEvent]:
        """
        Return any remaining buffered content and reset.
        Call this when stream ends.
        """
        events = []
        
        # Process any remaining incomplete content
        if self.buffer.strip():
            # Try to extract any remaining variants
            variant_index = 0
            for variant_match in self.variant_pattern.finditer(self.buffer):
                variant_text = variant_match.group(1).strip()
                if variant_text and self.current_platform:
                    events.append({
                        "platform": self.current_platform,
                        "variant_index": variant_index,
                        "text": variant_text
                    })
                    variant_index += 1
        
        self.buffer = ""
        return events
    
    def get_parsed_data(self) -> dict:
        """
        Reconstruct the complete JSON structure from parsed events for storage.
        """
        result = {}
        for event in self._get_all_events():
            platform = event["platform"]
            if platform not in result:
                result[platform] = []
            result[platform].append(event["text"])
        return result
    
    def _get_all_events(self) -> list[ParsedEvent]:
        """Get all accumulated events."""
        # This would be populated by tracking all events yielded
        return []


class ChunkAccumulator:
    """
    Accumulates chunks before passing to parser.
    Helps reduce parsing overhead by batching small chunks.
    """
    
    def __init__(self, min_chunk_size: int = 50):
        self.buffer = ""
        self.min_chunk_size = min_chunk_size
    
    def add(self, chunk: str) -> str:
        """
        Add chunk and return accumulated content if threshold met, otherwise empty string.
        """
        self.buffer += chunk
        if len(self.buffer) >= self.min_chunk_size or '\n' in self.buffer:
            result = self.buffer
            self.buffer = ""
            return result
        return ""
    
    def flush(self) -> str:
        """Return remaining buffered content."""
        result = self.buffer
        self.buffer = ""
        return result


def parse_xml_response_to_json(xml_content: str) -> dict:
    """
    Parse final XML response and convert to JSON structure for storage.
    """
    result = {}
    platform_pattern = re.compile(r'<platform\s+name="([^"]+)">')
    variant_pattern = re.compile(r'<variant>(.*?)</variant>', re.DOTALL)
    
    for platform_match in platform_pattern.finditer(xml_content):
        platform_name = platform_match.group(1)
        platform_start = platform_match.end()
        
        # Find next platform or end of content
        next_platform = platform_pattern.search(xml_content, platform_start)
        if next_platform:
            platform_end = next_platform.start()
        else:
            platform_end = xml_content.find('</platform>', platform_start)
        
        platform_section = xml_content[platform_start:platform_end]
        
        variants = []
        for variant_match in variant_pattern.finditer(platform_section):
            variant_text = variant_match.group(1).strip()
            if variant_text:
                variants.append(variant_text)
        
        if variants:
            result[platform_name] = variants
    
    return result
