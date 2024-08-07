from pathlib import Path

import attr
import pylexibank
from clldutils.misc import slug


@attr.s
class CustomLanguage(pylexibank.Language):
    Source = attr.ib(default=None)
    Location = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "hsiuhmongmien"
    language_class = CustomLanguage
    form_spec = pylexibank.FormSpec(
        missing_data=[""],
        separators=";,",
        brackets={"(": ")", "[": "]"},
        strip_inside_brackets=True,
        first_form_only=True,
    )

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        # read in data
        data = self.raw_dir.read_csv("HM_official.tsv", dicts=True, delimiter="\t", quotechar='"')
        # add languages
        languages = args.writer.add_languages(lookup_factory="Name")
        sources = {l["Name"]: l["Source"] for l in self.languages}

        # make concept dictionary
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.number + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            concepts[concept.english] = idx
        # create forms
        for cogid_, entry in pylexibank.progressbar(
            enumerate(data), desc="cldfify the data", total=len(data)
        ):
            cogid = cogid_ + 1
            for language, value in languages.items():
                for row in args.writer.add_forms_from_value(
                    Language_ID=value,
                    Local_ID="{0}-{1}".format(cogid, value),
                    Parameter_ID=concepts[entry["Gloss"]],
                    Value=entry[language],
                    Source=sources[language],
                ):
                    args.writer.add_cognate(lexeme=row, Cognateset_ID=cogid)
