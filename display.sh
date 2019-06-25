set -x
GCOV_PREFIX=/sys/kernel/debug/gcov
GCOV_PATH=$YAKIN_DIR/coverage/gcov
find ${GCOV_PATH} -name 'info*' | sed ':a;N;$!ba;s/\n/ -a /g' | xargs lcov -o ${GCOV_PATH}/$YAKIN.merged -a
mkdir -p $YAKIN_DIR/coverage/output
genhtml -o $YAKIN_DIR/coverage/output ${GCOV_PATH}/$YAKIN.merged 
echo "Reoprt saved at coverage/output"