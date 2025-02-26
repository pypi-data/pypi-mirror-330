import os
import sys
import numpy as np
import moderngl as mgl
import glm
import pygame as pg
from PIL import Image as PIL_Image


texture_sizes = (8, 64, 512, 1024, 2048)


class Image():
    name: str
    """Name of the image"""   
    index: glm.ivec2
    """Location of the image in the texture arrays"""
    data: np.ndarray
    """Array of the texture data"""
    size: int
    """The width and height in pixels of the image"""

    def __init__(self, path: str | os.PathLike | pg.Surface | mgl.Texture) -> None:
        """
        A basilisk image object that contains a moderngl texture
        Args:
            path: str | os.PathLike | pg.Surface
                The string path to the image. Can also read a pygame surface
        """
        
        # Check if the user is loading a pygame surface
        if isinstance(path, str) or isinstance(path, os.PathLike):
            return self._from_path(path)
        elif isinstance(path, pg.Surface):
            return self._from_surface(path)
        elif isinstance(path, mgl.Texture):
            return self._from_texture(path)
        
        raise TypeError(f'Invalid path type: {type(path)}. Expected a string or os.PathLike')

    def _from_path(self, path: str | os.PathLike) -> None:
        """
        Loads a basilisk image from a pygame surface
        Args:
        """
        
        # Get name from path
        self.name = path.split('/')[-1].split('\\')[-1].split('.')[0]

        # Load image
        img = PIL_Image.open(path).convert('RGBA')
        # Set the size in one of the size buckets
        size_buckets = texture_sizes
        self.size = size_buckets[np.argmin(np.array([abs(size - img.size[0]) for size in size_buckets]))]
        img = img.resize((self.size, self.size)) 
        # Get the image data
        self.data = img.tobytes()

        # Default index value (to be set by image handler)
        self.index = glm.ivec2(1, 1)

    def _from_surface(self, surf: pg.Surface) -> None:
        """
        Loads a basilisk image from a pygame surface
        Args:
        """
        
        # Set the size in one of the size buckets
        size_buckets = texture_sizes
        self.size = size_buckets[np.argmin(np.array([abs(size - surf.get_size()[0]) for size in size_buckets]))]
        surf = pg.transform.scale(surf, (self.size, self.size)).convert_alpha()
        # Get image data
        self.data = pg.image.tobytes(surf, 'RGBA')

        # Default index value (to be set by image handler)
        self.index = glm.ivec2(1, 1)

    def _from_texture(self, texture: mgl.Texture):
        """
        
        """
        ...

    def __repr__(self) -> str:
        """
        Returns a string representation of the object
        """
        return f'<Basilisk Image | {self.name}, ({self.size}x{self.size}), {sys.getsizeof(self.data) / 1024 / 1024:.2} mb>'