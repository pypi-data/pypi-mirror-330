"""
Constants for the package
"""

import json
import os
from enum import Enum

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
FASTTEXT_WEIGHTS = ["lid.176.ftz", "discord_langdetect.ftz"]
WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "weights")

top_languages = json.load(
    open(
        os.path.join(
            os.path.join(os.path.dirname(__file__), "data"), "top_languages.json"
        ),
        "r",
    )
)


TOP_LANGUAGES = [
    lang for lang, _ in sorted(top_languages.items(), key=lambda x: x[1], reverse=True)
]


class LANGUAGES(Enum):
    """ALL supported languages by the package"""

    ABKHAZIAN = "AB"
    AFAR = "AA"
    AFRIKAANS = "AF"
    AKAN = "AK"
    ALBANIAN = "SQ"
    AMHARIC = "AM"
    ARABIC = "AR"
    ARAGONESE = "AN"
    ARMENIAN = "HY"
    ASSAMESE = "AS"
    AVARIC = "AV"
    AVESTAN = "AE"
    AYMARA = "AY"
    AZERBAIJANI = "AZ"
    BAMBARA = "BM"
    BASHKIR = "BA"
    BASQUE = "EU"
    BELARUSIAN = "BE"
    BENGALI = "BN"
    BIHARI = "BH"
    BISLAMA = "BI"
    BOSNIAN = "BS"
    BRETON = "BR"
    BULGARIAN = "BG"
    BURMESE = "MY"
    CATALAN = "CA"
    CHAMORRO = "CH"
    CHECHEN = "CE"
    CHICHEWA = "NY"
    CHINESE = "ZH"
    CHUVASH = "CV"
    CORNISH = "KW"
    CORSICAN = "CO"
    CREE = "CR"
    CROATIAN = "HR"
    CZECH = "CS"
    DANISH = "DA"
    DIVEHI = "DV"
    DUTCH = "NL"
    DZONGKHA = "DZ"
    ENGLISH = "EN"
    ESPERANTO = "EO"
    ESTONIAN = "ET"
    EWE = "EE"
    FAROESE = "FO"
    FIJIAN = "FJ"
    FINNISH = "FI"
    FRENCH = "FR"
    FULAH = "FF"
    GALICIAN = "GL"
    GANDA = "LG"
    GEORGIAN = "KA"
    GERMAN = "DE"
    GREEK = "EL"
    GREENLANDIC = "KL"
    GUARANI = "GN"
    GUJARATI = "GU"
    HAITIAN = "HT"
    HAUSA = "HA"
    HEBREW = "HE"
    HERERO = "HZ"
    HINDI = "HI"
    HIRI_MOTU = "HO"
    HUNGARIAN = "HU"
    ICELANDIC = "IS"
    IDO = "IO"
    IGBO = "IG"
    INDONESIAN = "ID"
    INTERLINGUA = "IA"
    INTERLINGUE = "IE"
    INUKTITUT = "IU"
    INUPIAK = "IK"
    IRISH = "GA"
    ITALIAN = "IT"
    JAPANESE = "JA"
    JAVANESE = "JV"
    KANNADA = "KN"
    KANURI = "KR"
    KASHMIRI = "KS"
    KAZAKH = "KK"
    KHMER = "KM"
    KIKUYU = "KI"
    KINYARWANDA = "RW"
    KIRGHIZ = "KY"
    KIRUNDI = "RN"
    KOMI = "KV"
    KONGO = "KG"
    KOREAN = "KO"
    KURDISH = "KU"
    KWANYAMA = "KJ"
    LAO = "LO"
    LATIN = "LA"
    LATVIAN = "LV"
    LIMBURGISH = "LI"
    LINGALA = "LN"
    LITHUANIAN = "LT"
    LUBA = "LU"
    LUXEMBOURGISH = "LB"
    MACEDONIAN = "MK"
    MALAGASY = "MG"
    MALAY = "MS"
    MALAYALAM = "ML"
    MALTESE = "MT"
    MANX = "GV"
    MAORI = "MI"
    MARATHI = "MR"
    MARSHALLESE = "MH"
    MOLDAVIAN = "MO"
    MONGOLIAN = "MN"
    NAURU = "NA"
    NAVAJO = "NV"
    NDONGA = "NG"
    NEPALI = "NE"
    NORTH_NDEBELE = "ND"
    NORTHERN_SAMI = "SE"
    NORWEGIAN = "NO"
    NORWEGIAN_BOKMÅL = "NB"
    NORWEGIAN_NYNORSK = "NN"
    OCCITAN = "OC"
    OJIBWA = "OJ"
    OLD_CHURCH_SLAVONIC = "CU"
    ORIYA = "OR"
    OROMO = "OM"
    OSSETIAN = "OS"
    PALI = "PI"
    PANJABI = "PA"
    PASHTO = "PS"
    PERSIAN = "FA"
    POLISH = "PL"
    PORTUGUESE = "PT"
    QUECHUA = "QU"
    ROMANIAN = "RO"
    ROMANSH = "RM"
    RUSSIAN = "RU"
    SAMOAN = "SM"
    SANGO = "SG"
    SANSKRIT = "SA"
    SARDINIAN = "SC"
    SCOTTISH_GAELIC = "GD"
    SERBIAN = "SR"
    SERBO_CROATIAN = "SH"
    SHONA = "SN"
    SICHUAN_YI = "II"
    SINDHI = "SD"
    SINHALESE = "SI"
    SLOVAK = "SK"
    SLOVENIAN = "SL"
    SOMALI = "SO"
    SOTHO = "ST"
    SOUTH_NDEBELE = "NR"
    SPANISH = "ES"
    SUNDANESE = "SU"
    SWAHILI = "SW"
    SWATI = "SS"
    SWEDISH = "SV"
    TAGALOG = "TL"
    TAHITIAN = "TY"
    TAJIK = "TG"
    TAMIL = "TA"
    TATAR = "TT"
    TELUGU = "TE"
    THAI = "TH"
    TIBETAN = "BO"
    TIGRINYA = "TI"
    TONGA = "TO"
    TSONGA = "TS"
    TSWANA = "TN"
    TURKISH = "TR"
    TURKMEN = "TK"
    TWI = "TW"
    UIGHUR = "UG"
    UKRAINIAN = "UK"
    URDU = "UR"
    UZBEK = "UZ"
    VENDA = "VE"
    VIETNAMESE = "VI"
    VOLAPÜK = "VO"
    WALLOON = "WA"
    WELSH = "CY"
    WESTERN_FRISIAN = "FY"
    WOLOF = "WO"
    XHOSA = "XH"
    YIDDISH = "YI"
    YORUBA = "YO"
    ZHUANG = "ZA"
    ZULU = "ZU"

    @property
    def iso_code_639_1(self) -> str:
        """Return the ISO 639-1 code of this language."""
        return self.value

    @classmethod
    def all_iso_codes_639_1(cls) -> set:
        """Return a set of all ISO 639-1 codes."""
        return {lang.value for lang in cls}

    @classmethod
    def all(cls) -> set:
        """Return a set of all supported languages."""
        return set(cls.__members__.keys())

    @classmethod
    def from_iso_code_639_1_str(cls, iso_code: str) -> "LANGUAGES":
        """Return the language with the given ISO 639-1 code."""
        iso_code = iso_code.upper()

        for lang in cls:
            if lang.value == iso_code:
                return lang

        raise ValueError(f"Language with ISO 639-1 code {iso_code} not found")

    def __str__(self):
        return super().__str__().split(".")[1]
