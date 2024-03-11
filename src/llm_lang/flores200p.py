# coding=utf-8
# source=https://huggingface.co/datasets/facebook/flores/blob/751d24d88b0d7d90ec0b533a52965050f694eae0/flores.py
"""NOTE: (MODIFIED) The FLORES-200 Evaluation Benchmark for Low-Resource and Multilingual Machine Translation"""

import os
import sys
import datasets

from typing import Union, List, Optional

# Usage
# fl = flores200p.Flores200P(config_name="eng_Latn-fil_Latn", base_path="data/processed")
# fl.download_and_prepare()
# ds = fl.as_dataset(split="dev")


_CITATION = """
@article{nllb2022,
  author    = {NLLB Team, Marta R. Costa-jussà, James Cross, Onur Çelebi, Maha Elbayad, Kenneth Heafield, Kevin Heffernan, Elahe Kalbassi,  Janice Lam, Daniel Licht, Jean Maillard, Anna Sun, Skyler Wang, Guillaume Wenzek, Al Youngblood, Bapi Akula, Loic Barrault, Gabriel Mejia Gonzalez, Prangthip Hansanti, John Hoffman, Semarley Jarrett, Kaushik Ram Sadagopan, Dirk Rowe, Shannon Spruit, Chau Tran, Pierre Andrews, Necip Fazil Ayan, Shruti Bhosale, Sergey Edunov, Angela Fan, Cynthia Gao, Vedanuj Goswami, Francisco Guzmán, Philipp Koehn, Alexandre Mourachko, Christophe Ropers, Safiyyah Saleem, Holger Schwenk, Jeff Wang},
  title     = {No Language Left Behind: Scaling Human-Centered Machine Translation},
  year      = {2022}
}

@inproceedings{,
  title={The FLORES-101  Evaluation Benchmark for Low-Resource and Multilingual Machine Translation},
  author={Goyal, Naman and Gao, Cynthia and Chaudhary, Vishrav and Chen, Peng-Jen and Wenzek, Guillaume and Ju, Da and Krishnan, Sanjana and Ranzato, Marc'Aurelio and Guzm\'{a}n, Francisco and Fan, Angela},
  year={2021}
}

@inproceedings{,
  title={Two New Evaluation Datasets for Low-Resource Machine Translation: Nepali-English and Sinhala-English},
  author={Guzm\'{a}n, Francisco and Chen, Peng-Jen and Ott, Myle and Pino, Juan and Lample, Guillaume and Koehn, Philipp and Chaudhary, Vishrav and Ranzato, Marc'Aurelio},
  journal={arXiv preprint arXiv:1902.01382},
  year={2019}
}
"""

_DESCRIPTION = """\
The creation of FLORES-200 doubles the existing language coverage of FLORES-101.
Given the nature of the new languages, which have less standardization and require
more specialized professional translations, the verification process became more complex.
This required modifications to the translation workflow. FLORES-200 has several languages
which were not translated from English. Specifically, several languages were translated
from Spanish, French, Russian and Modern Standard Arabic. Moreover, FLORES-200 also
includes two script alternatives for four languages. FLORES-200 consists of translations
from 842 distinct web articles, totaling 3001 sentences. These sentences are divided
into three splits: dev, devtest, and test (hidden). On average, sentences are approximately
21 words long.
"""

_HOMEPAGE = "https://github.com/facebookresearch/flores"

_LICENSE = "CC-BY-SA-4.0"

