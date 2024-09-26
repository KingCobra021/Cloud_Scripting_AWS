#!/bin/bash
while getopts ":t:" opt; do #allows the user to use the -t switch
  case $opt in
    t) #in case user uses -t
      TAG_VALUE="$OPTARG" #stores the argument passed after -t to tag_value variable
      ;;
    \?) #incase user makes a mistake and uses a switch tha doesn't exist
      echo "Invalid option: -$OPTARG" >&2 #prints a error massage notifying the user
      exit 1 # exit code 1 means program exits with error
      ;;
    :) # usesr uses -t but doesn't provid an argument
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac 
done #ends the while loop 

if [ -z "$TAG_VALUE" ]; then # -z cheks if the tag_value is empty or noit and if it is exits wiht code 1 and diplays an error
  echo "Usage: stopAll.sh -t <tag-value>"
  exit 1
fi

INSTANCE_IDS=$(aws ec2 describe-instances --filters "Name=tag:Department,Values=$TAG_VALUE" --query "Reservations[*].Instances[*].InstanceId" --output text)

#chooses the instances that have the entered tag attached

if [ -z "$INSTANCE_IDS" ]; then #checks to see if the instance_ids is emty which suggest that the instance with the enmtred tag doesn't exist
  echo "No instances found with tag 'Department'=$TAG_VALUE."
  exit 0
fi

read -p "Are you sure you want to remove all machines wiht the tag $TAG_VALUE ?" choice

if [[ $choice == "Yes" || $choice == "yes" ]]; then
	aws ec2 stop-instances --instance-ids $INSTANCE_IDS #stoips the instances that mached the tag
	echo "Instances stopped successfully."
else
	echo "Exiting...."
	exit 0
fi
