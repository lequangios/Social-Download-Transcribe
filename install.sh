apt install python3.10-venv
sudo chown -R $USER:www-data /var/www/python_app
chmod 775 /var/www/python_app
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
sudo pip install openai-whisper openai yt-dlp Flask certifi gunicorn youtube_dl --no-cache-dir
#/usr/local/lib/python3.10/dist-packages/flask
#/etc/systemd/system/flaskrest.service
#venv/bin/gunicorn
sudo systemctl start flaskrest.service
sudo systemctl enable flaskrest.service
sudo systemctl status flaskrest.service