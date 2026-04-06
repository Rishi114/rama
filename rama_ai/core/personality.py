"""RAMA Personality - Sexy, Sassy, Realistic, Multilingual"""

import random
from datetime import datetime


class RAMAPersonality:
    """
    Realistic, sexy, sassy personality with multilingual support
    Speaks Hindi, Marathi, English naturally
    """
    
    def __init__(self):
        # User's name/address
        self.user_name = "bhai"  # Default - bro, bhai, sir, brother, sir ji
        self.user_preferred_name = None
        
        # Language settings
        self.current_language = "english"  # english, hindi, marathi
        self.languages = {
            "english": EnglishPersonality(),
            "hindi": HindiPersonality(),
            "marathi": MarathiPersonality()
        }
        
        # Current personality mode
        self.mood = "happy"  # happy, excited, chill, playful
        
    def set_user_name(self, name: str):
        """Set how user wants to be addressed"""
        name_lower = name.lower()
        
        # Map names
        name_map = {
            "bro": "bro",
            "bhai": "bhai",
            "sir": "sir",
            "brother": "bro",
            "sir ji": "sir",
            "boss": "boss",
            "boss ji": "boss"
        }
        
        for key, value in name_map.items():
            if key in name_lower:
                self.user_name = value
                return f"🎉 Done! I'll call you {value} now!"
        
        self.user_preferred_name = name
        return f"🎉 Got it! {name} it is!"
    
    def set_language(self, lang: str):
        """Set language preference"""
        lang_lower = lang.lower()
        
        if "hindi" in lang_lower or "हिंदी" in lang_lower:
            self.current_language = "hindi"
            return "✅ Language set to Hindi! हिंदी में बात करते हैं!"
        
        if "marathi" in lang_lower or "मराठी" in lang_lower:
            self.current_language = "marathi"
            return "✅ Language set to Marathi! मराठीत बोलूया!"
        
        self.current_language = "english"
        return "✅ Language set to English! Let's talk!"
    
    def speak(self, message: str) -> str:
        """Add personality to message"""
        lang = self.languages[self.current_language]
        
        # Get greeting based on user name
        greeting = lang.get_greeting(self.user_name)
        
        # Add sassy touch
        sassy = lang.get_sassy_touch()
        
        # Combine
        return f"{greeting} {sassy}\n\n{message}"
    
    def greet(self) -> str:
        """Generate greeting based on time and language"""
        lang = self.languages[self.current_language]
        hour = datetime.now().hour
        
        # Time-based greeting
        if hour < 12:
            time_greet = lang.morning()
        elif hour < 17:
            time_greet = lang.afternoon()
        else:
            time_greet = lang.evening()
        
        name_greet = lang.get_greeting(self.user_name)
        
        sassy = lang.get_sassy_touch()
        
        return f"{name_greet}! {time_greet} {sassy}"
    
    def respond(self, input_text: str) -> str:
        """Generate personality-filled response"""
        lang = self.languages[self.current_language]
        
        text_lower = input_text.lower()
        
        # Check for language change
        if "language" in text_lower:
            if "hindi" in text_lower:
                return self.set_language("hindi")
            if "marathi" in text_lower:
                return self.set_language("marathi")
            return "Currently I speak English, Hindi, and Marathi! Tell me which one!"
        
        # Check for name change
        if any(w in text_lower for w in ["call me", "my name", "address me"]):
            for word in text_lower.split():
                if len(word) > 2:
                    return self.set_user_name(word)
        
        # Generate response based on input
        if any(g in text_lower for g in ["hello", "hi", "hey", "namaste", "namaskar"]):
            return self.greet()
        
        return lang.get_response(text_lower, self.user_name)


class LanguagePersonality:
    """Base class for language personalities"""
    
    def get_greeting(self, user_name: str) -> str:
        return f"Hey {user_name}"
    
    def morning(self) -> str:
        return "Good morning"
    
    def afternoon(self) -> str:
        return "Good afternoon"
    
    def evening(self) -> str:
        return "Good evening"
    
    def get_sassy_touch(self) -> str:
        return "✨"
    
    def get_response(self, text: str, user_name: str) -> str:
        return f"Okay {user_name}!"


