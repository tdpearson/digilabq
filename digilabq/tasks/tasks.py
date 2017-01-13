from celery.task import task
from dockertask import docker_task
from subprocess import call,STDOUT
from PIL import Image
import requests

#Default base directory 
#basedir="/data/static/"


#Example task
@task()
def processimage(inpath, outpath, outformat="TIFF", filter="ANTIALIAS", scale=None):
    """
    Digilab TIFF derivative Task

    args:
      inpath - path string to input image
      outpath - path string to output image
      outformat - string representation of image format - default is "TIFF"
      scale - percentage to scale by represented as a decimal
      filter - string representing filter to apply to resized image - default is "ANTIALIAS"
    """

    image = Image.open(inpath)
    if scale:
        imagefilter = getattr(Image, filter.upper())
        size = [x * scale for x in image.size]
        image.thumbnail(size, imagefilter)
    image.save(outpath, outformat)
    return "Success"
    
