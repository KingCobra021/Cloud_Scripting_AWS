#!/bin/bash

ami_ID=$(~/Desktop/findAMI.sh)

count=0
key_name=""
security_group_name=""
security_group_id=""

while getopts ":c:k:s:" opt; do #allows the user to use the -c -k and -s switches
  case $opt in
    c) #in case user uses -c
      count="$OPTARG" #stores the argument passed after -c to count variable
      ;;
    k) #in case user uses -k
      key_name="$OPTARG" #stores the argument passed after -k to key_name variable
      ;;
    s) #in case user uses -s
      security_group_name="$OPTARG" #stores the argument passed after -s to security_group variable
      ;;
    \?) #incase user makes a mistake and uses a switch tha doesn't exist
      echo "Invalid option: -$OPTARG" >&2 #prints a error massage notifying the user
      exit 1 # exit code 1 means program exits with error
      ;;
    :) # usesr uses the switches but doesn't provid an argument
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac 
done #ends the while loop 


if [ -z "$key_name" ] || [ -z "$security_group_name" ]; then
	echo "please provide necessary values"
	exit 1
elif [ "$count" -eq 0 ]; then
	echo "please specify how many instances have to be made!"
	exit 1
fi

security_group_id=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=$security_group_name" \
    --query "SecurityGroups[*].GroupId" \
    --output text)

if [ -z "$security_group_id" ]; then

	echo "security group with the name $security_group_name does not exist!"
	exit 1
fi

echo " creating instances......"

aws ec2 run-instances --image-id "$ami_ID" --count "$count" --instance-type t2.micro \
--key-name "$key_name" --security-group-ids "$security_group_id"