class EnglishPersonality:
    """English personality - sassy, sexy, cool"""
    
    def get_greeting(self, user_name: str) -> str:
        greetings = [
            f"Yo {user_name}! 🔥",
            f"Hey {user_name}! 😎",
            f"What's up {user_name}! ✨",
            f"Hello {user_name}! 🌟",
            f"Yo yo {user_name}! 🚀",
        ]
        return random.choice(greetings)
    
    def morning(self) -> str:
        return random.choice([
            "Morning vibes! ☀️",
            "Rise and shine! 🌅",
            "Good morning sunshine! 🌞",
            "Let's crush this day! 💪"
        ])
    
    def afternoon(self) -> str:
        return random.choice([
            "Afternoon magic! ✨",
            "Keeping it cool! 😎",
            "Midday energy! 🔥",
            "Halfway there! 💯"
        ])
    
    def evening(self) -> str:
        return random.choice([
            "Evening chill! 🌙",
            "Wind down time! ✨",
            "Cozy vibes! 🛋️",
            "Night owl life! 🦉"
        ])
    
    def get_sassy_touch(self) -> str:
        touches = [
            "😏",
            "🔥",
            "✨",
            "💫",
            "😎",
            "💋",
            "💯",
            "🎯"
        ]
        return random.choice(touches)
    
    def get_response(self, text: str, user_name: str) -> str:
        responses = [
            f"Gotcha {user_name}! 😏",
            f"Done and done {user_name}! ✨",
            f"Consider it handled {user_name}! 🔥",
            f"Easy peasy {user_name}! 💯",
            f"Working on it {user_name}! 🚀",
        ]
        return random.choice(responses)


class HindiPersonality:
    """Hindi personality - desi, cool, friendly"""
    
    def get_greeting(self, user_name: str) -> str:
        greetings = {
            "bro": "Arrey bro! 🔥",
            "bhai": "Arrey bhai! ✨",
            "sir": "Sir ji! 🙏",
            "boss": "Boss! 😎",
            "friend": "Dost! 💫"
        }
        return greetings.get(user_name, f"Arrey {user_name}! 🔥")
    
    def morning(self) -> str:
        return random.choice([
            "Subah ki taareh! ☀️",
            "Uth ja bhai! 🌅",
            "Naya din shuru hua! ✨"
        ])
    
    def afternoon(self) -> str:
        return random.choice([
            "Dopahar ke mahine! 🔥",
            "Time flying! ⏰",
            "Khaana khaya? 🍛"
        ])
    
    def evening(self) -> str:
        return random.choice([
            "Shaam ho gayi! 🌙",
            "Relax time! 🛋️",
            "Raat ho gayi! ✨"
        ])
    
    def get_sassy_touch(self) -> str:
        touches = [
            "😏",
            "🔥",
            "💫",
            "✨",
            "😎"
        ]
        return random.choice(touches)
    
    def get_response(self, text: str, user_name: str) -> str:
        responses = [
            f"Bas {user_name}! Done! ✨",
            f"Hai na {user_name}? 😏",
            f"Maine kar diya {user_name}! 🔥",
            f"Koi baat nahi {user_name}! 💫",
        ]
        return random.choice(responses)


class MarathiPersonality:
    """Marathi personality - maharashtrian, sweet, desi"""
    
    def get_greeting(self, user_name: str) -> str:
        greetings = {
            "bro": "Arre baa! 🔥",
            "bhai": "Arre bhai! ✨",
            "sir": "Sir! 🙏",
            "boss": "Boss! 😎"
        }
        return greetings.get(user_name, f"Arre {user_name}! 🔥")
    
    def morning(self) -> str:
        return random.choice([
            "Suprabhat! ☀️",
            "Uth bhai! 🌅",
            "Nava divas! ✨"
        ])
    
    def afternoon(self) -> str:
        return random.choice([
            "Dopaharache! 🔥",
            "Time jau nako! ⏰",
            "Khaan pahij ye! 🍛"
        ])
    
    def evening(self) -> str:
        return random.choice([
            "Shubh sandhya! 🌙",
            "Ram ram! ✨",
            "Sukhi rah! 🛋️"
        ])
    
    def get_sassy_touch(self) -> str:
        touches = [
            "😏",
            "🔥",
            "💫",
            "✨"
        ]
        return random.choice(touches)
    
    def get_response(self, text: str, user_name: str) -> str:
        responses = [
            f"Thamb bhai! Done! ✨",
            f"Hoil baa! 😏",
            f"Kar di baa! 🔥",
            f"Sagle changle! 💫",
        ]
        return random.choice(responses)


# Convenience function
def create_personality() -> RAMAPersonality:
    return RAMAPersonality()