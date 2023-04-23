#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma pack(push, 1)

#include <sys/socket.h>
#include <arpa/inet.h>

#include <sys/errno.h>

#define socket_t int
#define mreq_t ip_mreq

#define EDGE_MULTICAST "211.1.1.1"
#define TEST_MULTICAST "224.0.1.2"

#define EDGE_LOCALEDGE "127.0.0.254"
#define TEST_LOCALHOST "127.0.0.1"

union uip_mreq_t
{
    unsigned char raw[255];
    struct ip_mreq data;
};

int main()
{
    printf("[INFO]: %s\n", "Multicast");

    socket_t s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    mreq_t mreq;
    int result = 0;
    size_t length = sizeof(mreq_t);
    size_t length_div2 = length / 2;

    result = inet_aton(TEST_MULTICAST, &mreq.imr_multiaddr);
    printf("[INFO]: %d\n", result);

    result = inet_aton(TEST_LOCALHOST, &mreq.imr_interface);
    printf("[INFO]: %d\n", result);

    result = setsockopt(s, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, length);
    printf("[INFO]: %d\n", result);

    result = setsockopt(s, IPPROTO_IP, IP_DROP_MEMBERSHIP, &mreq, length);
    printf("[INFO]: %d\n", result);

    uip_mreq_t onion;
    onion.data = mreq;
    char buffer[255] = "";
    char tmp[255] = "";
    for (size_t i = 0; i < length; ++i)
    {
        sprintf(tmp, "%u, ", (unsigned int)onion.raw[i]);
        strcat(buffer, tmp);
    }
    printf("[INFO]: %s\n", buffer);

    uip_mreq_t noino;
    for (size_t i = 0; i < length_div2; ++i)
    {
        noino.raw[length_div2 - i - 1] = onion.raw[i];
        noino.raw[length - i - 1] = onion.raw[length_div2 + i];
    }

    char reffub[255] = "";
    char pmt[255] = "";
    for (size_t i = 0; i < length; ++i)
    {
        sprintf(pmt, "%u, ", (unsigned int)noino.raw[i]);
        strcat(reffub, pmt);
    }
    printf("[INFO]: %s\n", reffub);

    result = setsockopt(s, IPPROTO_IP, IP_ADD_MEMBERSHIP, &(noino.data), length);
    printf("[INFO]: %d\n", result);

    result = setsockopt(s, IPPROTO_IP, IP_DROP_MEMBERSHIP, &(noino.data), length);
    printf("[INFO]: %d\n", result);

    printf("[INFO]: %s\n", strerror(errno));

    return 0;
}

#pragma pack(pop)
