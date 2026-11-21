# ParaCzech: Lexicon of Czech Paradigms

Citation: Kyjánek, L., & Bonami, O. (2026). ParaCzech v1.0: Lexicon of Czech Paradigms (Version v1.0) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.18262654

Data set developer(s): Lukáš Kyjánek, Olivier Bonami

Data sheet author(s): Lukáš Kyjánek, Olivier Bonami

## Motivation

**For what purpose was the dataset created?**

This dataset was created to facilitate in-depth empirical and quantitative studies of Czech inflectional morphology and morphophonology. It bridges the gap between fragmented existing resources by integrating morphological, morphosyntactic, and frequency information with a newly generated, large-scale phonemic layer into a unified, interoperable framework (the Paralex standard). It is intended for use in linguistics, computational morphophonology, and NLP applications.

**Who created the dataset (for example, which team, research group) and on behalf of which entity (for example, company, institution, organization)?**

- Lukáš Kyjánek, Université Paris Cité: language expertise, dataset creation, data extraction and harmonisation, phonemic transcription generation, annotation interface development, validation of transcription
- Olivier Bonami, Université Paris Cité: dataset design, corrections, methodology, quantitative evaluation

**Who funded the creation of the dataset?** 

The creation of this dataset did not receive any specific grant funding. It was developed as part of Lukáš Kyjánek's doctoral research at Université Paris Cité.

**Any other comments?**

We utilise and build upon data from existing high-quality resources, namely MorfFlexCZ, the SYN v9 corpus, and the DeriNet database. We thank the creators of these resources for making their data openly available.

## Composition

Paralex datasets document paradigms of inflected forms.

The dataset provides an exhaustive inventory of Czech nouns, adjectives, and verbs. Because its core vocabulary originates from training data (MorfFlexCZ) for morphological taggers, the content is remarkably heterogeneous. Alongside the standard codified lexicon, it includes a vast array of peripheral material, such as non-standard colloquialisms, orthographic variants, and common typos.

The relational structure of the tables explicitly tags morphological features, overabundant forms, stylistic labels, and historical remnants (e.g., dual forms). This granular tagging allows users to effortlessly filter out unwanted noise and generate custom subsets. At the item level, each word form is paired with its IPA-compliant phonemic transcription and detailed frequency metrics in a large corpus of Czech (SYN v9).

Finally, to support interoperability with modern vector space models, each record features a unique key -- a concatenation of the orthographic form and its original morphological tag. This identifier enables the immediate mapping of the lexicon's entries to existing distributional semantic representations from the Package of word embeddings of Czech from a large corpus (Kyjánek & Bonami, 2022).

The following subchapters presents descriptions of individual columns included in the tables.

### paraczech_forms.csv

* **`forms_id`**: A unique string identifier for the specific word form record.
* **`orth_form`**: The orthographic representation of the inflected word form.
* **`lexeme`**: A foreign key linking to the `lexeme_id` in the `lexemes.csv` table. It corresponds to the standard citation form (nominative singular for nouns, nominative singular masculine for adjectives, and infinitive for verbs) and is explicitly disambiguated in cases of homonymy or multiple meanings.
* **`phon_form` & `candidate_phon_form`**: The IPA-compliant phonological transcriptions of the `orth_form`. Generated via an automatic rule-based tool and manually validated, these are split into two columns to ensure data transparency. The `phon_form` column contains highly reliable transcriptions for native vocabulary, whereas `candidate_phon_form` stores less reliable transcriptions for candidate borrowings.
* **`cell`**: The specific bundle of morphosyntactic features expressed by the word form. The exact definitions of the utilized feature abbreviations can be found in the `paraczech_feature-values.csv` file.
* **`UCNK`**: The original positional morphological tag used in the Czech National Corpus (CNC) to encode the word form's morphosyntactic properties.
* **`overabundance_tag`**: A tag classifying situations of overabundance—where multiple distinct word forms legitimately occupy the exact same paradigmatic cell. These classifications are derived from the original MorfFlexCZ annotations and are fully documented in `paraczech_tags.csv`.
* **`frequency` & `frequency_per_million`**: The absolute and relative usage frequencies of the given word form, calculated using data from the large-scale SYN v9 corpus.
* **`extracted_exponent`**: The inflectional ending (exponent) of the word form, systematically isolated using regular expressions based on the word's morphosyntactic classification.

### paraczech_lexemes.csv

