#!/usr/bin/env bash
DATE=$(date -u +%Y%m%d-%H%M%S); mongoexport --db openrecipes --collection recipeitems --out - | gzip -c > $DATE-recipeitems.json.gz
