#!/bin/bash

ME=`basename "$0"`;
LCK="/tmp/${ME}.LCK";
exec 8>$LCK;

flock -x 8;

scp example-email-* <username>@<ip-address>:/var/mail/
rm example-email-*