* **`lexeme_id`**: A unique key that includes explicit disambiguation information. It serves as the primary identifier for the lexeme and links directly to the `lexeme` foreign key in the `forms.csv` table.
* **`label`**: A clean, shortened version of the `lexeme_id`. It is stripped of all technical annotations and disambiguation markers, representing the pure text string of the citation form.
* **`original_techlemma`**: The original format of the lemma as extracted from the MorfFlexCZ database, preserving all original technical and stylistic annotations. Based on the MorfFlexCZ documentation, this string contains a wealth of additional linguistic information that has not yet been harmonised into separate columns.
* **`frequency`**: The aggregated absolute frequency of all token occurrences for the given lexeme, calculated using data from the large-scale SYN v9 corpus.
* **`gender`**: The grammatical gender of nouns and adjectives. For masculine nouns, this column also explicitly specifies animacy.
* **`deverbative_transgressive`**: Indicates the tense (present or past) in which a transgressive (gerund) verb form is realized.
* **`possessor_gender`**: Specifies the grammatical gender of the possessor (masculine or feminine), applicable specifically to possessive adjectives.
* **`aspect`**: The verbal aspect (e.g., perfective, imperfective).
* **`POS`**: The part-of-speech tag identifying the broad grammatical category of the lexeme.
* **`variant_tag`**: A tag classifying the lexeme's position within language stratification (e.g., standard written Czech, dialects, slang). Detailed explanations of these tags are provided in the `paraczech_tags.csv` file.
* **`register_tag`**: A tag indicating specific situational or stylistic usage, identifying words as archaisms (historisms), vulgarities, or colloquialisms. Detailed explanations are provided in `paraczech_tags.csv`.
* **`epistemic_tag`**: A tag indicating whether the lexeme represents a misspelled variant or typo. Detailed explanations are provided in `paraczech_tags.csv`.
* **`indeclinable`**: A boolean value (`True`/`False`) indicating whether the lexeme is indeclinable. This property was systematically inferred by surveying the attested word forms associated with the lexeme within the dataset.
* **`infl_class`**: A prediction of the lexeme's standard inflectional class. This classification was generated using a tool that combined word forms available directly from the source with data from the MorphoDiTa tagger. The assigned classes strictly adhere to the morphological taxonomy introduced by Cvrček et al. 2015. A complete list and notation guide for these classes can be found in `docs/dictionary_of_classes.csv`.
* **`infl_type`**: A broader specification relevant to the lexeme's inflectional behaviour: it indicates the grammatical gender for nouns, the declension type (hard, soft, or possessive) for adjectives, and the verb group/class (1–5) for verbs.

### paraczech_graphemes.csv

* **`grapheme_id`**: The basic character represented in lowercase.
* **`grapheme_upper_case`**: The corresponding uppercase representation of the letter.
* **`canonical_order`**: An integer indicating the standard alphabetical sorting order of the grapheme.

### paraczech_sounds.csv

* **`sound_id`**: The primary identifier of the phoneme (IPA symbol).
* **`label`**: Full phonetic description using standard IPA nomenclature.
* **`syllabic`**: `[+syll]` Functions as a syllable nucleus (vowels and syllabic consonants).
* **`long`**: `[+long]` Phonemic length or duration; distinguishes short and long vowels.
* **`consonantal`**: `[+cons]` Formed with a drastic obstruction in the central vocal tract.
* **`sonorant`**: `[+son]` Produced with a vocal tract configuration that allows air to flow freely, maintaining spontaneous voicing.
* **`continuant`**: `[+cont]` Air is not blocked within the oral cavity (fricatives, vibrants, and vowels).
* **`delayed release`**: `[+del rel]` Distinguishes affricates (slow release of the closure) from plain stops.
* **`approximant`**: `[+approx]` Constriction is not narrow enough to produce turbulent noise (glides and liquids).
* **`trill`**: `[+trill]` Produced by a series of rapid vibrations of the articulator (vibrants like *r* and *ř*).
* **`nasal`**: `[+nas]` Produced with a lowered velum, allowing air to escape through the nasal cavity.
* **`voice`**: `[+voice]` Produced with vocal fold vibration.
* **`labial`**: `[+lab]` Produced with the involvement of the lips.
* **`round`**: `[+round]` Produced with lip rounding (primarily back vowels in Czech).
* **`labiodental`**: `[+lab-dent]` Specifically produced with the lower lip and upper teeth (e.g., *f*, *v*, *ɱ*).
* **`coronal`**: `[+cor]` Produced by raising the tongue blade or tip from its neutral position.
* **`anterior`**: `[+ant]` Produced with a constriction at or in front of the alveolar ridge.
* **`strident`**: `[+strid]` Produced with high-intensity friction noise (sibilants and affricates).
* **`lateral`**: `[+lat]` Produced by lowering the midsection of the tongue, allowing air to flow over the sides (e.g., *l*).
* **`dorsal`**: `[+dors]` Produced by raising the body/back of the tongue.
* **`mid`**: `[+mid]` Distinguishes mid-height vowels (*e*, *o*) from high (*i*, *u*) and low (*a*) vowels.
* **`high`**: `[+high]` Produced with the tongue body raised above the neutral position.
* **`low`**: `[+low]` Produced with the tongue body lowered below the neutral position.
* **`front`**: `[+front]` Produced with the tongue body moved forward from the neutral position.
* **`back`**: `[+back]` Produced with the tongue body moved backward from the neutral position.

