# ansible_playbook

## Synopsis

Run an Ansible playbook. Ansible is a free-software platform for configuring and managing computers which combines multi-node software deployment, ad hoc task execution, and configuration management.

Playbooks are Ansible’s configuration, deployment, and orchestration language. They can describe a policy you want your remote systems to enforce, or a set of steps in a general IT process.

This neuron can be used to perform complex operation with all [modules available from Ansible](http://docs.ansible.com/ansible/modules.html).


## Options

| parameter | required | default | choices | comment                                      |
|-----------|----------|---------|---------|----------------------------------------------|
| task_file | YES      |         |         | path to the Playbook file that contain tasks |



## Synapses example

Call the playbook named playbook.yml
```
   - name: "Ansible-test"
    neurons:
      - ansible_playbook: "playbook.yml"
      - say:
          message: "Tache terminée"
    signals:
      - order: "playbook"
```

Content of the playbook. This playbook will use the [URI module](http://docs.ansible.com/ansible/uri_module.html) to interact with a webservice on a remote server.
```
---
- name: Playbook
  hosts: localhost
  gather_facts: no
  connection: local

  tasks:   
    - name: "Call api"
      uri:
          url: "http://192.168.0.17:8000/app"
          HEADER_Content-Type: "application/json"
          method: POST
          user: admin
          password: secret
          force_basic_auth: yes
          status_code: 201
          body_format: json
          body: >
            {"app_name": "music", "state": "start"}
```


## Note

Ansible contain a lot of modules that can be useful for Kalliope

- [Notification](http://docs.ansible.com/ansible/list_of_notification_modules.html): can be used to send a message to Pushbullet, IRC channel, Rocket Chat and a lot of other notification services
- [Files](http://docs.ansible.com/ansible/list_of_files_modules.html): can be used to perform a backup or synchronize two file path
- [Windows](http://docs.ansible.com/ansible/list_of_windows_modules.html): Can be used to control a Windows Desktop

Shell neuron or script neuron can perform same actions. Ansible is just a way to simplify some execution or enjoy some [already made plugin](http://docs.ansible.com/ansible/modules_by_category.html). 

Here is the example of synapse you would use to perform a call to a web service without Ansible:
```
- name: "start-music"
    neurons:
      - shell:
          cmd: "curl -i --user admin:secret -H \"Content-Type: application/json\" -X POST -d '{\"app_name\":\"music\",\"state\":\"start\"}' http://192.168.0.17:8000/app"      
    signals:
      - order: "start music rock"
```
