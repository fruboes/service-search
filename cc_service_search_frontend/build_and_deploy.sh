#! /bin/bash

cd "$(dirname "$0")"
set -e
npm run build


rm -rf  ../cc_service_search/website_data/*
cp -R ./build/* ../cc_service_search/website_data/

