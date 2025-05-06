## Minisaltproject

# Linkki puhtaaseen asennusohjeeseen tämän perusteella 
https://github.com/vmniemi/saltdocker/blob/main/README.md 






# Miksi docker saltstackissa ?
Eristys ja toistettavuus, Nopea käyttöönotto, Docker takaa että SaltStackin riippuvuudet ja versiot ovat aina oikeat ja hallinnassa 



## Tavoitteet projektilla

Olen kuullut jatkuvasti puhetta dockerista, joten päätin aloittaa siitä.Aloitin projektin miettimällä mitä kurssilla opetuista haluaisin opetella lisää. Olin jo aikaisemmin pohtinut näitä aiheita:

Jotain python kokeilua 

Git integraatio


Docker?


## Lopulliset tavoitteet

# 1. Saltstackin käyttö
   - Soveltaminen, tilojen ja moduulien kirjoittaminen ja itsevarmuuden kehittäminen
# 2. Dockerin opettelu
   - Mikä docker on, miten tuoda se saltilla
# 3. Gitin käyttö
   - Halusin opetella sen käyttöä enemmän
# 4 Python
   - En oikeastaan halua olla mikään koodari, mutta Pythonista on varmasti hyötyä backend ja infrahommissa. Lisäksi Saltstack on tehty Pythonilla.
   - Halusin siis kokeilla sillä asioita
 








# 1: Asennukset ja konffit

virtualbox

vagrant

salt

```ruby
$minion = <<MINION
sudo apt-get update
sudo apt-get -y install curl
sudo mkdir -p /etc/apt/keyrings
sudo curl -fsSL https://packages.broadcom.com/artifactory/api/security/keypair/SaltProjectKey/public | sudo tee /etc/apt/keyrings/salt-archive-keyring.pgp
sudo curl -fsSL https://github.com/saltstack/salt-install-guide/releases/latest/download/salt.sources | sudo tee /etc/apt/sources.list.d/salt.sources
sudo apt-get update
sudo apt-get -y install salt-minion
echo "master: 192.168.56.102" | sudo tee /etc/salt/minion
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
```



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





installs.sls (koko tiedosto erillisenä (installslsfinal.md))

