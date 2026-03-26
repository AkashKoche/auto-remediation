#!/bin/bash
echo "Executing clear_disk for instance: $1"

echo "Cleaning /tmp directory..."

rm -rf /tmp/*

echo "Disk cleanup complete."
