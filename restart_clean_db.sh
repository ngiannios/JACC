./kill_open_processes.sh jacc_client.py
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

python3 jacc_add_nodes.py -p 80 --nodePort 80
python3 jacc_add_nodes.py -p 80 --nodePort 81
python3 jacc_add_nodes.py -p 80 --nodePort 82
python3 jacc_add_nodes.py -p 80 --nodePort 83
python3 jacc_add_nodes.py -p 80 --nodePort 84
python3 jacc_add_nodes.py -p 80 --nodePort 85
python3 jacc_add_nodes.py -p 81 --nodePort 80
python3 jacc_add_nodes.py -p 82 --nodePort 80
python3 jacc_add_nodes.py -p 83 --nodePort 80
python3 jacc_add_nodes.py -p 84 --nodePort 80
python3 jacc_add_nodes.py -p 85 --nodePort 80


