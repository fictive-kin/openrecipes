#!/usr/bin/env bash

# This needs to be run under the scrapy_proj directory.
# You should define SERVER as an env var when calling this.
# Example:
#    SERVER=foobar.com:6800; run_site_spiders.sh

scrapy list | grep -v .feed | xargs -I {} curl http://$SERVER/schedule.json -d project=openrecipes -d spider={}
