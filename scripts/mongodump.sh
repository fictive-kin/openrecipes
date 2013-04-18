#!/usr/bin/env bash
DATE=$(date -u +%Y%m%d-%H%M%S); mongodump --db openrecipes --collection recipeitems --out $DATE-dump
