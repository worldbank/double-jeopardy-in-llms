# Notes

We combine the FLORES200 and the FLORES+ datasets to create a single dataset for this project. Some languages are present in both datasets, so we need to remove the duplicates.

Download the FLORES 200 dataset: https://huggingface.co/datasets/facebook/flores

```
cd data/raw

wget https://tinyurl.com/flores200dataset -O flores200dataset.tar.gz
tar -xvzf flores200dataset.tar.gz
```

Download FLORES+: https://github.com/openlanguagedata/flores/releases/download/v2.0-rc.1/floresp-v2.0-rc.1.zip

Language reference:

- FLORES200: https://github.com/facebookresearch/flores/tree/main/flores200
- FLORES+: https://github.com/openlanguagedata/flores



