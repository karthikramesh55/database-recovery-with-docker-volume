# Database Recovery with Docker Volume

A kata demonstrating how Docker volumes persist data even when containers are stopped and removed.
This kata uses a PostgreSQL alpine database instance as a container to investigate as to whether data stored in a Docker volume remains accessible after removing the container that was attached to the volume, and creating a new container.
The docker-compose YAML configures the PostgreSQL alpine database service container instantiation + exposure of source port onto the target port + volume attachment 

## Quick Start

### 1. Start PostgreSQL Container

```bash
python3 manage_postgresql_storage.py start
```

This creates and starts a PostgreSQL container with a named volume (`postgres_volume`) attached.

### 2. Create Sample Data

```bash
python3 manage_postgresql_storage.py create-data
```

This creates a `users` table and inserts sample records.

### 3. View Data

```bash
python3 manage_postgresql_storage.py view-data
```

Display all records from the users table.

### 4. Test Data Persistence

```bash
# Stop and remove the container
python3 manage_postgresql_storage.py stop

# Start a new container
python3 manage_postgresql_storage.py start

# Verify data still exists
python3 manage_postgresql_storage.py view-data
```

The data persists because it's stored in the Docker volume, not in the container!

The workflow is as follows:
1. Starting the PostgreSQL container
2. Creating synthetic data
3. Displaying the created data
4. Stopping and removing the container
5. Creating a new container
6. Verifying the created data persisted with the new container

## Available Commands

| Command | Description |
|---------|-------------|
| `start` | Start PostgreSQL container with volume |
| `stop` | Stop and remove container (volume persists) |
| `create-data` | Create sample table and insert data |
| `view-data` | Display current data in database |
| `view-volume-info` | Show Docker volume details |

## Configuration

The PostgreSQL configuration is defined in `docker-compose.yml`:

- **Database**: `testdb`
- **User**: `dbuser`
- **Password**: `dbpassword`
- **Port**: `5432`
- **Volume**: `postgres_volume`

## 📁 Project Structure

```
.
├── docker-compose.yml                       # Docker Compose configuration
├── manage_postgresql_storage.py             # Database management script
├── .env.example                             # Environment variables template (i.e. PostgreSQL database access)
└── README.md                                # README markdown content description
```

## Understanding Docker Volumes

### What happens when you run the commands:

1. **`docker-compose up`**: Creates container and volume (if not exists)
2. **`docker-compose down`**: Removes container BUT keeps the volume
3. **New container**: Mounts the existing volume with all data intact

### Volume Location

To inspect where Docker stores the volume data:

```bash
python3 manage_postgresql_storage.py volume-info
```

Or directly with Docker:

```bash
docker volume inspect postgres_volume
```

## Manual Testing

You can also interact with the database directly:

```bash
# Connect to PostgreSQL
docker exec -it postgres-persistent psql -U dbuser -d testdb

# Run SQL commands
testdb=# SELECT * FROM users;
testdb=# \dt  -- List tables
testdb=# \q   -- Quit
```

## Cleanup

To completely remove everything including the volume:

```bash
# Stop containers
python3 manage_postgresql_storage.py stop

# Remove the volume
docker volume rm postgres_volume
```

## Key points

- Docker volumes persist independently of container lifecycle
- Named volumes can be shared between container recreations
- Data stored in volumes survives `docker-compose down`
- Volumes are ideal for database storage in development
- Volume data can be backed up, restored, and migrated
