from deep_translator import GoogleTranslator

def test_translation():
    text = "Stock Market News for Jan 16, 2026"
    print(f"Original: {text}")
    
    try:
        translated = GoogleTranslator(source='auto', target='ko').translate(text)
        print(f"Translated: {translated}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_translation()
