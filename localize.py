import json
class Localize:
    lang = "fr"
    strings = {}


    @staticmethod
    def set_lang(lang):
        Localize.lang = lang

    @staticmethod
    def get(text):
        if Localize.lang not in Localize.strings:
            Localize.strings[Localize.lang] = {}

        if text not in Localize.strings[Localize.lang]:
            Localize.strings[Localize.lang][text] = text

        return Localize.strings[Localize.lang][text]

    @staticmethod
    def load():
        with open('localizations.dat') as infile:
            Localize.strings = json.load(infile)

    @staticmethod
    def save():
        with open('localizations.dat', 'w') as outfile:
            json.dump(Localize.strings, outfile, sort_keys=True, indent=4,)

_ = Localize.get