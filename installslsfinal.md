```yaml
install_prerequisites:
  pkg.installed:
    - pkgs:
      - ca-certificates
      - curl
      - gnupg
      - lsb-release

create_keyring_directory:
  file.directory:
    - name: /etc/apt/keyrings
    - mode: 0755

add_docker_gpg_key:
  cmd.run:
    - name: >
        curl -fsSL https://download.docker.com/linux/debian/gpg |
        gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    - creates: /etc/apt/keyrings/docker.gpg
    - require:
      - pkg: install_prerequisites
      - file: create_keyring_directory

add_docker_repository:
  file.managed:
    - name: /etc/apt/sources.list.d/docker.list
    - contents: |
        deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable
    - require:
      - cmd: add_docker_gpg_key

update_package_index:
  cmd.run:
    - name: apt-get update
    - require:
      - file: add_docker_repository

install_docker:
  pkg.installed:
    - pkgs:
      - docker-ce
      - docker-ce-cli
      - containerd.io
      - docker-buildx-plugin
      - docker-compose-plugin
    - require:
      - cmd: update_package_index

start_and_enable_docker:
  service.running:
    - name: docker
    - enable: True
    - require:
      - pkg: install_docker
```
