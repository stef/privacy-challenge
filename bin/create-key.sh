#!/bin/sh

alias gpg='gpg --keyring keys/keyring.pub --no-default-keyring --secret-keyring keys/keyring.sec'
gpg --batch --gen-key keys/pcgenkeytpl
gpg --export --armor pc@ctrlc.hu >keys/pubkey.asc
