#!/usr/bin/env bash
DATE=$(date -u +%Y%M%d); mongodump --db openrecipes --collection recipeitems --out $DATE-dump
