# CS254_project_data
US NCAA Women's Soccer Data

Using python, we pulled Women's Soccer data form https://stats.ncaa.org/ which has much publicly available data on NCAA athletics. In the zip file are the various files containing the data. This file will walk you through the contents of each file.

To run the program, you'll need Final_Prepared_Data.zip as well as the Neural Net.ipynd, and the Archive.zip has the folder Matthew used on his mac to run the final program -- Neural Net.ipynb is included in Archive.zip as well. Finally, you'll need the training data located on google drive at Google Drive Links because I was unable to upload these to Github. With the data in their respective folders (training in Neural_Net_Data and testing in Final_Prepared_Data), you should be able to run the program sans issues.

In alphabetical order, these are the files and what they do/contain:

150.zip: Dummy Data Sets 100-150, should you be interested in seeing the data generated.

Archive.zip: As explained above, this is a compressed file holding all the necessary code for running the neural network on a mac. If you put the data accessable at google drive in a folder Neural_Net_Data, and the contents of Final_Prepared_Data in a identically named folder, you will be able to run the program.

Data_Final.zip: The final data we used. Collected via python code from https://stats.ncaa.org/, each team has a specific ID for a certain sport, gender, and year. So, for example, 480829 is the ID for the 2019 Women's Soccer season at Stanford. Going to https://stats.ncaa.org/teams/480829 will take you to this page. Our program accessed the relevant pages, and downloaded the relevant sections. Inside Data_Final.zip is a textfile for each ID, with the team name in the first line and then each game of the season afterwards. This data is unprocessed at this point.

Final_Prepared_Data.zip: A compressed file containing the real-life data, ready for use once compressed.

Google Drive Links: Has links to google drive where you can download the Neural_Network_Data data (it was too big to upload myself and takes a long time to compress/decompress). Let us know if you're unable to access it, although I edited the permissions so you should be good to go.

Neural Net.ipynd: The same file in Archive.zip that has the code for our neural network

azimutghal.py: The code for taking latitude and longitude and converting it to points on a plane that we were going to use if we got further into our project.

byhand.py: A file used to do some tedious work that was easier to accomplish by hand than by code.

competition_tester.py: A file used to generate dummy data by simulating competitions, 15 seasons per data set.

data_checker.py: A file that helps to verify the data we retrieved is valid

data_loader.py: A file that helps ensure we don't mistakenly fail to interpret the same team as two separate teams (for example, making sure that we don't consider "Akron" as a different team than "Akron Zips", since the mascot of Akron is the Zips, whatever they may be)

data_prep.py: A file that takes the dummy data and converts it into data usable by the neural network. It outputs input files (x), team files that say which teams played a given game (t), and the true values that we want to train the network to learn (y). The files this outputs can be seen in the google drive links.

dictionary_maker.xlsx: A excel sheet used in conjunction with byhand.py to get necessary data for data_loader.py

final_getter_efficient: The ultimate file we used to get data from https://stats.ncaa.org/, downloading all Women's Soccer games it can.

tournamnet_visualization.xlsx: Used to visualize the tournament while constructing competition_tester.py

true_data_prep.py: Prepares the actual data from https://stats.ncaa.org/ to be inputted into the neural network, like the dummy data but without y values calculated since we don't know them.

url.py: The old way we got data from https://stats.ncaa.org/ that we stopped using due to inefficiency and etc.
