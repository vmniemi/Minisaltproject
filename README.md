# Minisaltproject


## ToDo
# orjalle docker luvat (lisää group)
# Oma nettisivu nginx (flask?)
# Muut lisäosat (Git ja IDD?)
# Lisää docker säätöä?

Aloitin projektin miettimällä mitä kurssilla opetuista haluaisin opetella lisää. Olin jo aikaisemmin pohtinut näitä aiheita:

Jotain python kokeilua (Infrastructure Drift Detection?)
Git integraatio
Docker?

Olen kuullut jatkuvasti puhetta dockerista, joten päätin aloittaa siitä.

# 1: Asennukset ja konffit

virtualbox

vagrant

salt

    $minion = <<MINION
    sudo apt-get update
    sudo apt-get -y install curl
    sudo mkdir -p /etc/apt/keyrings
    sudo curl -fsSL https://packages.broadcom.com/artifactory/api/security/keypair/SaltProjectKey/public | sudo tee /etc/apt/keyrings/salt-archive-keyring.pgp
    sudo curl -fsSL https://github.com/saltstack/salt-install-guide/releases/latest/download/salt.sources | sudo tee /etc/apt/sources.list.d/salt.sources
    sudo apt-get update
    sudo apt-get -y install salt-minion
    echo "master: 192.168.56.102">/etc/salt/minion
    sudo systemctl restart salt-minion
    MINION

    $master = <<MASTER
    sudo apt-get update
    sudo apt-get -y install curl
    sudo curl -fsSL https://packages.broadcom.com/artifactory/api/security/keypair/SaltProjectKey/public | sudo tee /etc/apt/keyrings/salt-archive-keyring.pgp
    sudo curl -fsSL https://github.com/saltstack/salt-install-guide/releases/latest/download/salt.sources | sudo tee /etc/apt/sources.list.d/salt.sources
    sudo apt-get update
    sudo apt-get -y install salt-master
    MASTER

    Vagrant.configure("2") do |config|
	  config.vm.box = "debian/bookworm64"

	config.vm.define "slave1" do |slave1|
	    slave1.vm.provision :shell, inline: $minion
		slave1.vm.hostname = "slave1"
		slave1.vm.network "private_network", ip: "192.168.56.101"
	end

	config.vm.define "master", primary: true do |master|
		master.vm.provision :shell, inline: $master
		master.vm.hostname = "master"
		master.vm.network "private_network", ip: "192.168.56.102"
	  end
	
  end



![Salt1](https://github.com/user-attachments/assets/3d64b520-b014-4c77-bfbd-1c6b6e356571)


![salttest1](https://github.com/user-attachments/assets/d415ee47-3a9b-4088-87f1-4ef803f084af)


# 2 Itse docker



srv/salt kansion luonti

 	sudo mkdir -p srv/salt
  	cd srv/salt


![srvsalt](https://github.com/user-attachments/assets/2ce4a8c4-ac29-4bac-a176-362fcf461c79)

![dockersrv](https://github.com/user-attachments/assets/06e41597-b9e3-4ab8-bfd9-9c0fcba41330)



   Sisälle loin docker kansion,  jonka sisällä on init.sls ja install.sls

   init.sls

   ![dockerinitsls](https://github.com/user-attachments/assets/a225b08a-811f-46c7-a86d-4b564fc4475d)





installs.sls (koko tiedosto erillisenä (tiedostonimi))

![installsls](https://github.com/user-attachments/assets/f322e05e-5575-49c2-ae75-9963b9c04afb)



Lopuksi menin vielä top.sls ja 




   base:
    '*':
     - docker		



	sudo salt '*' state.apply docker


Tuli tämänlainen joten menin orjalle ja 

	sudo systemctl restart salt-minion


 


 
 
![applydocker1](https://github.com/user-attachments/assets/3593f24e-4dd2-4df3-8e07-e28d362c7bf8)




tulin takaisin ja kokeilin uudestaan 


![apply2 1](https://github.com/user-attachments/assets/29328725-ff20-4148-83f1-806217fd7077)




![apply2 2](https://github.com/user-attachments/assets/e85391cb-9f6e-4122-87bc-74bb5a06cd72)












Testasin, että docker oli asennettu komennolla 




 ![hellodocker](https://github.com/user-attachments/assets/fde67ad1-4bb1-41ff-bace-85b720c4d912)




Tein vielä simppelin automatisoidoin testin test.sls /srv/salt/docker kansioon jossa on 



![testauto](https://github.com/user-attachments/assets/cf3955a8-692e-4644-b441-1c3d05a8e269)


Testasin ajamalla 

	sudo salt '*' state.apply docker.test


![docker test](https://github.com/user-attachments/assets/45cd737a-6cc5-4ba2-a198-358bd5c934a4)


Sama lopputulos kuin manuaalisella komennolla 



Olin vielä epäilevä, koska kaikki oli mennyt liian hyvin joten halusin varmasti varmistaa, että docker on oikeasti asennettu 

Tämä toimii

![slavetest1](https://github.com/user-attachments/assets/492211a1-019c-4696-9e6f-418ab7e54dde)


Tämä ei toimi 

![slavetest2](https://github.com/user-attachments/assets/d43fc546-da84-4339-964e-4e3a4fd28605)

Perehtyessäni dockeriin enemmän,   https://docker-py.readthedocs.io/en/stable/,  dockeri voi myös toimia pythonilla, joten kokeilin 

	sudo salt '*' pip.install docker


 ![pipinstall](https://github.com/user-attachments/assets/e66d9be7-97a6-4ec8-909d-e5c1aa352ddd)



Ja nyt se toimii


![docker ver2](https://github.com/user-attachments/assets/97a21f1f-7267-4cb2-9a93-5b88a64a1ae6)



Nyt voin dockeria voi (toivottavasti) alkamaan käyttämään. Kokeilin ensiksi iha perus nginx pull


![nginxpull1](https://github.com/user-attachments/assets/49e62dcd-4a04-4c80-898b-8bc4c4a7287c)


Ensimmäisen kerran


![nginxpull2](https://github.com/user-attachments/assets/afa6e0fb-ab69-4eda-8672-d66ef68b5a6c)



Uudestaan (idempotentti)

![nginxpull3](https://github.com/user-attachments/assets/3ace1c28-3cc3-40d6-9bf2-46df15323c6f)


Kävin tässä vaiheessa varmuuden vuoksi tarkistamassa, että docker on asenettu ja pyörii

![dockerlocal1](https://github.com/user-attachments/assets/1d25863a-f715-406a-b222-7619ad7e5f88)


Kun yritin käyttää docker images, orjalla ei ollut lupia


![local1problem](https://github.com/user-attachments/assets/982c96c5-edcc-40ee-9fcb-bfed92ebd2dd)




Voisin myös halutessani lisätä docker.pull_nginx top.sls jos haluaisin ajaa docker kansiossa olevia monia moduuleita samaan aikaan.

		sudo salt '*' state.apply docker

  vs
  
  		sudo salt '*' state.apply docker.pull_nginx






 # Lähteet




https://docs.saltproject.io/en/latest/ref/states/all/salt.states.docker_container.html

https://docs.docker.com/engine/install/debian/#install-using-the-repository

https://docker-py.readthedocs.io/en/stable/

https://assets.hostinger.com/content/tutorials/pdf/Docker-Cheat-Sheet.pdf

https://docs.saltproject.io/en/3006/topics/tutorials/gitfs.html



