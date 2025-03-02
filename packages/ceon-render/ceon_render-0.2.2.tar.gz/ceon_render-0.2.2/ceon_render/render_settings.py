from dataclasses import dataclass, field


@dataclass
class CeonRenderJobSettings:
    """
    Stores configurable settings that can be set for a particular render job.
    This is used in conjunction with a CeonRenderPipelineJob to generate
    a full executable AppRenderJob instance.
    This class is app/type(frames, geo, sim) agnostic, it simply stores various settings
    which can be extracted when building the CeonRenderJob instance.


    frame_dimensions: The dimensions of frames to be rendered [width, height]
    frame_range: A frame range to be rendered [start, stop, step]
    env: A dict containing any environment variables to be set for this job.
    """

    # Frame rendering config
    frame_dimensions: tuple[int, int] | None = None
    frame_range: tuple[int, int, int] | None = None
    env: dict = field(default_factory=dict)

    # Sim/geo config
    # TODO
