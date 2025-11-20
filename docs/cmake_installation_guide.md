# CMake Installation and Configuration Guide

## Problem

When attempting to use the Kitware APT repository to update CMake, we encountered GPG key verification errors:

```
W: GPG error: https://apt.kitware.com/ubuntu jammy InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 16FAAD7AF99A65E2
E: The repository 'https://apt.kitware.com/ubuntu jammy InRelease' is not signed.
```

**Root Causes:**
1. Missing or expired GPG key for the Kitware repository
2. Permission issues with existing keyring files
3. Multiple conflicting repository configurations
4. Network connectivity issues with keyservers (Intel proxy restrictions)

**Additional Issue:**
- Ubuntu 22.04 (Jammy) standard repositories only provide CMake 3.22.1
- Latest CMake 4.2.0 not available through standard APT repositories

## Solution: Manual Installation from GitHub

### Step 1: Download Latest CMake Binary

```bash
# Check latest version
curl -s https://api.github.com/repos/Kitware/CMake/releases/latest | grep "tag_name" | cut -d '"' -f 4

# Download CMake 4.2.0 installer
cd /tmp
wget https://github.com/Kitware/CMake/releases/download/v4.2.0/cmake-4.2.0-linux-x86_64.sh
```

### Step 2: Install to /opt/cmake

```bash
# Make installer executable
chmod +x cmake-4.2.0-linux-x86_64.sh

# Install to /opt/cmake (requires sudo)
sudo bash ./cmake-4.2.0-linux-x86_64.sh --prefix=/opt/cmake --skip-license
```

### Step 3: Configure System to Use New CMake

```bash
# Register with update-alternatives
sudo update-alternatives --install /usr/bin/cmake cmake /opt/cmake/bin/cmake 1 --force

# Fix permissions (critical step!)
sudo chmod -R 755 /opt/cmake
```

### Step 4: Verify Installation

```bash
# Check version
cmake --version
# Output: cmake version 4.2.0

# Check location
which cmake
# Output: /usr/bin/cmake
```

## Troubleshooting

### Permission Denied Error
If you get "Permission denied" when running cmake:
```bash
sudo chmod -R 755 /opt/cmake
```

### Old Version Still Appears
If the old version (3.22.1) is still active:
```bash
# Check alternatives
sudo update-alternatives --config cmake

# Force refresh
hash -r
```

### Switch Between Versions
To switch between installed CMake versions:
```bash
sudo update-alternatives --config cmake
# Select the version you want from the menu
```

## Cleanup (Optional)

Remove temporary installer:
```bash
rm -f /tmp/cmake-4.2.0-linux-x86_64.sh
```

Remove problematic Kitware repository configuration:
```bash
sudo rm -f /etc/apt/sources.list.d/*kitware*
sudo rm -f /etc/apt/trusted.gpg.d/kitware.gpg
sudo apt update
```

## Installation Locations

| Component | Location |
|-----------|----------|
| CMake binary | `/opt/cmake/bin/cmake` |
| Symlink | `/usr/bin/cmake` → `/etc/alternatives/cmake` → `/opt/cmake/bin/cmake` |
| Supporting tools | `/opt/cmake/bin/` (ccmake, cpack, ctest, cmake-gui) |
| Old CMake (APT) | `/usr/bin/cmake` (priority 0, inactive) |

## Version Information

- **Installed:** CMake 4.2.0
- **Previous:** CMake 3.22.1 (Ubuntu APT)
- **Installation Date:** November 19, 2025
- **Installation Method:** GitHub binary release

## Notes

- The old CMake 3.22.1 from APT remains installed but is not used by default
- `update-alternatives` manages version switching automatically
- This installation is system-wide and accessible to all users
- The installation does not conflict with Python/UV virtual environments
- CMake modules and data files are located in `/opt/cmake/share/cmake-4.2/`

## Alternative Installation Methods (Not Used)

We attempted but did not succeed with:
1. **APT with Kitware repository** - GPG key verification failed
2. **Snap package** - Unable to contact snap store (network restrictions)
3. **Building from source** - Not attempted due to time constraints

The manual binary installation proved to be the most reliable method in this environment.
