#!/bin/bash

# 
# Lenovo x3650 M5 fan control speed
#
# Liam Slusser
# 2024-04-16
# lslusser@gmail.com

HOST="192.168.1.2"
USERNAME="MYUSERNAME"
PASS="MYPASSWORD"

# Check if an argument was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 [speed] [fan] [temperature]"
    echo ""
    echo "Where speed is a number between 0 and 100:"
    echo "   0   = Turn speed back to auto (system default)"
    echo "   1   = lowest speed 1%"
    echo "   100 = highest fan speed 100%"
    exit 1
fi

# Check if the argument is 'fan'
if [ "$1" = "fan" ]; then
    echo "Fan name        | ID |Status|Fan.ID| Fan speed"
    ipmitool -I lanplus -H ${HOST} -U ${USERNAME} -P ${PASS} sdr type Fan
    exit 1
fi

# Check if the argument is 'fan'
if [ "$1" = "temperature" ]; then
    echo "Sensor name      | ID |Status|TempID| Temperature"
    ipmitool -I lanplus -H ${HOST} -U ${USERNAME} -P ${PASS} sdr type Temperature
    exit 1
fi


# Get the first argument
percentage=$1

# Validate that the input is a number and between 1 and 100
if ! [[ $percentage =~ ^[0-9]+$ ]] || [ $percentage -lt 0 ] || [ $percentage -gt 100 ]; then
    echo "Invalid input. Please enter a number between 0 and 100."
    exit 1
fi

if [ "$percentage" -eq 0 ]; then
    echo "Setting fan speed to auto (system default & disable fan override)"
    echo "Setting Fan 1 to auto"
    ipmitool -I lanplus -H ${HOST} -U ${USERNAME} -P ${PASS} raw 0x3a 0x07 0x01 0x80 0x00
    echo "Setting Fan 2 to auto"
    ipmitool -I lanplus -H ${HOST} -U ${USERNAME} -P ${PASS} raw 0x3a 0x07 0x02 0x80 0x00
    echo "Setting Fan 3 to auto"
    ipmitool -I lanplus -H ${HOST} -U ${USERNAME} -P ${PASS} raw 0x3a 0x07 0x03 0x80 0x00
    echo "Setting Fan 4 to auto"
    ipmitool -I lanplus -H ${HOST} -U ${USERNAME} -P ${PASS} raw 0x3a 0x07 0x04 0x80 0x00
    exit 1
fi

# Convert percentage to a value between 1 and 255
# Formula: value = ((percentage * 254) / 100) + 1
value=$(( ((percentage * 254) / 100) + 1 ))

# Convert the value to hexadecimal
hex_value=$(printf '%x\n' $value)

# Output the results
echo "Percentage: $percentage"
echo "Decimal value (1-255): $value"
echo "Hexadecimal value: $hex_value"

echo "Setting Fan 1 to ${value}%"
ipmitool -I lanplus -H ${HOST} -U ${USERNAME} -P ${PASS} raw 0x3a 0x07 0x01 0x${hex_value} 0x01
echo "Setting Fan 2 to ${value}%"
ipmitool -I lanplus -H ${HOST} -U ${USERNAME} -P ${PASS} raw 0x3a 0x07 0x02 0x${hex_value} 0x01
echo "Setting Fan 3 to ${value}%"
ipmitool -I lanplus -H ${HOST} -U ${USERNAME} -P ${PASS} raw 0x3a 0x07 0x03 0x${hex_value} 0x01
echo "Setting Fan 4 to ${value}%"
ipmitool -I lanplus -H ${HOST} -U ${USERNAME} -P ${PASS} raw 0x3a 0x07 0x04 0x${hex_value} 0x01
