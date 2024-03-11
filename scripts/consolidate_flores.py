import shutil
import fire
from pathlib import Path


F200_DIRNAME = "flores200_dataset"
FP_DIRNAME = "floresp-v2.0-rc.1"

# We want to consolidate the FLORES+ and FLORES200 datasets into a single directory.

raw_dir = Path('data/raw/')
processed_dir = Path('data/processed/flores200p_dataset')
processed_dir.mkdir(exist_ok=True, parents=True)


def consolidate(split):
    assert split in ["dev", "devtest"], "Only dev and devtest splits are supported"

    # Load all language codes available
    f200 = raw_dir.glob(f"{F200_DIRNAME}/{split}/*.{split}")
    fp = raw_dir.glob(f"{FP_DIRNAME}/{split}/{split}.*")

    lang_codes = set([f.name.replace(f".{split}", "") for f in f200] + [f.name.replace(f"{split}.", "") for f in fp])

    # We consolidate the two datasets, and use the flores200 convention {lang_code}.{split} for naming the files.
    print(len(lang_codes))

    target_dir = processed_dir / split
    target_dir.mkdir(exist_ok=True, parents=True)

    for lang_code in lang_codes:
        f200_file = raw_dir / F200_DIRNAME / split / f"{lang_code}.{split}"
        fp_file = raw_dir / FP_DIRNAME / split / f"{split}.{lang_code}"

        print(f200_file)

        if f200_file.exists() and fp_file.exists():
            # If both files exist, we use the FLORES+ since it should the be latest.
            print(f"Both files exist for {lang_code}, using FLORES+")
            shutil.copy(fp_file, target_dir / f"{lang_code}.{split}")
        else:
            print(f"File exists for {lang_code}: F200={f200_file.exists()}, FP={fp_file.exists()}")

            source_file = f200_file if f200_file.exists() else fp_file
            shutil.copy(source_file, target_dir / f"{lang_code}.{split}")


    # Save the lang_codes
    with open(processed_dir / f"lang_codes.txt", "w") as f:
        for lang_code in lang_codes:
            f.write(f"{lang_code}\n")

    # Copy the metadata
    shutil.copy(raw_dir / F200_DIRNAME / f"metadata_{split}.tsv", target_dir / f"metadata_{split}.tsv")


if __name__ == "__main__":
    # poetry run python -m scripts.consolidate_flores --split=dev
    fire.Fire(consolidate)
