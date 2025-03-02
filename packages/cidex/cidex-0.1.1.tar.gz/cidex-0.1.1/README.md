# cidex

cidex is a convention used in my [rtfm indexes](https://github.com/cibere/Rtfm-Indexes) repository as a way of conveying information to my [rtfm lookup](https://github.com/cibere/Rtfm-Indexes) repository for displaying rtfm results for docs/manuals that don't follow convention.

As the cidex convention allows for customization than other conventions allow, it is also possible to use a custom cidex index file by putting it at the root of your domain, and naming it ``index.cidex``. For example: `https://google.com/index.cidex`. If you have multiple versions, you can return a `VariantManifest`

# Current Specifications

You should put a file called `index.cidex` in the root of your domain, for example: `https://google.com/index.cidex`. This can be any data structure specified in these specifications.

## VariantManifest

This is a manifest that can point to different versions of docs that are available on your domain.

This can also be recursive, so if you had multiple projects with multiple versions, you can have manifests pointing to other manifests.

```json
{
    "variants": [
        // list of variants, which can be accessed by querying `index-{variant}.cidex
        "stable", // can be accessed with `index-stable.cidex`
        "latest", // can be accessed with `index-latest.cidex`
        "v1", // can be accessed with `index-v1.cidex`
        "v2", // can be accessed with `index-v2.cidex`
    ],
    "version": "2.1" // this must be set to 2.1 for this version of the specification
}
```

## CacheIndex

This data structure shows the entire cache that should be used when querying your doc/manual.

```json
{
    "name": "the name of the project the index is for",
    "favicon_url": "a direct link to the icon to show when displaying the entries. This can also be `null`",
    "cache": { // the cache's keys should be used for searching/matching, however it should never be displayed. The information in the EntryObject should be used when displaying the results
        "entry-1": EntryObject,
        "entry-2": EntryObject,
    },
    "version": "2.1", // this must be set to 2.1 for this version of the specification
    "type": "cache-index" // this indicates that this is a cache index
}
```

## ApiIndex

This data structure should be used when you want to use an api instead of a static cache.

Note: When using this index, the api is responsible for sorting & matching the entries.

```json
{
    "name": "the name of the project the index is for",
    "favicon_url": "a direct link to the icon to show when displaying the entries. This can also be `null`",
    "url": "the url that should be used when sending a POST request to the api",
    "options": {
        // any information that the api might use to determine how to process the request and return the correct entruies
    },
    "version": "2.1", // this must be set to 2.1 for this version of the specification
    "type": "api-index" // this indicates that this is an api index
}
```

When sending a request to the api, you should use the following payload:
```json
{
    "query": "the text that you are searching for",
    "options": {
        // the options from the options key in the ApiIndex
    },
    "version": "2.1", // this must be set to 2.1 for this version of the specification
}
```
and as a response, the api should return a [`CacheIndex`](#cacheindex) with the same version as the payload.

## Entry

The entry object is the object that actually includes the information to display for each result.

```json
{
    "text": "the title/text to display",
    "url": "the url to go to when selected/clicked",
    "options": EntryOptions // extra options for customizing how the result should be displayed.
}
```

### EntryOptions

The options available for entry objects isn't well defined yet, but here are the keys that my [rtfm plugin for flow launcher](https://github.com/cibere/Flow.Launcher.Plugin.rtfm) accepts:

Note: All of these are optional
```json
{
    "sub": "the subtitle to display",
    "icon": "a url to an icon for this specific entry",
    "title_highlight_data": [], // a list of ints that corospond to which characters in the result's text should be highlighted
    "title_tooltip": "the text that should appear when hovering over the title",
    "sub_tooltip": "the text that should appear when hovering over the subtitle",
}