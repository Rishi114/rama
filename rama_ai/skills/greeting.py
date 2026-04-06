"""Greeting Skill - Friendly conversation"""

from skills.skill_base import Skill
import random


class GreetingSkill(Skill):
    """Greeting with sassy personality"""
    
    triggers = ["hello", "hi", "hey", "good morning", "how are"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        responses = [
            "Well, well... look who's awake! 👀",
            "Hey there! I'm RAMA, your personal AI! ✨",
            "Yo! Ready to rock? 🚀",
            "Hello, human! 😄 What can I do for you?"
        ]
        return random.choice(responses)