# pprint.pprint(codes, width=120, compact=True)
_LANGUAGES = [
    'ace_Arab', 'ace_Latn', 'acm_Arab', 'acq_Arab', 'aeb_Arab', 'afr_Latn', 'ajp_Arab', 'aka_Latn', 'als_Latn', 'amh_Ethi',
    'apc_Arab', 'arb_Arab', 'arb_Latn', 'ars_Arab', 'ary_Arab', 'arz_Arab', 'asm_Beng', 'ast_Latn', 'awa_Deva', 'ayr_Latn',
    'azb_Arab', 'azj_Latn', 'bak_Cyrl', 'bam_Latn', 'ban_Latn', 'bel_Cyrl', 'bem_Latn', 'ben_Beng', 'bho_Deva', 'bjn_Arab',
    'bjn_Latn', 'bod_Tibt', 'bos_Latn', 'bug_Latn', 'bul_Cyrl', 'cat_Latn', 'ceb_Latn', 'ces_Latn',
    'cjk_Latn', 'ckb_Arab', 'cmn_Hans', 'cmn_Hant', 'crh_Latn', 'cym_Latn', 'dan_Latn', 'deu_Latn', 'dik_Latn',
    'dyu_Latn', 'dzo_Tibt', 'ell_Grek', 'eng_Latn', 'epo_Latn', 'est_Latn', 'eus_Latn', 'ewe_Latn', 'fao_Latn', 'fij_Latn',
    'fil_Latn', 'fin_Latn', 'fon_Latn', 'fra_Latn', 'fur_Latn', 'fuv_Latn', 'gaz_Latn', 'gla_Latn', 'gle_Latn', 'glg_Latn',
    'grn_Latn', 'guj_Gujr', 'hat_Latn', 'hau_Latn', 'heb_Hebr', 'hin_Deva', 'hne_Deva', 'hrv_Latn', 'hun_Latn',
    'hye_Armn', 'ibo_Latn', 'ilo_Latn', 'ind_Latn', 'isl_Latn', 'ita_Latn', 'jav_Latn', 'jpn_Jpan', 'kab_Latn', 'kac_Latn',
    'kam_Latn', 'kan_Knda', 'kas_Arab', 'kas_Deva', 'kat_Geor', 'kaz_Cyrl', 'kbp_Latn', 'kea_Latn', 'khk_Cyrl', 'khm_Khmr',
    'kik_Latn', 'kin_Latn', 'kir_Cyrl', 'kmb_Latn', 'kmr_Latn', 'knc_Arab', 'knc_Latn', 'kon_Latn', 'kor_Hang', 'lao_Laoo',
    'lij_Latn', 'lim_Latn', 'lin_Latn', 'lit_Latn', 'lmo_Latn', 'ltg_Latn', 'ltz_Latn', 'lua_Latn', 'lug_Latn', 'luo_Latn',
    'lus_Latn', 'lvs_Latn', 'mag_Deva', 'mai_Deva', 'mal_Mlym', 'mar_Deva', 'min_Arab', 'min_Latn', 'mkd_Cyrl',
    'mlt_Latn', 'mni_Beng', 'mos_Latn', 'mri_Latn', 'mya_Mymr', 'nld_Latn', 'nno_Latn', 'nob_Latn', 'npi_Deva',
    'nqo_Nkoo', 'nso_Latn', 'nus_Latn', 'nya_Latn', 'oci_Latn', 'ory_Orya', 'pag_Latn', 'pan_Guru', 'pap_Latn', 'pbt_Arab',
    'pes_Arab', 'plt_Latn', 'pol_Latn', 'por_Latn', 'prs_Arab', 'quy_Latn', 'ron_Latn', 'run_Latn', 'rus_Cyrl', 'sag_Latn',
    'san_Deva', 'sat_Olck', 'scn_Latn', 'shn_Mymr', 'sin_Sinh', 'slk_Latn', 'slv_Latn', 'smo_Latn', 'sna_Latn', 'snd_Arab',
    'som_Latn', 'sot_Latn', 'spa_Latn', 'srd_Latn', 'srp_Cyrl', 'ssw_Latn', 'sun_Latn', 'swe_Latn', 'swh_Latn',
    'szl_Latn', 'tam_Taml', 'taq_Latn', 'taq_Tfng', 'tat_Cyrl', 'tel_Telu', 'tgk_Cyrl', 'tgl_Latn', 'tha_Thai', 'tir_Ethi',
    'tpi_Latn', 'tsn_Latn', 'tso_Latn', 'tuk_Latn', 'tum_Latn', 'tur_Latn', 'twi_Latn', 'tzm_Tfng', 'uig_Arab', 'ukr_Cyrl',
    'umb_Latn', 'urd_Arab', 'uzn_Latn', 'vec_Latn', 'vie_Latn', 'war_Latn', 'wol_Latn', 'xho_Latn', 'ydd_Hebr', 'yor_Latn',
    'yue_Hant', 'zgh_Tfng', 'zho_Hans', 'zho_Hant', 'zsm_Latn', 'zul_Latn'
]

_SPLITS = ["dev", "devtest"]

_SENTENCES_PATHS = {
    lang: {
        split: os.path.join("flores200p_dataset", split, f"{lang}.{split}")
        for split in _SPLITS
    } for lang in _LANGUAGES
}

_METADATA_PATHS = {
    split: os.path.join("flores200p_dataset", f"metadata_{split}.tsv")
    for split in _SPLITS
}

from itertools import permutations

def _pairings(iterable, r=2):
    previous = tuple()
    for p in permutations(sorted(iterable), r):
        if p > previous:
            previous = p
            yield p


