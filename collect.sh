#!/bin/sh
#set -x
GCOV_PREFIX=/sys/kernel/debug/gcov
GCOV_PATH=$YAKIN_DIR/coverage/gcov

function cpGcov() {
    # First, Check gcov is enable
    if ! test -d /sys/kernel/debug/gcov/ ; then
    	echo "Target system do not enable gcov, skip progress..."
    fi
    
    for i in $(find /sys/kernel/debug/gcov/$YAKIN_DIR/ -name '*.gcda');do rm -rf ${YAKIN_DIR}${i##*$YAKIN};cp -rf $i ${YAKIN_DIR}${i##*$YAKIN};done
    for i in $(find $YAKIN_DIR -name '*.gcno'); do cp -rf $i ${i//.tmp_/} 2> /dev/null ; done
}
cpGcov 
TIME=$(date +"%s")
[ -d $GCOV_PATH ] || mkdir $GCOV_PATH
geninfo --no-recursion $YAKIN_DIR -o $GCOV_PATH/info_$filename.$TIME > /dev/null
# fsync file
python - <<END
import os;
fd = os.open( "$GCOV_PATH/info_$filename.$TIME", os.O_RDONLY  );
os.fsync(fd);
os.close(fd);
END
# delete broken record
find ${GCOV_PATH} -size -20k -type f -exec rm -rf {} \;