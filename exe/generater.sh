#! /bin/bash
echo "------------------------------------------------------------------"
echo "This is one tool to generate secret key for vio."
echo "------------------------------------------------------------------"
sleep 1
echo "enter your username"
read uname
echo "enter your password"
read -s pword

bit=`getconf LONG_BIT`

if [ $bit -eq 32 ]
then
	echo "32"
	echo -e "$uname\n$pword" | ./digest_generater_X86
else
	echo "64"
	echo -e "$uname\n$pword" | ./digest_generater_X64
fi

