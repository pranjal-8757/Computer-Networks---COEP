#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// Splits a dotted IP string into individual integer octets
void splitIPAddress(char *addr, int result[]) {
    char *part = NULL;
    int index = 0;

    part = strtok(addr, ".\0");
    while (part != NULL && index < 4) {
        result[index++] = atoi(part);
        part = strtok(NULL, ".\0");
    }
}

int main() {

    char ipString[16];
    int ip[4], mask[4];
    int totalSubnets = 0;
    char ipClass;
    int classValue = 0;
    int cidr = 0;

    // Read IP class
    printf("Enter class (A/B/C): ");
    scanf("%c", &ipClass);

    // Assign class value
    // A -> 1, B -> 2, C -> 3
    if (ipClass == 'A' || ipClass == 'a')
        classValue = 1;
    else if (ipClass == 'B' || ipClass == 'b')
        classValue = 2;
    else if (ipClass == 'C' || ipClass == 'c')
        classValue = 3;
    else {
        printf("Invalid class!\n");
        return 0;
    }

    // Display CIDR range
    printf("'/\\' notation range for class %c: /%d - /32\n",
           ipClass, classValue * 8);

    // Read CIDR bits
    printf("Enter num subnet bits: /");
    scanf("%d", &cidr);

    if (cidr > 32 || cidr < classValue * 8) {
        printf("Invalid value for subnet of class %c!\n", ipClass);
        return 0;
    }

    // -------- Subnet Mask Calculation --------
    int remaining = cidr;

    for (int i = 0; i < 4; i++) {
        if (remaining >= 8) {
            mask[i] = 255;
            remaining -= 8;
        }
        else if (remaining > 0) {
            mask[i] = 256 - (1 << (8 - remaining));
            remaining = 0;
        }
        else {
            mask[i] = 0;
        }
    }

    printf("Subnet Mask: %d.%d.%d.%d\n",
           mask[0], mask[1], mask[2], mask[3]);

    // Read and parse IP address
    printf("Enter IP address: ");
    scanf("%s", ipString);
    splitIPAddress(ipString, ip);

    // -------- Subnet & Host Calculation --------
    int subnetBits = cidr - (classValue * 8);
    totalSubnets = pow(2, subnetBits);
    printf("Number of subnet grps: %d\n", totalSubnets);

    int hostBits = 32 - cidr;
    int hostsPerSubnet = pow(2, hostBits) - 2;
    printf("Number of hosts per subnet grp: %d\n", hostsPerSubnet);

    // -------- Network, Broadcast & Host Range --------
    int subnetOctet = cidr / 8;
    int remainder = cidr % 8;

    if (remainder != 0)
        subnetOctet++;

    int blockSize = 256 / pow(2, subnetBits);

    for (int s = 0; s < totalSubnets; s++) {

        int network[4] = { ip[0], ip[1], ip[2], ip[3] };
        int broadcast[4] = { ip[0], ip[1], ip[2], ip[3] };

        network[subnetOctet - 1] = s * blockSize;
        broadcast[subnetOctet - 1] = (s * blockSize) + blockSize - 1;

        for (int j = subnetOctet; j < 4; j++) {
            network[j] = 0;
            broadcast[j] = 255;
        }

        printf("\nSubnet %d\n", s + 1);
        printf("Network ID: %d.%d.%d.%d\n",
               network[0], network[1], network[2], network[3]);

        printf("Broadcast Addr: %d.%d.%d.%d\n",
               broadcast[0], broadcast[1], broadcast[2], broadcast[3]);

        printf("Valid Host Range: %d.%d.%d.%d - %d.%d.%d.%d\n",
               network[0], network[1], network[2], network[3] + 1,
               broadcast[0], broadcast[1], broadcast[2], broadcast[3] - 1);
    }

    return 0;
}
