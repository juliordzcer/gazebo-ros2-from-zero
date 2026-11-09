# Gazebo & ROS 2 from zero

Code, files and commands for the YouTube series **Gazebo from zero**, **ROS 2 from zero** and **ROS 2 + Gazebo**.
Every video has its own folder with what you need to follow along.

Versions used in the series:

| What | Version | Support |
| --- | --- | --- |
| Ubuntu | 24.04 LTS (Noble) | until 2029 |
| Gazebo | Harmonic (`gz sim` 8), LTS | until May 2029 |
| ROS 2 | Jazzy (later in the series) | officially paired with Harmonic |

## Install Gazebo Harmonic on Ubuntu 24.04

These are the official steps from
[gazebosim.org/docs/harmonic/install_ubuntu](https://gazebosim.org/docs/harmonic/install_ubuntu/),
explained one by one as in video 1. On Windows, run the same steps inside WSL2 with Ubuntu 24.04.

`sudo` runs a command as administrator, so it will ask for your password. `apt` is Ubuntu's package manager:
it downloads and installs software from repositories.

```bash
# 1) Refresh the list of available packages (it doesn't install anything)
sudo apt-get update

# 2) Three small tools: curl (downloads files), lsb-release (tells your Ubuntu version),
#    gnupg (checks digital signatures). Answer "y" when apt asks to continue.
sudo apt-get install curl lsb-release gnupg

# 3) Download Gazebo's signing key: apt uses it to check the packages really come from the Gazebo team
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg

# 4) Add Gazebo's repository to apt's sources. The line uses your architecture (amd64)
#    and your Ubuntu code name (noble); tee writes it to the file as administrator.
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# 5) Refresh again: now apt also knows the Gazebo packages
sudo apt-get update

# 6) Install Gazebo Harmonic (one package with everything; it takes a few minutes)
sudo apt-get install gz-harmonic
```

Check it:

```bash
gz sim --versions     # prints 8.x
gz sim                # opens the quick start window
```

Useful options: `-r` starts the simulation running, `-s` server only (no window), `-g` window only,
`-v 4` more messages when something goes wrong.

To uninstall: `sudo apt remove gz-harmonic && sudo apt autoremove`

## Videos

| # | Video | Folder |
| --- | --- | --- |
| G1 | Install Gazebo Harmonic and first steps | [g01](g01) |

More folders are added with each new video.

## License

MIT: use and copy anything here freely.
