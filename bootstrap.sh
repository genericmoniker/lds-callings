#!/usr/bin/env bash

# Heroku repository:
add-apt-repository "deb https://cli-assets.heroku.com/branches/stable/apt ./"
curl -L https://cli-assets.heroku.com/apt/release.key | apt-key add -

apt-get update
apt-get install -y python3.6 python3.6-venv heroku redis-server postgresql

python3.6 -m venv .venv
.venv/bin/pip install wheel
.venv/bin/pip install -r requirements.txt

# Can I do this here?
sudo -u postgres createuser -s $(whoami)
createdb lds-callings
createdb createdb lds-callings-test
# DATABASE_URL=postgres:///lds-callings
