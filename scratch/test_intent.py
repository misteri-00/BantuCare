import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.chatbot import classify_intent, INTENT_PATTERNS

text = "Kak, tolong! Saya mau donasi 50 ribu tapi malah ketik 500 ribu di aplikasi. Bisa dicancel atau dikembalikan ga ya dananya?"
print(f"Result: {classify_intent(text)}")
