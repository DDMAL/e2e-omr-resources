The Python script `get_text_per_folio.py` is meant to retrieve the text from each folio of a manuscript, 
as provided by the Cantus Database. The script requires the path to a CSV file containing the text of 
the complete manuscript. This CSV file can be obtained through the Cantus DB by following
[these instructions](http://ddmal.music.mcgill.ca/e2e-omr-documentation/tutorial/music-reconstruction.html#text-alignment)). 

The script returns a set of text files, one for each folio. 
The text file for a given folio contains the text of all the chants of that folio and the last segment (8-words long)
of the chant from the previous folio, given that sometimes a chant continues into the next folio.

In the folder `Salzinnes`, you can find the CSV file from the Salzinnes Antiphonal (extracted 
from [this entry](https://cantus.uwaterloo.ca/source/123723) of the Cantus DB) and the generated text files.
To generate these text files again, just run:

```
$ python get_text_per_folio.py CantusDB_Salzinnes.csv
```
