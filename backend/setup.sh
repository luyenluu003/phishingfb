sudo apt-get -y update&&sudo apt-get -y upgrade
sudo apt-get -y install python3 python3-pip nginx
sudo apt-get install ca-certificates fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils
mkdir -p ~/.config/pip/
rm -rf ~/.config/pip/pip.conf
echo "[global]" >>~/.config/pip/pip.conf
echo "break-system-packages = true" >>~/.config/pip/pip.conf
echo "export PATH="$HOME/.local/bin:$PATH"" >>~/.bashrc
source ~/.bashrc
pip install -r requirements.txt

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.94/linux64/chromedriver-linux64.zip

sudo dpkg -i google-chrome-stable_current_amd64.deb
unzip chromedriver-linux64.zip
sudo mv -f chromedriver-linux64/chromedriver /usr/local/bin/
sudo chown admin:admin /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver

rm google-chrome-stable_current_amd64.deb
rm -rf *chrome*

sudo cp -r default /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo cp -r gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
