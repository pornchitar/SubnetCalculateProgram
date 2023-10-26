import ipaddress


def format_subnet_bitmap(network_class, subnet_mask, subnet_bits):
    subnet_mask = int(subnet_mask)  # Convert subnet_mask to an integer
    formatted_subnet_bitmap = format(subnet_mask, '032b')
    nnn_bits = formatted_subnet_bitmap[:subnet_bits].replace('1', 'n').replace('0','h')
    hhh_bits = formatted_subnet_bitmap[subnet_bits:].replace('0', 'h').replace('1', 'n')

    if network_class == 'A':
        class_number = '0'
    elif network_class == 'B':
        class_number = '10'
    elif network_class == 'C':
        class_number = '110'
    else:
        class_number = '??'  # Unknown class

    # Replace the first 3 characters in nnn_bits with "110"
    nnn_bits = nnn_bits[len(class_number):]

    formatted_bitmap = class_number + nnn_bits + hhh_bits
    formatted_bitmap_with_dots = '.'.join([formatted_bitmap[i:i + 8] for i in range(0, len(formatted_bitmap), 8)])
    return formatted_bitmap_with_dots
def calculate_subnet_info(network_class, ip_address, subnet_bits, max_subnets, mask_bits, hosts_per_subnet):
    network_class = network_class.upper()
    ip_address = ipaddress.IPv4Address(ip_address)
    subnet_bits = int(subnet_bits)

    if network_class == 'A':
        subnet_mask = 0xFF000000
    elif network_class == 'B':
        subnet_mask = 0xFFFF0000
    elif network_class == 'C':
        subnet_mask = 0xFFFFFF00
    else:
        print("Invalid Network Class")
        return

    subnet_mask >>= (32 - subnet_bits)
    subnet_mask <<= (32 - subnet_bits)
    network_address = int(ip_address) & subnet_mask
    subnet_mask = ipaddress.IPv4Address(subnet_mask)

    # Calculate various subnet information
    subnet_range = 2 ** (32 - subnet_bits)
    hosts_per_subnet = 2 ** (32 - subnet_bits) - 2  # Subtract 2 for network and broadcast addresses
    subnet_id = ipaddress.IPv4Address(network_address)
    broadcast_address = ipaddress.IPv4Address(network_address + subnet_range - 1)
    host_address_range = (subnet_id + 1, broadcast_address - 1)
    subnet_bitmap = format_subnet_bitmap(network_class,subnet_mask, subnet_bits)

    print(f"Network Class: {network_class}")
    print(f"IP Address: {ip_address}")
    print(f"Subnet Mask: {subnet_mask}")
    print(f"Subnet Bits: {subnet_bits}")
    print(f"Maximum Subnets: {max_subnets}")
    print(f"Mask Bits: {mask_bits}")
    print(f"Hosts per Subnet: {hosts_per_subnet}")
    print(f"Host Address Range: {host_address_range[0]} - {host_address_range[1]}")
    print(f"Subnet ID: {subnet_id}")
    print(f"Broadcast Address: {broadcast_address}")
    print(f"Subnet Bitmap: {subnet_bitmap}")


if __name__ == "__main__":
    network_class = input("Enter Network Class (A, B, C): ")
    ip_address = input("Enter IP Address (e.g., 192.168.1.1): ")
    subnet_bits = input("Enter Subnet Bits (e.g., 24): ")
    max_subnets = 2 ** (32 - int(subnet_bits))
    mask_bits = 32 - int(subnet_bits)
    hosts_per_subnet = 2 ** (32 - int(subnet_bits)) - 2
    calculate_subnet_info(network_class, ip_address, subnet_bits, max_subnets, mask_bits, hosts_per_subnet)