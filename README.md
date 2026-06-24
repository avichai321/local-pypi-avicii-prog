# Avicii Local PyPI Mirror 📦

A local, offline PyPI server for use in air-gapped or offline environments.
This project allows you to pre-download Python packages (Wheels) for both **Windows** and **Linux** platforms, and serve them locally using a lightweight PyPI server in Docker.

---

## 🚀 How it Works

1. **Define packages**: List the required libraries and versions in `requirements.txt`.
2. **Download packages (Online)**: Run the download script on an internet-connected machine to fetch the `.whl` files for both Windows and Linux.
3. **Start the server (Offline)**: Run the local PyPI server using Docker Compose to serve the downloaded packages.
4. **Install packages**: Configure pip on client machines to install libraries from this local mirror.

---

## 🛠️ Step-by-Step Guide

### Step 1: Define Packages
Open [requirements.txt](file:///home/avihayda/avicii-local-pypi/requirements.txt) and add the libraries you need.

### Step 2: Download Wheels (Run on an Internet-connected Machine)
The scripts automatically download the appropriate wheels for Windows (`win_amd64`) and Linux (`manylinux2014_x86_64`).

#### 🐧 On Linux:
Run the [download_packages.sh](file:///home/avihayda/avicii-local-pypi/download_packages.sh) script:
```bash
chmod +x download_packages.sh
./download_packages.sh
```

#### 🪟 On Windows:
Double-click [download_package.bat](file:///home/avihayda/avicii-local-pypi/download_package.bat) or run it from CMD:
```cmd
download_package.bat
```

All downloaded packages will be saved to a directory named `packages`.

---

### Step 3: Run the Local PyPI Server
Once the packages are downloaded, you can transfer the project folder to the offline environment and start the PyPI server:

```bash
docker-compose up -d
```

The server will run on port **`8080`** and will be accessible at: `http://localhost:8080` (or `http://<server-ip>:8080` on the local network).

---

## 📦 Package as a Portable Docker Image (Air-Gapped)

If you want to package the server and all downloaded packages into a single, self-contained Docker image that you can export and run anywhere without copying any folders:

> 💡 **Note:** Depending on your system permissions, you may need to prefix the `docker` and `docker-compose` commands with `sudo`.

### 1. Build the Self-Contained Image
Run this on your internet-connected machine (after downloading the packages). You can build it in one of two ways:

#### Option A: Build using Docker Compose
```bash
docker-compose build
```

#### Option B: Build using Docker CLI
```bash
docker build -t avicii-local-pypi:latest .
```

### 2. Export the Image to a File
Save the built image to a `.tar` archive:
```bash
docker save -o avicii-local-pypi.tar avicii-local-pypi:latest
```

### 3. Load the Image on the Offline Machine
Transfer the `avicii-local-pypi.tar` file to your air-gapped machine and load it:
```bash
docker load -i avicii-local-pypi.tar
```

### 4. Run the Container Offline
Start the container on the target machine. You don't need to copy any packages or mount any volumes, because the packages are already baked inside the image:
```bash
docker run -d -p 8080:8080 --name avicii_local_pypi --restart always avicii-local-pypi:latest
```

---

### Step 4: Install Packages on Client Machines
On any target computer (make sure it has network access to the server):

> 💡 **Tip:** If the PyPI server is hosted on a different machine, replace `localhost` with the server's IP address.

#### Install a single package:
```bash
pip install <package_name> --index-url http://localhost:8080/simple/ --trusted-host localhost
```

#### Install from requirements.txt:
```bash
pip install -r requirements.txt --index-url http://localhost:8080/simple/ --trusted-host localhost
```

---

### ⚙️ Permanent Pip Configuration (Optional)
To avoid typing the index URL and trusted host flags every time, you can configure pip globally on the client machines:

#### 🐧 On Linux / macOS:
Create or edit `~/.config/pip/pip.conf` and add:
```ini
[global]
index-url = http://localhost:8080/simple/
trusted-host = localhost
```

#### 🪟 On Windows:
Create or edit `%APPDATA%\pip\pip.ini` (typically `C:\Users\<Username>\AppData\Roaming\pip\pip.ini`) and add:
```ini
[global]
index-url = http://localhost:8080/simple/
trusted-host = localhost
```

Once configured, you can use normal `pip install` commands.