![installsls](https://github.com/user-attachments/assets/f322e05e-5575-49c2-ae75-9963b9c04afb)



Lopuksi menin vielä top.sls ja 




   base:
    '*':
     - docker		




Ajoin sen 

	sudo salt '*' state.apply docker


Tuli tämänlainen joten menin orjalle ja 

	sudo systemctl restart salt-minion


 


 
 
![applydocker1](https://github.com/user-attachments/assets/3593f24e-4dd2-4df3-8e07-e28d362c7bf8)




tulin takaisin ja kokeilin uudestaan 


![apply2 1](https://github.com/user-attachments/assets/29328725-ff20-4148-83f1-806217fd7077)




![apply2 2](https://github.com/user-attachments/assets/e85391cb-9f6e-4122-87bc-74bb5a06cd72)












Testasin, että docker oli asennettu komennolla 

		sudo salt '*' cmd.run 'docker run hello-world'


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


Menin orjalle selvittämään sen nimen

![slaveid](https://github.com/user-attachments/assets/5a8283d3-9762-4de1-aafe-793bc7dfc78d)


user.sls tiedosto

![docker user1](https://github.com/user-attachments/assets/f4fa357e-9898-4534-a1a2-6e334ac4ce86)


Ajo 1

![docker user2](https://github.com/user-attachments/assets/a900e16b-1c43-40fb-98df-ed8b4e2d76b1)

Ajo 2


![docker user3](https://github.com/user-attachments/assets/b973cee5-e1a5-4fe6-80af-d72b748097ed)



Ja nyt docker images toimii

![dockerimageswork](https://github.com/user-attachments/assets/dbc10e2b-c294-4054-9a03-d6a0720458c3)

Voisin myös halutessani lisätä docker.pull_nginx top.sls jos haluaisin ajaa docker kansiossa olevia monia moduuleita samaan aikaan.

		sudo salt '*' state.apply docker

  vs
  
  		sudo salt '*' state.apply docker.pull_nginx



Tällä hetkellä docker kansio näyttää tältä

![dockertree1](https://github.com/user-attachments/assets/7475fe2b-7c10-480c-b208-f85358b510a8)



![srvsaltrakenne](https://github.com/user-attachments/assets/2dfa4572-cdbb-441c-a749-0fe253e89794)



# 3 Github

Loin ssh avainparin salt-masterille ja lisäsin sen julkisen avaimen omalle Github-tililleni, jotta voin saada sen sinne

	ssh-keygen


Laitoin vahingossa branchin master eikä main. 

![github1](https://github.com/user-attachments/assets/a3a46165-25a4-4608-93b8-820a497f969e)


Poistin masterin 

![master delete](https://github.com/user-attachments/assets/2c11d029-b18a-4817-b7b7-bc837ace1ec6)



Ja jouduin kikkailemaan aika paljon, mutta sain lopuksi tehtyä

![mainkikkailu](https://github.com/user-attachments/assets/8730e1d0-4a47-451c-89e3-531ff5ce96e7)


Testasin vielä varmasti, että toimii

![gittest1](https://github.com/user-attachments/assets/2f060ff7-00eb-4ffa-92f3-c232b8fbce51)


![gittest2](https://github.com/user-attachments/assets/39335b5c-49ff-4696-a5c5-e6df6f87ea61)




# 4 Lisäilyt ja jatkoprojekti ideat

GitFs: Sen avulla moduuleita voi vetää suoraan github reposta.



![mastergitfs](https://github.com/user-attachments/assets/2d639217-338e-49e2-8ca5-8839a58314f6)


![fileserver](https://github.com/user-attachments/assets/c1fa14f3-9e21-4451-8066-d9e335fd91bc)



	sudo apt-get install -y libgit2-dev
 	sudo apt-get install -y python3-pygit2


  Tämä error kuitenkin tulee, joten en tällä hetkellä pysty tekemään sitä


  ![gitfserror](https://github.com/user-attachments/assets/8d7e8b57-d924-4ae0-97f2-30b767382a03)




  # Check

  Tämä salt komento kertoo mitä tapahtuisi jos state.apply tehtäisiin eli testaa mitä tapahtuisi

  	sudo salt '*' state.apply test=True


Tämä näyttää mitä on suunniteltu tapahtuvan ja näyttää esim. syntaksin.

   	sudo salt '*' state.show_highstate

Halusin automatsoida tarkastuksen, että onko mitään muuttunut. Saltissa on niin sanottuja "runners", jotka pyörii vain masterilla eikä orjilla. Tätä varten pitää tehdä kansio niille.


![salt runner](https://github.com/user-attachments/assets/9274c092-5800-48b1-b404-5b1b8ad84fa4)



Lisäksi menin laittamaan custom moduulit ja runnerit päälle

	sudoedit /etc/salt/master 



	


![enablerunners](https://github.com/user-attachments/assets/145ff9de-57f8-488a-b144-0bc7912c7e3e)



Tein /srv/salt/_runners check.py tiedoston


Tässä siis käytetään 

	sudo salt '*' state.apply test=True
 tarkastamaan, onko mitään muutoksia


![checkpy](https://github.com/user-attachments/assets/4a318388-3750-421a-99a5-0f8d442c79cc)



	sudo systemctl restart salt-master
 	sudo salt-run saltutil.sync_runners
  	

![checkpy2](https://github.com/user-attachments/assets/164de2ad-41fd-4eea-a54a-1d6a22db9cdb)



Kävin korjaamassa kirjoitusvirheen

Itse tarkastus tehdään komennolla 

	sudo salt-run check.detect


![checkpy3](https://github.com/user-attachments/assets/a2c7a2e8-b794-4e09-b410-ab411335cf9e)




    
  # Koventaminen 

  
  # Pillars?, Grains?




  


 # Lähteet


https://terokarvinen.com/palvelinten-hallinta/

https://docs.saltproject.io/salt/user-guide/en/latest/topics/overview.html#rules-of-yaml

https://docs.saltproject.io/en/latest/ref/states/all/salt.states.docker_container.html

https://docs.docker.com/engine/install/debian/#install-using-the-repository

https://docker-py.readthedocs.io/en/stable/

https://assets.hostinger.com/content/tutorials/pdf/Docker-Cheat-Sheet.pdf

https://docs.saltproject.io/en/3006/topics/tutorials/gitfs.html

https://www.w3schools.com/python/



