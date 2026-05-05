"""
Offline, Lightweight AI Module for Mindease
Deeply human, emotionally intelligent companion.

Response philosophy:
  1. Mirror the feeling first.
  2. Gate the response on intensity (HIGH → breathe, MEDIUM → question+offer, LOW → natural chat).
  3. Ask ONE meaningful question.
  4. Keep it human: short sentences, "…" pauses, ≤1 emoji.
  5. Never lecture. Never sound robotic.
"""

import random
from typing import Dict, List, Any

# =====================================================================
# PART 1: MOOD DETECTION
# =====================================================================

EMOJI_TO_MOOD: Dict[str, str] = {
    "😊": "happy",
    "😐": "neutral",
    "😢": "sad",
    "😡": "angry",
    "😴": "tired",
    "😍": "loved",
}

def detect_mood_from_emoji(emoji: str) -> str:
    """Map emoji strictly to core moods. Fallback to neutral if unknown."""
    if not emoji:
        return "neutral"
    if emoji in EMOJI_TO_MOOD:
        return EMOJI_TO_MOOD[emoji]
    for key, val in EMOJI_TO_MOOD.items():
        if key in emoji:
            return val
    return "neutral"


# =====================================================================
# PART 2: EMOTION DETECTION
# =====================================================================

_KEYWORD_MAP: Dict[str, List[str]] = {
    "overwhelm":  ["too much", "overwhelmed", "drowning", "can't handle", "cant handle", "stressed out"],
    "anxious":    ["worry", "anxious", "anxiety", "panic", "scared", "nervous", "afraid"],
    "hopeful":    ["excited", "looking forward", "getting better", "hope", "optimistic"],
    "grief":      ["loss", "miss", "gone", "heartbreak", "grieving", "lost someone"],
    "burnout":    ["exhausted", "done", "give up", "drained", "burnt out", "burned out"],
    "lonely":     ["lonely", "alone", "no one", "nobody", "isolated", "left out"],
}

def detect_emotion_from_text(text: str) -> str:
    """Extract deeper emotional signal from raw text input."""
    if not text:
        return "none"
    lower_text = text.lower()
    for emotion, keywords in _KEYWORD_MAP.items():
        if any(kw in lower_text for kw in keywords):
            return emotion
    return "none"


# =====================================================================
# PART 3: INTENSITY EVALUATION
# =====================================================================

_HIGH_KEYWORDS = [
    "overwhelmed", "can't handle", "cant handle", "exhausted", "hate this",
    "panic", "drowning", "give up", "breakdown", "falling apart",
    "can't breathe", "cant breathe", "too much", "done with everything",
]
_MEDIUM_KEYWORDS = [
    "tired", "frustrated", "sad", "annoying", "hard", "struggling",
    "down", "low", "not great", "not okay", "a little off", "meh",
]

def evaluate_intensity(user_message: str) -> str:
    """Evaluate emotional intensity from keywords and syntax."""
    lower = user_message.lower()
    if any(kw in lower for kw in _HIGH_KEYWORDS):
        return "high"
    if any(kw in lower for kw in _MEDIUM_KEYWORDS):
        return "medium"
    return "low"


# =====================================================================
# PART 4: EMOTIONAL REFLECTION (Step 1 of prompt)
# Mirror the feeling before anything else.
# =====================================================================

_REFLECTIONS: Dict[str, List[str]] = {
    "happy": [
        "That sounds really lovely…",
        "Oh, that's so good to hear…",
        "I can feel the warmth in that…",
    ],
    "neutral": [
        "I hear you…",
        "Okay, I'm with you…",
        "Got it… I'm here.",
    ],
    "sad": [
        "That sounds really heavy…",
        "I can feel how much that hurts…",
        "Oh… that's a lot to carry.",
    ],
    "angry": [
        "That sounds so frustrating…",
        "Ugh, that really doesn't seem fair…",
        "I can feel how much that got to you…",
    ],
    "tired": [
        "That sounds really draining…",
        "You sound so worn out…",
        "That's a lot of weight to carry around…",
    ],
    "loved": [
        "That sounds so warm and beautiful…",
        "Oh, that's really touching…",
        "I love hearing that for you…",
    ],
}

