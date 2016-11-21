# wikipedia_searcher

## Synopsis

Get the summary of a Wikipedia page.

## Options

| parameter | required | default | choices                     | comment                                                                                                                           |
|-----------|----------|---------|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| language  | yes      |         | E.g: "fr", "en", "it", "es" | See the list of available language in the "Note" section                                                                          |
| query     | yes      |         |                             | The wikipedia page you are looking for.  This parameter can be passed as an argument in the neuron from the order with {{ query}} |
| sentences | no       | 10      | Integer in range 1-10       | if set, return the first number of sentences(can be no greater than 10) specified in this parameter.                              |


## Return Values

| Name       | Description                             | Type   | sample                                                                                                                              |
|------------|-----------------------------------------|--------|-------------------------------------------------------------------------------------------------------------------------------------|
| summary    | Plain text summary of the searched page | string |  Wikipedia is a collaboratively edited, multilingual, free Internet encyclopedia supported by the non-profit Wikimedia Foundation.. |
| returncode | Error code. See bellow                  | string | SummaryFound                                                                                                                        |
| may_refer  | List of pages that can refer the query  | list   | ['Marc Le Bot', 'Bot', 'Jean-Marc Bot', 'bot', 'pied bot', 'robot', 'Sam Bot', 'Famille Both', 'Yves Bot', 'Ben Bot', 'Botswana']   |


| returncode          | Description                             |
|---------------------|-----------------------------------------|
| SummaryFound        | A summary hs been found from the querry |
| DisambiguationError | The query match more than ony one page. |
| PageError           | No Wikipedia matched a query            |

## Synapses example

This synapse will look for the {{ query }} spelt by the user on Wikipedia
```
- name: "wikipedia-search"
  signals:
    - order: "look on wikipedia {{ query }}"
  neurons:
    - wikipedia_searcher:
        language: "en"
        args:
          - query
        file_template: "wikipedia_returned_value.j2"

```

## Templates example 

This template will simply make Kalliope speak out loud the summary section of the Wikipédia page of the query.
If the query match more than one page, Kaliope will give the user all matched pages.
If the query doesn't match any page on Wikipedia, kalliope will notify the user.
```
{% if returncode == "DisambiguationError" %}
    The query match following pages    
    {% if may_refer is not none %}
        {% for page in may_refer %}
            {{ page }}
        {% endfor %}
    {% endif %}
{% elif returncode == "PageError" %}
    I haven't  found anything on this
{% else %}
    {{ summary }}
{% endif %}
```

## Notes

Available languages in [the detailed list of the offical Wikipedia page](https://en.wikipedia.org/wiki/List_of_Wikipedias#Detailed_list). The column is called "Wiki". E.g: "en"
