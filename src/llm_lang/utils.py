import pandas as pd
import tiktoken
from .external import flores


def get_dataset(lang, lang2=None, split="dev"):
    config_name = lang
    if lang2:
        config_name = f"{lang}-{lang2}"

    fl = flores.Flores200(config_name=config_name)
    fl.download_and_prepare()

    return fl.as_dataset(split=split)


def get_data_column(ds, lang):
    return ds[f"sentence_{lang}"]


def get_tokens(ds, lang, tokenizer=None, model_name=None):
    if tokenizer:
        assert model_name is None, "Either tokenizer or model_name must be provided"
    else:
        assert model_name, "Either tokenizer or model_name must be provided"
        tokenizer = tiktoken.encoding_for_model(model_name)

    # We can do encode_batch, but I don't think it's necessary.
    return tokenizer.encode_batch(get_data_column(ds, lang))


def get_token_stats(ds, lang: str, model_name: str = None):
    tokens_list = get_tokens(ds, lang, model_name=model_name)
    n_tokens = [len(t) for t in tokens_list]
    token_stats = pd.Series(n_tokens).describe()
    token_stats.index = [f"n_tokens_{i}" for i in token_stats.index]

    token_stats = {
        "lang": lang,
        "model_name": model_name,
        **token_stats.to_dict()}

    token_stats["n_tokens"] = n_tokens
    token_stats["str_len"] = list(map(len, get_data_column(ds, lang)))
    token_stats["nbytes"] = list(map(lambda s: len(s.encode("utf-8")), get_data_column(ds, lang)))

    return token_stats
