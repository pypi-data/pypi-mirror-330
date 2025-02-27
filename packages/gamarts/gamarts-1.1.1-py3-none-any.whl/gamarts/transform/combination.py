"""The binary transformation file contains transformation that include other arts."""
from pygame import Surface, transform as tf
from .transformation import Transformation

class Concatenate(Transformation):
    """The concatenate transformation concatenates multiple arts into one bigger animation."""

    def __init__(self, *others) -> None:
        """
        The concatenate transformation concatenates multiple arts into a longer one animation.

        Params:
        ---
        - *others: Art, the other arts the transformed art will be concatenated with.

        Raises:
        ---
        - ValueError, if all the arts do not have the exact same size.
        """
        super().__init__()
        if len(set(other.size for other in others)) != 1:
            raise ValueError("All arts must have the same size to be concatenated.")
        self.others = others

    def apply(self, surfaces: tuple[Surface], durations: tuple[int], introduction: int, index: int, width: int, height: int, **ld_kwargs):
        need_to_unloads = []
        for art in self.others:
            if not art.is_loaded():
                need_to_unloads.append(True)
                art.load(**ld_kwargs)
            else:
                need_to_unloads.append(False)

        surfaces = surfaces + sum((art.surfaces for art in self.others), ())
        durations = durations + sum((art.durations for art in self.others), ())

        for other, need_to_unload in zip(self.others, need_to_unloads):
            if need_to_unload:
                other.unload()

        return surfaces, durations, introduction, None, width, height

def _combine_arts(*durations: tuple[int], introduction: int) -> tuple[list[tuple[int, tuple[int]]], int]:
    """Combine a list of durations to create a new art."""
    indexes = [0 for _ in durations]
    output = []
    tot_time = 0
    mx = max(sum(d) for d in durations)
    matrix_duration = [list(d) for d in durations]

    output_introduction = None
    for durations in matrix_duration:
        durations[-1] = durations[-1] + (mx - sum(durations))

    while tot_time < mx:

        if indexes[0] == introduction and output_introduction is None:
            output_introduction = len(output)

        mn = min(dur[0] for dur in matrix_duration)
        output.append((mn, tuple(indexes)))

        for i, durations in enumerate(matrix_duration):
            durations[0] -= mn
            if durations[0] == 0:
                durations.pop(0)
                indexes[i] += 1
        tot_time += mn

    return output, output_introduction

class Average(Transformation):
    """
    Compute the average of the frames of the art. The average is computed taking into account the time and durations of the frames.
    If the art have different total durations, the last frame of shorter arts is extend.
    """

    def __init__(self, *others) -> None:
        """
        Compute the average of the frames of the art.

        Params:
        ---
        - *others: Art, the other arts the transformed art will be averaged with.

        Raises:
        ---
        - ValueError, if all the arts do not have the exact same size.
        """
        super().__init__()
        if len(set(other.size for other in others)) != 1:
            raise ValueError("All arts must have the same size to be concatenated.")
        self.others = others

    def apply(self, surfaces: tuple[Surface], durations: tuple[int], introduction: int, index: int, width: int, height: int, **ld_kwargs):
        need_to_unloads = []
        for art in self.others:
            if not art.is_loaded():
                need_to_unloads.append(True)
                art.load(**ld_kwargs)
            else:
                need_to_unloads.append(False)

        combined_arts, introduction = _combine_arts(durations, *(other.durations for other in self.others), introduction=introduction)
        new_surfaces = []
        new_durations = []
        all_surfaces = [surfaces] + [other.surfaces for other in self.others]
        for duration, (indexes) in combined_arts:
            avg = tf.average_surfaces([surf[index] for surf, index in zip(all_surfaces, indexes)])
            new_surfaces.append(avg)
            new_durations.append(duration)

        for other, need_to_unload in zip(self.others, need_to_unloads):
            if need_to_unload:
                other.unload()

        return new_surfaces, new_durations, introduction, None, width, height

class Blit(Transformation):
    """
    Copy an art over another one. The blitting is computed taking into account the time and durations of the frames.
    If the art have different total durations, the last frame of shortest art is extend.
    """

    def __init__(self, other, x: int, y: int) -> None:
        """
        Copy an art over another one.
        
        Params:
        ---
        - other: art, the art to be blitted on top of this one.
        - x, y: int, the coordinate on which the other art is blitted.
        """
        super().__init__()
        self.other = other
        self.pos = (x,y)

    def apply(self, surfaces: tuple[Surface], durations: tuple[int], introduction: int, index: int, width: int, height: int, **ld_kwargs):
        need_to_unload = False
        if not self.other.is_loaded():
            self.other.load(**ld_kwargs)
            need_to_unload = True

        combined_arts, introduction = _combine_arts(durations, self.other.durations, introduction=introduction)
        new_surfaces = []
        new_durations = []
        for duration, (idx1, idx2) in combined_arts:
            back = surfaces[idx1].copy()
            back.blit(self.other.surfaces[idx2], self.pos)
            new_surfaces.append(back)
            new_durations.append(duration)

        if need_to_unload:
            self.other.unload()

        return new_surfaces, new_durations, introduction, None, width, height