class Flores200PConfig(datasets.BuilderConfig):
    """BuilderConfig for the FLORES-200P dataset."""
    def __init__(self, lang: str, lang2: str = None, **kwargs):
        """
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(version=datasets.Version("1.0.0"), **kwargs)
        self.lang = lang
        self.lang2 = lang2


class Flores200P(datasets.GeneratorBasedBuilder):
    """FLORES-200P dataset."""

    BUILDER_CONFIGS = [
        Flores200PConfig(
            name=lang,
            description=f"FLORES-200P: {lang} subset.",
            lang=lang
        )
        for lang in _LANGUAGES
    ] +  [
        Flores200PConfig(
            name="all",
            description=f"FLORES-200P: all language pairs",
            lang=None
        )
    ] +  [
        Flores200PConfig(
            name=f"{l1}-{l2}",
            description=f"FLORES-200P: {l1}-{l2} aligned subset.",
            lang=l1,
            lang2=l2
        ) for (l1,l2) in _pairings(_LANGUAGES)
    ]

    def _info(self):
        features = {
            "id": datasets.Value("int32"),
            "URL": datasets.Value("string"),
            "domain": datasets.Value("string"),
            "topic": datasets.Value("string"),
            "has_image": datasets.Value("int32"),
            "has_hyperlink": datasets.Value("int32")
        }
        if self.config.name != "all" and "-" not in self.config.name:
            features["sentence"] = datasets.Value("string")
        elif "-" in self.config.name:
            for lang in [self.config.lang, self.config.lang2]:
                features[f"sentence_{lang}"] = datasets.Value("string")
        else:
            for lang in _LANGUAGES:
                features[f"sentence_{lang}"] = datasets.Value("string")
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = self.base_path

        def _get_sentence_paths(split):
            if isinstance(self.config.lang, str) and isinstance(self.config.lang2, str):
                sentence_paths = [os.path.join(dl_dir, _SENTENCES_PATHS[lang][split]) for lang in (self.config.lang, self.config.lang2)]
            elif isinstance(self.config.lang, str):
                sentence_paths = os.path.join(dl_dir, _SENTENCES_PATHS[self.config.lang][split])
            else:
                sentence_paths = [os.path.join(dl_dir, _SENTENCES_PATHS[lang][split]) for lang in _LANGUAGES]
            return sentence_paths
        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={
                    "sentence_paths": _get_sentence_paths(split),
                    "metadata_path": os.path.join(dl_dir, _METADATA_PATHS[split]),
                }
            ) for split in _SPLITS
        ]

    def _generate_examples(self, sentence_paths: Union[str, List[str]], metadata_path: str, langs: Optional[List[str]] = None):
        """Yields examples as (key, example) tuples."""
        if isinstance(sentence_paths, str):
            with open(sentence_paths, "r") as sentences_file:
                with open(metadata_path, "r") as metadata_file:
                    metadata_lines = [l.strip() for l in metadata_file.readlines()[1:]]
                    for id_, (sentence, metadata) in enumerate(
                        zip(sentences_file, metadata_lines)
                    ):
                        sentence = sentence.strip()
                        metadata = metadata.split("\t")
                        yield id_, {
                            "id": id_ + 1,
                            "sentence": sentence,
                            "URL": metadata[0],
                            "domain": metadata[1],
                            "topic": metadata[2],
                            "has_image": 1 if metadata == "yes" else 0,
                            "has_hyperlink": 1 if metadata == "yes" else 0
                        }
        else:
            sentences = {}
            if len(sentence_paths) == len(_LANGUAGES):
                langs = _LANGUAGES
            else:
                langs = [self.config.lang, self.config.lang2]
            for path, lang in zip(sentence_paths, langs):
                with open(path, "r") as sent_file:
                    sentences[lang] = [l.strip() for l in sent_file.readlines()]
            with open(metadata_path, "r") as metadata_file:
                metadata_lines = [l.strip() for l in metadata_file.readlines()[1:]]
            for id_, metadata in enumerate(metadata_lines):
                metadata = metadata.split("\t")
                yield id_, {
                    **{
                        "id": id_ + 1,
                        "URL": metadata[0],
                        "domain": metadata[1],
                        "topic": metadata[2],
                        "has_image": 1 if metadata == "yes" else 0,
                        "has_hyperlink": 1 if metadata == "yes" else 0
                    }, **{
                        f"sentence_{lang}": sentences[lang][id_]
                        for lang in langs
                    }
                }
