import datasets
import pandas as pd
import tiktoken

from .external import flores


def get_dataset(lang: str, lang2: str = None, split: str = "dev"):
    """Get the dataset for the given language(s) and split.

    Args:
        lang (str): The language code.
        lang2 (str): The second language code.
        split (str): The split to use.

    Returns:
        Dataset: The dataset.
    """

    config_name = lang
    if lang2:
        config_name = f"{lang}-{lang2}"

    fl = flores.Flores200(config_name=config_name)
    fl.download_and_prepare()

    return fl.as_dataset(split=split)


def get_data_column(ds: datasets.arrow_dataset.Dataset, lang: str):
    """Get the data column for the given language.

    Args:
        ds (Dataset): The dataset.
        lang (str): The language code.

    Returns:
        List[str]: The data column.
    """

    if lang == "all":
        return [k for l in ds.column_names if l.startswith("sentence_") for k in ds[l]]

    return ds[f"sentence_{lang}"]


def get_tokens(
    ds: datasets.arrow_dataset.Dataset,
    lang: str,
    tokenizer=None,
    model_name: str = None,
):
    if tokenizer:
        assert model_name is None, "Either tokenizer or model_name must be provided"
    else:
        assert model_name, "Either tokenizer or model_name must be provided"
        tokenizer = tiktoken.encoding_for_model(model_name)

    # We can do encode_batch, but I don't think it's necessary.
    return tokenizer.encode_batch(get_data_column(ds, lang))


def get_token_stats(
    ds: datasets.arrow_dataset.Dataset, lang: str, model_name: str = None
):
    """Get token statistics for the given language.

    Args:
        ds (Dataset): The dataset.
        lang (str): The language code.
        model_name (str): The model name.

    Returns:
        Dict: The token statistics.
    """

    tokens_list = get_tokens(ds, lang, model_name=model_name)
    n_tokens = [len(t) for t in tokens_list]
    token_stats = pd.Series(n_tokens).describe()
    token_stats.index = [f"n_tokens_{i}" for i in token_stats.index]

    token_stats = {"lang": lang, "model_name": model_name, **token_stats.to_dict()}

    token_stats["n_tokens"] = n_tokens
    token_stats["str_len"] = list(map(len, get_data_column(ds, lang)))
    token_stats["nbytes"] = list(
        map(lambda s: len(s.encode("utf-8")), get_data_column(ds, lang))
    )

    return token_stats


def compute_premium(input: str, encoding: str = "cl100k_base") -> int:
    """
    Calculate the premium based on the input string and encoding.

    Parameters
    ----------
    input : str
        The input string for which premium needs to be calculated.
    encoding : str, optional
        The encoding method to be used (default is "cl100k_base").

    Returns
    -------
    int
        The premium calculated based on the input string and encoding.

    Notes
    -----
    This function calculates the premium by encoding the input string using the specified encoding
    method and returning the length of the resulting tokens.
    """

    tokens = tiktoken.get_encoding(encoding).encode(input)
    return len(tokens)
