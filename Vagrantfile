# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 8888, host: 8888

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  config.vm.synced_folder "./", "/code"
  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
   config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
     vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
     vb.memory = "4096"
     vb.cpus = "2"
     vb.name = "AUFACE"

  end
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
    sudo apt-get upgrade


    # Install developer tools used to compile OpenCV 3.2
    sudo apt-get install -y build-essential cmake git pkg-config
    # Install libraries and packages used to read various image formats from
    # disk
    sudo apt-get install -y libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev
    # Install a few libraries used to read video formats from disk
    sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
    # Install GTK so we can use OpenCV’s GUI features
    sudo apt-get install -y libgtk2.0-dev
    # Install packages that are used to optimize various functions inside
    # OpenCV, such as matrix operations
    sudo apt-get install -y libatlas-base-dev gfortran

    # install graphviz to allow for graph plotting
    sudo apt-get install -y graphviz graphviz-dev

    sudo apt-get install imagemagick

    # Install Python 3, Pip and some other tools
    sudo apt-get -y install python3 python3-pip python3.4-dev

    sudo apt-get -y install python3-matplotlib
    #
    

    sudo pip3 install virtualenvwrapper
    sudo pip3 install suplemon

    sudo apt-get install build-essential cmake
    sudo apt-get install libgtk-3-dev
    sudo apt-get install libboost-all-dev
    

    # Fix locale to UTF-8
    sudo echo "export LANGUAGE=en_US.UTF-8" >> /home/vagrant/.bashrc
    sudo echo "export LANG=en_US.UTF-8" >> /home/vagrant/.bashrc
    sudo echo "export LC_ALL=en_US.UTF-8" >> /home/vagrant/.bashrc

    export LANGUAGE=en_US.UTF-8
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8

    # Make virtual environment and install the required Python packages
    mkdir ~/.virtualenvs
    sudo echo "export WORKON_HOME=~/.virtualenvs" >> /home/vagrant/.bashrc
    sudo echo "VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'" >> /home/vagrant/.bashrc
    sudo echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc

    export WORKON_HOME=~/.virtualenvs
    export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'
    source /usr/local/bin/virtualenvwrapper.sh

    mkvirtualenv cv

    pip install numpy
    pip install scipy
    pip install scikit-image
    pip install pillow
 
   


    # This is necessary to get matplotlib support from system-wide
    # Debian package
    toggleglobalsitepackages


    sudo apt-get install -y git
    cd ~
    git clone https://github.com/opencv/opencv.git
    cd opencv
    git checkout 3.1.0
    cd ~
    git clone https://github.com/opencv/opencv_contrib.git
    cd opencv_contrib
    git checkout 3.1.0
    
    cd ~/opencv
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
	  -D CMAKE_INSTALL_PREFIX=/usr/local \
	  -D INSTALL_C_EXAMPLES=OFF \
	  -D INSTALL_PYTHON_EXAMPLES=ON \
	  -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	  -D BUILD_EXAMPLES=ON ..

    make -j2

    sudo make install
    sudo ldconfig

    cd ~/.virtualenvs/cv/lib/python3.4/site-packages/
    ln -s /usr/local/lib/python3.4/site-packages/cv2.cpython-34m.so cv2.so

    # Install XFce
    sudo apt-get install xfce4
    sudo apt-get install -y xfce4 virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11
    sudo apt-get install -y gnome-icon-theme-full tango-icon-theme
    # Permit anyone to start the GUI
    sudo sed -i 's/allowed_users=.*$/allowed_users=anybody/' /etc/X11/Xwrapper.config

    sudo VBoxClient --clipboard
    sudo VBoxClient --draganddrop
    sudo VBoxClient --display
    sudo VBoxClient --checkhostversion
    sudo VBoxClient --seamless

    # Install Firefox and geckodriver so that we can get selenium to work
    sudo apt-get install -y firefox
    mkdir /home/vagrant/bin
    cd /home/vagrant/bin
    wget https://github.com/mozilla/geckodriver/releases/download/v0.13.0/geckodriver-v0.13.0-linux64.tar.gz
    tar -xvzf geckodriver-v0.13.0-linux64.tar.gz
    rm geckodriver-v0.13.0-linux64.tar.gz
    chmod +x geckodriver
    sudo ln -s ~/bin/geckodriver /usr/local/bin/


    # Install Webcam drivers
    
    sudo apt-get install build-essential linux-headers-`uname -r`
    sudo apt-get install guvcview


    # Install PyCharm
    sudo apt-get purge openjdk*
    sudo apt-get -y install software-properties-common
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get -y update
    echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
    echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
    sudo apt-get -y install oracle-java8-installer
    sudo update-java-alternatives -s java-8-oracle

    wget -q -O - http://archive.getdeb.net/getdeb-archive.key
    sudo sh -c 'echo "deb http://archive.getdeb.net/ubuntu trusty-getdeb apps" >> /etc/apt/sources.list.d/getdeb.list'
    sudo apt-get update
    sudo apt-get install -y --force-yes pycharm

    echo "==================================================================="
    echo "=                             DONE                                ="
    echo "==================================================================="
    echo "To log onto the VM:"
    echo "$ vagrant ssh or use putty 127.0.0.1:2222 vagrant/vagrant"
    echo "To start the GUI:"
    echo "$ startxfce4&"
    echo "$ cd /code"
    echo "$ workon cv"
  SHELL
end
