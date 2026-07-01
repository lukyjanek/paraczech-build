# Changelog

All notable changes to this project will be documented in this file.

## [1.0] - 2026-07

### Added
- **Initial release of the ParaCzech lexicon v1.0**
- Harmonisation of morphological data for Czech nouns, adjectives, and verbs extracted from MorfFlexCZ 2.0 into the relational Paralex standard.
- Integration of absolute and relative frequency metadata (per million words) derived from the SYN v9 corpus at the word form, lexeme, and paradigm cell levels.
- Generation of an IPA-compliant phonemic layer using a rule-based grapheme-to-phoneme script.
- Structural separation of phonemic transcriptions into `phon_form` (highly reliable transcriptions of native words) and `candidate_phon_form` (transcriptions of borrowings requiring user caution).
- Incorporation of morphological and morphosyntactic tag mappings to three distinct schemas: Leipzig Glossing Rules, Universal Dependencies (UD), and UniMorph.
- Automatic assignment of inflectional classes and morphological exponents adhering to standard Czech morphological taxonomies.
- Distribution scripts enabling users to dynamically generate custom data subsets.
- Unique keys (concatenation of orthographic form and morphological tag) for immediate interoperability with existing distributional semantic representations and word embeddings.
