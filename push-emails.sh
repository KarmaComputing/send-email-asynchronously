#!/bin/bash
set -euxo pipefail

ME=`basename "$0"`;
LCK="/tmp/${ME}.LCK";
exec 8>$LCK;

flock -x 8;

PATH_TO_EMAILS=$1
echo Running push-emails as $USER
source "$HOME/.keychain/${HOSTNAME}-sh"
scp $PATH_TO_EMAILS/* <username>@<ip>:<path-to-server-emails-dir>
rm $PATH_TO_EMAILS/* || true
