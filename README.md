# trestle-bot

trestle-bot assists users in leveraging [Compliance-Trestle](https://github.com/IBM/compliance-trestle) in automated workflows or [OSCAL](https://github.com/usnistgov/OSCAL) formatted compliance content management. 

In addition to trestle-bot, this repo contains the trestle-bot GitHub Action that can optionally be used to host the trestle-bot service within GitHub Actions.

> WARNING: This project is under active development.

## Basic Configuration


```

name: Example Workflow
...

    steps:
      - uses: actions/checkout@v3
      - name: Run trestlebot
        id: trestlebot
        uses: RedHatProductSecurity/trestle-bot@main
        with:
          markdown_path: "markdown/profiles"
          oscal_model: "profile"
```

## Inputs and Outputs

Checkout [`action.yml`](./action.yml) for a full list of supported inputs and outputs.

### Additional information on workflow inputs

- `markdown_path`: This is the location for Markdown generated by the `trestle author <model>-generate` commands
- `ssp_index_path`: This is a text file that stores the component definition information by name in trestle with the ssp name. Example below

```json
 "ssp1": {
            "profile": "profile1",
            "component definitions": [
                "comp1",
                "comp2"
            ]
        },
```