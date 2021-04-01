from jupyterhub_configurator.hooks import hookimpl

@hookimpl
def jupyterhub_configurator_fields():
    return {
        "schema.default_interface": {
            "type": "string",
            "traitlet": "Spawner.default_url",
            "title": "Default User Interface",
            "enum": ["/tree", "/lab", "/nteract"],
            "default": "/tree",
            "enumMetadata": {
                "/tree": {
                    "title": "Classic Notebook",
                    "description": "The original single-document interface for creating Jupyter Notebooks.",
                },
                "/lab": {
                    "title": "JupyterLab",
                    "description": "A Powerful next generation notebook interface",
                },
                "/nteract": {
                    "title": "Nteract",
                    "description": "Nteract notebook interface",
                },
            },
        }
    }
