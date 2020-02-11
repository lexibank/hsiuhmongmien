from pathlib import Path

import attr
from clldutils.misc import slug
from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.forms import FormSpec
from pylexibank.util import progressbar

@attr.s
class CustomLanguage(Language):
    Source = attr.ib(default=None)
    Location = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "hsiuhmongmien"
    language_class = CustomLanguage
    form_spec = FormSpec(
          missing_data=[''],
          separators=";/,",
          brackets={'(': ')', '[': ']'},
          strip_inside_brackets=True,
          first_form_only=True
      )

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        # read in data
        data = self.raw_dir.read_csv("HM_official.tsv",
                dicts=True,
                delimiter="\t",
                quotechar='"')
        # add languages
        languages_dict = {}
        languages = args.writer.add_languages(lookup_factory="Name")
        for lang in self.languages:
            languages_dict[lang['Name']]={'Source': lang['Source'], 'ID': lang['ID']}
        # make concept dictionary
        concepts=args.writer.add_concepts(
            id_factory=lambda c: "%s_%s" % (c.number, slug(c.english)),
            lookup_factory="Name")
        # make forms
        for cogid_, entry in progressbar(
            enumerate(data), desc="cldfify the data", total=len(data)
            ):
            cogid = cogid_ + 1
            for language, value in languages_dict.items():
                for row in args.writer.add_forms_from_value(
                    Language_ID = value['ID'],
                    Parameter_ID = concepts[entry['Gloss']],
                    Value=entry[language].replace(" ", ""),
                    Source=[value['Source']]
                    ):
                    args.writer.add_cognate(
                        lexeme=row,
                        Cognateset_ID=cogid)
