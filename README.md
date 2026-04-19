# Czech Paralex Lexicon (CPL)

Paralex is a standard for morphological lexicons which document inflectional paradigms. It is available [here](https://paralex-standard.org/).


## Input resources

- [MorfFlexCZ 2.0](https://ufal.mff.cuni.cz/morfflex)
    - [MorfFlexCZ 2.1](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-5833) is available, but not used
- [SYN v9 corpus](https://wiki.korpus.cz/doku.php/en:cnk:syn:verze9)
    - [SYN v13 corpus](https://wiki.korpus.cz/doku.php/en:cnk:syn:verze13) exists, but v14 will be available
- [DeriNet 2.1](https://ufal.mff.cuni.cz/derinet)
- [Tool for Automatic Classification of Czech Verbs into Classes and Conjugation Groups](https://github.com/lukyjanek/czech-verb-classes)
- [Tool for Automatic phonetic transcription of the Czech, Slovak and Polish languages](https://github.com/lukyjanek/phonetic-transcription)
- [Tool for Recognition of foreign words in the Czech language](https://github.com/lukyjanek/foreign-words-recognition)


## Process of the creation CPL

0.  Downloading input resources (must be done manually)

1.  Extracting pieces of information from the input resources
    - <input type="checkbox" checked> extracting nouns, adjectives, and verbs from MorfFlexCZ
    - <input type="checkbox" checked> extracting frequencies of wordforms from SYN v9
    - <input type="checkbox" checked> extracting links among spelling variants from DeriNet 2.1
    - (?) extracting morphological segmentations from DeriNet 2.1
    - (?) extracting links for derivational morphology from DeriNet 2.1

2. Decomposing original morphological tags into the Leipzig format
    - <input type="checkbox" checked> transcription of individual positions of the original tag (https://www.eva.mpg.de/lingua/pdf/Glossing-Rules.pdf)
    - <input type="checkbox" checked> inferring particular pieces of annotation (e.g., possessivity mark with adjectives)

3. Adding new annotations on the basis of other available resources and tools
    - <input type="checkbox" checked> distinguishing spelling variants (but not included yet)
    - <input type="checkbox" checked> distinguishing native words <em>vs.</em> borrowings
    - <input type="checkbox" checked> distinguishing commonn nouns <em>vs.</em> proper nouns
    - <input type="checkbox" checked> adding phonetic transcriptions
    - <input type="checkbox" checked> adding frequencies
    - <input type="checkbox" checked> adding knowledge from techlemma from MorfFlexCZ
    - <input type="checkbox" > distinguishing noun, adjectival, and verbal classes
    - (?) adding information about being a part of the same derivational family
    - (?) adding information about derivational morphology
    - (?) adding morphological segmentation
    - (?) adding origin of words (like EtymWordNet)

4. Storing resulting data in the Paralax standard format
    - <input type="checkbox" checked> distributing individual pieces of data into particular files
    - <input type="checkbox" checked> linking individual pieces of data using IDs
    - <input type="checkbox" checked> creating relevant metadata

5. Distribution / Publication of dataset; make smaller datasets besides the large one
    - <input type="checkbox" checked> large one: word forms attested in a corpus
    - <input type="checkbox" checked> word forms attested in a corpus with a threshold (50/10 occurrences)
    - <input type="checkbox" checked> all lexemes such that all cells of that lexeme are attested in the corpus (tried but imposible for adj and verbs)
    - <input type="checkbox" checked> summed frequencies of all word forms of a lexeme and check that they are above a threshold; include all word forms including those bellow threshold (50/10 occurrences)

6. Analysing Czech inflectional system on the basis of CPL
    - <input type="checkbox" checked> make simple statistics about the dataset
    - <input type="checkbox" checked> evaluate phonetic transcription
        - small dataset and annotator would evaluate accuracy; correlate transcription of borrowings and native words separately, arr. 500 borrowings and 500 native words (rejection sampling above frequency of words)
        - ideas about phonetic transcription from Sacha and Estonia lexicon
        - https://www.antvaset.com/ipa-to-speech


## Notes and comments during the work on CPL
- spelling variants available only for citation forms of words; what about wordforms (infer from lemmas)?
- morphological segmentation also available only for citation forms of words; what about wordforms (infer from lemmas + inflectional classes)?
- as the size of SYN v9 is 4,719,008,171 tokens without interpunction, the relative frequency (per million) is counted as <strong>the absolute frequency / number of tokens without interpunction × 1,000,000</strong>


- paragraph about affirmation/negation - they are one lexeme
- inflectional classes needds to be from grammar, but it usually do not cover all cases

- nouns, adjectives (tag for possessive adjective), verbs
leipzig format decomposition

- all lemmas from morfflex that are attested in SYN
- those that are not attested in SYN will get frequency to 0

- phonetic transcription by tool, but double check borrowings ("googlovat") - exclude them? but we want reality of Czech... especially nouns and verbs; what about false negatives
- are borrowings with strange/unaddapted orthography (?)
- borrowings maybe without transcription

- proper nouns, personal names, city names included but wihtout phonetic transcription

- overabundace tag Yes, but be carefull about spelling variants