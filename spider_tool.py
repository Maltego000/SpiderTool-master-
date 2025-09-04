#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import socket
import threading
import time
import json
import re
import requests
import nmap
import whois
import dns.resolver
from ipwhois import IPWhois
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime

init(autoreset=True)

class SpederTool:
    def __init__(self):
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def print_banner(self):
        """Выводит красивый баннер Spider Tool"""
        os.system('clear' if os.name == 'posix' else 'cls')
        banner = f"""
{Fore.RED}{Style.BRIGHT}
  _________      .__    .___             ___________           .__   
 /   _____/_____ |__| __| _/___________  \__    ___/___   ____ |  |  
 \_____  \\\\____ \\|  |/ __ |/ __ \\_  __ \\   |    | /  _ \\ /  _ \\|  |  
 /        \\  |_> >  / /_/ \\  ___/|  | \\/   |    |(  <_> |  <_> )  |__
/_______  /   __/|__\\____ |\\___  >__|      |____| \\____/ \\____/|____/
        \\/|__|           \\/    \\/                                    
{Style.RESET_ALL}
{Fore.RED}{Style.BRIGHT}Dev ->>> Мальтего {Style.RESET_ALL}
"""
        print(banner)

    def print_menu(self):
        menu = f"""
{Fore.WHITE}[{Fore.RED}01{Fore.WHITE}]{Fore.RED} Search Domain 
{Fore.WHITE}[{Fore.RED}02{Fore.WHITE}]{Fore.RED} Search IP 
"""
        print(menu)

    def get_whois_info(self, domain):
        try:
            w = whois.whois(domain)
            return {
                'domain_name': w.domain_name,
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'name_servers': w.name_servers,
                'emails': w.emails,
                'org': w.org,
                'country': w.country
            }
        except Exception as e:
            return None

    def get_dns_records(self, domain):
        dns_info = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                dns_info[record_type] = [str(answer) for answer in answers]
            except:
                dns_info[record_type] = []
        
        return dns_info

    def get_subdomains(self, subdomain):
        subdomains = []
        
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'blog', 'shop', 'api', 'dev', 'test',
            'staging', 'cdn', 'images', 'static', 'assets', 'support', 'help',
            'docs', 'portal', 'app', 'mobile', 'secure', 'vpn', 'remote'
        ]
        
        def check_subdomain(sub):
            try:
                subdomain = f"{sub}.{domain}"
                socket.gethostbyname(subdomain)
                subdomains.append(subdomain)
            except:
                pass
        
        threads = []
        for sub in common_subdomains:
            thread = threading.Thread(target=check_subdomain, args=(sub,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        return subdomains

    def get_ip_info(self, ip):
        try:
            obj = IPWhois(ip)
            results = obj.lookup_rdap()
            
            return {
                'ip': ip,
                'country': results.get('asn_country_code'),
                'description': results.get('asn_description'),
                'cidr': results.get('asn_cidr'),
                'registry': results.get('asn_registry'),
                'network_name': results.get('network', {}).get('name') if results.get('network') else None,
                'network_country': results.get('network', {}).get('country') if results.get('network') else None
            }
        except Exception as e:
            return None

    def get_geolocation(self, ip):
        try:
            response = self.session.get(f'http://ip-api.com/json/{ip}')
            if response.status_code == 200:
                data = response.json()
                return {
                    'country': data.get('country'),
                    'region': data.get('regionName'),
                    'city': data.get('city'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'timezone': data.get('timezone'),
                    'isp': data.get('isp'),
                    'org': data.get('org')
                }
        except Exception as e:
            return None

    def port_scan(self, target, port_range="1-1000"):
        nm = nmap.PortScanner()
        try:
            result = nm.scan(target, port_range)
            
            open_ports = []
            if target in result['scan']:
                for port in result['scan'][target]['tcp']:
                    state = result['scan'][target]['tcp'][port]['state']
                    service = result['scan'][target]['tcp'][port]['name']
                    if state == 'open':
                        open_ports.append({'port': port, 'service': service})
            
            return open_ports
        except Exception as e:
            return []

    def web_crawl(self, domain):
        try:
            url = f"http://{domain}"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            text = soup.get_text().lower()
            
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            phones = re.findall(r'(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9})', text)
            
            technologies = []
            if 'wordpress' in text:
                technologies.append('WordPress')
            if 'jquery' in text:
                technologies.append('jQuery')
            if 'bootstrap' in text:
                technologies.append('Bootstrap')
            
            return {
                'emails': list(set(emails)),
                'phones': list(set(phones)),
                'technologies': technologies,
                'title': soup.title.string if soup.title else None
            }
        except Exception as e:
            return None

    def search_domain(self, domain):
        """Полный поиск по домену"""        
        results = {
            'domain': domain,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'whois': self.get_whois_info(domain),
            'dns': self.get_dns_records(domain),
            'subdomains': self.get_subdomains(domain),
            'web_info': self.web_crawl(domain)
        }
        
        try:
            ip = socket.gethostbyname(domain)
            results['ip'] = ip
            results['ip_info'] = self.get_ip_info(ip)
            results['geolocation'] = self.get_geolocation(ip)
            results['open_ports'] = self.port_scan(ip)
        except:
            results['ip'] = None
        
        self.results[domain] = results
        self.save_results(domain, results)
        
        return results

    def search_ip(self, ip):
        """Полный поиск по IP адресу"""
        results = {
            'ip': ip,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip_info': self.get_ip_info(ip),
            'geolocation': self.get_geolocation(ip),
            'open_ports': self.port_scan(ip)
        }
        
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            results['hostname'] = hostname
            results['whois'] = self.get_whois_info(hostname)
        except:
            results['hostname'] = None
        
        self.results[ip] = results
        self.save_results(ip, results)
        
        return results

    def save_results(self, target, results):
        """Сохраняет результаты в JSON файл"""
        filename = f"osint_results_{target.replace('.', '_').replace(':', '_')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved in {filename}")

    def run(self):
        """Главный цикл программы"""
        while True:
            self.print_banner()
            self.print_menu()
            
            try:
                choice = input(f"\n->>> ")
                
                if choice == '01' or choice == '1':
                    domain = input(f"Domain ->>> ")
                    if domain:
                        self.search_domain(domain)
                        input(f"\n[x] - Clear Screen ")
                
                elif choice == '02' or choice == '2':
                    ip = input(f"IP ->>> ")
                    if ip:
                        self.search_ip(ip)
                        input(f"\n[x] - Clear Screen")
                
                else:
                    break
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                time.sleep(2)

if __name__ == "__main__":
    speder = SpederTool()
    speder.run()