def _get_reflection(mood: str) -> str:
    pool = _REFLECTIONS.get(mood, _REFLECTIONS["neutral"])
    return random.choice(pool)


# =====================================================================
# PART 5: INTENSITY-GATED CORE RESPONSES (Steps 2 & 3 of prompt)
# =====================================================================

# HIGH — slow down, suggest breathing gently
_HIGH_CORES: List[str] = [
    "Let's pause for a moment… we can take a small breath together 💛",
    "Hey… let's just slow down for a second. You don't have to figure it all out right now.",
    "That's a lot. Let's breathe through this one step at a time 💛",
    "I'm right here. Let's just take one breath together before anything else.",
]

# MEDIUM — ask a question, offer help
_MEDIUM_CORES: Dict[str, List[str]] = {
    "happy": [
        "Do you want to tell me more about what's been going well?",
        "What's been the best part of it for you?",
    ],
    "neutral": [
        "Is there something specific sitting on your mind?",
        "Do you want to just talk, or is there something I can help with?",
    ],
    "sad": [
        "Do you want to talk about what's been weighing on you?",
        "Would it help to share more of what's going on?",
    ],
    "angry": [
        "Do you want to talk about what happened?",
        "What's been frustrating you the most?",
    ],
    "tired": [
        "Have you been mentally tired, or is it more physical?",
        "What's been draining you the most lately?",
    ],
    "loved": [
        "What's been making you feel this way?",
        "Do you want to share more about it?",
    ],
}

# LOW — natural, warm, conversational
_LOW_CORES: Dict[str, List[str]] = {
    "happy": [
        "That's really nice. Tell me what's been making you smile.",
        "That's lovely. What's the best part of your day been?",
        "I love hearing that. What happened?",
    ],
    "neutral": [
        "How's the rest of your day looking?",
        "Anything interesting on your mind today?",
        "I'm here. What would you like to talk about?",
    ],
    "sad": [
        "You don't have to go through this alone. I'm right here.",
        "It's okay to feel this way. Take your time.",
        "I'm listening… whenever you're ready.",
    ],
    "angry": [
        "It sounds like something really got to you. I'm listening.",
        "That makes sense. I'd feel the same way.",
        "You're allowed to feel this. Tell me what happened.",
    ],
    "tired": [
        "Rest is doing something. Be gentle with yourself today.",
        "You've carried a lot. It's okay to slow down.",
        "Your body is telling you something. I hope you can rest soon.",
    ],
    "loved": [
        "That's really beautiful. Hold onto that feeling.",
        "Those moments are so special. I'm glad you have that.",
        "Love like that is worth everything.",
    ],
}


def _get_core_response(mood: str, intensity: str) -> str:
    if intensity == "high":
        return random.choice(_HIGH_CORES)

    if intensity == "medium":
        pool = _MEDIUM_CORES.get(mood, _MEDIUM_CORES["neutral"])
        return random.choice(pool)

    pool = _LOW_CORES.get(mood, _LOW_CORES["neutral"])
    return random.choice(pool)


# =====================================================================
# PART 6: MEANINGFUL FOLLOW-UP QUESTION (Step 3 of prompt)
# One question only. Skipped for HIGH (breathing takes priority).
# =====================================================================

_FOLLOWUP_QUESTIONS: Dict[str, List[str]] = {
    "happy": [
        "What's been the highlight of your day?",
        "What made you smile the most today?",
    ],
    "neutral": [
        "Is there anything on your mind right now?",
        "How are you feeling underneath all of it?",
    ],
    "sad": [
        "What's the hardest part of this for you?",
        "Is there one thing that's been weighing on you the most?",
    ],
    "angry": [
        "What's the thing that got to you the most?",
        "What would have made this situation feel fairer?",
    ],
    "tired": [
        "When did you last truly rest?",
        "What's been taking the most out of you?",
    ],
    "loved": [
        "What does this connection mean to you?",
        "Who in your life makes you feel the most seen?",
    ],
}

_EMOTION_FOLLOWUPS: Dict[str, str] = {
    "overwhelm": "What feels like the heaviest thing on your plate right now?",
    "anxious":   "What's the thought that keeps coming back the most?",
    "burnout":   "What's one thing you could let go of today, even just for an hour?",
    "grief":     "Would you like to tell me about them?",
    "lonely":    "Is there someone you wish you could reach out to right now?",
    "hopeful":   "What's giving you that sense of hope?",
}

