import unittest
from src.cjlutils import StringUtil
from src.cjlutils.StringUtil import StandardEncodingsEnum

origins = [
    '1',
    '123',
    '11111111',
    '12121212',
    '121212121',
    '12121212121',
    '111122223333',
    'a',
    'abc',
    '一',
    '一二三',
    '123abc一二三',
    '`-=[]\\;\',/',
    '~!@#$%^&*()_+{}|:"<>?',
    '`-=【】、；，。、',
    '~！@#￥%……&*（）——+「」|："《》？',
    '`~!@#$%^&*()_+-=[]{}|;:,.<>?/\\',
    '饕餮',
    '魑魅魍魉',
    '鳏寡孤独',
    'œ∑´®†¥¨ˆøπ“‘',
    'œ∑®†¥¥øπåß∂ƒ©˙∆˚¬…æΩ≈ç√∫µ≤≥µ¡™£¢∞§¶•ªº–≠',
    'Œ∑´®†Á¨ˆØ∏ÅÍÎÏ©ÓÔ˚Ò…ÆΩ≈Ç√ı˜Â≤≥ı¡™£¢∞§¶•ªº–≠',
]
special_origins = {
    "<unk>", "<pad>", "<s>", "</s>",
    "\'", "\"", "’", "‘", "“", "”", "\\", "?", "%",
    "'⋆⃝",
    "'⚜",
    "'🇹🇷҉͜͡★KILIC⍣✮",
    "'الو ",
    "'乖乖-emo",
    "'𓆩ℍ𝕖𝕒𝕣𝕥",
    "🔥迎中秋特惠买4送1：‍🔥",
    "'The game wheel of fortune you participated in 🇹🇷҉͜͡★KILIC⍣✮",
    "'❥͢",
    "فر☛Ɠɦ᭄يدة ",
    "ᴬᴰᴹᴵᴺ᭄🇰​🇦​🇦​🇳​",
    "🖤ꙵ͜͡✵кяιsтαℓ",
    "✌️𝙛𝙞𝙙𝙚𝙡 𝙝𝙖𝙣✌️ ",
    "Sÿ🔥حاتم",
    "ادم 😎adam",
    "غـᬼ🇵🇸⑅⃝ـᬼزاوية🇪🇬𓅇꙰᭄ɳ",
    "تـ͢آڵــᬼᬼ🫀⑅⃝ـينℳ⁷⁷⁷",
    "♛جہوكُہر♛",
    "👑أّلَمشُـرفُـ🔥ميّأّر𓅇꙰",
    "ÃĤϻẸĎ..ẸĹ.ŤỖŘЌẸЎ♥🔥",
    "𝗕𝗼𝘀𝘀⚡",
    "وكيلͣــͫــͥـͬــͣـᷜــة❣️",
    "نقاء الروح ⭐҉⍣⃝M🧿",
    "⭐نوتيلا⭐",
    "💥ᓚ⅃ᴝ♡Lჺ💥 ",
    "🥂محمོ࿆ــᩧودღ🥂",
    "تـ͢آڵــᬼᬼ🫀⑅⃝ـينℳ⁷⁷⁷",
    "وكيـ𓆩𓃗‌⍣⃝ŤŘẸŇĎـ⍣⃟𖣘 ـل",
    "الساهر ❌ 🇸🇦",
    "مغلق حساب ",
    "𝄠",
    "\'𝄠",
    "🐰⃝꙰🇹𝐴𝑅𝑎🐰⃝꙰🐰agency",
    "🔰",
    "M⑅⃝S",
    "كيداهم🏵️",
    "𝄠𝄠🌠بًــ፝͡ۦحًــر.༄ᵛᶦᵖ🥃",
    "ERDAL🪓21",
    "🎙سـᘓ᭄⑅ــيرينᴬᵈᵐⁱⁿ᭄",
    "💞⋆ᤢⷦ⋆ᤢᷴ⋆ᷢᤢ⋆ⷮᤢ🅒🅘🅦🅐🅝",
    "🎙سـᘓ᭄⑅ــيرينᴬᵈᵐⁱⁿ᭄",
    "M⑅⃝S💔ᤂ᪱ɹ̤ᓗฺใ⎽බᦇɹɹɹمشر فة",
    "『𝕬𝖘𝖎𝖘𝖙𝖆𝖓 𝕰𝖑𝖆",
    "²³⁰",
    "ȷ᎗ᓄ",
    "𓆩ℍ𝕖𝕒𝕣𝕥",
    "⏤͟͟͞𓄂",
    "✪»ⷨ͢🇮🇳𝐌𝐫.𝐀яυη",
    "خي 🇱🇧 وكيل ",
    "✮͜͡❥ɒɛɩɪॖӈѧтսͷ",
    "⚜️Edward♘",
    "🌹🎇 COFFEE LOVELY 💫✨",
    "ťȁ🐯ïǥȩȑ🆚️",
    "草莓🀼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰼󤰧",
    "😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡 😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🐧",
    "family 𝐕❍𝐈𝐂𝐄𔒝AττracτᎥoภ you applied for has passed your joining application.",
    "'حـᬼuـنـ𓆩a𓆪",
    "@✬͜͡𝑨𝒕𝒕𝒊𝒕𝒖𝒅𝒆▓࿐",
    """[الشحن من وكيل الشحن] لقد نجحت في إرسال عملات ذهبية.
المرسل:
مستر علي U.A⚜️（ID：80003）
المستفيد:
 عــᬼ™ـدنـ𓆩𓆪ـآטּ☝（ID：2100744）
الوقت:
2023-11-27 09:54:04 (توقيت السعودية)
مبلغ الشحن (العملات الذهبية):
800""",
    """声音大 玩的🌸	状态‍🔥热 还
可以看🦋下雨""",
    """


    """,
    "حـ",
    " عــᬼ™ـدنـ𓆩𓆪ـآטּ☝（ID：2100744）",
    "ok吖这回真晚安💤",
}


