# Production Documentation Server

This guide shows you how to serve Toybox 2.0 documentation in production with automatic updates using systemd and git hooks.

## Overview

For production documentation serving, we recommend:

1. **Static Build** - Generate HTML files with `mkdocs build`
2. **Web Server** - Serve static files with Nginx/Apache
3. **Auto-Update** - Watch git repository for changes
4. **Systemd Service** - Ensure documentation stays running

## Architecture

```
┌──────────────────────────────────────────────────┐
│  Git Repository (GitHub/GitLab)                  │
│  - docs/ directory                               │
│  - mkdocs.yml                                    │
└─────────────────┬────────────────────────────────┘
                  │
                  │ Git Pull (manual or automated)
                  ▼
┌──────────────────────────────────────────────────┐
│  Production Server                               │
│  /var/www/toybox-docs/                          │
│  ├── docs/                                       │
│  ├── mkdocs.yml                                  │
│  └── site/  ← Generated HTML                    │
└─────────────────┬────────────────────────────────┘
                  │
                  │ File Watcher (inotify-tools)
                  │ or Git Hooks (post-merge)
                  ▼
┌──────────────────────────────────────────────────┐
│  Auto-Build Service (systemd)                    │
│  Watches: docs/, mkdocs.yml                     │
│  Action: mkdocs build                            │
└─────────────────┬────────────────────────────────┘
                  │
                  │ Serves static files
                  ▼
┌──────────────────────────────────────────────────┐
│  Nginx/Apache Web Server                         │
│  Port: 80/443                                    │
│  DocumentRoot: /var/www/toybox-docs/site/       │
└──────────────────────────────────────────────────┘
```

## Option 1: Static Build + Nginx (Recommended)

This is the most efficient and scalable approach.

### Step 1: Install Prerequisites

```bash
# Install web server
sudo apt update
sudo apt install nginx

# Install UV and Python
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Install git and file watcher
sudo apt install git inotify-tools
```

### Step 2: Clone Repository

```bash
# Create documentation directory
sudo mkdir -p /var/www/toybox-docs
sudo chown $USER:$USER /var/www/toybox-docs

# Clone repository
cd /var/www/toybox-docs
git clone <your-repo-url> .

# Or if already cloned elsewhere
rsync -av /opt/projects/toybox2/ /var/www/toybox-docs/
```

### Step 3: Build Documentation

```bash
cd /var/www/toybox-docs

# Install dependencies
uv sync --extra docs

# Build static site
uv run mkdocs build

# Verify output
ls -la site/
```

### Step 4: Configure Nginx

Create `/etc/nginx/sites-available/toybox-docs`:

```nginx
server {
    listen 80;
    server_name docs.toybox.local;  # Change to your domain
    
    root /var/www/toybox-docs/site;
    index index.html;
    
    # Enable gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript 
               application/javascript application/json application/xml+rss;
    
    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Main location
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

Enable site:

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/toybox-docs /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### Step 5: Add SSL/TLS (Optional but Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d docs.toybox.local

# Auto-renewal is configured automatically
```

### Step 6: Create Auto-Rebuild Script

Create `/usr/local/bin/rebuild-docs.sh`:

```bash
#!/bin/bash

# Configuration
DOCS_DIR="/var/www/toybox-docs"
LOG_FILE="/var/log/toybox-docs-rebuild.log"
LOCK_FILE="/tmp/toybox-docs-rebuild.lock"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Prevent concurrent builds
if [ -f "$LOCK_FILE" ]; then
    log_message "Build already in progress, skipping"
    exit 0
fi

# Create lock file
touch "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

log_message "Starting documentation rebuild"

cd "$DOCS_DIR" || exit 1

# Pull latest changes
log_message "Pulling latest changes from git"
git pull origin main >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    log_message "ERROR: Git pull failed"
    exit 1
fi

# Check if docs-related files changed
CHANGED_FILES=$(git diff HEAD@{1} HEAD --name-only)
if echo "$CHANGED_FILES" | grep -qE "^(docs/|mkdocs\.yml)"; then
    log_message "Documentation files changed, rebuilding"
    
    # Ensure dependencies are up to date
    uv sync --extra docs >> "$LOG_FILE" 2>&1
    
    # Build documentation
    uv run mkdocs build --clean >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        log_message "Documentation rebuilt successfully"
        
        # Set proper permissions
        chmod -R 755 site/
        
        # Optional: Clear nginx cache if using
        # sudo systemctl reload nginx
    else
        log_message "ERROR: Documentation build failed"
        exit 1
    fi
else
    log_message "No documentation changes detected, skipping rebuild"
fi

log_message "Rebuild process completed"
```

