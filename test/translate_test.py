from googletrans import Translator 

translator = Translator()
mytext = "नमस्ते। क्या हाल है?"
translation = translator.translate(mytext)
detection = translator.detect(mytext)

print(detection.lang)
print(translation.text)

if detection.lang == "hi":
    print("IT WAS HINDI!")