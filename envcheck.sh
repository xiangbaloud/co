[ -d coverage/gcov ] || `echo "create folder gcov under folder coverage first"; exit 1`
[ -d coverage/output ] || `echo "create folder output under folder coverage first"; exit 1`

grep "\-DSSD_SIZE_IN_SEU=0" Makefile
if (($? == 0))
then
	echo "You should set SSD_SIZE_IN_SEU to a smaller value, e.g. 200, to avoid a long run"
	exit 1
fi

grep "ftest-coverage" Makefile | grep "#"
if (($? == 0))
then
	echo "You should enable the line of -ftest-coverage in Makefile to run coverage"
	exit 1;
fi

exit 0

