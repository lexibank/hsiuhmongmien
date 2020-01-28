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

#    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
#        return super().cldf_specs()

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        # read in data
        data = self.raw_dir.read_csv("HM_official.tsv",
                dicts=True,
                delimiter="\t",
                quotechar='"')
        # add languages
        languages = {}
        for lang in self.languages:
            args.writer.add_languages(lookup_factory="Name")
            # args.writer.add_language(
            #      ID = lang['ID'],
            #      Name = lang['Name'],
            #      Family = lang['Family'],
            #      Glottocode = lang['Glottocode'],
            #      Latitude = lang['Latitude'],
            #      Longitude = lang['Longitude']
            #  )
            languages[lang['Name']]={'Source': lang['Source'], 'ID': lang['ID']}
        # make concept dictionary
        concepts = {}
        for concept in self.concepts:
            idx = concept['ID']+'_'+slug(concept['GLOSS'])
            args.writer.add_concept(
                ID=idx,
                Name=concept['GLOSS'],
                Concepticon_ID=concept['CONCEPTICON_ID'],
                Concepticon_Gloss=concept['CONCEPTICON_GLOSS'])
            concepts[concept['GLOSS']]=idx
        # create forms
        for cogid_, entry in progressbar(
            enumerate(data), desc="cldfify the data", total=len(data)
            ):
            cogid = cogid_ + 1
            for language, value in languages.items():
                for row in args.writer.add_forms_from_value(
                    Language_ID = value['ID'],
                    Parameter_ID=concepts[entry['Gloss']],
                    Value=entry[language],
                    Source=[value['Source']]
                    ):
                    args.writer.add_cognate(
                        lexeme=row,
                        Cognateset_ID=cogid)
