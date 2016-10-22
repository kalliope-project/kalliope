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


## Notes

