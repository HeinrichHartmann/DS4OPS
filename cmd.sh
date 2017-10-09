#!/bin/bash
echo "#"
echo "# Data Science 4 Effective Operations"
echo "#"
printf "# starting jupyter notebook ... "
jupyter notebook --ip 0.0.0.0 --port 9999 &> notebook.log &
sleep 3
printf "done\n"

IP=$(curl -s icanhazip.com)
LINK_L=$(jupyter notebook list | tail -n1 | cut -d: -f1-3)
LINK_P=$(echo $LINK_L | sed "s/0.0.0.0/$IP/g")
echo "#"
echo "# * local url: $LINK_L"
echo "# * public url: $LINK_P"
echo "#"

bash