# def contains(string: str, sub: str) -> bool
class ContainsTest(unittest.TestCase):

    def test_none(self):
        string = None
        sub = None
        self.assertFalse(StringUtil.contains(string, sub))

    def test_none_string(self):
        string = None
        sub = 'sub'
        self.assertFalse(StringUtil.contains(string, sub))

    def test_none_sub(self):
        string = 'string'
        sub = None
        self.assertFalse(StringUtil.contains(string, sub))

    def test_empty_string(self):
        string = ''
        sub = 'sub'
        self.assertFalse(StringUtil.contains(string, sub))

    def test_empty_sub(self):
        string = 'string'
        sub = ''
        self.assertTrue(StringUtil.contains(string, sub))

    def test_contains(self):
        string = 'string'
        sub = 'str'
        self.assertTrue(StringUtil.contains(string, sub))

    def test_not_contains(self):
        string = 'string'
        sub = 'sub'
        self.assertFalse(StringUtil.contains(string, sub))


# def index_of_first(string: str, substring) -> int
class IndexOfFirstTest(unittest.TestCase):
    def test_none(self):
        string = None
        sub = None
        self.assertEqual(-1, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_none_string(self):
        string = None
        sub = 'sub'
        self.assertEqual(-1, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_none_sub(self):
        string = 'string'
        sub = None
        self.assertEqual(-1, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_empty_string(self):
        string = ''
        sub = 'sub'
        self.assertEqual(-1, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_empty_sub(self):
        string = 'string'
        sub = ''
        self.assertEqual(0, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_prefix(self):
        string = 'string'
        sub = 'str'
        self.assertEqual(0, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_suffix(self):
        string = 'string'
        sub = 'ing'
        self.assertEqual(3, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_middle(self):
        string = 'string'
        sub = 'ri'
        self.assertEqual(2, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_not_contains(self):
        string = 'string'
        sub = 'sub'
        self.assertEqual(-1, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_special_origin_same(self):
        for special in special_origins:
            string = special
            sub = string
            self.assertEqual(0, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_special_origin_pre(self):
        for special in special_origins:
            string = special
            sub = string[:len(string) // 2]
            self.assertEqual(0, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_special_origin_suf(self):
        for special in special_origins:
            string = special
            sub = string[len(string) // 2:]
            self.assertEqual(string.find(sub), StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_special_origin_middle(self):
        for special in special_origins:
            string = special
            start_index = len(string) // 2
            stop_index = len(string) - start_index
            sub = string[start_index:stop_index]
            self.assertGreaterEqual(start_index, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')
            self.assertEqual(string.find(sub), StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_special_origin_not_contains(self):
        for special in special_origins:
            string = special
            sub = string + 'sub'
            self.assertEqual(-1, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_regex_char0(self):
        string = '\\[.*'
        sub = '\\'
        self.assertEqual(0, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')

    def test_regex_char1(self):
        string = '\\[.*'
        sub = '.'
        self.assertEqual(2, StringUtil.index_of_first(string, sub), f'origin: {string}, sub: {sub}')


# def index_of_last(string: str, substring: str) -> int
class IndexOfLastTest(unittest.TestCase):
    def test_none(self):
        string = None
        sub = None
        self.assertEqual(-1, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_none_string(self):
        string = None
        sub = 'sub'
        self.assertEqual(-1, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_none_sub(self):
        string = 'string'
        sub = None
        self.assertEqual(-1, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_empty_string(self):
        string = ''
        sub = 'sub'
        self.assertEqual(-1, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_empty_sub(self):
        string = 'string'
        sub = ''
        self.assertEqual(6, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_prefix(self):
        string = 'string'
        sub = 'str'
        self.assertEqual(0, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_suffix(self):
        string = 'string'
        sub = 'ing'
        self.assertEqual(3, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_middle(self):
        string = 'string'
        sub = 'ri'
        self.assertEqual(2, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_not_contains(self):
        string = 'string'
        sub = 'sub'
        self.assertEqual(-1, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_special_origin_same(self):
        for special in special_origins:
            string = special
            sub = string
            self.assertEqual(0, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_special_origin_pre(self):
        for special in special_origins:
            string = special
            sub = string[:len(string) // 2]
            self.assertEqual(string.rfind(sub), StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_special_origin_suf(self):
        for special in special_origins:
            string = special
            sub = string[len(string) // 2:]
            self.assertEqual(len(string) // 2, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')

    def test_special_origin_middle(self):
        for special in special_origins:
            string = special
            start_index = len(string) // 4
            stop_index = len(string) - start_index
            sub = string[start_index:stop_index]
            self.assertLessEqual(start_index, StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')
            self.assertEqual(string.rfind(sub), StringUtil.index_of_last(string, sub), f'origin: {string}, sub: {sub}')


class ToAndFromBytesMatchTestDefaultEncode(unittest.TestCase):

    def test_none(self):
        origin = None
        encoded = StringUtil.to_bytes(origin)
        decoded = StringUtil.from_bytes(encoded)
        self.assertEqual(origin, decoded)

    def test_empty(self):
        origin = ''
        encoded = StringUtil.to_bytes(origin)
        decoded = StringUtil.from_bytes(encoded)
        self.assertEqual(origin, decoded)

    def test_regular(self):
        for origin in origins:
            encoded = StringUtil.to_bytes(origin)
            decoded = StringUtil.from_bytes(encoded)
            self.assertEqual(origin, decoded)

    def test_special(self):
        for origin in special_origins:
            encoded = StringUtil.to_bytes(origin)
            decoded = StringUtil.from_bytes(encoded)
            self.assertEqual(origin, decoded)


class ToAndFromBytesMatchTestUtf32Be(unittest.TestCase):
    encode = StandardEncodingsEnum.UTF_32_BE

    def test_none(self):
        origin = None
        encoded = StringUtil.to_bytes(origin, encode=self.encode)
        decoded = StringUtil.from_bytes(encoded, encode=self.encode)
        self.assertEqual(origin, decoded)

    def test_empty(self):
        origin = ''
        encoded = StringUtil.to_bytes(origin, encode=self.encode)
        decoded = StringUtil.from_bytes(encoded, encode=self.encode)
        self.assertEqual(origin, decoded)

    def test_regular(self):
        for origin in origins:
            encoded = StringUtil.to_bytes(origin, encode=self.encode)
            decoded = StringUtil.from_bytes(encoded, encode=self.encode)
            self.assertEqual(origin, decoded)

    def test_special(self):
        for origin in special_origins:
            encoded = StringUtil.to_bytes(origin, encode=self.encode)
            decoded = StringUtil.from_bytes(encoded, encode=self.encode)
            self.assertEqual(origin, decoded)


class ToAndFromBytesMatchTestUtf32Str(unittest.TestCase):
    encode = 'utf_32'

    def test_none(self):
        origin = None
        encoded = StringUtil.to_bytes(origin, encode=self.encode)
        decoded = StringUtil.from_bytes(encoded, encode=self.encode)
        self.assertEqual(origin, decoded)

    def test_empty(self):
        origin = ''
        encoded = StringUtil.to_bytes(origin, encode=self.encode)
        decoded = StringUtil.from_bytes(encoded, encode=self.encode)
        self.assertEqual(origin, decoded)

    def test_regular(self):
        for origin in origins:
            encoded = StringUtil.to_bytes(origin, encode=self.encode)
            decoded = StringUtil.from_bytes(encoded, encode=self.encode)
            self.assertEqual(origin, decoded)

    def test_special(self):
        for origin in special_origins:
            encoded = StringUtil.to_bytes(origin, encode=self.encode)
            decoded = StringUtil.from_bytes(encoded, encode=self.encode)
            self.assertEqual(origin, decoded)


class ToBytesTest(unittest.TestCase):
    def test_none(self):
        origin = None
        encoded = StringUtil.to_bytes(origin)
        self.assertEqual(None, encoded)

    def test_empty(self):
        origin = ''
        encoded = StringUtil.to_bytes(origin)
        self.assertEqual(b'', encoded)

    def test_single(self):
        for i in range(128):
            origin = chr(i)
            encoded = StringUtil.to_bytes(origin)
            self.assertEqual(bytes([i]), encoded)

    def test_single_gbk(self):
        encode_type = 'gbk'
        for i in range(128):
            origin = str(chr(i))
            encoded = StringUtil.to_bytes(origin, encode_type)
            self.assertEqual(origin.encode(encode_type), encoded)

    def test_multiple(self):
        encode_type = StandardEncodingsEnum.UTF_8
        origin = ''.join([chr(i) for i in range(128)])
        encoded = StringUtil.to_bytes(origin, encode_type)
        self.assertEqual(b''.join([bytes([i]) for i in range(128)]), encoded)

        origin = '零一二三四五六七八九十百千万亿'
        encoded = StringUtil.to_bytes(origin)
        print(f'origin: {origin}, encoded: {encoded}, encode_type: {encode_type}')

    def test_multiple_gbk(self):
        encode_type = 'gbk'
        origin = ''.join([chr(i) for i in range(128)])
        encoded = StringUtil.to_bytes(origin, encode_type)
        self.assertEqual(b''.join([bytes([i]) for i in range(128)]), encoded)

        origin = '零一二三四五六七八九十百千万亿'
        encoded = StringUtil.to_bytes(origin, encode_type)
        print(f'origin: {origin}, encoded: {encoded}, encode_type: {encode_type}')


class ToCamelTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(StringUtil.to_camel_case(''), '')
        self.assertEqual(StringUtil.to_camel_case(None), None)

    def test_normal(self):
        self.assertEqual(StringUtil.to_camel_case('my_variable_name'), 'myVariableName')
        self.assertEqual(StringUtil.to_camel_case('user_id'), 'userId')
        self.assertEqual(StringUtil.to_camel_case('some_long_variable_name'), 'someLongVariableName')

    def test_no_snake(self):
        self.assertEqual(StringUtil.to_camel_case('a'), 'a')
        self.assertEqual(StringUtil.to_camel_case('aa'), 'aa')
        self.assertEqual(StringUtil.to_camel_case('ab'), 'ab')

    def test_number(self):
        self.assertEqual(StringUtil.to_camel_case('1'), '1')
        self.assertEqual(StringUtil.to_camel_case('1_2'), '12')
        self.assertEqual(StringUtil.to_camel_case('1_2'), '12')
        self.assertEqual(StringUtil.to_camel_case('1_23'), '123')
        self.assertEqual(StringUtil.to_camel_case('1_2_3'), '123')


class ToSnakeTest(unittest.TestCase):
    def test_from_chat_gtp(self):
        # 驼峰格式字符串
        self.assertEqual('my_variable_name', StringUtil.to_snake_case('myVariableName'))
        self.assertEqual('user_id', StringUtil.to_snake_case('userId'))
        self.assertEqual('some_long_variable_name', StringUtil.to_snake_case('someLongVariableName'))
        self.assertEqual('my_variable_name', StringUtil.to_snake_case('MyVariableName'))
        self.assertEqual('my_j_s_o_n_data', StringUtil.to_snake_case('myJSONData'))
        self.assertEqual('my_u_r_l_address', StringUtil.to_snake_case('MyURLAddress'))
        self.assertEqual('my_var_123_name', StringUtil.to_snake_case('myVar_123_Name'))
        self.assertEqual('my__variable__name', StringUtil.to_snake_case('my__variable__name'))
        self.assertEqual('my_variable_name', StringUtil.to_snake_case('my_variable_name'))
        self.assertEqual('character_a', StringUtil.to_snake_case('CharacterA'))

        # None 值
        self.assertIsNone(StringUtil.to_snake_case(None))

        # 空字符串
        self.assertEqual(StringUtil.to_snake_case(''), '')

if __name__ == '__main__':
    unittest.main()
