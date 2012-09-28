#! /bin/bash
echo "------------------------------------------------------------------"
echo "This is one tool to generate secret key for vio."
echo "------------------------------------------------------------------"
sleep 1
echo "enter your username"
read uname
echo "enter your password"
read -s pword
echo -e "$uname\n$pword" | digest_generater