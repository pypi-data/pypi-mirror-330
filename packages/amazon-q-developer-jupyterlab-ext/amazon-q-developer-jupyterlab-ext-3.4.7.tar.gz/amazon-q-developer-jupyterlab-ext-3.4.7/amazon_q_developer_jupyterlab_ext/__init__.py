import json
from pathlib import Path

from .handlers import setup_handlers

HERE = Path(__file__).parent.resolve()

with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": data["name"]}]


def _jupyter_server_extension_points():
    return [{"module": "amazon_q_developer_jupyterlab_ext"}]


def _load_jupyter_server_extension(server_app):
    """Registers the API handler to receive HTTP requests from the frontend extension.
    Parameters
    ----------
    server_app: jupyterlab.labapp.LabApp
        JupyterLab application instance
    """
    url_path = "amazon_q_developer_jupyterlab_ext"
    setup_handlers(server_app.web_app, url_path)
    server_app.log.info(
        f"Registered amazon_q_developer_jupyterlab_ext extension at URL path /{url_path}"
    )

# For backward compatibility with the classical notebook
load_jupyter_server_extension = _load_jupyter_server_extension