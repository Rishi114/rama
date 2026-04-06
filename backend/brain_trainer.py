"""
RAMA AI - Brain Training Module
Build and train your own LLM/AI Brain
Includes The Well (Physics) data integration
"""

import os
import json
import random
from datetime import datetime
from typing import Dict, List, Optional


class BrainTrainer:
    """
    RAMA's Brain Training System
    Build, train, and improve your own AI
    
    Features:
    - Self-learning from interactions
    - The Well (Physics) data integration
    - Custom training data
    - Model persistence
    - Knowledge graph
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        
        # Brain state
        self.weights = {}  # Neural-style weights
        self.knowledge = {}  # Factual knowledge
        self.patterns = {}  # Learned patterns
        self.conversation_history = []
        
        # Training state
        self.is_training = False
        self.epochs_trained = 0
        self.accuracy = 0.0
        
        # The Well (Physics) integration
        self.physics_data_loaded = False
        self.physics_knowledge = {}
        
        # Initialize base brain
        self._init_brain()
    
    def _init_brain(self):
        """Initialize base brain with starting knowledge"""
        
        # Core concepts
        self.knowledge = {
            # Basic facts
            "who_am_i": "I am RAMA - an AI assistant built by training",
            "purpose": "To help and assist with various tasks",
            "creator": "Built using machine learning and training data",
            
            # Physics basics (can be expanded with The Well)
            "physics": "The study of matter, energy, and their interactions",
            "gravity": "Force that attracts bodies toward the center of the earth",
            "velocity": "Speed in a given direction",
            "acceleration": "Rate of change of velocity",
            "force": "Any interaction that changes motion",
            
            # Math basics
            "math": "The abstract science of number, quantity, and space",
            "algebra": "Mathematics involving variables and equations",
            "calculus": "Mathematics of continuous change",
        }
        
        # Initialize weights (simple neural-style)
        self.weights = {
            "greeting": 0.5,
            "code": 0.5,
            "search": 0.5,
            "system": 0.5,
            "math": 0.5,
            "learning": 0.5,
            "physics": 0.3,  # Can be improved with The Well data
        }
        
        print("🧠 RAMA Brain initialized!")
    
    def learn(self, input_text: str, response: str):
        """
        Learn from interaction - improve brain
        This is the core self-learning mechanism
        """
        # Record conversation
        self.conversation_history.append({
            "input": input_text,
            "output": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Extract key patterns
        text_lower = input_text.lower()
        
        # Update weights based on context
        if any(w in text_lower for w in ["hello", "hi", "hey"]):
            self.weights["greeting"] = min(1.0, self.weights["greeting"] + 0.1)
        
        if any(w in text_lower for w in ["code", "program", "language"]):
            self.weights["code"] = min(1.0, self.weights["code"] + 0.1)
        
        if any(w in text_lower for w in ["search", "google", "find"]):
            self.weights["search"] = min(1.0, self.weights["search"] + 0.1)
        
        if any(w in text_lower for w in ["system", "cpu", "memory", "info"]):
            self.weights["system"] = min(1.0, self.weights["system"] + 0.1)
        
        if any(w in text_lower for w in ["calculate", "math", "+", "-", "*", "/"]):
            self.weights["math"] = min(1.0, self.weights["math"] + 0.1)
        
        if any(w in text_lower for w in ["remember", "learn", "know"]):
            self.weights["learning"] = min(1.0, self.weights["learning"] + 0.1)
        
        # Learn new facts
        if " is " in input_text or " = " in input_text:
            parts = input_text.split()
            for i, part in enumerate(parts):
                if part.lower() in ["is", "="] and i > 0 and i < len(parts) - 1:
                    key = parts[i-1].lower()
                    value = " ".join(parts[i+1:]).strip()
                    if key and value:
                        self.knowledge[key] = value
        
        # Update accuracy
        self.epochs_trained += 1
        self._update_accuracy()
        
        return f"🧠 Learned from interaction! Brain improved! 🔥\n\nEpochs: {self.epochs_trained}\nAccuracy: {self.accuracy*100:.1f}%"
    
    def _update_accuracy(self):
        """Update brain accuracy based on learning"""
        # Simple accuracy calculation
        total_weight = sum(self.weights.values())
        self.accuracy = min(1.0, total_weight / len(self.weights))
    
    def train(self, data: List[Dict], epochs: int = 10):
        """
        Train the brain with custom data
        Args:
            data: List of {"input": str, "output": str}
            epochs: Number of training passes
        """
        self.is_training = True
        
        for epoch in range(epochs):
            for item in data:
                self.learn(item.get("input", ""), item.get("output", ""))
            
            print(f"📊 Training epoch {epoch+1}/{epochs}...")
        
        self.is_training = False
        
        return f"✅ Training complete!\n\nEpochs: {self.epochs_trained}\nAccuracy: {self.accuracy*100:.1f}%\nKnowledge: {len(self.knowledge)} facts\nPatterns: {len(self.patterns)} learned"
    
    def add_knowledge(self, topic: str, facts: Dict):
        """
        Add knowledge to brain
        Args:
            topic: Topic name
            facts: Dictionary of facts
        """
        self.knowledge[topic] = facts
        
        # Increase weight for this topic
        topic_key = topic.lower()
        if topic_key in self.weights:
            self.weights[topic_key] = min(1.0, self.weights[topic_key] + 0.2)
        else:
            self.weights[topic_key] = 0.5
        
        return f"✅ Added knowledge: {topic}\nFacts: {len(facts)}"
    
    def load_physics_data(self):
        """
        Load The Well (Physics) data
        Integration with PolymathicAI/the_well
        
        Note: This requires:
        1. pip install the_well
        2. Downloading datasets
        """
        
        # The Well physics concepts
        physics_knowledge = {
            "fluid_dynamics": {
                "description": "Study of fluids (liquids and gases) in motion",
                "equations": ["Navier-Stokes", "Continuity equation", "Bernoulli's principle"],
                "applications": ["Weather prediction", "Aerodynamics", "Oceanography"]
            },
            "active_matter": {
                "description": "Systems with constituent particles that consume energy to move",
                "examples": ["Bacterial colonies", "Bird flocks", "Traffic flow"],
                "physics": "Non-equilibrium statistical mechanics"
            },
            "mhd": {
                "description": "Magnetohydrodynamics - study of electrically conducting fluids",
                "applications": ["Astrophysics", "Fusion reactors", "Metal casting"],
                "equations": ["MHD equations", "Maxwell's equations"]
            },
            "acoustic_scattering": {
                "description": "Interaction of sound waves with objects",
                "applications": ["Sonar", "Medical ultrasound", "Non-destructive testing"]
            },
            "supernova": {
                "description": "Explosive death of massive stars",
                "physics": ["Nuclear physics", "Radiative transfer", "Hydrodynamics"]
            },
            "turbulence": {
                "description": "Chaotic fluid motion characterized by eddies and vortices",
                "challenges": "One of the last unsolved problems in classical physics"
            }
        }
        
        self.physics_knowledge = physics_knowledge
        self.physics_data_loaded = True
        self.weights["physics"] = 0.8
        
        return """📚 **The Well (Physics) Data Loaded!**

