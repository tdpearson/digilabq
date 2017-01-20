from celery.task import task
#from celery.task.sets import TaskSet
#from celery.exceptions import Ignore
#from celery import states
from dockertask import docker_task
from subprocess import check_call
from tempfile import NamedTemporaryFile
from PIL import Image
import os


#Default base directory 
basedir="/data/static/"
hostname ="http://localhost"

#libtiff-tools needs to be installed within the docker container


def _processimage(inpath, outpath, outformat="TIFF", filter="ANTIALIAS", scale=None, crop=None):
    """
    Internal function to create image derivatives
    """
        
    try:
        image = Image.open(inpath)
    except (IOError, OSError):
        # workaround for Pillow unrecognized tiff image
        if inpath.split(".")[-1].upper() in ["TIF", "TIFF"]:
            with NamedTemporaryFile() as tmpfile:
                check_call(("tiff2rgba", inpath, tmpfile.name))
                image = Image.open(tmpfile.name)
        else:
            raise Exception
        
    if crop:
        image = image.crop(crop)
        
    if scale:
        imagefilter = getattr(Image, filter.upper())
        size = [x * scale for x in image.size]
        image.thumbnail(size, imagefilter)
    image.save(outpath, outformat)


@task()
def processimage(inpath, outpath, outformat="TIFF", filter="ANTIALIAS", scale=None, crop=None):
    """
    Digilab TIFF derivative Task

    args:
      inpath - path string to input image
      outpath - path string to output image
      outformat - string representation of image format - default is "TIFF"
      scale - percentage to scale by represented as a decimal
      filter - string representing filter to apply to resized image - default is "ANTIALIAS"
      crop - list of coordinates to crop from - i.e. [10, 10, 200, 200]
    """
    
    task_id = str(processimage.request.id)
    #create Result Directory
    resultDir = os.path.join(basedir, 'oulib_tasks/', task_id)
    os.makedirs(resultDir)

    _processimage( inpath=os.path.join(basedir, inpath),
                   outpath=os.path.join(basedir, outpath),
                   outformat=outformat,
                   filter=filter,
                   scale=scale,
                   crop=crop
                 )

    return "{0}/oulib_tasks/{1}".format(hostname,task_id)

