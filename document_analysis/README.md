# Document Analysis

In this folder you will find the training data and models (generated with this data) for the individual manuscripts processed at DDMAL. 
Some models where generated with an old method (see [this archived page on document analysis](https://ddmal.music.mcgill.ca/e2e-omr-documentation/tutorial/archived-document-analysis.html)). 
However, the current method for document analysis can be found in the [Document Analysis by Iterative Training with Paco Classifier](https://ddmal.music.mcgill.ca/e2e-omr-documentation/tutorial/iterative-training.html) page.
The deault settings of this Paco Trainer work very good, but [here](MS_73/README.md#important-notes) are a few notes on when changing these 
settings could be useful (as it was the case for `MS 73`).

**The MS_73 manuscript shows the current way of training,** 
using the Paco's method for iterative training (see [documentation](https://ddmal.music.mcgill.ca/e2e-omr-documentation/tutorial/iterative-training.html)). 
In this method, we train with ZIP Pixel files, each containing the image and layers corresponding to one page. 
The workflows used to label the data of a page as belonging to the different layers, train the models, and classify a new page are provided by the three 
JSON files in this folder.
