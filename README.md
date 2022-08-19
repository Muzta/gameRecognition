ResNet Training
===============
The following instructions must be made in the folder resnetMiPropioDataset

```bash
cd resnetMiPropioDataset
```

Scrapping
---------
First, you must configurate the file extractDatabase.py options

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
startMoment(str): Moment of the video when start recording. Follow the formats: HH:MM:SS / MM:SS / SS
endMoment(str): Moment of the video when end recording. Follow the formats: HH:MM:SS / MM:SS / SS
```
You can find an example in extractImages/datasetVideoLinks.txt


