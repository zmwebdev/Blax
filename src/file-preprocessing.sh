#!/usr/bin/env bash

# Read data_text_dir path from a config file.
WIKIDIR=$1

# Text preprocessing.
# Remove <doc id ... line and its next line (title of an article).
for FILE in $( find ${WIKIDIR} -name "wiki_*" ); do
    echo "Processing ${FILE}"
    #sed -i -e '/^$/d; /<doc id/,+1d; s/<\/doc>//g' ${FILE}
    sed -i -e '/<doc id/d; /<\/doc>/d' ${FILE}
done

## Concat all text files in each text directory.
#for DIR in $( find ${WIKIDIR} -mindepth 1 -type d ); do
#    echo "Processing ${DIR}"
#    for f in $( find ${DIR} -name "wiki_*" ); do cat $f >> ${DIR}/all.txt; done 
#done
