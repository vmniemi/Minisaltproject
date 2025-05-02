add-docker-user:
  user.present:
    - name: deploy

add-user-to-docker-group:
  group.present:
    - name: docker
    - addusers:
      - deploy
