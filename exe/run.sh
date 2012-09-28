#! /bin/bash

bit=`getconf LONG_BIT`

if [ $bit -eq 32 ]
then
	echo "32"
	./vio_X86 -f ./vio.conf
else
	echo "64"
	./vio_X64 -f ./vio.conf
fi