def _get_followup(mood: str, emotion: str, intensity: str) -> str:
    """Return one meaningful question. Empty string for HIGH intensity."""
    if intensity == "high":
        return ""

    # Emotion-specific question takes priority
    if emotion in _EMOTION_FOLLOWUPS:
        return _EMOTION_FOLLOWUPS[emotion]

    pool = _FOLLOWUP_QUESTIONS.get(mood, _FOLLOWUP_QUESTIONS["neutral"])
    return random.choice(pool)


# =====================================================================
# PART 7: CONTEXT PREFIX
# =====================================================================

def _get_context_prefix(mood: str, previous_moods: List[str]) -> str:
    if not previous_moods:
        return ""
    last = previous_moods[-1]
    if last in ["sad", "angry", "tired"] and mood in ["happy", "loved"]:
        return "I'm really glad things are feeling a bit lighter… "
    if last == "sad" and mood == "sad":
        return "I see you're still carrying something heavy… "
    if last in ["happy", "loved"] and mood in ["sad", "angry"]:
        return "It sounds like something shifted… "
    return ""


# =====================================================================
# PART 8: ACTION TRIGGER LOGIC
# =====================================================================

def _decide_action_trigger(intensity: str, context: List[Dict]) -> str | None:
    negative_streak = sum(
        1 for c in context[-3:]
        if c.get("mood") in ["sad", "angry", "tired"]
    )
    if intensity == "high" or negative_streak >= 3:
        return "breathing_exercise"
    return None


# =====================================================================
# MAIN ENTRY POINT
# =====================================================================

def handle_chat(
    user_message: str,
    emoji: str,
    context: List[Dict[str, Any]],
    mood_override: str | None = None,
) -> Dict[str, Any]:
    """
    Main entry point for AI logic. Completely offline and crash-proof.

    Implements the companion prompt template:
      Step 1 → Emotional reflection (mirror the feeling)
      Step 2 → Intensity-gated response (HIGH: breathe | MEDIUM: question | LOW: chat)
      Step 3 → One meaningful follow-up question
      Step 4 → Human: short sentences, "…" pauses, ≤1 emoji

    context format: [{"user": "…", "ai": "…", "mood": "…", "emotion": "…"}, …]
    """
    try:
        # Sanitize
        user_message = str(user_message or "").strip()
        emoji = str(emoji or "").strip()
        context = context[-5:] if isinstance(context, list) else []

        # Detect state
        # mood_override lets callers (e.g. controller) pass a pre-resolved mood
        # string directly, bypassing emoji lookup.
        if mood_override and mood_override in _REFLECTIONS:
            mood = mood_override
        else:
            mood = detect_mood_from_emoji(emoji)
        emotion = detect_emotion_from_text(user_message)
        intensity = evaluate_intensity(user_message)

        # Determine action trigger (breathing exercise)
        action_trigger = _decide_action_trigger(intensity, context)

        # Context-awareness prefix
        previous_moods = [c.get("mood") for c in context if c.get("mood")]
        prefix = _get_context_prefix(mood, previous_moods)

        # --- Build the response ---

        # Step 1: Mirror the emotion
        reflection = _get_reflection(mood)

        # Step 2: Intensity-gated body
        core = _get_core_response(mood, intensity)

        # Step 3: One meaningful question (omitted for HIGH — breathing takes over)
        followup = _get_followup(mood, emotion, intensity)

        # Assemble with natural pauses
        parts = [f"{prefix}{reflection}", core]
        if followup:
            parts.append(followup)

        final_response = "\n\n".join(parts)

        # Update context
        new_context = context + [{
            "user": user_message,
            "ai": final_response,
            "mood": mood,
            "emotion": emotion,
        }]

        return {
            "mood": mood,
            "emotion": emotion,
            "intensity": intensity,
            "response": final_response,
            "context": new_context[-5:],
            "action_trigger": action_trigger,
        }

    except Exception:
        # NEVER CRASH.
        return {
            "mood": "neutral",
            "emotion": "none",
            "intensity": "low",
            "response": "I'm here for you… whenever you're ready. 💛",
            "context": context,
            "action_trigger": None,
        }
