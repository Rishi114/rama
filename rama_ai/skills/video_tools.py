"""Video Learning and Transcript Skills"""

from skills.skill_base import Skill
from typing import Any


class VideoLearningSkill(Skill):
    """Learn from video content"""
    
    triggers = ["learn from video", "video", "youtube", "watch video", "video summary", "video transcript"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.video_tools import VideoLearningTool
        
        tool = VideoLearningTool()
        
        input_lower = input_text.lower()
        
        # Extract video URL
        urls = self._extract_urls(input_text)
        
        if urls:
            url = urls[0]
            return await tool.learn_from_video(url)
        
        if "list" in input_lower or "show" in input_lower:
            return tool.list_learned_videos()
        
        if "summarize" in input_lower:
            return """📝 **Video Summary:**

Provide a video URL to summarize:
- "summarize https://youtube.com/watch?v=..."

I can:
1. Extract transcript
2. Summarize key points
3. Store in knowledge base"""
        
        return """📺 **Video Learning:**

Learn from videos - YouTube, Bilibili, and more!

Commands:
- `learn from video <URL>` - Learn from video
- `video list` - Show learned videos  
- `summarize video <URL>` - Summarize video

Example: `learn from video https://youtube.com/watch?v=...`"""
    
    def _extract_urls(self, text):
        """Extract URLs from text"""
        import re
        url_pattern = r'https?://[^\s]+'
        return re.findall(url_pattern, text)


class TranscriptSkill(Skill):
    """Extract and process video transcripts"""
    
    triggers = ["transcript", "subtitle", "captions", "srt", "vtt"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.video_tools import TranscriptExtractor
        
        tool = TranscriptExtractor()
        
        input_lower = input_text.lower()
        
        if "extract" in input_lower:
            return """📝 **Transcript Extraction:**

To extract transcript from video:

1. YouTube (requires yt-dlp):
   `pip install yt-dlp`
   `yt-dlp --write-subs --write-auto-subs <url>`

2. Local video:
   Provide video file path and I'll extract using ffmpeg + Whisper"""
        
        if "format" in input_lower:
            return """📝 **Transcript Formats:**

Supported:
- TXT - Plain text
- JSON - Segment-based JSON
- SRT - SubRip subtitle format
- VTT - WebVTT format

Use 'format transcript as json' to convert."""
        
        return """📝 **Transcript Tools:**

Extract and process video transcripts:

- `extract transcript <video>` - Extract from video
- `format transcript as json` - Convert format

For YouTube: `pip install yt-dlp` first!"""


class VideoAnalysisSkill(Skill):
    """Analyze video content"""
    
    triggers = ["analyze video", "video analysis", "video frames", "extract frames"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.video_tools import VideoAnalysisTool
        
        tool = VideoAnalysisTool()
        
        return """🎬 **Video Analysis:**

Analyze video content:

- Extract key frames
- Get metadata (duration, resolution)
- Scene detection
- Object recognition (future)

Requirements:
- ffmpeg for frame extraction
- Computer vision models for analysis

Provide a video to analyze!"""