Make executable:

```bash
sudo chmod +x /usr/local/bin/rebuild-docs.sh

# Test manually
sudo /usr/local/bin/rebuild-docs.sh
```

### Step 7: Create Systemd Services

**Auto-rebuild on git changes:**

Create `/etc/systemd/system/toybox-docs-rebuild.service`:

```ini
[Unit]
Description=Toybox Documentation Auto-Rebuild Service
After=network.target

[Service]
Type=oneshot
User=www-data
Group=www-data
WorkingDirectory=/var/www/toybox-docs
ExecStart=/usr/local/bin/rebuild-docs.sh
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Periodic git pull and rebuild:**

Create `/etc/systemd/system/toybox-docs-rebuild.timer`:

```ini
[Unit]
Description=Rebuild Toybox Documentation Every 10 Minutes
Requires=toybox-docs-rebuild.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=10min
AccuracySpec=1min

[Install]
WantedBy=timers.target
```

Enable and start:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable timer
sudo systemctl enable toybox-docs-rebuild.timer

# Start timer
sudo systemctl start toybox-docs-rebuild.timer

# Check status
sudo systemctl status toybox-docs-rebuild.timer
sudo systemctl list-timers toybox-docs-rebuild.timer
```

## Option 2: MkDocs Development Server (Simple but Not Recommended)

For small teams or internal documentation, you can run `mkdocs serve` as a service.

### Systemd Service for MkDocs Serve

Create `/etc/systemd/system/toybox-docs.service`:

```ini
[Unit]
Description=Toybox Documentation Server
After=network.target

[Service]
Type=simple
User=toybox-docs
Group=toybox-docs
WorkingDirectory=/var/www/toybox-docs
Environment="PATH=/home/toybox-docs/.local/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/toybox-docs/.local/bin/uv run mkdocs serve -a 0.0.0.0:8011
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security hardening
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/www/toybox-docs

[Install]
WantedBy=multi-user.target
```

Create dedicated user:

```bash
# Create service user
sudo useradd -r -s /bin/bash -d /var/www/toybox-docs toybox-docs

# Set ownership
sudo chown -R toybox-docs:toybox-docs /var/www/toybox-docs

# Install UV for service user
sudo -u toybox-docs bash -c "curl -LsSf https://astral.sh/uv/install.sh | sh"
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable toybox-docs.service
sudo systemctl start toybox-docs.service
sudo systemctl status toybox-docs.service
```

**Reverse proxy with Nginx:**

```nginx
server {
    listen 80;
    server_name docs.toybox.local;
    
    location / {
        proxy_pass http://127.0.0.1:8011;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for live reload
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Option 3: Git Hooks for Instant Updates

For immediate updates on push, use git hooks.

### Post-Merge Hook

Create `/var/www/toybox-docs/.git/hooks/post-merge`:

```bash
#!/bin/bash

LOG_FILE="/var/log/toybox-docs-rebuild.log"

echo "[$(date)] Post-merge hook triggered" >> "$LOG_FILE"

# Rebuild documentation
cd /var/www/toybox-docs
uv run mkdocs build --clean >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date)] Documentation rebuilt successfully" >> "$LOG_FILE"
    chmod -R 755 site/
else
    echo "[$(date)] ERROR: Build failed" >> "$LOG_FILE"
    exit 1
fi
```

Make executable:

```bash
chmod +x /var/www/toybox-docs/.git/hooks/post-merge
```

### Automated Git Pull Script

Create cron job for automatic pulls:

```bash
# Edit crontab for deployment user
crontab -e

