#!/bin/bash

DIR=$(dirname $1)
TARGET=$(basename $1 .md)
PDOPTS="--from markdown+simple_tables --smart --standalone"
PDOPTS=$PDOPTS" --include-in-header=$HOME/css/critic.css"

SEDSTR=''
SEDSTR=$SEDSTR's/{++/<ins>/g;s/++}/<\/ins>/g'
SEDSTR=$SEDSTR';s/{--/<del>/g;s/--}/<\/del>/g'
SEDSTR=$SEDSTR';s/{~~/<del>/g;s/~>/<\/del><ins>/g;s/~~}/<\/ins>/g'
SEDSTR=$SEDSTR';s/{>>/<span class="critic comment">/g;s/<<}/<\/span>/g'
SEDSTR=$SEDSTR';s/{==/\<mark>/g;s/==}/<\/mark>/g'

# Convert critic markup to tags and proces through pandoc
sed "$SEDSTR" < $1 | pandoc $PDOPTS -o "$DIR/$TARGET".html
