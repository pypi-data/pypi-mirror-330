"""
Constants for the package
"""

import json
import os
from enum import Enum
from typing import FrozenSet

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


class ISO_639_1(Enum):
    """Language codes in ISO 639-1 format"""

    AB = 1
    AA = 2
    AF = 3
    AK = 4
    SQ = 5
    AM = 6
    AR = 7
    AN = 8
    HY = 9
    AS = 10
    AV = 11
    AE = 12
    AY = 13
    AZ = 14
    BM = 15
    BA = 16
    EU = 17
    BE = 18
    BN = 19
    BH = 20
    BI = 21
    BS = 22
    BR = 23
    BG = 24
    MY = 25
    CA = 26
    CH = 27
    CE = 28
    NY = 29
    ZH = 30
    CV = 31
    KW = 32
    CO = 33
    CR = 34
    HR = 35
    CS = 36
    DA = 37
    DV = 38
    NL = 39
    DZ = 40
    EN = 41
    EO = 42
    ET = 43
    EE = 44
    FO = 45
    FJ = 46
    FI = 47
    FR = 48
    FF = 49
    GL = 50
    LG = 51
    KA = 52
    DE = 53
    EL = 54
    KL = 55
    GN = 56
    GU = 57
    HT = 58
    HA = 59
    HE = 60
    HZ = 61
    HI = 62
    HO = 63
    HU = 64
    IS = 65
    IO = 66
    IG = 67
    ID = 68
    IA = 69
    IE = 70
    IU = 71
    IK = 72
    GA = 73
    IT = 74
    JA = 75
    JV = 76
    KN = 77
    KR = 78
    KS = 79
    KK = 80
    KM = 81
    KI = 82
    RW = 83
    KY = 84
    RN = 85
    KV = 86
    KG = 87
    KO = 88
    KU = 89
    KJ = 90
    LO = 91
    LA = 92
    LV = 93
    LI = 94
    LN = 95
    LT = 96
    LU = 97
    LB = 98
    MK = 99
    MG = 100
    MS = 101
    ML = 102
    MT = 103
    GV = 104
    MI = 105
    MR = 106
    MH = 107
    MO = 108
    MN = 109
    NA = 110
    NV = 111
    NG = 112
    NE = 113
    ND = 114
    SE = 115
    NO = 116
    NB = 117
    NN = 118
    OC = 119
    OJ = 120
    CU = 121
    OR = 122
    OM = 123
    OS = 124
    PI = 125
    PA = 126
    PS = 127
    FA = 128
    PL = 129
    PT = 130
    QU = 131
    RO = 132
    RM = 133
    RU = 134
    SM = 135
    SG = 136
    SA = 137
    SC = 138
    GD = 139
    SR = 140
    SH = 141
    SN = 142
    II = 143
    SD = 144
    SI = 145
    SK = 146
    SL = 147
    SO = 148
    ST = 149
    NR = 150
    ES = 151
    SU = 152
    SW = 153
    SS = 154
    SV = 155
    TL = 156
    TY = 157
    TG = 158
    TA = 159
    TT = 160
    TE = 161
    TH = 162
    BO = 163
    TI = 164
    TO = 165
    TS = 166
    TN = 167
    TR = 168
    TK = 169
    TW = 170
    UG = 171
    UK = 172
    UR = 173
    UZ = 174
    VE = 175
    VI = 176
    VO = 177
    WA = 178
    CY = 179
    FY = 180
    WO = 181
    XH = 182
    YI = 183
    YO = 184
    ZA = 185
    ZU = 186

    def __str__(self):
        return super().__str__().split(".")[1]

    def all() -> FrozenSet["ISO_639_1"]:
        """Return a set of all supported languages."""
        return frozenset(ISO_639_1.__members__.keys())