### paraczech_cells.csv

* **`cell_id`**: The primary key for the paradigmatic cell, which directly links to the `cell` column in the `paraczech_forms.csv` table.
* **`POS`**: The part-of-speech tag defining the broad grammatical category for the cell.
* **`ud`**: The translation of the cell's morphosyntactic features into the Universal Dependencies (UD) annotation schema.
* **`unimorph`**: The translation of the cell's morphosyntactic features into the UniMorph annotation schema.
* **`frequency`**: The aggregated absolute frequency of all token occurrences falling into this specific paradigmatic cell, calculated using data from the large-scale SYN v9 corpus.

### paraczech_feature-values.csv

* **`value_id`**: The primary key representing the specific value of a morphosyntactic feature (e.g., *prs*, *pst*, *fut*).
* **`label`**: A descriptive label explaining the exact meaning of the given feature value.
* **`feature`**: The broader morphosyntactic category to which this value belongs (e.g., tense, case, number).
* **`POS`**: The part(s) of speech for which this specific feature value is applicable or determined.
* **`ud`**: The translation of the feature value into the Universal Dependencies (UD) annotation schema.
* **`unimorph`**: The translation of the feature value into the UniMorph annotation schema.
* **`canonical_order`**: An integer indicating the standard, conventional sorting order of the values within their respective morphosyntactic category.

### paraczech_tags.csv

* **`tag_id`**: The primary key representing the specific tag used in the dataset (e.g., within the `lexemes.csv` or `forms.csv` tables).
* **`tag_column_name`**: The exact name of the column in the dataset where the corresponding tag is applied.
* **`comment`**: A detailed explanation or description clarifying the exact meaning and context of the given tag.

## Distribution

Due to the exhaustive size and heterogeneity of the lexicon, the dataset release bundle includes a dedicated distribution script (``scripts/paraczech_subset.py``). This tool is designed to help users easily generate manageable, custom subsets tailored to their specific theoretical or analytical needs.

We highly recommend utilising this script to ensure that quantitative analyses are conducted on well-documented, productive lexical material while maintaining optimal computational efficiency.

The script needs Python packages: ``re``, ``argparse``, ``pandas``
You can run the script in the following way (for having subset of words with frequency equal or higher to 50):
```
python3 paraczech_subset.py --input_folder=='../paraczech/' --output_prefix=='subsample' --freq_token==50
```

The current version of the script provides the following parameters (limitation of the dataset):

* ``--freq_token`` [int] Absolute frequency of a word form. Sets the minimum occurrence count for a specific orthographic word form in the corpus. This is used to remove rare or unique word forms.
* ``--freqPM_token`` [float] Relative frequency of a word form (Per Million). A normalized metric defining the minimum density of a word form's occurrence. This allows you to set frequency limits that are independent of the total corpus size.
* ``--freq_type`` [int] Lexeme (Lemma) frequency. The aggregate frequency of all word forms belonging to a specific lemma. This parameter filters the dataset at the level of the lexeme rather than individual grammatical forms.
* ``--freq_cell`` [int] Paradigm cell frequency. The count of occurrences for a specific grammatical category (a single cell in a morphological paradigm). This is useful for filtering out poorly represented grammatical forms where statistical analysis might be unreliable.
* ``--only_nondefective_phonology`` [bool] Filter by phonological quality. When enabled, this parameter excludes word forms with "defective" or ambiguous phonetic transcriptions. Such entries typically represent loanwords or foreign expressions that have not yet undergone full phonological adaptation to the Czech language. Enabling this filter ensures that the dataset contains only standard, fully adapted vocabulary, which is crucial for analyses focused on native or established Czech phonotactics.

After application of the desired parameter(s), each other table is updated with respect to the extracted content, which is the main benefit of the script.

### License

The ParaCzech dataset is provided under a Creative Commons Attribution 4.0 International (CC BY 4.0) license. Users are free to share, adapt, and build upon the material for any purpose, even commercially, as long as appropriate credit is given to the original authors and any changes made to the dataset are clearly indicated.

## Maintenance

The dataset is primarily maintained by its creators. The most transparent and efficient way to reach us is by opening an issue on our GitHub repository. For specific inquiries or potential collaborations, feel free to contact us directly via email.

## References & Acknowledgements

The development of ParaCzech builds upon the foundational work of several major Czech linguistic resources. For a complete list of citations, including the original documentation for the MorfFlexCZ, SYN v9, and DeriNet projects, please refer to the `docs/sources.bib` file included in this repository.

We extend our gratitude to the Institute of the Czech National Corpus (ÚČNK) for providing the frequency data and the MorfFlexCZ and DeriNet development teams for their pioneering work, which remains the cornerstone of modern Czech morphological research.