# Add this line (pulls every 10 minutes)
*/10 * * * * cd /var/www/toybox-docs && git pull origin main >> /var/log/toybox-docs-pull.log 2>&1
```

## Option 4: GitHub Actions Deployment

Automate deployment with GitHub Actions.

Create `.github/workflows/deploy-docs.yml`:

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      
      - name: Install dependencies
        run: uv sync --extra docs
      
      - name: Build documentation
        run: uv run mkdocs build --clean
      
      - name: Deploy to production server
        uses: easingthemes/ssh-deploy@v4
        with:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          REMOTE_HOST: ${{ secrets.REMOTE_HOST }}
          REMOTE_USER: ${{ secrets.REMOTE_USER }}
          SOURCE: "site/"
          TARGET: "/var/www/toybox-docs/site/"
```

## Monitoring and Maintenance

### Check Service Status

```bash
# Check documentation server
sudo systemctl status toybox-docs-rebuild.timer
sudo systemctl status nginx

# View recent rebuilds
sudo journalctl -u toybox-docs-rebuild.service -f

# Check rebuild logs
tail -f /var/log/toybox-docs-rebuild.log
```

### Monitor Nginx Access

```bash
# Access logs
tail -f /var/log/nginx/access.log

# Error logs
tail -f /var/log/nginx/error.log
```

### Performance Monitoring

```bash
# Check site size
du -sh /var/www/toybox-docs/site

# Check build time
time uv run mkdocs build
```

## Security Best Practices

### 1. Restrict Access

```nginx
# In Nginx config - IP whitelist
location / {
    allow 192.168.1.0/24;  # Your internal network
    allow 10.0.0.0/8;
    deny all;
    
    try_files $uri $uri/ =404;
}
```

### 2. Rate Limiting

```nginx
# In http block
limit_req_zone $binary_remote_addr zone=docs:10m rate=10r/s;

# In server block
location / {
    limit_req zone=docs burst=20 nodelay;
    try_files $uri $uri/ =404;
}
```

### 3. Authentication

```bash
# Install htpasswd
sudo apt install apache2-utils

# Create password file
sudo htpasswd -c /etc/nginx/.htpasswd docuser

# Add to Nginx config
location / {
    auth_basic "Documentation Access";
    auth_basic_user_file /etc/nginx/.htpasswd;
    try_files $uri $uri/ =404;
}
```

## Troubleshooting

### Service Won't Start

```bash
# Check systemd status
sudo systemctl status toybox-docs-rebuild.service

# Check journal logs
sudo journalctl -xe -u toybox-docs-rebuild.service

# Verify permissions
ls -la /var/www/toybox-docs
namei -l /var/www/toybox-docs/site
```

### Build Fails

```bash
# Manual build test
cd /var/www/toybox-docs
uv run mkdocs build --verbose

# Check dependencies
uv sync --extra docs

# Verify Python version
python --version
```

### Git Pull Issues

```bash
# Check git status
cd /var/www/toybox-docs
git status

# Verify remote
git remote -v

# Fix authentication
git config credential.helper store
```

## Performance Optimization

### 1. Enable Caching

```nginx
# In Nginx server block
location / {
    # HTML files - short cache
    location ~* \.html$ {
        expires 5m;
        add_header Cache-Control "public, must-revalidate";
    }
    
    # Static assets - long cache
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 2. Compress Assets

```bash
# Pre-compress files
cd /var/www/toybox-docs/site
find . -type f \( -name '*.html' -o -name '*.css' -o -name '*.js' \) -exec gzip -k9 {} \;
```

```nginx
# Serve pre-compressed files
gzip_static on;
```

### 3. Use CDN (Optional)

Point your domain to Cloudflare or similar CDN for:
- DDoS protection
- Global caching
- Automatic SSL
- Performance optimization

## Recommended Setup Summary

**For Production:**
1. ✅ Static build with Nginx
2. ✅ Systemd timer for auto-rebuild (every 10 minutes)
3. ✅ Git hooks for instant updates
4. ✅ SSL/TLS with Let's Encrypt
5. ✅ Monitoring with systemd journal
6. ✅ Backup strategy for `/var/www/toybox-docs`

**Quick Setup Commands:**

```bash
# One-time setup
sudo /usr/local/bin/setup-docs-server.sh

# Monitor
sudo systemctl status toybox-docs-rebuild.timer
tail -f /var/log/toybox-docs-rebuild.log

# Manual rebuild
sudo systemctl start toybox-docs-rebuild.service
```

This setup ensures your documentation is always up-to-date with minimal manual intervention!
