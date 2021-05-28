mkdir data
cd data
git clone https://github.com/mitre/cti.git
cd ..
python3 cti-importer.py -p ./data/cti
