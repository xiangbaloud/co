1. turn on below line in Makefile
   EXTRA_CFLAGS += -Wframe-larger-than=4096 -ftest-coverage -fprofile-arcs
	
2. then change 

   CFLAGS_SSD_SIZE_IN_SEU := -DSSD_SIZE_IN_SEU=200 and then make

3. run scripts/start.run and then see the report in coverage/output
