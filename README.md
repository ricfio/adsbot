# Classified Ads Publishing Bot (python/selenium)

AdsBot is an automated system to publish classified ads for used items on specialized websites.  
Ad publishing is currently available for the following websites:

- [Subito.it](https://www.subito.it)

**DISCLAIMER**  
This software is provided for educational purposes only.  
You should not use it to publish your ads without the explicit permission from the specific service provider's platform.

## Getting start

This project uses a specific docker image `ricfio/adsbot` based on the repository [ricfio/sandbox-slenium](https://github.com/ricfio/sandbox-selenium).  

The first time you need to build the docker image:  

```bash
make docker-build
```

Then you can login docker container with this command:  

```bash
make docker-login
```

Now you can use the software inside the docker container:

```bash
./adsbot.py
```

```console
usage: adsbot.py [--help] <command>

<command>
 - list               List ads
 - publish            Publish ads
```

List Ads:

```bash
./adsbot.py list
```

Publish Ads:

```bash
./adsbot.py publish
```

## Configuration

You need a registered account to publish ads on [Subito.it](https://www.subito.it).  
Update your `.env` file adding `SUBITO_USERNAME` and `SUBITO_PASSWORD` variables:  

```yaml
# Application Config Path (for Dependency Injection)
CONFIG_PATH=config.json

# Subito.it
SUBITO_USERNAME=
SUBITO_PASSWORD=
```

The software use a very basic dependency injection system based on a `config.json` file (see `CONFIG_PATH`).  
You would like change the `CONFIG_PATH` to `config.test.json` (test configuration).  

Here the `config.test.json` content:

```json
{
  "datasource": {
    "name": "json_file_reader",
    "args": {
      "adlist_json_path": "./data/test/ads_subito_it.json",
      "images_base_path": "./data/test/images"
    }
  },
  "publishers": [
    {
      "name": "subito_it",
      "args": {
      }
    }
  ]
}
```

You can change the json filepath (`adlist_json_path`) to point to a folder with the ads to publish.  
Of course you can change the ads path, but you could also update the json content.  

You can found some examples of ads in the json file used for the automatic testing:  

- `./data/test/ads_subito_it.json`

## Appendix

This software has been implemented in [Python](https://www.python.org/) language and uses [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/).

### TODO

Some features could be implemented in the next releases are:

- [X] Improve CLI to select only a subset of ads (--offset=, --limit=)
- [ ] Add tests for CLI
- [ ] Implement new alternative datasources to fetch ads (for example: from Databases, API, etc.)
- [ ] Add other service providers to support ads multi publishing
