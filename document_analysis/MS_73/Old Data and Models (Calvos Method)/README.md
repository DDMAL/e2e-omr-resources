# Models

The models were generated with [Calvo's Method](https://github.com/DDMAL/Calvo_classifier/tree/sample_generator#mode-of-use-for-training-the-model) (outside of Rodan), using the images provided in the `training_data` folder. For processing a music document with staff lines and text,
only three models are necessary: one for music symbols, one for staff lines, and one for background (which will include the text).

We used the default values of the settings of this training job:
- `maximum number of samples per label = 15,000`
- `epochs = 20`
- `early stop = 10`
- `patch height = 256`
- `patch width = 256`
- `batch size = 16`
- We used `150 GB` for the memory.
You should try to use the least amount of memory that allows the job to finish. Normally, you won't need more than `150 GB` of memory for procesing a maximum of `15k samples` per layer for `3 layers`. We still need to experiment to find out the minimum amount of memory needed.
- The training was completed in less than `4 hours`, so the default setting of `6 hours` is fine.

# Training Data
As indicated in the [End-to-End OMR Documentation - Hints section](http://ddmal.music.mcgill.ca/e2e-omr-documentation/hints.html#staff-size-height-and-training):
> The document-analysis classifier and trainer jobs are sensitive to the size of images. For music with staves, the distance between staff lines in pixels (staff size height) tends to be a predictor of how well it will perform. For instance, with the original CDN-Hsmu M2149.L4 images, the staff size height is 64 px. Values around this point may result in better classification and training results, but note that this is not an optimized measure.

For better classification results, the size of the images used for training data was modified to have a staff size height closer to 64 px. For the [CDN-Mlr MS Medieval 0073](https://cantus.uwaterloo.ca/source/680970) manuscript, this implied to **reduce the original image size by 31%**. This should be kept in mind at the moment of processing the complete manuscript through the OMR workflow. **All images to be processed should be resized by this factor as well (for this manuscript)**. This is done in the _Resize Image_ job at the beginning of the end-to-end OMR workflow (as indicated in [this image](http://ddmal.music.mcgill.ca/e2e-omr-documentation/hints.html#staff-size-height-and-training)).

The folios randomly selected for the training data are: 040, 068, 094, 102, 125, 168, 176, 230, and 270. These were reduced in size according to the previous ratio (0.31) and the set of images were combined into a big file including all nine of them. The same was done to the set of layers generated in Pixel. The combined layers can be found in the `training_data` folder. The combined images can be generated again by retrieving the original images from the IIIF Manifest, reducing their size by 0.31, and combining them into one file (in ascending order—040, 068, 094, 102, 125, 168, 176, 230, and 270) by using Image Magick as indicated in the tutorial section for [Image Layering](http://ddmal.music.mcgill.ca/e2e-omr-documentation/tutorial/document-analysis.html#image-layering).
