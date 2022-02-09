install:
	sudo cp httpsserver.service /etc/systemd/system/httpsserver.service
	sudo systemctl enable httpsserver.service
	sudo systemctl start httpsserver
forward:
	sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
	sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
	sudo iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
	sudo iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
status:
	sudo systemctl status httpsserver
remove:
	sudo systemctl stop httpsserver
	sudo systemctl disable httpsserver.service
	sudo rm /etc/systemd/system/httpsserver.service
