import short_language_detection as sld

# Create a detector
predictor = sld.Detector()

print(f"supported languages: {len(predictor.supported_languages)}")

# Detect the language of a text
print(predictor.detect("no")[0])
