# Rest API

Kalliope provides the REST API to manage the synapses. For configuring the API refer to the [settings documentation](settings/settings.md#rest-api).

- [Synapses API](api/synapses.md)
- [Settings API](api/settings.md)

## Main API views

### Get Kalliope's version

Normal response codes: 200

Error response codes: unauthorized(401)

Curl command:

```bash
curl -i --user admin:secret -X GET  http://localhost:5000/
```

Output example:

```JSON
{
  "Kalliope version": "0.4.2"
}
```
