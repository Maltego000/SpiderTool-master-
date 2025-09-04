# Spider OSINT Tool 🕷️
Powerful Open Source Intelligence (OSINT) tool for deep analysis of domains and IP addresses.
##  Features
### Domain Analysis
- **WHOIS information** - registrar, registration dates, contacts
- **DNS records** - A, AAAA, MX, NS, TXT, CNAME records
- **Subdomain discovery** - automatic subdomain detection
- **Web analysis** - website technologies, contact data
- **Contact extraction** - email addresses and phone numbers
### IP Address Analysis
- **Geolocation** - country, city, coordinates
- **Provider information** - ISP, organization
- **Port scanning** - open port detection
- **Reverse DNS** - domain name resolution
- **Network analysis** - CIDR, registry
### Additional Features
- **Automatic saving** - results in JSON format
- **Clean interface** - no unnecessary messages
- **Colored interface** - beautiful banner and navigation
- **Multithreading** - fast subdomain discovery
## 🚀 Installation
1. Clone the repository:
```bash
git clone <repository-url>
#  Spider OSINT Tool
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey)](https://github.com)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com)
> A powerful and ethical Open Source Intelligence (OSINT) reconnaissance tool for cybersecurity professionals, researchers, and ethical hackers.
Spider OSINT Tool provides comprehensive domain and IP address analysis capabilities, designed with simplicity and effectiveness in mind. Perfect for security assessments, digital forensics, and educational purposes.
##  Key Features
###  Domain Intelligence
- **WHOIS Analysis** - Complete registrant information, dates, and contacts
- **DNS Enumeration** - A, AAAA, MX, NS, TXT, CNAME record discovery  
- **Subdomain Discovery** - Multi-threaded subdomain enumeration
- **Technology Stack Detection** - Web framework and CMS identification
- **Contact Extraction** - Email addresses and phone number harvesting
###  IP Address Analysis  
- **Geolocation Intelligence** - Country, region, city with coordinates
- **Network Information** - ISP, organization, and ASN details
- **Port Scanning** - Comprehensive TCP port enumeration
- **Reverse DNS** - PTR record resolution and hostname mapping
- **Network Range Analysis** - CIDR and registry information
###  Advanced Capabilities
- **Clean Interface** - Minimalist design focused on results
- **JSON Output** - Structured data export for automation
- **Multi-threading** - Accelerated reconnaissance operations
- **Rate Limiting** - Respectful scanning to avoid detection
- **Cross-platform** - Works on Linux, Windows, and macOS
##  Quick Start
### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection
- (Optional) nmap for advanced port scanning
### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/spider-osint-tool.git
cd spider-osint-tool
```
2. Install dependencies:
```bash
pip install -r requirements.txt
python3 spider-Tool.py
```
```
**IP search:**
```
->>> 2
IP ->>> 8.8.8.8
```
Results saved in json results file
```
##  Detailed Usage Guide
### Domain Reconnaissance
Perform comprehensive analysis of any domain:
```bash
->>> 1
Domain ->>> target-domain.com
```
**What gets analyzed:**
- WHOIS registration data
- All DNS record types
- Common subdomain enumeration
- Web technology fingerprinting  
- Contact information extraction
- Associated IP addresses
### IP Address Investigation
Deep dive into IP address intelligence:
```bash
->>> 2  
IP ->>> 192.168.1.1
```
**Information gathered:**
- Geographic location with coordinates
- ISP and organization details
- Open port scanning (1-1000 range)
- Reverse DNS lookups
- Network ownership data
##  Project Structure
```
spider-osint-tool/
├── speder.py           # Main application file
├── spider_tool.py      # Extended version with additional features
├── osint_libs.py       # Additional libraries
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
├── LICENCE            # License
└── replit.md          # Project configuration
```
## 🔧 System Requirements
- **Python:** 3.8+
- **Operating System:** Windows, Linux, macOS
- **Nmap:** For port scanning (installed automatically)
- **Internet connection:** For executing requests
##  Report Formats
The tool supports creating reports in the following formats:
- **JSON** - structured data for programmatic processing
- **CSV** - tabular data for Excel analysis
- **XML** - XML structure for integration
- **HTML** - beautiful web reports for viewing
##  Security
- All scans are performed ethically and legally
- Tool uses only publicly available information
- Does not perform attacking actions
- Respects request rate limits
##  Legal Information
This tool is intended exclusively for:
- Educational purposes
- Testing your own infrastructure
- Information security research
**User bears full responsibility for using the tool in accordance with applicable legislation.**
├── speder.py              # Main application entry point
├── spider_tool.py         # Extended version with advanced features
├── osint_libs.py          # Supporting library functions
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
├── LICENSE               # MIT license with ethical guidelines
├── .gitignore            # Git ignore patterns
└── replit.md             # Development environment config
```
-- Technical Details
- `requests` - HTTP library for web requests
- `python-nmap` - Network port scanning
- `dnspython` - DNS resolution and queries
- `python-whois` - WHOIS protocol implementation
- `colorama` - Cross-platform colored terminal text
- `ipwhois` - IP address WHOIS lookups
- `beautifulsoup4` - HTML parsing for web analysis
-- Output Format
Results are automatically saved in JSON format:
```json
{
  "domain": "example.com",
  "timestamp": "2025-09-03 14:30:22",
  "ip": "93.184.216.34",
  "whois": {
    "registrar": "IANA",
    "creation_date": "1995-08-14",
    "expiration_date": "2025-08-13"
  },
  "dns": {
    "A": ["93.184.216.34"],
    "MX": ["0 ."]
  },
  "geolocation": {
    "country": "United States",
    "city": "Norwell", 
    "coordinates": "42.1508,-70.8128"
  }
}