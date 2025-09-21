## MEI Files Encoding the Music and Text of the Einsiedeln manuscript (CH-E 611)

These MEI files were obtained through the end-to-end OMR workflow in Rodan.

The naming convention of these files is: `<siglum>_<folio number>`. Example for folio 1r in the [Einsiedeln manuscript](https://cantusdatabase.org/source/123606): `CH-E_611_001r`

Towards the end of the correction of the Einsiedeln manuscript, we realized that Rodan and Neon were assuming that the default octave of C clefs was C3, when it should be C4. Consequently, all elements following a C clef were being encoded an octave too low. We first corrected this by adding `dis="8" dis.place="above"` tags to all C clefs. We then decided that the default octave of C clefs should be fixed properly, so that all future files are encoded correctly. Rodan and Neon have now been updated and C clefs have--and are displayed at--the correct octave. Those fixes occurred after Ensiedeln folios were run through end-to-end OMR and after they were all corrected in Neon once, but before they were all reviewed and finalized, so there are some mismatches between files in different folders. The files are organized as follows:
  
- The folder `ready_for_neon` contains the files as obtained by the OMR workflow, before being corrected by a user in Neon. If one of these files is uploaded to Neon, all of the pitched elements following a C clef will show up an octave too low. This is because they were encoded when the default C clef octave was C3, but Neon now assumes a default octave of C4.
- The folder `Processed` contains the files corrected by a user in Neon. In Neon, these will behave like the files in the `ready_for_neon` folder.
- The folder `Reviewed_once` contains the same files after review (the review is also done in Neon). In all of these files, the pitched elements following C clefs are an octave too low. In some of these files, C clefs have a `dis="8" dis.place="above"` tag--this tag is not desired.
- The folder `Reviewed no pitch correction needed` contains the files that were reviewed after the default clef octave in Neon was fixed. These files are completely correct; the octave of C clefs is correct, as is the octave of all pitched elements following them.

A (fairly) complete record of the OMR and correction of this manuscript can be found here: https://docs.google.com/spreadsheets/d/1JjNyhZvEtv-3U5kgqcnsE0mCwHs8A-Px12CYYNLPsVw/edit#gid=0
