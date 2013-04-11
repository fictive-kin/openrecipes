#!/usr/bin/env bash
DATE=$(date -u +%Y%M%d); mongoexport --db openrecipes --collection recipeitems --out - | gzip -c > $DATE-recipeitems.json.gz
