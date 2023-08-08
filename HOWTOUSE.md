# OperantBehaviorAnalysis-Python
For ease of use, this document describes helpful applications for interacting with and running scripts in this repository.

Before beginning, make a GitHub account, and make sure git is installed on your computer: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.

First of all, fork this repository to your personal GitHub. I recommend creating working branches for yourself rather than working directly in master. 
You can also periodically update this fork by pulling changes from the original repository into your fork.

## Applications for Download
#### Anaconda Navigator
- This application allows you to create python environments which contain all the required packages for using this repository
- Download the most recent version here: https://www.anaconda.com/distribution/#macos
- If you have windows, make sure to go to the windows tab and download the graphical interface
- Go to environments and create a new one with a useful name, in the latest version of Python
- Install pytest, openpyxl, numpy, scipy, matplotlib, natsort, and pandas in that environment
#### GitHub Desktop
- This application allows you to connect your local git with GitHub without having to go through Shell (but everything can definitely be done in Shell if you so choose)
- Download here: https://desktop.github.com/
- Connect the application to your github account
- Add your forked repository
- You can also fetch changes from your fork on GitHub whenever you need
- Later, once you have made changes, you can make commits and push them to your GitHub fork
- If you feel these changes are important, you can create a pull request to this repository and the changes can be discussed and incorporated
#### PyCharm
- This is the application I like to use for editing and running scripts (but there are many others)
- PyCharm is very well integrated with Git
- Download community version here: https://www.jetbrains.com/pycharm/download/#section=mac
- Create new project, with the location as your local cloned repository, and the environment you created in Anaconda
    (you can also add packages from within PyCharm if needed by going to settings or preferences-->project-->interpreter then use the + to add packages)
- Make sure you are in the desired branch (check Git at bottom of screen)
- Now you can interact with scripts, making new ones, changing them, and running them
- To run a script, open it and go to Run --> Run, and click on the configuration that matches the script name
    (If the configuration is already set properly, you can just click the green arrow)
- Each day's data file must be in an individual folder
    (if you have multiple files for one day, you can paste the text from one file into another and delete the extra file)
- Most scripts in this repository are set up so they loop through days of data you select
    (You will be asked for a number of days, and then a window will open that many times for you to select data)
    (the 'day' listed in the file will be based on the order you select files, if you do not start on day 1 you will need to manually edit this in the final data file)
- Scripts are written to output an excel file called 'output' into the local python folder
    (this will need to be saved into a different location with an informative name, otherwise will be re-written next time script is run)
- Depending on what you want to see as the output, you may need to add print statements or code for graphing
- If a graph is output in a new window, you will need to click the red square to stop running the program when you are done with the graph
