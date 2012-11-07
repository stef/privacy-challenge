#!/bin/sh

alias gpg='gpg --keyring keys/keyring.pub --no-default-keyring --secret-keyring keys/keyring.sec'
gpg --batch --gen-key keys/pcgenkeytpl
gpg --export --armor ono@vps598.greenhost.nl >keys/pubkey.asc
