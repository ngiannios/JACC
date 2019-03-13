./kil_open_processes jacc_client.py
rm -f ./log/app*.log
rm -f ./blockchain*.txt
rm -f ./wallet*.txt

git pull https://github.com/ngiannios/jacc

python3 jacc_client.py -p 80 &
python3 jacc_client.py -p 81 &
python3 jacc_client.py -p 82 &
python3 jacc_client.py -p 83 &
python3 jacc_client.py -p 84 &
python3 jacc_client.py -p 85 &
