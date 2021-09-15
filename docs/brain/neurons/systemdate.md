Give the current time from the system where Kalliope is installed. Return a dict of parameters that can be used in a template.

## Input parameters

None

## Returned values

| name      | description                                       | type   | sample |
| --------- | ------------------------------------------------- | ------ | ------ |
| hours     | Hour (24-hour clock) as a decimal number [00,23]. | string | 22     |
| minutes   | Minute as a decimal number [00,59].               | string | 54     |
| weekday   | Weekday as a decimal number [0(Sunday),6].        | string | 4      |
| month     | Month as a decimal number [01,12].                | string | 4      |
| day_month | Day of the month as a decimal number [01,31].     | string | 12     |
| year      | Year with century as a decimal number             | string | 2016   |

## Synapses example

Simple synapse that give the current time with only hours and minutes

```yaml
- name: "time"
  signals:
    - order: "what time is it"
  neurons:
    - systemdate:
        say_template:
          - "It' {{ hours }} hours and {{ minutes }} minutes"
```

Synapse that give complete date and time with a template file.

```yaml
- name: "time"
  signals:
    - order: "what time is it"
  neurons:
    - systemdate:
        file_template: en_systemdate_template_example.j2
```

## Templates example

This template will transcribe received numbers from the neuron into natural language

```
"It's {{ hours }} hours and {{ minutes }} minutes
```

This template, which must be placed in a file_template, will give the complete date and time.

```jinja2
{% set day_of_week = {
    "0": "sunday",
    "1": "monday",
    "2": "tuesday",
    "3": "wednesday",
    "4": "thursday",
    "5": "friday",
    "6": "saturday"
    }[weekday] | default("")
-%}

{% set month_word = {"1": "january", "2": "february", "3": "march", "4": "april", "5": "may", "6": "june", "7": "july", "8": "august", "9": "september", "10": "october", "11": "november", "12": "december"}[month] | default("") -%}

{% set day_month_formated = {
    "1": "first",
    "2": "second",
    "3": "third",
    "4": "fourth",
    "5": "fifth",
    "6": "sixth",
    "7": "seventh",
    "8": "eighth",
    "9": "ninth",
    "10": "tenth",
    "11": "eleventh",
    "12": "twelfth",
    "13": "thirteenth",
    "14": "fourteenth",
    "15": "fifteenth",
    "16": "sixteenth",
    "17": "seventeenth",
    "18": "eighteenth",
    "19": "nineteenth",
    "20": "twentieth",
    "21": "twenty-first",
    "22": "twenty-second",
    "23": "twenty-third",
    "24": "twenty-fourth",
    "25": "twenty-fifth",
    "26": "twenty-sixth",
    "27": "twenty-seventh",
    "28": "twenty-eighth",
    "29": "twenty-ninth",
    "30": "thirtieth",
    "31": "thirty-first",

}[day_month] | default("") -%}

It' {{ hours }} hours and {{ minutes }} minutes.
We are the {{ day_of_week }} {{ month_word }} the {{ day_month_formated }} {{ year }}
```

## Notes

> **Note:** As the neuron is based on the local system date, this last must be well configured. A good practice is the installation and configuration of a NTP client
> to synchronize the time on your Linux system with a centralized NTP server.
