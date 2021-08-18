#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from PIL import Image as PILImage
from io import BytesIO


def box_blur_kernel(size, c=1):
    """
    Return a kernel for a 'box blur' (https://en.wikipedia.org/wiki/Box_blur) of
    a given size.  The optional parameter c is a scaling factor applied to each
    element of the kernel
    """
    return [[c/size**2 for i in range(size)] for j in range(size)]


class Image:
    """
    A class to represent images, including support for a few different image
    manipulations.
    """
    def __init__(self, width, height, pixels):
        self.width = width
        """The width of the image, in pixels."""
        self.height = height
        """The height of the image, in pixels."""
        self.pixels = pixels
        """The pixel values of the image, in row-major order."""

    def get_pixel(self, x, y):
        """
        Returns the value of the pixel at location (x, y).
        Raises an exception if the given location is out of range.
        """
        return self.pixels[x + self.width*y]

    def get_pixel_extend(self, x, y):
        """
        Returns the value of the pixel at location (x,y).
        If the pixel value is out of range, returns the value at the nearest
        valid pixel.
        """
        x = max(0, min(self.width-1, x))
        y = max(0, min(self.height-1, y))
        return self.get_pixel(x, y)

    def set_pixel(self, x, y, c):
        """
        Sets the value of the pixel at location x
        """
        self.pixels[x + self.width*y] = c

    def apply_per_pixel(self, func):
        """
        Returns a new image of the same shape as self, whose pixel values are
        the result of passing self's pixels through the function func.

        func is a function of a single parameter (a pixel value).
        """
        result = Image.new(self.width, self.height)
        for x in range(result.width):
            for y in range(result.height):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x, y, newcolor)
        return result

    def inverted(self):
        """
        Returns a copy of self with the colors inverted.
        """
        return self.apply_per_pixel(lambda c: 255-c)

    def correlate(self, kernel):
        """
        Perform a correlation between self and the given kernel.  Returns a new
        image containing the result of the correlation.

        The kernel is given as a 2-d array (list of lists).
        """
        out = Image.new(self.width, self.height)
        kern_size = len(kernel)//2  # the 'half-width' of the kernel
        for x in range(self.width):
            for y in range(self.height):
                # for each pixel, loop over the surrounding pixels, multiplying
                # each by the associated value in the kernel and accumulating
                # the results.
                v = 0
                for kx in range(len(kernel)):
                    for ky in range(len(kernel)):
                        px = x - kern_size + kx
                        py = y - kern_size + ky
                        v += self.get_pixel_extend(px, py) * kernel[ky][kx]
                # finally, set the pixel to the accumulated value.
                out.set_pixel(x, y, v)
        return out

    def finalize(self):
        """
        Mutate self so that all of its pixel values are valid (i.e., integers
        in the range 0-255, inclusive).
        """
        self.pixels = [max(0, min(255, int(round(i)))) for i in self.pixels]

    def blurred(self, n):
        """
        Correlate the image with a blur kernel of size n (the higher this value
        is, the blurrier the resulting image is).
        """
        out = self.correlate(box_blur_kernel(n))
        out.finalize()
        return out

    def sharpened(self, n):
        """
        Return a new image, the result of an "unsharp mask" on the image.  n is
        the size of the blur kernel used (the higher this value is, the
        "sharper" the resulting image is).
        """
        # start by creating an appropriate kernel.  this the sum of:
        # * a 'delta' of size 2 at the center value (to take care of scaling
        #   the original image up by a factor of 2)
        # * a negative copy of the blur kernel (to take care of subtracting the
        #   blurred copy of the image)
        kern = box_blur_kernel(n, -1)
        kern[n//2][n//2] += 2
        out = self.correlate(kern)
        out.finalize()
        return out

    def edges(self):
        """
        Use a Sobel filter (https://en.wikipedia.org/wiki/Sobel_operator) to
        find the edges of the image.
        """
        sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
        # Correlating with the two kernels above results in two images: one
        # that has the vertical edges only, and one that has the horizontal
        # edges only.
        rx = self.correlate(sobel_x)
        ry = self.correlate(sobel_y)
        # Once we have those, loop over the pixels, combining them .
        out = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                val = (rx.get_pixel(x, y)**2 + ry.get_pixel(x, y)**2)**0.5
                out.set_pixel(x, y, val)
        # Finally, make sure the resulting values form a proper image.
        out.finalize()
        return out

    def copy(self):
        """
        Return a new instance of Image with identical size and pixels to this
        image.
        """
        out = Image.new(self.width, self.height)
        out.pixels = self.pixels[:]
        return out

    def minimum_energy_column(self):
        """
        Return the index of the column of the image with minimal energy (here,
        energy is defined according to the edge detection method above).
        """
        # Compute the edges, and sum the values of the resulting image down
        # each of the columns.
        e = self.edges()
        col_sums = []
        for c in range(self.width):
            col_sums.append(sum(e.get_pixel(c, r) for r in range(self.height)))
        # The value we return is the index of the column with the minimal sum
        # (if there is a tie, the left-most column with that value is
        # returned).
        return min(range(len(col_sums)), key=lambda x: col_sums[x])

    def kill_column(self, c):
        """
        Mutate the image to remove the pixels in the given column (c)
        """
        # Compute a list of the pixel indices we want to remove.  These are
        # sorted so that the highest value comes first so that removing one
        # pixel value doesn't affect the locations of the others.
        # Then, loop through and remove these pixels one by one.
        seamix = sorted([r*self.width + c for r in range(self.height)], reverse=True)
        for ix in seamix:
            self.pixels.pop(ix)
        self.width -= 1  # don't forget to adjust the width!

    def remove_low_energy_columns(self, ncols):
        """
        Return a new image whose width is decreased by ncols, by repeatedly
        computing and removing the column with the lowest energy.
        """
        # Start with a copy of the original image (so that we aren't mutating
        # the original), and repeatedly remove the lowest-energy column from it
        # until we reach the desired size.
        out = self.copy()
        for i in range(ncols):
            out.kill_column(out.minimum_energy_column())
        return out

    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass

    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
