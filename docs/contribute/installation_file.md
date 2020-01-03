# install.yml file

The installation file, called install.yml, must be placed at the root of a repository. This one will be read by Kalliope in order to install your module from the [command line](../cli.md) by any Kalliope user.

## How to create an install.yml file

The module installation process is based on the Ansible program. Ansible is an IT orchestrator. It means it can help you to perform configuration management, application deployment or task automation.

The `install.yml` file must contains what we called a Playbook in the Ansible world.
A playbook is like a recipe or an instructions manual which tells Ansible what to do against an host. In our case, the host will be the local machine of the current user who asked Kalliope to install the module.

Let's see a basic playbook, the one used by the neuron wikipedia_searcher

```yaml
- name: Kalliope wikipedia_searcher neuron install
  hosts: localhost
  gather_facts: no
  connection: local
  become: true

  tasks:
    - name: "Install pip dependencies"
      pip:
        name: wikipedia
        version: 1.4.0
        executable: pip3
```

As the file is a **playbook**, it can contains multiple **play**. That's why the file start with a "-", the yaml syntax to define a list of element. In this example, our playbook contains only one play.

The first element is the `name`. It can be anything you want. Here we've set what the play do.

The `hosts` parameter is, like the name sugest us, to design on which host we want to apply our configuration. In the context of a Kalliope module installation, it will always be **localhost**.

By default, ansible call a module to [gather useful variables](http://docs.ansible.com/ansible/setup_module.html) about remote hosts that can be used in playbooks.
In this example, we don't need it and so we disable the `gather_facts` feature in order to win a couple seconds during the installation process.

In most of case, our play will need to apply admin operations. In this case, installing a python lib. So we set `become` to true to be allowed to install our lib as root user.

The next part is `tasks`. This key must contains a list of task to apply on the target system.

The only task we've added here is based on the [pip Ansible module](http://docs.ansible.com/ansible/pip_module.html).

Ansible comes with a lot of modules, see the [complete list here](http://docs.ansible.com/ansible/modules_by_category.html).

Here is an example which use the [apt module](http://docs.ansible.com/ansible/apt_module.html) to install Debian packages
```yaml
tasks:
  - name: Install packages
    apt: name={{ item }} update_cache=yes
    with_items:
      - flac
      - mplayer
```
