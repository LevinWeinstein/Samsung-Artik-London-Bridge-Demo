// python -m SimpleHTTPServer
// python api.py

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>

int main(int argc, char *argv[]){

	pid_t process_id = 0;
	pid_t sid = 0;

	process_id = fork();

	if (process_id < 0){
		dprintf(2, "error\n");
		exit(1);
	}
	if (process_id > 0){
		printf("Success, child process entered\n");
		exit(0);
	}
	umask(0);
	sid = setsid();
	if (sid < 0)
		exit(1);
	close(STDIN_FILENO);
	close(STDOUT_FILENO);
	close(STDERR_FILENO);
	system("python api.py");
	return (0);
}
