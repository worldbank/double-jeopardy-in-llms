# Double Jeopardy and Climate Impact in the Use of Large Language Models: Socio-economic Disparities and Reduced Utility for Non-English Speakers

This work investigates the socio-economic disparities and reduced utility for non-English speakers in the use of large language models (LLMs). We use the FLORES-200 dataset and Ethnologue to analyze the socio-economic disparities in the use of LLMs. We also use the OpenAI's GPT-4 API to assess the reduced utility of LLMsfor non-English speakers.

<br>
<br>
<p align="center">
<img src="./reports/double-jeopardy-llm.png" style="width:75%"/>
</p>
<p align="center">
<strong>Double Jeopardy and Climate Impact in the Use of Large Language Models: Socio-economic Disparities and Reduced Utility for Non-English Speakers</strong>
<br>
<a href="https://arxiv.org/abs/2410.10665">Paper on ArXiv</a>
</p>
<br>


## Data sources

This section provides an overview of the datasets and APIs used in the paper.

- FLORES-200 and FLORES+: A multilingual dataset covering 100 languages, with 1,000 sentences per language. Used for evaluating translation quality and computing the tokenization premium relative to English.
- Ethnologue: Provides linguistic data, including the number of speakers, geographic distribution, and writing systems. We use Ethnologue to estimate the number of speakers for each language.
- World Development Indicators (WDI): Contains socio-economic data at the country level. Specifically, we use the GDP per capita in current US\$ (NY.GDP.PCAP.CD) and the annual population growth rates (SP.POP.GROW) indicators to compute the population-weighted GDP for each language and for aligning population estimates to 2022 based on historical figures from Ethnologue.
- OpenAI GPT-4 (and Turbo) APIs: Used to assess the reduced utility of LLMs for non-English speakers. We applied back-translation with different prompting methods to generate reference translations for FLORES sentences. The LLM translated non-English sentences into English, with the original English sentences serving as a benchmark for evaluating translation quality.

## Code

This section provides a listing and brief description of the code used in the paper.

- `scripts/`: This folder contains the scripts used to generate the data and analyze the results.
- `notebooks/`: This folder contains the notebooks used to generate the data and analyze the results.
- `reports/`: This folder contains assets for the paper. Currently, it contains the figures generated for the paper.

## Citation

Please cite our paper as follows when referencing this work.

``` bibtex
@misc{solatorio2024doublejeopardyclimateimpact,
      title={Double Jeopardy and Climate Impact in the Use of Large Language Models: Socio-economic Disparities and Reduced Utility for Non-English Speakers},
      author={Aivin V. Solatorio and Gabriel Stefanini Vicente and Holly Krambeck and Olivier Dupriez},
      year={2024},
      eprint={2410.10665},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2410.10665},
}
```

## Code of Conduct

The <span style="color:#3EACAD">template</span> maintains a [Code of Conduct](docs/CODE_OF_CONDUCT.md) to ensure an inclusive and respectful environment for everyone. Please adhere to it in all interactions within our community.

## License

The <span style="color:#3EACAD">template</span> is licensed under the [**Mozilla Public License**](https://www.mozilla.org/en-US/MPL). Remember to replace the [license](LICENSE) if necessary. If open source, [choose an open source license](https://choosealicense.com).

