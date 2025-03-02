from dataclasses import dataclass


@dataclass
class CeonRenderJobSettings:
    """
    Stores configurable settings that can be set for a particular render job.
    This is used in conjunction with a CeonRenderPipelineJob to generate
    a full executable CeonRenderJob instance.
    This class is app/type(frames, geo, sim) agnostic, it simply stores various settings
    which can be extracted when building the CeonRenderJob instance.
    """

    # Frame rendering config
    frame_dimensions: tuple[int, int] | None = None
    frame_range: tuple[int, int, int] | None = None

    # Sim/geo config
    # TODO
