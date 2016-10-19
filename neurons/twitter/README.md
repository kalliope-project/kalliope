# Twitter 

## Synopsis

This neuron allows you to send a tweet on your timeline.

## Options

| parameter           | required | default | choices | comment                     |
|---------------------|----------|---------|---------|-----------------------------|
| consumer_key        | yes      | None    |         | User info                   |
| consumer_secret     | yes      | None    |         | User info                   |
| access_token_key    | yes      | None    |         | User info                   |
| access_token_secret | yes      | None    |         | User info                   |
| tweet               | yes      | None    |         | The sentence to be tweeted  |

## Return Values

| Name  | Description                     | Type   | sample          |
|-------|---------------------------------|--------|-----------------|
| tweet | The tweet which has been posted | string | coucou kalliopé |

## Synapses example

```
- name: "post-tweet"
    neurons:
      - twitter:
          consumer_key: ""
          consumer_secret: ""
          access_token_key: ""
          access_token_secret: ""
          args:
            - tweet
    signals:
      - order: "post on Twitter {{ tweet }}"
```

## Notes

In order to be able to post on Twitter, you need to grant access of your application on Twitter by creating your own app associate to your profile. 

### How to create my Twitter app

1. Sign in your [Twitter account](https://www.twitter.com)
2. Let's create your app [apps.twitter.com](https://apps.twitter.com)
3. click on the button "Create New App"
4. Fill in your application details
5. Create your access token (to post a tweet, you need at least "Read and Write" access)
6. Get your consumer_key, consumer_secret, access_token_key and access_token_secret from the tab "Key and access token" (Keep them secret !)
7. Post your first message with this neuron !