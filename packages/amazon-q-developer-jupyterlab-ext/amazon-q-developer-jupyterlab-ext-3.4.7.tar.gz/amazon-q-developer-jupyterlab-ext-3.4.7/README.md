# Amazon Q Developer for JupyterLab

Amazon Q Developer is an AI coding companion which provides developers with real-time code suggestions in JupyterLab. Individual developers can use Q Developer for free in JupyterLab and AWS SageMaker Studio.

![Codewhisperer demo](https://docs.aws.amazon.com/images/amazonq/latest/qdeveloper-ug/images/qdev-demo-example.png)

## Requirements

In order to use Q Developer in JupyterLab, you must have a version of JupyterLab >= 4 installed. You will also need a free [AWS Builder ID](https://docs.aws.amazon.com/signin/latest/userguide/sign-in-aws_builder_id.html) account to access Q Developer. (You can set that up the first time you log in.)

In order to use Q Developer in SageMaker Studio, you must have set up a SageMaker Studio notebook instance, along with an execution role with the appropriate IAM Permissions. 

## Getting Started

Install [JupyterLab](https://pypi.org/project/jupyterlab) on your computer or if you already have JupyterLab installed, check it’s version by running the following command.

```
pip show jupyterlab
```

Note the version in the response, and follow the use the corresponding directions in one of the following sections.

### Installation Using Pip for Jupyter Lab version >= 4.0

You can install and enable the Q Developer extension for JupyterLab 4 with the following commands. 

```
# JupyterLab 4
pip install amazon-q-developer-jupyterlab-ext
```

Once installed, choose ****Get Started**** from the Amazon Q panel at the bottom of the window. This will enable to you log in to [AWS Builder ID](https://docs.aws.amazon.com/signin/latest/userguide/sign-in-aws_builder_id.html) to access Amazon Q Developer. Refer to [Setting up Q Developer with JupyterLab](https://docs.aws.amazon.com/codewhisperer/latest/userguide/jupyterlab-setup.html) for detailed setup instructions.

### SageMaker Studio

To setup the Q Developer extension with a SageMaker Studio notebook instance, you must add IAM Permissions for 
`codewhisperer:GenerateRecommendations` for your user profile. Then you must install and enable the extension with the following commands.

```
conda activate studio
pip install amazon-q-developer-jupyterlab-ext~=1.0
jupyter server extension enable amazon_q_developer_jupyterlab_ext
conda deactivate
restart-jupyter-server
```

After you complete installation and refresh your browser, an Amazon Q panel will appear at the bottom of the window. Refer to [Setting up Q Developer with SageMaker Studio](https://docs.aws.amazon.com/codewhisperer/latest/userguide/sagemaker-setup.html) for detailed setup instructions. 

## Features

### Code Completion

Q Developer for JupyterLab provides AI powered suggestions as ghost text with the following default keybindings. These can be modified in the settings.


|              Action	                  |      Key Binding       |
| ------------------------------ | ----------- |
| Manually trigger Q Developer | Alt C (Window) / ⌥ C (Mac)        |
| Accept a recommendation        | Tab       |
| Next recommendation            | Right arrow |
| Previous recommendation        | Left arrow  |
| Reject a recommendation        | ESC         |



Python is the only supported programming language for now. Users can start or pause suggestions by toggling the menu item in the Amazon Q panel that will appear at the bottom of the window.

### Code References

With the reference log, you can view references to code recommendations. You can also update and edit code recommendations suggested by Q Developer.

To view Code References for accepted suggestions, choose **Open Code Reference Log** from the Amazon Q panel at the bottom of the window. Users can also turn off code suggestions with code references in Settings.


## More Resources

* [Amazon Q Developer User Guide](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html)
* [Setting up Amazon Q Developer with JupyterLab](https://docs.aws.amazon.com/codewhisperer/latest/userguide/jupyterlab-setup.html)
* [Setting up Q Developer with Amazon SageMaker Studio](https://docs.aws.amazon.com/codewhisperer/latest/userguide/sagemaker-setup.html)

## Change Log

3.4.7
* Add "Other Features" tab in Amazon Q footbar and the tab
* Add Q customization support for chat response
* Add Q customization support for code completions

3.4.6
* Bugfix for Tab keybind being overridden in JupyterLab v4.3.1+
* Remove source URLs from ETL-specific responses
* Bugfix for suggestions not appearing in .py files

3.4.5
* Bugfix for Completions not within the active code cell.

3.4.4
* Default to Q enabled with free tier in MD

3.4.3
* Update Logic for Glue Code Completion trigger for code recommendations to account for upgrades made in Connections Logic by hitting GetConnection API for MaxDome
* For legal compliance, the Q telemetry settings copy needed to be updated, along with ensuring that when customers choose to opt out of code references, they aren't shown anywhere. It was determined that they were still shown in python files even when opted out.

3.4.2
* Follow up to update code inserted into code reference log should not render any html

3.4.1
* Updated language in Q IDE settings related to telemetry 

3.4.0
* Update code inserted into code reference log should not render any html

3.3.0
* Add user agent to http request
* Update Code Completion Trigger for MaxDomeConnectionMagics

3.2.0
* Add support for Glue code completions in MD environments when using Glue-related kernel.

3.1.0
* Fix ArrowDown, ArrowUp not working in JupyterLab 4.2
* Fix dispatch not triggering re-render in JupyterLab 4.2
* Add support for SSO mode

3.0.0
* Rename legacy [Amazon CodeWhisperer for JupyterLab](https://pypi.org/project/amazon-codewhisperer-jupyterlab-ext/) to [Amazon Q Developer for JupyterLab](https://pypi.org/project/amazon-q-developer-jupyterlab-ext/)
