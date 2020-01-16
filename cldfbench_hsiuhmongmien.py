from collections import OrderedDict
from pathlib import Path

import attr
from clldutils.misc import slug
from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as MyDataset
from pylexibank.forms import FormSpec
from pylexibank.util import progressbar

@attr.s
class CustomConcept(Concept):
    Gloss_in_Source = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    Family = attr.ib(default="Hmong-Mien")
    DataSource = attr.ib(default=None)
    Name_in_Source = attr.ib(default=None)
    Location = attr.ib(default=None)


class Dataset(MyDataset):
    dir = Path(__file__).parent
    id = "hsiuhmongmien"
    language_class = CustomLanguage
    concept_class = CustomConcept
    form_spec = FormSpec(
        missing_data=[''],
        separators=";/,",
        first_form_only=True
    )

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return super().cldf_specs()

    def cmd_download(self, args):
        """
        Download files to the raw/ directory. You can use helpers methods of `self.raw_dir`, e.g.

        >>> self.raw_dir.download(url, fname)
        """
        pass

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        # read in data
        data = self.raw_dir.read_csv("HM_merged.tsv",
                dicts=True,
                delimiter="\t")
        # add languages
        languages = args.writer.add_languages(
                lookup_factory='Name')
        # make concept dictionary
        concepts = {}
        for concept in self.concepts:
            idx = concept['ID']+'_'+slug(concept['GLOSS'])
            args.writer.add_concept(
                ID=idx,
                Name=concept['GLOSS'])
            concepts[concept['GLOSS']]=idx
        # create forms
        for cogid_, entry in progressbar(
            enumerate(data), desc="cldfify the data", total=len(data)
            ):
            cogid = cogid_ + 1
            #print(entry)
            for language in languages:
                for row in args.writer.add_forms_from_value(
                    Language_ID=languages[language],
                    Parameter_ID=concepts[entry['Gloss']],
                    Value=entry[language],
                    Source=["Hsiu2015"]
                ):
                    args.writer.add_cognate(
                        lexeme=row,
                        Cognateset_ID=cogid)
