chmod +x check_in.py
chmod +x check_in.sh
chmod +x last_will.py
chmod +x last_will.sh
chmod +x schedule_cron.py
virtualenv -p /usr/bin/python3.8 venv
source venv/bin/activate
pip install -r requirements.txt
./last_will.py
deactivate