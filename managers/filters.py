import cv2
import numpy
import utils

# This files func used for Edge Detection


def strokeEdge(src, dst, blurKsize=7, edgeKsize=5):

    """"
    Trying to create custom filter in order to find the boundary of the object in the image
    Cleaning images with digital noise with medianBlur
    Then convert the image in grayscale
    Then apply Laplacian to do a bold marker on the edges
    Args:
        edgeKsize: whole number which represents the filter kernel

    """
    if blurKsize >= 3: # used for medianBlur blurKsize
        blurredSrc = cv2.medianBlur(src, edgeKsize)
        graySrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
    else: # used for laplacianBlur edgeKsize is used
        graySrc = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        # apply laplacian
        cv2.Laplacian(graySrc, cv2.CV_8U, graySrc, ksize=edgeKsize)


    normalizedInverseAlpha = (1.0 / 255) * (255 - graySrc)
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalizedInverseAlpha

    cv2.merge(channels, dst)


