Vagrant.configure(2) do |config|

  config.vm.box = "hashicorp/precise32"
  config.vm.provision :shell, path: "vagrantsetup.sh"



  config.vm.network :forwarded_port, guest: 80, host: 4567

  config.vm.network "public_network"

  config.vm.host_name = "sitegenerator"

  config.ssh.forward_x11 = true



end
