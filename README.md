# Profinder

Telegram Profile Finder OSINT tool

## How to run

Place file `.env` with Telegram API_ID and API_HASH. Then configure `config.py`, where:

* `names` - dict of some keys (just for printing) and combinations of names that will be searched
* `groups` - array of group (chat) names, where to find

Or you can pass files with names and/or groups to the script with corresponding `-n` and `-g` options. Then you can run it with:

`python3 profinder.py`

* Use `-s` to set sleep time in seconds between each name resolution (search quieter)
* `-M` - more name combinations (also check just by surname)
* `-o` - save final results to file
* `-sd` - save dump of users from chats to the file for future scans
* `-d` - load dump with user chats. In this case the script even doesn't need to interact with telegram
* `-v` - verbose output. Prints each name resolution results immediately

## Files format

If you want to use a file with names or groups, then it should have the following format:

### Names:

```
Surname First_name [something that will not be read]
```

### Groups:

Just a name of a group on each new line
