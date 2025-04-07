#!/usr/bin/env python3

import sys
import os
import binascii

def usage():
    print("Usage: paybin [options]")
    print("Options:")
    print("  -u <char>,<count>     : Unicode UTF-8 (repeats character)")
    print("  -b <hex>              : Bytes (e.g., '1234' becomes \\x12\\x34)")
    print("  -r <hex>              : Bytes in reverse order")
    print("  -bx <hex-string>      : Hex-encoded bytes (e.g., '\\x12\\x34')")
    print("  -rx <hex-string>      : Hex-encoded bytes in reverse order")
    print("  -o <output-file>      : Specify output file (required)")
    print("  -v                    : Verbose mode (print payload details)")
    print("\nExample: paybin -u A,28 -r 76910408 -o output.bin")
    print("         paybin -v -u A,28 -rx \"\\x76\\x91\\x04\\x08\" -o output.bin")
    sys.exit(1)

def process_unicode(arg):
    try:
        char, count = arg.split(',')
        return char.encode() * int(count)
    except Exception as e:
        print(f"Error processing -u argument '{arg}': {e}")
        sys.exit(1)

def process_bytes(arg):
    try:
        # Split into pairs and convert each pair to a byte
        bytes_data = b''
        for i in range(0, len(arg), 2):
            if i+1 < len(arg):
                byte_val = int(arg[i:i+2], 16)
                bytes_data += bytes([byte_val])
        return bytes_data
    except Exception as e:
        print(f"Error processing -b argument '{arg}': {e}")
        sys.exit(1)

def process_bytes_reverse(arg):
    bytes_data = process_bytes(arg)
    return bytes_data[::-1]  # Reverse the bytes

def process_hex_bytes(arg):
    try:
        # Convert string with explicit \x escapes like "\x76\x91\x04\x08"
        arg = arg.strip('"\'')
        # Replace escaped hex with actual bytes
        return arg.encode().decode('unicode_escape').encode('latin1')
    except Exception as e:
        print(f"Error processing hex argument '{arg}': {e}")
        sys.exit(1)

def process_hex_bytes_reverse(arg):
    bytes_data = process_hex_bytes(arg)
    return bytes_data[::-1]  # Reverse the bytes

def bytes_to_plain(byte_string):
    """Convert all bytes to their hex representation regardless of whether they're printable or not."""
    result = "b'"
    for byte in byte_string:
        result += f"\\x{byte:02x}"
    result += "'"
    return result

def print_payload_info(payload):
    print(f"Payload length: {len(payload)} bytes")
    
    # Print as hex
    hex_view = binascii.hexlify(payload).decode()
    print(f"Hex view: {hex_view}")
    
    # Print as ASCII (with non-printable chars as dots)
    ascii_view = ''
    for byte in payload:
        if 32 <= byte <= 126:  # Printable ASCII
            ascii_view += chr(byte)
        else:
            ascii_view += '.'
    print(f"ASCII view: {ascii_view}")
    
    # Print all bytes as hex representation
    bytes_view = bytes_to_plain(payload)
    print(f"Bytes view: {bytes_view}")

def main():
    if len(sys.argv) < 2:
        usage()
    
    args = sys.argv[1:]
    result = b''
    output_file = None
    verbose = False
    
    i = 0
    while i < len(args):
        if args[i] == '-u' and i + 1 < len(args):
            result += process_unicode(args[i+1])
            i += 2
        elif args[i] == '-b' and i + 1 < len(args):
            result += process_bytes(args[i+1])
            i += 2
        elif args[i] == '-r' and i + 1 < len(args):
            result += process_bytes_reverse(args[i+1])
            i += 2
        elif args[i] == '-bx' and i + 1 < len(args):
            result += process_hex_bytes(args[i+1])
            i += 2
        elif args[i] == '-rx' and i + 1 < len(args):
            result += process_hex_bytes_reverse(args[i+1])
            i += 2
        elif args[i] == '-o' and i + 1 < len(args):
            output_file = args[i+1]
            i += 2
        elif args[i] == '-v':
            verbose = True
            i += 1
        else:
            print(f"Unknown argument: {args[i]}")
            usage()
    
    # Check if output file was specified
    if not output_file:
        print("Error: Output file must be specified with -o flag")
        usage()
    
    try:
        # Write to output file in binary mode
        with open(output_file, 'wb') as f:
            f.write(result)
        
        print(f"Payload written to {output_file} ({len(result)} bytes)")
        
        # Print detailed payload information if verbose mode is enabled
        if verbose:
            print_payload_info(result)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()