docker-packages:
  pkg.installed:
    - pkgs:
      - docker.io

docker-config-dir:
  file.directory:
    - name: /etc/docker
    - user: root
    - group: root
    - mode: 755

docker-service:
  service.running:
    - name: docker
    - enable: True
    - reload: True
