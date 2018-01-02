/*

Covert Tunnelling in ICMP 0x00 ECHO REPLY messages

  Many thanks to FuSyS and Richard Stevens ^_^

Dark Schneider X1999

*/

#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>

#define ICMP_ECHOREPLY	0
#define ICMP_ECHO	8

// definizione di alcune costanti 

#define IP_HDR	20
#define ICMP_HDR 8
#define ICMP_MINLEN	8
#define MAXMESG	4096
#define MAXPACKET 5004
#define LAST	1
#define REPLY	1
#define ECHO_TAG	0xF001
#define ECHO_LAST	0xF002

// Strutture e Variabili
// Lancio un doveroso Porko D*io liberatorio... dopo ore ho trovato come fare
// a togliermi dalle palle la fottuta icmp.dll (winsock maledette)

// IP Header
struct ip
{
	unsigned char	Hlen:4;         
	unsigned char	Version:4;       
	unsigned char	Tos;            
	unsigned short	LungTot;    
	unsigned short	Id;         
	unsigned short	Flags;
	unsigned char	Ttl; 
	unsigned char	Proto;           
	unsigned short	Checksum;       
	unsigned int	SourceIP;
	unsigned int	DestIP;

};

// ICMP Header
struct icmp {
			BYTE		Type;
			BYTE		Code; 
			USHORT		CheckSum;
			USHORT		Id;
			USHORT		Seq;
			ULONG		Dati;
			};

SOCKET				sockfd;
u_int				icmp_init =1;
struct sockaddr_in	clisrc;

// Funzione di checksum 

USHORT checksum(USHORT *buffer, int size)
{

  unsigned long cksum=0;

  while(size >1)
  {
	cksum+=*buffer++;
	size -=sizeof(USHORT);
  }
  
  if(size )
  {
	cksum += *(UCHAR*)buffer;
  }

  cksum = (cksum >> 16) + (cksum & 0xffff);
  cksum += (cksum >>16);
  return (USHORT)(~cksum);
}

// Reimplemento bcopy e bzero... Ma perche' cavolo windows non le
// rende disponibili?

void bzero(char *pnt, int dim_pnt )
{
	memset((char *)&pnt, 0, dim_pnt);
};

void bcopy(char *src, char *dest, int dim_src)
{
	memmove((char *)&dest, (char *)&src, dim_src);
};

// Micro$oft Sucks
// Funzioni di gestione dei pacchetti ICMP
// Fankulo a quegli stronzi maledetti che si sono inventati la icmp.dll
// Brutti bastardi pezzi di merda, la compatibilita' ve la siete ficcata su
// per il culo?
// Micro$oft Sucks

void ICMP_init(void)
	{
	if(icmp_init)
		{
		if((sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)) == INVALID_SOCKET)
			{
			fprintf(stderr, "impossibile creare raw ICMP socket");
			exit(0);
			}
		}
	icmp_init = 0;
	};

void ICMP_reset(void)
	{
	closesocket(sockfd);
	icmp_init = 1;
	};

int ICMP_send(char *send_mesg, size_t mesglen, ULONG dest_ip, int echo, int last)
	{
	int						sparato;
	struct tunnel
		{
		struct icmp		 icmp;
		UCHAR			 data[MAXMESG];
		} icmp_pk;
	int						icmplen	= sizeof(struct icmp);
	int						pack_dim;
	struct sockaddr_in		dest;
	int						destlen;

	if(mesglen > MAXMESG) return(-1);
	
	if(icmp_init) ICMP_init();

	destlen						= sizeof(dest);
	bzero((char *)&dest, destlen);
	dest.sin_family				= AF_INET;
	dest.sin_addr.s_addr		= dest_ip;
	pack_dim					= mesglen + sizeof(struct icmp);
	memset(&icmp_pk, 0, pack_dim);
	icmp_pk.icmp.Type			= ICMP_ECHOREPLY;
	bcopy(send_mesg, (char *)&icmp_pk.icmp.Dati, mesglen);
	icmp_pk.icmp.CheckSum		= checksum((USHORT *) &icmp_pk.icmp, (sizeof(struct icmp) + mesglen));
	if(echo) icmp_pk.icmp.Seq	= ECHO_TAG;
	if(last) icmp_pk.icmp.Seq	= ECHO_LAST;

	if(sparato = sendto(sockfd, (char *)&icmp_pk, pack_dim, 0, (struct sockaddr *)&dest, destlen) < 0)
		{
		perror("RAW ICMP SendTo: ");
		return(-1);
		} 
		else if(sparato != pack_dim)
		{
		perror("dimensioni pacchetto IP errate: ");
		return(-1);
		}
		return(sparato);
	};

int ICMP_recv(char *recv_mesg, size_t mesglen, int echo)
	{
	struct recv
		{
		struct ip	ip;
		struct icmp icmp;
		char		data[MAXMESG];
		} rcv_pk;
	int				pack_dim;
	int				accolto;
	int				iphdrlen;
	int				clilen = sizeof(clisrc);

	if(icmp_init) ICMP_init();
	while(1)
		{
		pack_dim = mesglen + sizeof(struct ip) + sizeof(struct icmp);
		memset(&rcv_pk, 0, pack_dim);
		if((accolto = recvfrom(sockfd, (char *)&rcv_pk, pack_dim, 0, (struct sockaddr *) &clisrc, &clilen)) < 0) continue;

		iphdrlen = rcv_pk.ip.Hlen << 2;
		if(accolto < (iphdrlen + ICMP_MINLEN)) continue;
		accolto -= iphdrlen;

		if(!echo)
			{
			if(!rcv_pk.icmp.Id && !rcv_pk.icmp.Code && rcv_pk.icmp.Type == ICMP_ECHOREPLY && rcv_pk.icmp.Seq != ECHO_TAG && rcv_pk.icmp.Seq != ECHO_LAST) break;
			}
		if(echo)
			{
			if(!rcv_pk.icmp.Id && !rcv_pk.icmp.Code && rcv_pk.icmp.Type == ICMP_ECHOREPLY && (rcv_pk.icmp.Seq == ECHO_TAG || rcv_pk.icmp.Seq == ECHO_LAST)) break;
			}
		}
		if(!echo)
			{
			accolto -= ICMP_HDR;
			bcopy((char *)&rcv_pk.icmp.Dati, recv_mesg, accolto);
			return(accolto);
			}
		if(echo)
			{
			if(rcv_pk.icmp.Seq == ECHO_TAG)
				{
				accolto -= ICMP_HDR;
				bzero(recv_mesg, sizeof(recv_mesg));
				bcopy((char *)&rcv_pk.icmp.Dati, recv_mesg, accolto);
				return(accolto);
				}
			return(-666);
			}
	};
