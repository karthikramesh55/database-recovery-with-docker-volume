#!/usr/bin/env python3

"""
Script to demonstrate PostgreSQL data persistence with Docker volumes
"""

import subprocess
import sys
import time
import argparse


def run_command(command, capture_output=False):
    """Run a shell command"""
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=True, 
                                   capture_output=True, text=True)
            return result.stdout
        else:
            subprocess.run(command, shell=True, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)


def start_postgres():
    """Start PostgreSQL container"""
    print("Starting PostgreSQL container...")
    run_command("docker-compose up -d")
    print("Waiting for PostgreSQL to be ready...")
    time.sleep(5)
    print("PostgreSQL is running!")
    print()


def stop_postgres():
    """Stop and remove container"""
    print("Stopping and removing PostgreSQL container...")
    run_command("docker-compose down")
    print("The PostgreSQL container has been removed, but the volume persists)!")
    print()


def create_data():
    """Create synthetic data in database"""
    print("Creating synthetic data in database...")
    
    # Create table
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    run_command(f'docker exec -i postgres-persistent psql -U dbuser -d testdb -c "{create_table_sql}"')
    
    # Insert data
    insert_data_sql = """
        INSERT INTO users (name, email) VALUES 
        ('Akio Morita', 'akio@invo.com'),
        ('Masaru Ibuka', 'masaru@invo.com'),
        ('Hayato Ikeda', 'hayato@invo.com');
    """
    run_command(f'docker exec -i postgres-persistent psql -U dbuser -d testdb -c "{insert_data_sql}"')
    
    print("Synthetic data created!")
    print()


def view_data():
    """View data from database"""
    print("Current data in database:")
    run_command('docker exec -i postgres-persistent psql -U dbuser -d testdb -c "SELECT * FROM users;"')
    print()


def show_volume():
    """Show volume information"""
    print("Docker volume information:")
    output = run_command("docker volume inspect postgres_volume", capture_output=True)
    print(output)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Data Persistence of a PostgreSQL database through Docker Volume",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  start                            - Start PostgreSQL container
  stop                             - Stop and remove container (volume persists)
  create-data                      - Create sample table and data
  view-data                        - View current data in database
  volume-info                      - Show Docker volume details
        """
    )
    
    parser.add_argument(
        'command',
        choices=['start', 'stop', 'create-data', 'view-data', 'volume-info', 'demo'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    print("=== PostgreSQL Docker Volume Persistence Demo ===")
    print()
    
    if args.command == 'start':
        start_postgres()
    elif args.command == 'stop':
        stop_postgres()
    elif args.command == 'create-data':
        create_data()
    elif args.command == 'view-data':
        view_data()
    elif args.command == 'view-volume-info':
        show_volume()


if __name__ == "__main__":
    main()
