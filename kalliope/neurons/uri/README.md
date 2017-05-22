# Uri

## Synopsis

Interacts with HTTP and HTTPS web services.

## Installation

CORE NEURON : No installation needed.  

## Options

| parameter      | required | default | choices                                      | comment                                                                    |
|----------------|----------|---------|----------------------------------------------|----------------------------------------------------------------------------|
| url            | YES      |         |                                              | HTTP or HTTPS URL in the form (http|https)://host.domain[:port]/path       |
| headers        | NO       |         | E.g: Content-Type: 'application/json'        | Add custom HTTP headers to a request in the format of a YAML hash          |
| data           | NO       |         | E.g: "{\"title\": \"foo\"}"                  | JSON data to send to the server. You must escape quotes in the YAML file.  |
| data_from_file | NO       |         | E.g: /path/to/my/file.json                   | JSON data loaded from a file.                                              |
| method         | NO       | GET     | GET, POST, DELETE, PUT, HEAD, PATCH, OPTIONS | The HTTP method of the request or response. It MUST be uppercase.          |
| user           | NO       |         |                                              | username for the basic authentication.                                     |
| password       | NO       |         |                                              | passwordfor the basic authentication.                                      |
| timeout        | NO       |         |                                              | The socket level timeout in seconds. Must be an integer without quotes     |


## Return Values

| Name            | Description                                                                            | Type   | sample                                                                                          |
|-----------------|----------------------------------------------------------------------------------------|--------|-------------------------------------------------------------------------------------------------|
| status_code     | Numeric, HTTP status code that signifies success of the request.                       | int    | 200                                                                                             |
| content         | The body content of the server answer. May be JSON serialized and usable in a template | string | {"title": "foo", "body": "bar", "userId": 1}                                                    |
| response_header | Response header from the server.                                                       | dict   | {'Date': 'Sat, 19 Nov 2016 11:17:56 GMT', 'Content-Length': '192', 'Content-Type': 'text/html'} |

## Synapses example

Simple call to a server. The default method is GET
```yml
  - name: "test-get-url"
    signals:
      - order: "test-get-url"
    neurons:
      - uri:
          url: "http://host.domain/get/1"             
```

A simple call with authentication
```yml
- name: "test-get-url-with-auth"
    signals:
      - order: "test-get-url-with-auth"
    neurons:
      - uri:
          url: "http://host.domain/get/1"        
          user: "admin"
          password: "secret"
```

A simple post with data inside the url 
```yml
- name: "test-post-url-with-auth"
    signals:
      - order: "test-post-url-with-data"
    neurons:
      - uri:
          url: "http://host.domain/login?email=user@host.domain&password=foobar123" 
          method: POST          
```

A post with json data. Note that we need to escape quotes from the payload.
```yml
- name: "test-post-url"
    signals:
      - order: "test-post-url"
    neurons:
      - uri:
          url: "http://host.domain/posts"
          method: POST
          headers:            
            Content-Type: 'application/json'      
          data: "{\"id\": 1,\"title\": \"foo\", \"body\": \"bar\", \"userId\": 1}"         
```

A post with json data imported from a file and a custom header.
```yml
- name: "test-post-url"
    signals:
      - order: "test-post-url"
    neurons:
      - uri:
          url: "http://host.domain/posts"
          method: POST
          headers:            
            Content-Type: 'application/json'
            user-agent: 'my-app/0.0.1'
          data_from_file: "/path/to/my/payload.json"        
```

And the `payload.json` would be (note that we don't need to escape any character):
```
{"title": "foo", "body": "bar", "userId": 1}
```

A simple call to a deletion. Here we also ask Kalliope to tell use if request was a success through a template, depending on the returned status code.
```yml
  - name: "test-delete-url"
    signals:
      - order: "test-delete-url"
    neurons:
      - uri:
          url: "http://host.domain/posts/1"
          method: DELETE          
          say_template:
            - "{% if status_code==201 %}delete complete{% else %}fail to delete{% endif %}"
```

Call to an URL to get a resource and make kalliope speaking out loud a value of returned content.
Here, we ask the server to return us the user with ID number 42. We know that the server will return a dict like the following
```
{
  "id": 42,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "company": {
    "name": "Romaguera-Crona",
    "catchPhrase": "Multi-layered client-server neural-net",
    "bs": "harness real-time e-markets"
  }
}
```

Here is the synapse we would use to make Kalliope speak out loud the name of the user and the name of his company
```yml
  - name: "test-get-url-with-template"
    signals:
      - order: "test-get-url-with-template"
    neurons:
      - uri:
          url: "http://host.domain/users/42"                
          say_template:
            - "The user name is {{ content.name }} and his company's name is {{ content.company.name }}"
```


## Templates example 

The following template will make kalliope read the content of the received json variable "title" from the remote server.
```
The title is {{ content.title }}
```

The following template will make Kalliope say if the request has been made with success or not depending on the returned status code.
```
{% if status_code==200 %}request complete{% else %}request failled{% endif %}
```

## Notes
> When the parameter `data` is used, you need to escape character that could be interpreted by the YAML syntax.
