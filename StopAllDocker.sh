#!/bin/bash

proccess_ids=$(docker ps -a -q)


read -p "are you sure you wan to remove $proccess_ids (yes/no): " choice


if [[ $choice == "Yes" || $choice == "yes" ]]; then
	docker stop $proccess_ids
	echo "Containers stopped successfully."
else
	echo "Exiting...."
	exit 0
fi
ubu
