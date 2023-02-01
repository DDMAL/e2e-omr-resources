# Models

The models were generated with the [Training model Patchwise Analysis of Music Document, Training](https://github.com/DDMAL/Calvo_classifier/tree/sample_generator#mode-of-use-for-training-the-model) job included in Rodan, 
using the data provided in the `training_data` folder. This data consists of ZIP files generated using the Pixel job (and with the help of the . These zip files contain the image and the layers necessary to train the model: background layer, layer 1 (for music symbols), layer 2 (for staff lines), layer 3 (for text), and layer 4 (for the selected region). We used a total of seven zip files, these are, seven images with their corresponding layers.

We used the default values of the settings of this training job:
- `maximum number of samples per label = 5,000`
- `maximum number of training epochs = 50`
- `patience (early stop) = 45`
- `patch height = 256`
- `patch width = 256`
- `batch size = 8`

The training was completed in 25 hours.

# Training Data
As indicated in the [End-to-End OMR Documentation - Hints section](http://ddmal.music.mcgill.ca/e2e-omr-documentation/hints.html#staff-size-height-and-training):
> The document-analysis classifier and trainer jobs are sensitive to the size of images. For music with staves, the distance between staff lines in pixels (staff size height) tends to be a predictor of how well it will perform. For instance, with the original CDN-Hsmu M2149.L4 images, the staff size height is 64 px. Values around this point may result in better classification and training results, but note that this is not an optimized measure.

For better classification results, the size of the images used for training data was modified to have a staff size height closer to 64 px. For the [CDN-Mlr MS Medieval 0073](https://cantus.uwaterloo.ca/source/680970) manuscript, this implied to **reduce the original image size by 31%**. This should be kept in mind at the moment of processing the complete manuscript through the OMR workflow. **All images to be processed should be resized by this factor as well (for this manuscript)**. This is done in the _Resize Image_ job at the beginning of the end-to-end OMR workflow (as indicated in [this image](http://ddmal.music.mcgill.ca/e2e-omr-documentation/hints.html#staff-size-height-and-training)).

The folios randomly selected for the training data are: 040, 068, 094, 102, 125, 168, 176, and 270. These were reduced in size according to the previous ratio (0.31) and the set of images were combined into a big file including all nine of them. The same was done to the set of layers generated in Pixel. The combined layers can be found in the `training_data` folder. The combined images can be generated again by retrieving the original images from the IIIF Manifest, reducing their size by 0.31, and combining them into one file (in ascending order—040, 068, 094, 102, 125, 168, 176, and 270) by using Image Magick as indicated in the tutorial section for [Image Layering](http://ddmal.music.mcgill.ca/e2e-omr-documentation/tutorial/document-analysis.html#image-layering).
