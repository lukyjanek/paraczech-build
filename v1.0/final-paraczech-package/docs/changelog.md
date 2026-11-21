# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0] - 2026-11

### Added
- **Initial release of the ParaCzech lexicon v1.0.0**, comprising 232,281 lexemes and over 7.9 million word forms across Czech nouns (14 paradigm cells), adjectives (336 cells), and verbs (64 cells).
- Harmonisation of morphological data for Czech nouns, adjectives, and verbs extracted from MorfFlexCZ 2.0 into the relational Paralex standard, including decomposition of MorfFlexCZ techlemmas into human-readable metadata while preserving original identifiers for backward compatibility.
- Integration of absolute and relative frequency metadata (per million words) derived from the SYN v9 corpus at the word form, lexeme, and paradigm cell levels, including reconciliation of tagset discrepancies between SYN v9 and MorfFlexCZ.
- Empirical lexical pruning removing over 15,000 completely unattested lexemes (zero cumulative frequency in SYN v9) while retaining zero-frequency word forms of attested lexemes to preserve complete inflectional paradigms.
- Paradigmatic standardisation: complete exclusion of archaic dual forms across all tables, explicit assignment of the positive degree (`pstg`) to all non-gradable adjectives (with frequency aggregation of merged cells), and sequential re-indexing of form identifiers.
- Generation of an IPA-compliant phonemic layer using a rule-based grapheme-to-phoneme script, accompanied by phonological (`sounds.csv` with distinctive features) and graphemic (`graphemes.csv`) inventories.
- Structural separation of phonemic transcriptions into `phon_form` (native vocabulary; 99.2% accuracy in auditory validation) and `candidate_phon_form` (borrowings; 90.7% accuracy, requiring user caution).
- Incorporation of morphological and morphosyntactic tag mappings to three distinct schemas: Leipzig Glossing Rules, Universal Dependencies (UD), and UniMorph.
- Automatic assignment of inflectional classes and morphological exponents adhering to standard Czech morphological taxonomies (including indeclinable words).
- Distribution scripts (`paraczech_subset.py`) enabling users to dynamically generate custom data subsets using frequency thresholds (token, lexeme, and cell levels), phonological quality filters (`--only_nondefective_phonology`), and register/overabundance criteria.
- Unique keys (concatenation of orthographic form and original MorfFlexCZ tag) for immediate interoperability with existing distributional semantic representations and word embeddings.
- Example analysis scripts reproducing the empirical study on Czech nominal paradigmatic predictability published in *Linguistica Pragensia*.
