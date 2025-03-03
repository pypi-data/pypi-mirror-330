import short_language_detection as sld

# Create a detector
predictor = sld.Detector()

print(
    predictor.supported_languages
)  # {'ro': 'ROMANIAN', 'ru': 'RUSSIAN', 'nl': 'DUTCH', ...}

# Detect the language of a text
print(predictor.detect("hello"))
# ({'language': 'ENGLISH', 'code': 'EN', 'score': 1.0, 'prefered': True, 'reliable': True},)
