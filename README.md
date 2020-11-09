# Sokkalingam
Sokkalingam is a fully featured and modular movie ticket booking ChatBot created and tested with RASA Framework and RASA-X

# Advantages of *sokkalingam*
	1. Built on RASA, so it is programed to understand Natural Language.
	2. Highly Interactive with the user.
	3. Totally modular story flow.
	4. Gives you link to full details of the movie on IMDB.
	5. Generates real-time seatmap of available seats each time the user queries for available seats.
	6. Generates an unique TicketID which can be used later to regenerate or retrieve the tickets
	7. Generates a QR Code with all the details of the ticket the bot collected.
	5. Functions smoothly, nearly close to production deployment.
	6. It can be deployed on any social platform possible or can be embeded in any website.
	
# Procedure to deploy

**NOTE : The procedure is framed assuming that you have basic knowledge of installing Python for your operating system, creating environments to work with projects and running python files.**
	
*As a prerequisite, I recommend you to have Anaconda and PyCharm installed for easier setup of environments and better productivity. 
This just being a recommendation, *sokkalingam* should work fine with mannual python setup with the required modules installed.* 
	
1. Install git and on your system, refer the below link to install git on your system depending on the operating system you use

[Link-1](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

[Link-2](https://www.linode.com/docs/development/version-control/how-to-install-git-on-linux-mac-and-windows/)

**ONLY FOR WINDOWS**
You need to download and install Visual C++ Build tools from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

2. Once you have installed Git for your operating system, clone *sokkalingam* repository by typing in 
	```
	git clone https://github.com/nagarajanmolrao/sokkalingam
	```
3. Open your Anaconda propmt or Terminal, Change into the directory of the repository.

4. If your on windows you can re-create the same environment I created using the command
	```
	conda env create -f environment.yml --name yourEnvironmentName
	```
	Replace *yourEnvironmentName* with a custom environment name.
	This will create a environment with all the dependencies and install RASA.
	
5. Activate the environment with the command 
	```
	conda activate yourEnvironmentName
	```
	
6. Once you are using the newly created environment, the first thing to do is to install RASA-X
This can be easily done by running the command
	```
	pip install rasa-x -i https://pypi.rasa.com/simple
	```
	
7. Once RASA-X is installed, Open your the project folder *sokkalingam* in PyCharm or any IDE you prefer.

8. Change your IDE's interpreter to the interpreter of your newly created environment.
Here in PyCharm, Follow these steps
	- At the right bottom corner of the window, select "Current interpreter"
	- Select "Add Interpreter" and in the left pane select "Conda Environment"
	- Select "Exsisting Environment" radio button
	- In the "Interpreter" drop down list, select a interpreter which has yourEnvironmentName in it
	   The entry would be something like,
		```
		C:\Users\Anmol\.conda\envs\yourEnvironmentName\python.exe
		```
	- In general,"globalEnvironmentPath\yourEnvironmentName\python.exe"
	- Click on "OK" and wait till package scanning process completes.
		
**NOTE : This will work if you are using Anaconda, You will have to figure out your own way for setup interpreter if you are using mannual setup.**

9. Run the following command to train the model
	```
	rasa train
	```
10. Please change the following values in the corresponding files mentioned
	1. *data/movieSchedule.json*
		- Add or change the dates to whatever dates you want the bot to allow users to book tickets for.
			This is important because the bot reads this file first and asks a user to choose a date to continue booking tickets.
			The bot reads and displays only dates that is greater than the current system date.
		- Change the name of the movie next to the key values on a particular date
			This is completely optional as this is just a movie name that will be displayed by the bot.
			You can leave the defaults unchanged.
	2. *data/movieDetails.json*
		- Add or change the dates to the same dates you changed in the *movieSchedule.json* file
			This is important because the bot searches for the date selected by the user, which is obiviously already present in the *movieSchedule.json* file, and 				sends the user the corresponding IMDB link based on the *movieChoice*.
		- Add or change the terminating string of the IMDB link of the movie corresponding to its position in the *movieSchedule.json* file.
			You need to add only "tt*******/" from "https://www.imdb.com/title/tt*******/"
	3. *data/movieSeatMap.json*
		- Add or change the dates to the same dates you changed in the *movieSchedule.json* and *"data/movieDetails.json"* file
			This is important because the bot searches for the date selected by the user in this file to see the currently available seats for the corresponding 					movie the user has selected.
		- Change any of the "0" to "1"
			If you change any of the "0" to "1", the corresponding seat of the corresponding show on the corresponding date is available for the user for booking.
			1 : If seat is available & 
			0 : If seat is booked
		
It's just simple, one Key containing a date in *"data/movieSchedule.json"*, should have same date as key and should have some values in the files *"data/movieDetails.json"* and *"data/movieSeatMap.json"*

You can refer the previous values as a template.
	
11. Run the *"Django_server.py"* file as it is required to send the images generated during the chat with *sokkalingam*.

12. Run the following comamnd to start the rasa actions file with debugging info
	```
	rasa run actions -x
	```
You need to have this running in order to get replies from *sokkalingam*.

13. You can start chatting with the *sokkalingam* using the command	
	```
	rasa shell
	```
	OR 
	You can also start up RASA-X and chat in the RASA interface using the command
	```
	rasa x
	```
	
14. Go party!

#screenshots
![1](Screenshots/1.jpg?raw=true)

![2](Screenshots/2.jpg?raw=true)

![3](Screenshots/3.jpg?raw=true)

![4](Screenshots/4.jpg?raw=true)

![5](Screenshots/5.jpg?raw=true)

![6](Screenshots/6.jpg?raw=true)

![7](Screenshots/7.jpg?raw=true)

	
For some reason, I don't know why , the generated images like the AvailableSeats and TicketQRCode don't show up on RASA-X.

You can still access the images by using the Django WebServer running in the backgroud on port 7000 by default or just open the file in your IDE.
