#!/usr/bin/env python

import argparse
import os
import subprocess
import shutil

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Automate common Zeek processes')
    parser.add_argument('pcap', metavar='PCAP_FILE', help='the PCAP file to analyze')
    parser.add_argument('-o', '--output', metavar='OUTPUT_DIR', help='the directory to output the results')
    parser.add_argument('-r', '--report', action='store_true', help='generate a HTML report of the results')
    parser.add_argument('-p', '--policy', metavar='POLICY_FILE', help='the Zeek policy file to use')
    parser.add_argument('-n', '--name', metavar='NAME', help='the name of the Zeek log file')
    args = parser.parse_args()
    
    # Create a directory to store the output if one isn't specified
    if not args.output:
        args.output = 'zeek-output'
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Set the name of the Zeek log file if one isn't specified
    if not args.name:
        args.name = 'zeek.log'
    
    # Run Zeek
    cmd = ['zeek', '-r', args.pcap, '-U', '-C', '-w', os.path.join(args.output, args.name)]
    if args.policy:
        cmd += ['-p', args.policy]
    subprocess.call(cmd)
    
    # Generate a report if requested
    if args.report:
        subprocess.call(['zeek', 'report', os.path.join(args.output, args.name)])
    
    # Copy the logs to a separate directory for easier analysis
    logs_dir = os.path.join(args.output, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    for filename in os.listdir(args.output):
        if filename.endswith('.log'):
            shutil.copy2(os.path.join(args.output, filename), os.path.join(logs_dir, filename))
    
    print('Zeek analysis complete.')

if __name__ == '__main__':
    main()
