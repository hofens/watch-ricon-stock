#!/usr/bin/env python3
"""
Product Monitor - Monitors the Ricn Mall API for product changes
"""
import json
import time
import hashlib
import requests
import logging
from datetime import datetime, time as dt_time
from typing import Dict, List, Optional, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class ProductMonitor:
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize the Product Monitor using configuration file
        
        :param config_file: Path to the configuration file
        """
        # Setup logging - basic config until we load the file settings
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('product_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.load_config(config_file)
        
        # Reconfigure logging with loaded config
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        
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
            self.polling_interval = config.get('polling_interval_seconds', 300)
            self.notify_method = config.get('notification_method', 'console')
            self.log_file = config.get('log_file', 'product_monitor.log')
            self.changes_log = config.get('changes_log', 'product_changes.log')
            
            # Load time range configuration
            time_range_config = config.get('time_range', {})
            self.enable_time_range = time_range_config.get('enable', False)
            self.start_time = time_range_config.get('start_time', '09:00')
            self.end_time = time_range_config.get('end_time', '23:59')
            
            # Convert time strings to time objects
            try:
                self.start_time_obj = datetime.strptime(self.start_time, '%H:%M').time()
                self.end_time_obj = datetime.strptime(self.end_time, '%H:%M').time()
            except ValueError:
                self.logger.error("Invalid time format in time_range configuration. Use HH:MM format.")
                raise
            
            self.previous_products_hash = None
            self.previous_products = []
            
        except FileNotFoundError:
            self.logger.error(f"Configuration file {config_file} not found.")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"Configuration file {config_file} is not valid JSON.")
            raise
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise
    
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
    
    def calculate_products_hash(self, products: List[Dict]) -> str:
        """
        Calculate a hash of the products list to detect changes
        
        :param products: List of product dictionaries
        :return: Hash string representing the products state
        """
        # Create a string representation of all products
        products_str = json.dumps(products, sort_keys=True)
        return hashlib.sha256(products_str.encode()).hexdigest()
    
    def detect_changes(self, current_products: List[Dict]) -> Dict[str, Any]:
        """
        Detect changes between current and previous product lists
        
        :param current_products: Current list of products
        :return: Dictionary containing change information
        """
        changes = {
            'new_products': [],
            'removed_products': [],
            'updated_products': [],
            'total_count_changed': False,
            'has_changes': False
        }
        
        current_hash = self.calculate_products_hash(current_products)
        
        # Check if total count changed
        if len(current_products) != len(self.previous_products):
            changes['total_count_changed'] = True
        
        # If we have a previous state, compare products
        if self.previous_products:
            current_ids = {p['id'] for p in current_products}
            previous_ids = {p['id'] for p in self.previous_products}
            
            # Find new products
            new_ids = current_ids - previous_ids
            changes['new_products'] = [p for p in current_products if p['id'] in new_ids]
            
            # Find removed products
            removed_ids = previous_ids - current_ids
            changes['removed_products'] = [p for p in self.previous_products if p['id'] in removed_ids]
            
            # Check for updated products
            common_ids = current_ids & previous_ids
            for pid in common_ids:
                current_product = next(p for p in current_products if p['id'] == pid)
                previous_product = next(p for p in self.previous_products if p['id'] == pid)
                
                # Compare key fields to detect updates
                if self.products_differ(current_product, previous_product):
                    changes['updated_products'].append({
                        'old': previous_product,
                        'new': current_product
                    })
        
        # Determine if there are any changes
        changes['has_changes'] = (
            bool(changes['new_products']) or 
            bool(changes['removed_products']) or 
            bool(changes['updated_products']) or
            changes['total_count_changed']
        )
        
        # Update the stored previous state
        self.previous_products = current_products.copy()
        self.previous_products_hash = current_hash
        
        return changes
    
    def products_differ(self, old_product: Dict, new_product: Dict) -> bool:
        """
        Compare two products to see if they differ in important fields
        
        :param old_product: Previous product state
        :param new_product: Current product state
        :return: True if products differ in important fields, False otherwise
        """
        # Compare important fields that would indicate a meaningful change
        important_fields = [
            'store_name', 'price', 'stock', 'sales', 'star'
        ]
        
        for field in important_fields:
            if old_product.get(field) != new_product.get(field):
                return True
        
        return False
    
    def notify_changes(self, changes: Dict[str, Any]):
        """
        Send notifications about detected changes
        
        :param changes: Dictionary containing change information
        """
        if not changes['has_changes']:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Product changes detected at {timestamp}:\n\n"
        
        if changes['new_products']:
            message += f"New products ({len(changes['new_products'])}):\n"
            for product in changes['new_products']:
                message += f"  - ID: {product['id']}\n"
                message += f"    Name: {product['store_name']}\n"
                message += f"    Price: {product['price']}\n"
                message += f"    Stock: {product['stock']}\n"
                message += f"    Sales: {product['sales']}\n"
                message += f"    Star Rating: {product['star']}\n\n"
            message += "\n"
        
        if changes['removed_products']:
            message += f"Removed products ({len(changes['removed_products'])}):\n"
            for product in changes['removed_products']:
                message += f"  - ID: {product['id']}\n"
                message += f"    Name: {product['store_name']}\n"
                message += f"    Price: {product['price']}\n"
                message += f"    Stock: {product['stock']}\n"
                message += f"    Sales: {product['sales']}\n"
                message += f"    Star Rating: {product['star']}\n\n"
            message += "\n"
        
        if changes['updated_products']:
            message += f"Updated products ({len(changes['updated_products'])}):\n"
            for update in changes['updated_products']:
                old_product = update['old']
                new_product = update['new']
                message += f"  - ID: {new_product['id']}\n"
                message += f"    Name: {new_product['store_name']}\n"
                if old_product['price'] != new_product['price']:
                    message += f"    Price changed from {old_product['price']} to {new_product['price']}\n"
                if old_product['stock'] != new_product['stock']:
                    message += f"    Stock changed from {old_product['stock']} to {new_product['stock']}\n"
                if old_product['sales'] != new_product['sales']:
                    message += f"    Sales changed from {old_product['sales']} to {new_product['sales']}\n"
                if old_product['star'] != new_product['star']:
                    message += f"    Star Rating changed from {old_product['star']} to {new_product['star']}\n"
                message += "\n"
            message += "\n"
        
        # Send notification based on method
        if self.notify_method == "console":
            print(message)
        elif self.notify_method == "file":
            with open(self.changes_log, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        elif self.notify_method == "email":
            self.send_email(message)
        else:
            self.logger.warning(f"Unknown notification method: {self.notify_method}")
    
    def send_email(self, message: str):
        """
        Send email notification using configured settings
        
        :param message: Message content
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = self.to_email
            msg['Subject'] = "Product Monitor - Changes Detected"
            
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Email notification sent to {self.to_email}")
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
    
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

    def start_monitoring(self):
        """
        Start the monitoring process
        """
        self.logger.info(f"Starting product monitoring for: {self.api_url}")
        self.logger.info(f"Polling interval: {self.polling_interval} seconds")
        self.logger.info(f"Notification method: {self.notify_method}")
        
        if self.enable_time_range:
            self.logger.info(f"Time range enabled: {self.start_time} to {self.end_time}")
        else:
            self.logger.info("Time range disabled - monitoring all day")
        
        # Fetch initial data to establish baseline and for startup notification
        self.logger.info("Fetching initial product data to establish baseline...")
        initial_data = self.fetch_products()
        if initial_data:
            # Set up initial state without triggering change detection
            self.previous_products = initial_data.get('list', []).copy()
            # Calculate initial hash to establish baseline
            if self.previous_products:
                self.previous_products_hash = self.calculate_products_hash(self.previous_products)
            self.logger.info(f"Baseline established with {len(self.previous_products)} products")
        else:
            self.logger.warning("Could not fetch initial data to establish baseline")
            self.previous_products = []
            self.previous_products_hash = None
        
        # Send a startup notification if using email
        if self.notify_method == "email":
            self.logger.info("Sending startup notification email...")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            startup_message = f"Product Monitor has started successfully!\n\n"
            startup_message += f"Monitoring API: {self.api_url}\n"
            startup_message += f"Polling interval: {self.polling_interval} seconds\n"
            startup_message += f"Time range enabled: {self.enable_time_range}\n"
            if self.enable_time_range:
                startup_message += f"Active time: {self.start_time} to {self.end_time}\n"
            startup_message += f"Started at: {timestamp}\n\n"
            
            # Add current product list to startup notification
            if self.previous_products:
                startup_message += f"Current products ({len(self.previous_products)}):\n\n"
                for product in self.previous_products:
                    startup_message += f"- ID: {product['id']}\n"
                    startup_message += f"  Name: {product['store_name']}\n"
                    startup_message += f"  Price: {product['price']}\n"
                    startup_message += f"  Stock: {product['stock']}\n"
                    startup_message += f"  Sales: {product['sales']}\n"
                    startup_message += f"  Star Rating: {product['star']}\n\n"
            else:
                startup_message += "No products currently available.\n"
                
            startup_message += "\nYou will receive notifications when product changes are detected."
            
            # Temporarily change the subject for startup message
            try:
                msg = MIMEMultipart()
                msg['From'] = self.smtp_user
                msg['To'] = self.to_email
                msg['Subject'] = "Product Monitor - Started Successfully"
                
                msg.attach(MIMEText(startup_message, 'plain', 'utf-8'))
                
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
                server.quit()
                
                self.logger.info(f"Startup notification email sent to {self.to_email}")
            except Exception as e:
                self.logger.error(f"Failed to send startup email: {e}")
        
        while True:
            try:
                # Check if we're in the allowed time range
                if not self.is_in_time_range():
                    sleep_minutes = 5  # Check again in 5 minutes
                    self.logger.info(f"Outside time range, sleeping for {sleep_minutes} minutes...")
                    time.sleep(sleep_minutes * 60)  # Sleep for 5 minutes before checking again
                    continue  # Skip the rest of the loop and re-check time
                
                self.logger.info("Fetching product data...")
                data = self.fetch_products()
                
                if data:
                    current_products = data.get('list', [])
                    changes = self.detect_changes(current_products)
                    
                    if changes['has_changes']:
                        self.logger.info(f"Changes detected! {len(changes['new_products'])} new, "
                                       f"{len(changes['removed_products'])} removed, "
                                       f"{len(changes['updated_products'])} updated")
                        self.notify_changes(changes)
                    else:
                        self.logger.info("No changes detected")
                else:
                    self.logger.warning("Failed to fetch product data")
                
                # Wait for the polling interval
                time.sleep(self.polling_interval)
                
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.polling_interval)


def main():
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description='Monitor Ricn Mall API for product changes')
    parser.add_argument('--config', type=str,
                        help='Path to the configuration file (default: config.local.json if exists, otherwise config.json)')
    
    args = parser.parse_args()
    
    # Handle config file path with priority: --config arg > config.local.json > config.json
    if args.config:
        # Use specified config file
        config_file = args.config
    elif os.path.exists('src/config.local.json'):
        # Use config.local.json if it exists
        config_file = 'src/config.local.json'
    elif os.path.exists('config.local.json'):
        # Check for config.local.json in current directory
        config_file = 'config.local.json'
    elif os.path.exists('src/config.json'):
        # Use config.json in src directory
        config_file = 'src/config.json'
    elif os.path.exists('config.json'):
        # Check for config.json in current directory
        config_file = 'config.json'
    else:
        # Default to config.json
        config_file = 'config.json'
    
    # Create and start the monitor
    monitor = ProductMonitor(config_file=config_file)
    
    monitor.start_monitoring()


if __name__ == "__main__":
    main()