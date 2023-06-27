## Welcome to the NYC511 CameraScrape!

More to Come!


WARNING!!! THIS Repository was made with an out of date version of Selenium.

For compatability please install a virtual environment along with the correct package versions shown in requirements.txt:


`python -v venv NYC_Cam_Venv
source NYC_Cam_Venv/bin/activate #assumes you're running MacOS
pip install -r requirements.txt
`

If you wish to add this environment to your jupyter notebook instance you must also do the following:

`
pip install ipykernel
python -m ipykernel install --user --name=NYC_Cam_Venv
`
 
From there you should now be able to select the "NYC_Cam_Venv" (you may use an alternative name if you wish) available under the kernels in your jupyter notebook instance (you may need to refresh the page first.)