#!/bin/bash -eu
set -e

VERSION=4.1.2
VARIANT=thonny

ARCHITECTURE="$(uname -m)"
if [[ "$ARCHITECTURE" == "x86_64" ]]; then
  echo
  echo "This script will download and install Thonny ($VARIANT-$VERSION) for Linux (32 or 64-bit PC)."
  read -p "Press ENTER to continue or Ctrl+C to cancel."

  FILENAME=$VARIANT-$VERSION-$ARCHITECTURE.tar.gz
  URL="https://github.com/thonny/thonny/releases/download/v$VERSION/$FILENAME"

  echo "Downloading $URL"

  TMPDIR=$(mktemp -d -p .)
  wget -O $TMPDIR/$FILENAME $URL
  tar -zxf $TMPDIR/$FILENAME -C $TMPDIR
  $TMPDIR/thonny/install
  rm -rf $TMPDIR

  echo
  read -p "Press ENTER to exit the installer."
else
  echo "Thonny only provides pre-built bundles for x86_64 (not $ARCHITECTURE)."
  TARGET=~/apps/thonny
  PYVER="$(python3 -V 2>&1)"
  GOODVER="Python 3\.(8|9|10|11|12)\.*"
  if [[ "$PYVER" =~ $GOODVER ]]; then
    PYLOC="$(which python3 2>&1)"
    echo "I could install Thonny into a venv under your existing $PYVER ($PYLOC)."
    read -p "Press ENTER to continue or Ctrl+C to cancel."

    # Install non-pip dependencies
    if [[ -f /etc/debian_version ]]; then
      if ! dpkg -s python3-tk > /dev/null ; then
        echo "Going to install 'python3-tk' first"
        sudo apt-get install python3-tk
      fi
      if ! dpkg -s python3-venv > /dev/null ; then
        echo "Going to install 'python3-venv' first"
        sudo apt-get install python3-venv
      fi
    elif [[ -f /etc/redhat-release ]]; then
      if rpm -qa | grep python3-tkinter > /dev/null ; then
        echo "Going to install 'python3-tkinter' first"
        sudo yum install python3-tkinter
      fi
    elif [[ -f /etc/SuSE-release ]]; then # TODO: this file is deprecated
      if ! rpm -qa | grep python3-tkinter > /dev/null ; then
        echo "Going to install 'python3-tkinter' first"
        sudo zypper install python3-tkinter
      fi
    elif [[ -f /etc/arch-release ]]; then
      if ! pacman -Qi tk > /dev/null ; then
        echo "Going to install 'tk' first"
        sudo pacman -S tk
      fi
    else
      echo "Can't determine your package manager, assuming Tkinter and venv are present."
    fi

    if [[ -d $TARGET ]]; then
      echo "Removing existing Thonny installation at $TARGET"
      rm -rf $TARGET
    fi

    echo "Creating virtual environment for Thonny"
    python3 -m venv $TARGET

    echo "Marking virtual environment as private to Thonny"
    echo ";Existence of this file indicates that Python in this directory is private for Thonny" > ${TARGET}/bin/thonny_python.ini

    echo "Installing Thonny's dependencies"
    $TARGET/bin/pip3 install 'jedi==0.18.*' 'pyserial==3.5' 'pylint==2.17.*' 'docutils==0.20.*' 'mypy==1.5.*' 'asttokens==2.2.*' 'Send2Trash==1.8.*' 'esptool==4.6.*' 'bcrypt==3.2.*' 'cryptography==38.*' 'paramiko==3.2.*' 'websockets==11.0.*' 'ptyprocess==0.7.*; sys_platform == "linux" or sys_platform == "darwin"' 'adafruit_board_toolkit==1.1.*; sys_platform == "win32" or sys_platform == "darwin"' 'dbus-next==0.2.*; sys_platform == "linux"'
    echo "Installing Thonny and its dependencies"
    $TARGET/bin/pip3 install thonny==${VERSION}

    echo "Creating the launcher"
    LAUNCHER=~/.local/share/applications/Thonny.desktop
    SITE_PACKAGES=$($TARGET/bin/python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
    echo "[Desktop Entry]" > $LAUNCHER
    echo "Type=Application" >> $LAUNCHER
    echo "Name=Thonny" >> $LAUNCHER
    echo "GenericName=Python IDE" >> $LAUNCHER
    echo "Exec=$TARGET/bin/thonny %F" >> $LAUNCHER
    echo "Comment=Python IDE for beginners" >> $LAUNCHER
    echo "Icon=$SITE_PACKAGES/thonny/res/thonny.png" >> $LAUNCHER
    echo "StartupWMClass=Thonny" >> $LAUNCHER
    echo "Terminal=false" >> $LAUNCHER
    echo "Categories=Development;IDE" >> $LAUNCHER
    echo "Keywords=programming;education" >> $LAUNCHER
    echo "MimeType=text/x-python;" >> $LAUNCHER
    echo "Actions=Edit;" >> $LAUNCHER
    echo "" >> $LAUNCHER
    echo "[Desktop Action Edit]" >> $LAUNCHER
    echo "Exec=$TARGET/bin/thonny %F" >> $LAUNCHER
    echo "Name=Edit with Thonny" >> $LAUNCHER

    UNINSTALLER="${TARGET}/bin/uninstall"
    echo "Creating the uninstaller ($UNINSTALLER)"
    echo "#!/usr/bin/env bash" > $UNINSTALLER
    echo "rm -rf $TARGET"
    echo "rm $LAUNCHER"
  else
    echo "Can't offer alternatives as your system doesn't seem to have suitable Python interpreter."
    exit 1
  fi
fi