class LANGUAGES(Enum):
    """ALL supported languages by the package"""

    ABKHAZIAN = 1
    AFAR = 2
    AFRIKAANS = 3
    AKAN = 4
    ALBANIAN = 5
    AMHARIC = 6
    ARABIC = 7
    ARAGONESE = 8
    ARMENIAN = 9
    ASSAMESE = 10
    AVARIC = 11
    AVESTAN = 12
    AYMARA = 13
    AZERBAIJANI = 14
    BAMBARA = 15
    BASHKIR = 16
    BASQUE = 17
    BELARUSIAN = 18
    BENGALI = 19
    BIHARI = 20
    BISLAMA = 21
    BOSNIAN = 22
    BRETON = 23
    BULGARIAN = 24
    BURMESE = 25
    CATALAN = 26
    CHAMORRO = 27
    CHECHEN = 28
    CHICHEWA = 29
    CHINESE = 30
    CHUVASH = 31
    CORNISH = 32
    CORSICAN = 33
    CREE = 34
    CROATIAN = 35
    CZECH = 36
    DANISH = 37
    DIVEHI = 38
    DUTCH = 39
    DZONGKHA = 40
    ENGLISH = 41
    ESPERANTO = 42
    ESTONIAN = 43
    EWE = 44
    FAROESE = 45
    FIJIAN = 46
    FINNISH = 47
    FRENCH = 48
    FULAH = 49
    GALICIAN = 50
    GANDA = 51
    GEORGIAN = 52
    GERMAN = 53
    GREEK = 54
    GREENLANDIC = 55
    GUARANI = 56
    GUJARATI = 57
    HAITIAN = 58
    HAUSA = 59
    HEBREW = 60
    HERERO = 61
    HINDI = 62
    HIRI_MOTU = 63
    HUNGARIAN = 64
    ICELANDIC = 65
    IDO = 66
    IGBO = 67
    INDONESIAN = 68
    INTERLINGUA = 69
    INTERLINGUE = 70
    INUKTITUT = 71
    INUPIAK = 72
    IRISH = 73
    ITALIAN = 74
    JAPANESE = 75
    JAVANESE = 76
    KANNADA = 77
    KANURI = 78
    KASHMIRI = 79
    KAZAKH = 80
    KHMER = 81
    KIKUYU = 82
    KINYARWANDA = 83
    KIRGHIZ = 84
    KIRUNDI = 85
    KOMI = 86
    KONGO = 87
    KOREAN = 88
    KURDISH = 89
    KWANYAMA = 90
    LAO = 91
    LATIN = 92
    LATVIAN = 93
    LIMBURGISH = 94
    LINGALA = 95
    LITHUANIAN = 96
    LUBA = 97
    LUXEMBOURGISH = 98
    MACEDONIAN = 99
    MALAGASY = 100
    MALAY = 101
    MALAYALAM = 102
    MALTESE = 103
    MANX = 104
    MAORI = 105
    MARATHI = 106
    MARSHALLESE = 107
    MOLDAVIAN = 108
    MONGOLIAN = 109
    NAURU = 110
    NAVAJO = 111
    NDONGA = 112
    NEPALI = 113
    NORTH_NDEBELE = 114
    NORTHERN_SAMI = 115
    NORWEGIAN = 116
    NORWEGIAN_BOKMÅL = 117
    NORWEGIAN_NYNORSK = 118
    OCCITAN = 119
    OJIBWA = 120
    OLD_CHURCH_SLAVONIC = 121
    ORIYA = 122
    OROMO = 123
    OSSETIAN = 124
    PALI = 125
    PANJABI = 126
    PASHTO = 127
    PERSIAN = 128
    POLISH = 129
    PORTUGUESE = 130
    QUECHUA = 131
    ROMANIAN = 132
    ROMANSH = 133
    RUSSIAN = 134
    SAMOAN = 135
    SANGO = 136
    SANSKRIT = 137
    SARDINIAN = 138
    SCOTTISH_GAELIC = 139
    SERBIAN = 140
    SERBO_CROATIAN = 141
    SHONA = 142
    SICHUAN_YI = 143
    SINDHI = 144
    SINHALESE = 145
    SLOVAK = 146
    SLOVENIAN = 147
    SOMALI = 148
    SOTHO = 149
    SOUTH_NDEBELE = 150
    SPANISH = 151
    SUNDANESE = 152
    SWAHILI = 153
    SWATI = 154
    SWEDISH = 155
    TAGALOG = 156
    TAHITIAN = 157
    TAJIK = 158
    TAMIL = 159
    TATAR = 160
    TELUGU = 161
    THAI = 162
    TIBETAN = 163
    TIGRINYA = 164
    TONGA = 165
    TSONGA = 166
    TSWANA = 167
    TURKISH = 168
    TURKMEN = 169
    TWI = 170
    UIGHUR = 171
    UKRAINIAN = 172
    URDU = 173
    UZBEK = 174
    VENDA = 175
    VIETNAMESE = 176
    VOLAPÜK = 177
    WALLOON = 178
    WELSH = 179
    WESTERN_FRISIAN = 180
    WOLOF = 181
    XHOSA = 182
    YIDDISH = 183
    YORUBA = 184
    ZHUANG = 185
    ZULU = 186

    @property
    def iso_code_639_1(self) -> ISO_639_1:
        """Return the ISO 639-1 code of this language."""
        for iso_code in ISO_639_1:
            if iso_code.value == self.value:
                return iso_code
        raise ValueError(f"No ISO 639-1 code found for language {self.name}")

    @classmethod
    def all(cls) -> FrozenSet["LANGUAGES"]:
        """Return a set of all supported languages."""
        return frozenset(cls.__members__.values())

    @classmethod
    def from_iso_code_639_1(cls, iso_code: ISO_639_1) -> "LANGUAGES":
        """Return the language with the given ISO 639-1 code."""
        for lang in cls:
            if lang.iso_code_639_1 == iso_code:
                return lang
        raise ValueError(f"No language found for ISO 639-1 code {iso_code}")

    @classmethod
    def from_iso_code_639_1_str(cls, iso_code: str) -> "LANGUAGES":
        """Return the language with the given ISO 639-1 code."""
        for lang in cls:
            if lang.iso_code_639_1.name.lower() == iso_code.lower():
                return lang
        raise ValueError(f"No language found for ISO 639-1 code {iso_code}")

    def __str__(self):
        return super().__str__().split(".")[1]
