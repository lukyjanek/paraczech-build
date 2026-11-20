# ParaCzech: Dataset Builder & Research Code

Welcome to the official repository for **ParaCzech**, a large-scale, interoperable, and phonologically explicit lexicon of contemporary Czech inflectional paradigms. 

This repository serves a dual purpose:
1. **Dataset Construction:** It contains the scripts and pipeline used to build, harmonise, and subset the ParaCzech dataset from its source resources.
2. **Research Reproducibility:** It provides the codebase for the quantitative morphological experiments featured in our research article published in *Linguistica Pragensia* (Kyjánek & Bonami, 2027).

## 📖 About ParaCzech
ParaCzech integrates morphological, morphosyntactic, and frequency data from major Czech resources (MorfFlexCZ, SYN v9, DeriNet) into the cross-linguistically interoperable **Paralex** standard. A distinctive contribution of this dataset is the inclusion of a large-scale, automatically generated, and manually validated phonemic layer.

*You can download the compiled dataset directly from [Zenodo](https://doi.org/10.5281/zenodo.18262654).*

### How to cite
Kyjánek, L., & Bonami, O. (2026). ParaCzech v1.0: Lexicon of Czech Paradigms (Version v1.0) [Dataset]. Zenodo. [https://doi.org/10.5281/zenodo.18262654](https://doi.org/10.5281/zenodo.18262654).


## 🗂️ Repository Structure

```text
├── v1.0/                            # Code for building the dataset
├── experimental-research/           # Code accompanying experiments with data
│   └── 2027-linguistica-pragensia/  # Linguistica Pragensia article (2027)
└── README.md             
```

## 📄 License

* **Dataset:** The ParaCzech dataset is provided under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.
* **Code:** The scripts and research codebase in this repository are licensed under the MIT License. See the `LICENSE` file for more details.

## 📬 Contact & Contributions

We explicitly invite the broader research community to use, refine, and augment the ParaCzech dataset. If you have questions, spot inconsistencies, or want to contribute new annotation layers (e.g., morphological segmentation, etymology), please open an issue or submit a pull request!
