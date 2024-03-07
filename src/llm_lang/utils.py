import tiktoken
from .external import flores


def get_dataset(lang, lang2=None, split="dev"):
    config_name = lang
    if lang2:
        config_name = f"{lang}-{lang2}"

    fl = flores.Flores200(config_name=config_name)
    fl.download_and_prepare()

    return fl.as_dataset(split=split)


def get_tokens(ds, lang, tokenizer=None, model_name=None):
    if tokenizer:
        assert model_name is None, "Either tokenizer or model_name must be provided"
    else:
        assert model_name, "Either tokenizer or model_name must be provided"
        tokenizer = tiktoken.encoding_for_model(model_name)

    # We can do encode_batch, but I don't think it's necessary.
    return tokenizer.encode(ds[f"sentence_{lang}"])
