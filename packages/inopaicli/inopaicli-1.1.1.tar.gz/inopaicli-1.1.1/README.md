# Inopai CLI

### This package is intended to help with inopai related automation tasks

Install this package via pip:

```pip install inopaicli``

## Context

inopaicli needs an inopai installation url as a parameter, i.e.

```
inopaicli --url https://inopai.com
```

## Commands

Possible commands:

```
actions_download_all
actions_update
app_get
app_get_element_definitions
app_get_schema
app_get_workflow_states
app_update
commands_print
curl_print
download_files
entries_export
entries_export_excel
entries_sync
entries_update
exports_download_all
exports_update
flatt_app_schema_and_export_entries
group_get
update_app_instance
```

## Usage example

With credentials stored in 

## Plugins

You can add plugins to your project that has the package installed, that act as package commands

The plugins folder must be called `inopaicli-plugins` and it has to be in your current working directory
