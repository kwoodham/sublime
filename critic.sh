#!/bin/bash

DIR=$(dirname $1)
TARGET=$(basename $1 .md)
PDOPTS="--from markdown+simple_tables --smart --standalone"
PDOPTS=$PDOPTS" --include-in-header=$HOME/css/markdown.css"

SEDSTR='s/{++/<ins>/g'
SEDSTR=$SEDSTR';s/++}/<\/ins>/g'
SEDSTR=$SEDSTR';s/{--/<del>/g'
SEDSTR=$SEDSTR';s/--}/<\/del>/g'
SEDSTR=$SEDSTR';s/{~~/<del>/g'
SEDSTR=$SEDSTR';s/~>/<\/del><ins>/g'
SEDSTR=$SEDSTR';s/~~}/<\/ins>/g'
SEDSTR=$SEDSTR';s/{>>/<span class="critic comment">/g'
SEDSTR=$SEDSTR';s/<<}/<\/span>/g'
SEDSTR=$SEDSTR';s/{==/\<mark>/g'
SEDSTR=$SEDSTR';s/==}/<\/mark>/g'

echo $SEDSTR

# Convert [[links]] to [links](./links.html) and process markdown
sed "$SEDSTR" < $1 | pandoc $PDOPTS -o "$DIR/$TARGET".html



