# ansible_playbook

## Synopsis

Run an Ansible playbook. Ansible is a free-software platform for configuring and managing computers which combines multi-node software deployment, ad hoc task execution, and configuration management.

Playbooks are Ansible’s configuration, deployment, and orchestration language. They can describe a policy you want your remote systems to enforce, or a set of steps in a general IT process.

This neuron can be used to perform complex operation with all [modules available from Ansible](http://docs.ansible.com/ansible/modules.html).

## Installation

CORE NEURON : No installation needed.  

## Options

| parameter     | required | default | choices      | comment                                                                                                                          |
|---------------|----------|---------|--------------|----------------------------------------------------------------------------------------------------------------------------------|
| task_file     | YES      |         |              | path to the Playbook file that contains tasks                                                                                    |
| sudo          | NO       | FALSE   | True | False | If the playbook will require root privileges (become=true) , this must be set to True and sudo_user and password set accordingly |
| sudo_user     | NO       |         |              | The target user with admin privileges. In most of case "root"                                                                    |
| sudo_password | NO       |         |              | The password of the sudo_user                                                                                                    |



## Synapses example

### Playbook without admin privileges

Call the playbook named playbook.yml
```yml
  - name: "Ansible-test"
    signals:
      - order: "playbook"
    neurons:
      - ansible_playbook: 
          task_file: "playbook.yml"
      - say:
          message: "The task is done"
```

Content of the playbook. This playbook will use the [URI module](http://docs.ansible.com/ansible/uri_module.html) to interact with a webservice on a remote server.
```yml
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

### Playbook with admin privileges

In some cases, a playbook requires sudo right to perform admin operations like installing a package.
In this case, you must give to the neuron the login and password of the user which has admin privileges.
```yml
  - name: "Ansible-root"
    signals:
      - order: "playbook"
    neurons:
      - ansible_playbook:
          task_file: "playbook-root.yml"
          sudo: true
          sudo_user: "root"
          sudo_password: "secret"
```

And the playbook would be. Notice that we use `become: True`
```yml
- hosts: localhost
  gather_facts: no
  connection: local
  become: True

  tasks:
    - name: "Install a useful train package"
      apt:
        name: sl
        state: present
```

## Note

Ansible contains a lot of modules that can be useful for Kalliope

- [Notification](http://docs.ansible.com/ansible/list_of_notification_modules.html): can be used to send a message to Pushbullet, IRC channel, Rocket Chat and a lot of other notification services
- [Files](http://docs.ansible.com/ansible/list_of_files_modules.html): can be used to perform a backup or synchronize two file path
- [Windows](http://docs.ansible.com/ansible/list_of_windows_modules.html): Can be used to control a Windows Desktop

Shell neuron or script neuron can perform same actions. Ansible is just a way to simplify some execution or enjoy some [already made plugin](http://docs.ansible.com/ansible/modules_by_category.html). 
