#!/bin/bash
# The input file is a list file of sra ID number
echo "downloading..."
#download file
dwfile=sra_dw_`date +%Y%m%d`
#creat a list file of dowlaod path
python3 ./sra_format.py $1
#use aspera to download data 
ascp -i $ascpkey --user=anonftp --host=ftp-private.ncbi.nlm.nih.gov --mode=recv -T -l 100m -k 1 --file-list sra_download_path.txt ./$dwfile
echo "Completely!"
