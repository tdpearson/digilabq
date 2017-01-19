from celery.task import task
from dockertask import docker_task
from subprocess import check_call
from tempfile import NamedTemporaryFile
from PIL import Image


#Default base directory 
#basedir="/data/static/"

#libtiff-tools needs to be installed within the docker container


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

    if scale:
        imagefilter = getattr(Image, filter.upper())
        size = [x * scale for x in image.size]
        image.thumbnail(size, imagefilter)
    image.save(outpath, outformat)
    return "Success"
    
