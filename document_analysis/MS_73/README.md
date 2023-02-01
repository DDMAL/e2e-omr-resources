# Models

The models were generated with the [Training model Patchwise Analysis of Music Document, Training](https://github.com/DDMAL/Calvo_classifier/tree/sample_generator#mode-of-use-for-training-the-model) job included in Rodan, 
using the data provided in the `training_data` folder. This data consists of ZIP files generated using the Pixel job (and with the help of the . These zip files contain the image and the layers necessary to train the model: background layer, layer 1 (for music symbols), layer 2 (for staff lines), layer 3 (for text), and layer 4 (for the selected region). We used a total of seven zip files, these are, seven images with their corresponding layers.

We used the default values of the settings of this training job:
- `maximum number of samples per label = 5,000` (default is 1,000)
- `maximum number of training epochs = 50` (default value)
- `patience (early stop) = 45` (default is 15)
- `patch height = 256` (default value)
- `patch width = 256` (default value)
- `batch size = 8` (default value)

The training was completed in 25 hours.

# Training Data
As indicated in the [End-to-End OMR Documentation - Hints section](http://ddmal.music.mcgill.ca/e2e-omr-documentation/hints.html#staff-size-height-and-training):
> The document-analysis classifier and trainer jobs are sensitive to the size of images. For music with staves, the distance between staff lines in pixels (staff size height) tends to be a predictor of how well it will perform. For instance, with the original CDN-Hsmu M2149.L4 images, the staff size height is 64 px. Values around this point may result in better classification and training results, but note that this is not an optimized measure.

For better classification results, the size of the images used for training data was modified to have a staff size height closer to 64 px. For the [CDN-Mlr MS Medieval 0073](https://cantus.uwaterloo.ca/source/680970) manuscript, this implied to **reduce the original image size by 31%**. This should be kept in mind at the moment of processing the complete manuscript through the OMR workflow. **All images to be processed should be resized by this factor as well (for this manuscript)**. This is done in the _Resize Image_ job at the beginning of the end-to-end OMR workflow (as indicated in [this image](http://ddmal.music.mcgill.ca/e2e-omr-documentation/hints.html#staff-size-height-and-training)).

The folios randomly selected for the training data are: 040, 068, 094, 102, 125, 168, 176, and 270. These were reduced in size according to the previous ratio (0.31) and the set of images were combined into a big file including all nine of them. The same was done to the set of layers generated in Pixel. The combined layers can be found in the `training_data` folder. The combined images can be generated again by retrieving the original images from the IIIF Manifest, reducing their size by 0.31, and combining them into one file (in ascending order—040, 068, 094, 102, 125, 168, 176, and 270) by using Image Magick as indicated in the tutorial section for [Image Layering](http://ddmal.music.mcgill.ca/e2e-omr-documentation/tutorial/document-analysis.html#image-layering).

# Important Notes

We modified two settings of the training job from their default value:
- `patience`
- `maximum number of samples per label`

The reasons for this are the following:
- Regarding **patience**:

    For the Paco's method (`Training model Patchwise Analysis of Music Document, Training` job), the default value of the `patience` is 15, while the default  of the `maximum number of epochs` is 50. This means that, for each layer, the model for pixel classification for that layer will be trained for up to 50 epochs or until the performance of the model (the validation accuracy) hasn't improved after 15 consecutive epochs, what happens first.
    
    By incrementing the patience to 45, we are almost guaranteeing that the models for each layer will be trained for 50 epochs. The reason why we wanted them to be trained for so long, is to guarantee that all models have a very good (almost perfect) validation accuracy.
    
    We have seen that validation accuracies greater or equal to `0.98` are necessary to have models that will perform very well when asked to classify the pixels of a new page. You can see the following lines in the [log file](./Training%20model%20for%20Patchwise%20Analysis%20of%20Music%20Document%2C%20Training%20-%20Log%20File.txt) the validation accuracy for each layer:
    - Background: 0.99636
    https://github.com/DDMAL/e2e-omr-resources/blob/e9703c586229db141151f2fe6850e1269ed3097f/document_analysis/MS_73/models/Training%20model%20for%20Patchwise%20Analysis%20of%20Music%20Document%2C%20Training%20-%20Log%20File.txt#L164
    - Layer 1 (music symbols): 0.99735
    https://github.com/DDMAL/e2e-omr-resources/blob/e9703c586229db141151f2fe6850e1269ed3097f/document_analysis/MS_73/models/Training%20model%20for%20Patchwise%20Analysis%20of%20Music%20Document%2C%20Training%20-%20Log%20File.txt#L325
    - Layer 2 (staff lines): 0.99443
    https://github.com/DDMAL/e2e-omr-resources/blob/e9703c586229db141151f2fe6850e1269ed3097f/document_analysis/MS_73/models/Training%20model%20for%20Patchwise%20Analysis%20of%20Music%20Document%2C%20Training%20-%20Log%20File.txt#L486
    - Layer 3 (text): 0.99940
    https://github.com/DDMAL/e2e-omr-resources/blob/e9703c586229db141151f2fe6850e1269ed3097f/document_analysis/MS_73/models/Training%20model%20for%20Patchwise%20Analysis%20of%20Music%20Document%2C%20Training%20-%20Log%20File.txt#L647
    
    With a lower value like 15 for the patience (and the maximum number of epochs being 50), some layers could have models trained until the 50 epoch while other layers' models are trained until the 15 epoch. These variation in the number of epochs for which the models are trained, end up with a high discrepancy in validation accuracy and, therefore, performance during classification. Forcing the models of all layers to be trained for the maximum number of epochs helps avoid this issue. **Important observation about validation accuracy:** It is important for all models to have their value around 0.98 or higher. If one model has a validation accuracy of 0.92 and the others are way higher, then when classifying a new page, the layer belonging to the model of the 0.92 validation accuracy will be completely empty.
    
- Regarding **maximum number of samples per label**:
The default value of the setting works very good in general. For the `MS_73`, where there was a lot of degradation (especially on text and notes), incrementing this setting proved to be useful.
