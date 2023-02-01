# e2e-omr-resources

For running an end-to-end OMR workflow, you need the resources indicated in the [end-to-end OMR documentation](http://ddmal.music.mcgill.ca/e2e-omr-documentation/#digital-resources). In this repository you can find these resources, some are applicable to different manuscripts, while others are manuscript-specific:

-	The *document analysis* or *document segmentation* models. These models are used to segment the image of a manuscript page into different layers (e.g., music symbol layer, staff-line layer, text, and background layer). The models are trained to identify the pixels belonging to a particular layer. 

  Currently, for this step, we use the jobs of [Pixel](https://ddmal.music.mcgill.ca/e2e-omr-documentation/overview/document-analysis.html#pixeljs), [Background Removal](https://ddmal.music.mcgill.ca/e2e-omr-documentation/overview/document-analysis.html#background-removal), [Paco Trainer](https://ddmal.music.mcgill.ca/e2e-omr-documentation/overview/document-analysis.html#paco-trainer), and [Paco Classifier](https://ddmal.music.mcgill.ca/e2e-omr-documentation/overview/document-analysis.html#paco-classifier). The first two jobs allow to prepare the training data, the Paco trainer allows to train the models with this data, and the Paco Classifier can then use these models to segment a new page into the corresponding layers.

  You can find the training data by going into the `document_analysis` folder, selecting a manuscript, and then go into `training_data` (e.g., `document_analysis/MS_73/training_data/`. You can also consult the parameters and jobs used for generating the models in the README of the particular manuscript (e.g., go to `document_analysis/MS_73/` and consult the README). Finally, you can use the models trained for a particular manuscript by looking into the `models` folder (e.g., go to `document_analysis/MS_73/models/`).

  Some of the manuscripts were trained with an old method (Calvo's Method), which required a single file per layer (see [Archived - Document Analysis Tutorial](https://ddmal.music.mcgill.ca/e2e-omr-documentation/tutorial/document-analysis.html)), and they also were trained with fewer layers (i.e., music symbols, staff lines, and background layers, with the latter including the text as well). These manuscripts were [Salzinnes Antiphonal](./document_analysis/Salzinnes) and [Einsideln](./document_analysis/Einsiedeln).

  **The `MS_73` manuscript shows the current way of training,** using the Paco's method for iterative training (see [documentation](https://ddmal.music.mcgill.ca/e2e-omr-documentation/tutorial/iterative-training.html)). In this method, we train with ZIP Pixel files, each containing the image and layers corresponding to one page. The workflows used to label the data of a page as belonging to the different layers, train the models, and classify a new page can be consulted in the [document analysis](./document_analysis) folder. For `MS_73` we use the four layers corresponding to the music symbols, staff lines, text, and background.


-	For processing the music symbol layer and successfully identify the individual symbols, you also need two files to provide to the interactive (or non-interactive) classifier:
    -	the *training data* for classifying music symbols: `music_symbol_recognition/split_training.xml`
    -	the *feature selection/weights* to optimize such classification process: `music_symbol_recognition/split_features.xml`

-	For the processing of the text (extracted from the background layer), you need two files:
    - the *OCR model*: `text_alignment/salzinnes_model-00054500.pyrnn`
    - the actual *transcript text* for each page of the manuscript. The text can be obtained from the Cantus Database. See [instructions](http://ddmal.music.mcgill.ca/e2e-omr-documentation/tutorial/music-reconstruction.html#text-alignment) on how to retrieve a CSV file including the text of the complete manuscript, and how to identify the rows in the file that relate to the text in a particular page. You can find the extracted texts for Salzinnes in `text_alignment/Salzinnes/`, and the python script used to retrieve these text files in `text_alignment/get_text_per_folio.py`

-	Finally, to encode everything together in an MEI file, you also need to provide a *CSV file mapping* the classes of glyphs to fragments of MEI code. This file can be obtained through CRES. For square neume notation, you could use one of the two files provided: the `mei_encoding/csv-square_notation_neume_component_level.csv` file if the classifier is splitting all neumes into puncta, or the `mei_encoding/csv-square_notation_neume_level.csv` file it the classifier is considering basic neumes (specifically the clivis, the podatus, the torculus, and the scandicus) as complete glyphs.
