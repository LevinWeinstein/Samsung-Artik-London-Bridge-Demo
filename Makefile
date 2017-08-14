all:
	gcc -o Setup setup.c
	make -C ./bin

clean:
	rm -f Setup
	make clean -C ./bin
