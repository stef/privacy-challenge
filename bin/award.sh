#!/bin/ksh

alias gpg='gpg --keyring keys/keyring.pub --no-default-keyring --secret-keyring keys/keyring.sec'
(echo "Achievement unlocked: $1";date -u) | gpg --clearsign --armor --default-key pc@ctrlc.hu