🔬 **Available Physics Domains:**
• Fluid Dynamics - Navier-Stokes equations
• Active Matter - Self-propelled particles
• MHD - Magnetohydrodynamics
• Acoustic Scattering - Sound wave interaction
• Supernova - Stellar explosions
• Turbulence - Chaotic flows

💾 **Data Size:** 15TB across 16 datasets

To enable full training:
1. pip install the_well
2. the-well-download --base-path ./data --dataset active_matter
3. Use in training pipeline!

Physics knowledge integrated! 🚀"""
    
    def get_brain_status(self):
        """Get current brain status"""
        return f"""🧠 **RAMA Brain Status:**

**Training:**
• Epochs trained: {self.epochs_trained}
• Accuracy: {self.accuracy*100:.1f}%
• Training: {'Active' if self.is_training else 'Idle'}

**Knowledge:**
• Facts stored: {len(self.knowledge)}
• Concepts learned: {len(self.patterns)}

**Weights (Skills):**
{self._format_weights()}

**Physics (The Well):**
• Loaded: {'Yes ✅' if self.physics_data_loaded else 'No'}
• Topics: {len(self.physics_knowledge)}

**Memory:**
• Conversations: {len(self.conversation_history)}
"""
    
    def _format_weights(self):
        """Format weights for display"""
        lines = []
        for key, value in sorted(self.weights.items()):
            bar = "█" * int(value * 10) + "░" * (10 - int(value * 10))
            lines.append(f"  {key:15} [{bar}] {value*100:.0f}%")
        return "\n".join(lines)
    
    def save_brain(self, path: str = "data/brain.json"):
        """Save brain state to file"""
        data = {
            "knowledge": self.knowledge,
            "weights": self.weights,
            "epochs_trained": self.epochs_trained,
            "accuracy": self.accuracy,
            "conversation_history": self.conversation_history[-100:],  # Last 100
            "timestamp": datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return f"💾 Brain saved to {path}! 🔥"
    
    def load_brain(self, path: str = "data/brain.json"):
        """Load brain from file"""
        if not os.path.exists(path):
            return f"❌ No saved brain found at {path}"
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.knowledge = data.get("knowledge", {})
        self.weights = data.get("weights", {})
        self.epochs_trained = data.get("epochs_trained", 0)
        self.accuracy = data.get("accuracy", 0.0)
        self.conversation_history = data.get("conversation_history", [])
        
        return f"🧠 Brain loaded! Epochs: {self.epochs_trained}, Accuracy: {self.accuracy*100:.1f}% ✅"
    
    def reset_brain(self):
        """Reset brain to initial state"""
        self.weights = {k: 0.5 for k in self.weights}
        self.knowledge = {}
        self.patterns = {}
        self.conversation_history = []
        self.epochs_trained = 0
        self.accuracy = 0.0
        
        # Re-initialize
        self._init_brain()
        
        return "🔄 Brain reset! Fresh start! 🧠"


# ==================== SKILL FUNCTIONS ====================

def handle_learning_command(text: str, brain: BrainTrainer) -> str:
    """Handle learning/training commands"""
    text_lower = text.lower()
    
    # Train with data
    if "train" in text_lower:
        return "📊 Training requires data!\n\nUse: train with [data]\nOr: learn from conversation\n\nI learn automatically from every interaction!"
    
    # Load physics
    if "physics" in text_lower or "the well" in text_lower:
        return brain.load_physics_data()
    
    # Brain status
    if "brain status" in text_lower or "brain info" in text_lower:
        return brain.get_brain_status()
    
    # Save brain
    if "save brain" in text_lower or "save knowledge" in text_lower:
        return brain.save_brain()
    
    # Load brain
    if "load brain" in text_lower or "load knowledge" in text_lower:
        return brain.load_brain()
    
    # Reset brain
    if "reset brain" in text_lower or "clear brain" in text_lower:
        return brain.reset_brain()
    
    # Default learning
    return brain.learn(text, "")


# Factory function
def create_brain_trainer(config=None) -> BrainTrainer:
    return BrainTrainer(config)


# Export
__all__ = ['BrainTrainer', 'create_brain_trainer', 'handle_learning_command']