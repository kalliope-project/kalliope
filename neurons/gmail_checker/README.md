# gmail_checker

## Synopsis

This neuron access to Gmail and gives the number of unread mails and their titles.

## Options

| parameter | required | default | choices | comment    |
|-----------|----------|---------|---------|------------|
| username  | YES      |         |         | User info. |
| password  | YES      |         |         | User info. |

## Return Values

| Name     | Description                                  | Type | sample                                                       |
|----------|----------------------------------------------|------|--------------------------------------------------------------|
| unread   | Number of unread messages                    | int  | 5                                                            |
| subjects | A List with all the unread messages subjects | list | ['Kalliope commit', 'Beer tonight?', 'cats have superpower'] |

## Synapses example

Simple example : 

```
  - name: "check-email"
    neurons:
      - gmail_checker:
          username: "me@gmail.com"
          password: "my_password"
          say_template: 
            -  "You have {{ unread }} new emails"
    signals:
      - order: "Do I have emails"
```

A complex example that read subject emails. This is based on a file_template
```
  - name: "check-email"
    neurons:
      - gmail_checker:
          username: "me@gmail.com"
          password: "my_password"
          file_template: /templates/my_email_template.j2            
    signals:
      - order: "Do I have emails"
```

Here the content of the `my_email_template.j2`
```
You have {{ unread }} email

{% set count = 1 %}
{% if unread > 0 %}
    {% for subject in subjects %}
     email number {{ count }}. {{ subject }}
     {% set count = count + 1 %}
    {% endfor %}
{% endif %}
```
## Notes

Gmail now prevent some mailbox to be accessed from tier application. If you receive a mail like the following:
```
Sign-in attempt prevented ... Someone just tried to sign in to your Google Account mail@gmail.com from an app that doesn't meet modern security standards.
```

You can allow this neuron to get un access to your email in your [Gmail account settings](https://www.google.com/settings/security/lesssecureapps).