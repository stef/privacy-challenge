#!/bin/ksh

basedir=$(realpath "${0%/*}/..")
alias gpg='gpg --keyring $basedir/keys/keyring.pub --no-default-keyring --secret-keyring $basedir/keys/keyring.sec'
(printf "Achievement unlocked: $1\n";date -u) | gpg --clearsign --armor --default-key ono@vps598.greenhost.nl 2>/dev/null
