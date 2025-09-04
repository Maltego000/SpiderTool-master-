#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
import os

class OSINTLogger:
    
    def __init__(self, log_file="osint_log.txt"):
        self.log_file = log_file
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
    def info(self, message):
        self.log(message, "INFO")
        
    def error(self, message):
        self.log(message, "ERROR")
        
    def warning(self, message):
        self.log(message, "WARNING")

class DataExporter:
    
    @staticmethod
    def to_csv(data, filename):
        flattened_data = DataExporter._flatten_dict(data)
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if flattened_data:
                fieldnames = flattened_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in flattened_data:
                    writer.writerow(row)
                    
    @staticmethod
    def to_xml(data, filename):
        """Экспорт в XML формат"""
        root = ET.Element("osint_results")
        DataExporter._dict_to_xml(data, root)
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        
    @staticmethod
    def to_html(data, filename):
        """Экспорт в HTML отчет"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>OSINT Report</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .target {{ background-color: #f0f0f0; padding: 15px; margin: 10px 0; border-left: 5px solid #d32f2f; }}
        .section {{ margin: 10px 0; }}
        .header {{ color: #d32f2f; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>OSINT Investigation Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""
        
        for target, info in data.items():
            html_content += f"""
    <div class="target">
        <h2>Target: {target}</h2>
        <div class="section">
            <div class="header">Timestamp:</div>
            <p>{info.get('timestamp', 'N/A')}</p>
        </div>
"""
            
            if 'geolocation' in info and info['geolocation']:
                geo = info['geolocation']
                html_content += f"""
        <div class="section">
            <div class="header">Geolocation:</div>
            <p>Country: {geo.get('country', 'N/A')}</p>
            <p>Region: {geo.get('region', 'N/A')}</p>
            <p>City: {geo.get('city', 'N/A')}</p>
            <p>Coordinates: {geo.get('lat', 'N/A')}, {geo.get('lon', 'N/A')}</p>
        </div>
"""
            
            if 'open_ports' in info and info['open_ports']:
                html_content += """
        <div class="section">
            <div class="header">Open Ports:</div>
            <table>
                <tr><th>Port</th><th>Service</th></tr>
"""
                for port in info['open_ports']:
                    html_content += f"<tr><td>{port['port']}</td><td>{port['service']}</td></tr>"
                
                html_content += "</table></div>"
            
            html_content += "</div>"
        
        html_content += """
</body>
</html>
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    @staticmethod
    def _flatten_dict(data, parent_key='', sep='_'):
        """Преобразует вложенный словарь в плоский"""
        items = []
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(DataExporter._flatten_dict(v, new_key, sep=sep).items())
                elif isinstance(v, list):
                    items.append((new_key, '; '.join(map(str, v))))
                else:
                    items.append((new_key, v))
        return [dict(items)] if items else []
    
    @staticmethod
    def _dict_to_xml(data, parent):
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, str(key).replace(' ', '_'))
                DataExporter._dict_to_xml(value, child)
        elif isinstance(data, list):
            for item in data:
                list_item = ET.SubElement(parent, 'item')
                DataExporter._dict_to_xml(item, list_item)
        else:
            parent.text = str(data) if data is not None else ''

class ReportGenerator:
    
    def __init__(self):
        self.exporter = DataExporter()
        self.logger = OSINTLogger()
        
    def generate_full_report(self, data, target_name):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = f"osint_report_{target_name.replace('.', '_').replace(':', '_')}_{timestamp}"
        
        json_file = f"{base_name}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        csv_file = f"{base_name}.csv"
        self.exporter.to_csv(data, csv_file)
        
        xml_file = f"{base_name}.xml"
        self.exporter.to_xml(data, xml_file)
        
        html_file = f"{base_name}.html"
        self.exporter.to_html(data, html_file)
        
        self.logger.info(f"Полный отчет создан для {target_name}")
        
        return {
            'json': json_file,
            'csv': csv_file,
            'xml': xml_file,
            'html': html_file
        }

class AdvancedOSINT:
    
    def __init__(self):
        self.logger = OSINTLogger()
       
    def analyze_patterns(self, results):
        patterns = {
            'common_ports': {},
            'common_services': {},
            'geographic_distribution': {},
            'technology_stack': []
        }
        
        for target, data in results.items():
            if 'open_ports' in data:
                for port in data['open_ports']:
                    port_num = port['port']
                    service = port['service']
                    
                    patterns['common_ports'][port_num] = patterns['common_ports'].get(port_num, 0) + 1
                    patterns['common_services'][service] = patterns['common_services'].get(service, 0) + 1
            
            if 'geolocation' in data and data['geolocation']:
                country = data['geolocation'].get('country')
                if country:
                    patterns['geographic_distribution'][country] = patterns['geographic_distribution'].get(country, 0) + 1
            
            if 'web_info' in data and data['web_info'] and 'technologies' in data['web_info']:
                patterns['technology_stack'].extend(data['web_info']['technologies'])
        
        return patterns
    
    def generate_threat_assessment(self, data):
        threat_level = 0
        threats = []
        
        if 'open_ports' in data:
            risky_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
            for port in data['open_ports']:
                if port['port'] in risky_ports:
                    threat_level += 1
                    threats.append(f"Открытый порт {port['port']} ({port['service']}) может быть уязвим")
        
        if threat_level == 0:
            risk_level = "Низкий"
        elif threat_level <= 3:
            risk_level = "Средний"
        else:
            risk_level = "Высокий"
        
        return {
            'risk_level': risk_level,
            'threat_score': threat_level,
            'threats': threats,
            'recommendations': self._get_recommendations(threats)
        }
    
    def _get_recommendations(self, threats):
        recommendations = []
        
        if any('22' in threat for threat in threats):
            recommendations.append("Рассмотрите использование ключей SSH вместо паролей")
        
        if any('80' in threat or '443' in threat for threat in threats):
            recommendations.append("Убедитесь в актуальности веб-сервера и используйте HTTPS")
        
        if any('21' in threat for threat in threats):
            recommendations.append("Рассмотрите замену FTP на более безопасные протоколы (SFTP/FTPS)")
        
        return recommendations

class DatabaseManager:
    
    def __init__(self, db_file="osint_results.db"):
        import sqlite3
        self.db_file = db_file
        self.init_database()
        
    def init_database(self):
        import sqlite3
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investigations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                data TEXT NOT NULL,
                investigation_type TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def save_investigation(self, target, data, investigation_type):
        import sqlite3
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO investigations (target, timestamp, data, investigation_type)
            VALUES (?, ?, ?, ?)
        ''', (target, datetime.now().isoformat(), json.dumps(data), investigation_type))
        
        conn.commit()
        conn.close()
        
    def get_investigations(self, target=None):
        import sqlite3
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        if target:
            cursor.execute('SELECT * FROM investigations WHERE target = ?', (target,))
        else:
            cursor.execute('SELECT * FROM investigations')
        
        results = cursor.fetchall()
        conn.close()
        
        return results