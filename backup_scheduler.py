import os
import datetime
import subprocess
import schedule
import time

def backup_database():
    # Create backup directory if it doesn't exist
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Generate backup filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'teataimi_backup_{timestamp}.sql')
    
    # Database credentials
    DB_USER = "root"
    DB_PASS = ""
    DB_NAME = "teataimi"
    
    # MySQL dump command
    cmd = f'mysqldump -u {DB_USER} {DB_NAME} > "{backup_file}"'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"Backup created successfully: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {str(e)}")

def cleanup_old_backups():
    # Keep backups for last 30 days only
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        return
        
    current_time = datetime.datetime.now()
    for filename in os.listdir(backup_dir):
        filepath = os.path.join(backup_dir, filename)
        file_time = datetime.datetime.fromtimestamp(os.path.getctime(filepath))
        if (current_time - file_time).days > 30:
            os.remove(filepath)
            print(f"Removed old backup: {filename}")

if __name__ == "__main__":
    # Schedule daily backup at 3 AM
    schedule.every().day.at("03:00").do(backup_database)
    # Cleanup old backups weekly
    schedule.every().sunday.do(cleanup_old_backups)
    
    print("Backup scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(60)