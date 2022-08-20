ResNet Training
===============
The following instructions must be made in the folder resnetMiPropioDataset:

```bash
cd resnetMiPropioDataset
```

Scrapping
---------
First, you must configurate the file extractDatabase.py options:

```python
DATASETNAME = 'your_dataset_name' #It'll be created in the folder datasets/
NIMAGES = 2 
LINKSFILEPATH = os.path.join('extractImages','your_extraction_file.txt') #The path of your extraction file
```

Then run it:
```bash
python extractDatabase.py
```

Extraction file
---------------
It must have the next format:

```
name, url, startMoment[Optional], endMoment[Optional] 
...

name(str): The name you would like for your images. It will be your class name.
url(str): The URL of the video where the images are taken.
startMoment(str): Moment of the video when start recording. Follow the formats: HH:MM:SS / MM:SS / SS .
endMoment(str): Moment of the video when end recording. Follow the formats: HH:MM:SS / MM:SS / SS .
```
You can find an example in extractImages/datasetVideoLinks.txt

Training a model
----------------

Run the file trainer.py:

```bash
python trainer.py [-m --model] [-d --dataset]


required arguments:

-m --model      Path and name where the model will be stored.
-d --dataset    Path of the dataset. Must be a file system with the structure: datasetName->className->[Images].

```

There are more configuration options in the source code:
```python

BATCH = 32 #Batch size
EPOCHS = 100 
ACCURACY = 1 #Stopping validation. Accuracy over trainning data
LOSS = 0 #Stopping validation. Loss over trainning data

```

Also, you can change your network at line 72:

```python
# You can use ResNet34, ResNet50 or ResNet101
model = ResNet101.build(numChannels=3, imgRows=224, ...

```

Test the model
--------------

To check the preformance of your model, you can run the modelTest.py file:

```bash
python modelTest.py [-m --model] [-d --dataset] [-w --width] [--e --height]


required arguments:

-m --model      Path of the model to check
-d --dataset    Name of the dataset in the folder datasets

optionals arguments:

-w --width      Widh of the model intput images (default = 224)
--e --height    Height of the model intput images (default = 224)
```

Before running it, you must modify the array 'labelNames' in the source code and set the classes of your model. You can find it at line 65:

```python
labelNames = numpy.array(['Deathloop', 'It takes two', ...
```

This method gives details for each image in de dataset, so it´s recommended using a small and controlled dataset.



