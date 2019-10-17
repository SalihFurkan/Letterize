# Letterize
In letterize, a GUI program allows you to draw any letter you want and predict the letter.
Machine Learning Algorithm is used to predict. Model is trained over MNIST dataset. Neural Network is used.
The draw system is taken from Tech with Tim and changed accordingly. I appreciate his work which lead me into this. 
Draw class is belonged to Tim, Letterize class is modified version of his DrawMain class.
# How to
You can draw any letter you want and when you click the read button, program takes the surface as image.
After obtaining it, image is prepared for the prediction, meaning image is preprocessed for the model.
Pretrained model predict the image and gives the letter. Letter is shown on a black label on the surface.
# Dataset
The dataset is taken from MNIST. You can directly download from the website. 
Only letters are included to the dataset, 26 characters.
I only train for 26 letters and even if you write in upper case, it understands as lower case.
