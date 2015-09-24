### Introduction

This is a modified version of the following script:

https://mixpanel.com/docs/api-documentation/data-export-api#libs-python

Which is adapted to support the Data Export API:

https://mixpanel.com/docs/api-documentation/exporting-raw-data-you-inserted-into-mixpanel


### Usage

You simply need to set `MIXPANEL_API_KEY` and `MIXPANEL_API_SECRET` at the top of the file and then you can start pulling data like follows:

```python
    api = MixpanelExportAPI(
        api_key = MIXPANEL_API_KEY,
        api_secret = MIXPANEL_API_SECRET
    )    
    data = api.request(['export'], {
        'from_date': '2015-09-01',
        'to_date': '2015-09-2',
        'event': ['play video'],
    })    
    pprint.pprint(data)
```