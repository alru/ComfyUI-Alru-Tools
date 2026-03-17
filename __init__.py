"""Alru Tools — utility nodes for ComfyUI."""

from typing_extensions import override

from comfy_api.latest import ComfyExtension, io
from .nodes.fetch_widget_value import FetchWidgetValue
from .nodes.ksampler import AlruKSamplerPlus
from .nodes.clip_encode import AlruCLIPTextEncodePositive, AlruCLIPTextEncodeNegative
from .nodes.selectors import AlruSelectSampler, AlruSelectScheduler, AlruSelectCheckpoint

WEB_DIRECTORY = "./web"


class AlruToolsExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            FetchWidgetValue,
            AlruKSamplerPlus,
            AlruCLIPTextEncodePositive,
            AlruCLIPTextEncodeNegative,
            AlruSelectSampler,
            AlruSelectScheduler,
            AlruSelectCheckpoint,
        ]


async def comfy_entrypoint() -> AlruToolsExtension:
    return AlruToolsExtension()
