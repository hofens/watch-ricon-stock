#!/usr/bin/env python3
"""
Product Monitor Once - Monitors the Ricn Mall API for stock availability
This script runs once, checks product stock, and sends email notification if any product is in stock.
"""
import json
import hashlib
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import argparse
import os


class ProductMonitorOnce:
    def __init__(self, config_file: str = "src/config.json"):
        """
        Initialize the Product Monitor Once using configuration file
        
        :param config_file: Path to the configuration file
        """
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('product_monitor_once.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.load_config(config_file)
        
        # Initialize SMTP attributes to None
        self.smtp_server = None
        self.smtp_port = None
        self.smtp_user = None
        self.smtp_password = None
        self.to_email = None
        
        # Load email configuration if needed
        if self.notify_method == 'email':
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                email_config = config.get('notification_config', {}).get('email', {})
                self.smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
                self.smtp_port = email_config.get('smtp_port', 587)
                self.smtp_user = email_config.get('smtp_user', '')
                self.smtp_password = email_config.get('smtp_password', '')
                self.to_email = email_config.get('to_email', '')
            except Exception as e:
                self.logger.error(f"Error loading email configuration: {e}")
    
    def load_config(self, config_file: str):
        """
        Load configuration from JSON file
        
        :param config_file: Path to the configuration file
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.api_url = config.get('api_url', 'https://newsite.ricn-mall.com/api/pc/get_products?page=1&limit=10&cid=9&sid=0&priceOrder=&news=0')
            self.notify_method = config.get('notification_method', 'console')
            self.log_file = config.get('log_file', 'product_monitor_once.log')
            self.changes_log = config.get('changes_log', 'product_changes.log')
            
            # Load time range configuration
            time_range_config = config.get('time_range', {})
            self.enable_time_range = time_range_config.get('enable', False)
            self.start_time = time_range_config.get('start_time', '09:00')
            self.end_time = time_range_config.get('end_time', '23:59')
            
            # Convert time strings to time objects
            try:
                from datetime import time as dt_time
                self.start_time_obj = datetime.strptime(self.start_time, '%H:%M').time()
                self.end_time_obj = datetime.strptime(self.end_time, '%H:%M').time()
            except ValueError:
                self.logger.error("Invalid time format in time_range configuration. Use HH:MM format.")
                raise
            
        except FileNotFoundError:
            self.logger.error(f"Configuration file {config_file} not found.")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"Configuration file {config_file} is not valid JSON.")
            raise
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise
    
    def is_in_time_range(self) -> bool:
        """
        Check if the current time is within the configured time range
        
        :return: True if current time is in range, False otherwise
        """
        if not self.enable_time_range:
            return True  # Always active if time range is disabled
        
        current_time = datetime.now().time()
        
        # Handle time ranges that cross midnight (e.g., 22:00 to 06:00)
        if self.end_time_obj < self.start_time_obj:  # Time range crosses midnight
            return current_time >= self.start_time_obj or current_time <= self.end_time_obj
        else:  # Normal time range (e.g., 09:00 to 23:00)
            return self.start_time_obj <= current_time <= self.end_time_obj

    def fetch_products(self) -> Optional[Dict[str, Any]]:
        """
        Fetch products from the API
        
        :return: Dictionary containing API response data or None if error
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 200:
                return data.get('data', {})
            else:
                self.logger.error(f"API returned error: {data.get('msg', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error while fetching products: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON response: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error while fetching products: {e}")
            return None
    
    def find_in_stock_products(self, products: List[Dict]) -> List[Dict]:
        """
        Find products that have stock available (stock > 0)
        
        :param products: List of product dictionaries
        :return: List of products with stock > 0
        """
        in_stock_products = []
        for product in products:
            if product.get('stock', 0) > 0:
                in_stock_products.append(product)
        return in_stock_products
    
    def notify_in_stock_products(self, in_stock_products: List[Dict]):
        """
        Send notifications about in-stock products
        
        :param in_stock_products: List of products that are in stock
        """
        if not in_stock_products:
            self.logger.info("No products are currently in stock")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Products with stock available at {timestamp}:\n\n"
        
        message += f"Found {len(in_stock_products)} product(s) in stock:\n\n"
        for product in in_stock_products:
            message += f"- ID: {product['id']}\n"
            message += f"  Name: {product['store_name']}\n"
            message += f"  Price: {product['price']}\n"
            message += f"  Stock: {product['stock']}\n"
            message += f"  Sales: {product['sales']}\n"
            message += f"  Star Rating: {product['star']}\n\n"
        
        message += f"Total products checked: {len(in_stock_products)}\n"
        
        # Send notification based on method
        if self.notify_method == "console":
            print(message)
        elif self.notify_method == "file":
            with open(self.changes_log, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        elif self.notify_method == "email":
            self.send_email(message, "Product Monitor - In Stock Items Found")
        else:
            self.logger.warning(f"Unknown notification method: {self.notify_method}")
    
    def send_email(self, message: str, subject: str = "Product Monitor - In Stock Items Found"):
        """
        Send email notification using configured settings
        
        :param message: Message content
        :param subject: Email subject
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = self.to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Email notification sent to {self.to_email}")
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
    
    def run_monitor_once(self):
        """
        Run the monitoring process once
        """
        self.logger.info(f"Starting single-run product monitoring for: {self.api_url}")
        
        # Check if we're in the allowed time range
        if not self.is_in_time_range():
            self.logger.info("Outside time range, skipping check")
            return
        
        self.logger.info("Fetching product data...")
        data = self.fetch_products()
        
        if data:
            current_products = data.get('list', [])
            self.logger.info(f"Fetched {len(current_products)} products")
            
            # Find products with stock > 0
            in_stock_products = self.find_in_stock_products(current_products)
            
            if in_stock_products:
                self.logger.info(f"Found {len(in_stock_products)} product(s) in stock!")
                self.notify_in_stock_products(in_stock_products)
            else:
                self.logger.info("No products in stock")
        else:
            self.logger.warning("Failed to fetch product data")


def main():
    parser = argparse.ArgumentParser(description='Single-run product stock monitor for Ricn Mall API')
    parser.add_argument('--config', type=str, default='src/config.json',
                        help='Path to the configuration file (default: src/config.json)')
    
    args = parser.parse_args()
    
    # Handle config file path - try different possible locations
    config_file = args.config
    
    # If the specified config file doesn't exist from current working directory
    if not os.path.exists(config_file):
        # Try src/config.json (for when running from project root)
        if os.path.exists('src/config.json'):
            config_file = 'src/config.json'
        # Or if running from src directory, try relative path
        elif os.path.exists('../src/config.json'):
            config_file = '../src/config.json'
    
    # Create and run the single-run monitor
    monitor = ProductMonitorOnce(config_file=config_file)
    monitor.run_monitor_once()


if __name__ == "__main__":
    main()