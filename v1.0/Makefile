version_1.0:
	python3 -B main.py \
		--extract_words_from_morfflex==True \
		--create_frequency_list_from_syn==True \
		--extract_spelling_variants_from_derinet==True \
		--add_native_vs_borrowed_word==True \
		--add_common_vs_proper_word==True \
		--add_phonetic_transcription==True \
		--merge_and_sort_words==True \
		--store_data==True \
		--make_distribution==True \
		--add_manual_corrections==True \
		--add_exponents==True \
		--add_inflectional_classes==True \
		--delete_name_type_tag==True \
		--delete_dual_number==True \
		--delete_archaic_verbal_cells==True \
		--delete_nonatested_lexemes==True \
		--label_adj_positive_grade==True \
		--change_form_ids==True \
		--sort_tables==True

validation:
	cp final-paraczech-package/build/paraczech.yml final-paraczech-package/
	paralex meta final-paraczech-package/paraczech.yml
	frictionless validate final-paraczech-package/paraczech.package.json
	paralex validate final-paraczech-package/paraczech.package.json
	rm final-paraczech-package/paraczech.yml
