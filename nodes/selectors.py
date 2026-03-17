"""Standalone selector nodes for sampler, scheduler, and checkpoint."""

import comfy.samplers
import folder_paths

from comfy_api.latest import io


class AlruSelectSampler(io.ComfyNode):
    """Select a sampler algorithm. Outputs as both Combo and String."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="AlruSelectSampler",
            display_name="Select Sampler",
            category="sampling/Alru Tools",
            inputs=[
                io.Combo.Input("sampler_name",
                               options=comfy.samplers.KSampler.SAMPLERS),
            ],
            outputs=[
                io.Combo.Output("SAMPLER_NAME"),
                io.String.Output("SAMPLER_NAME_STR"),
            ],
        )

    @classmethod
    def execute(cls, sampler_name) -> io.NodeOutput:
        return io.NodeOutput(sampler_name, sampler_name)


class AlruSelectScheduler(io.ComfyNode):
    """Select a noise scheduler. Outputs as both Combo and String."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="AlruSelectScheduler",
            display_name="Select Scheduler",
            category="sampling/Alru Tools",
            inputs=[
                io.Combo.Input("scheduler",
                               options=comfy.samplers.KSampler.SCHEDULERS),
            ],
            outputs=[
                io.Combo.Output("SCHEDULER"),
                io.String.Output("SCHEDULER_STR"),
            ],
        )

    @classmethod
    def execute(cls, scheduler) -> io.NodeOutput:
        return io.NodeOutput(scheduler, scheduler)


class AlruSelectCheckpoint(io.ComfyNode):
    """Select a checkpoint model. Outputs as both Combo and String."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="AlruSelectCheckpoint",
            display_name="Select Checkpoint",
            category="loaders/Alru Tools",
            inputs=[
                io.Combo.Input("ckpt_name",
                               options=folder_paths.get_filename_list("checkpoints")),
            ],
            outputs=[
                io.Combo.Output("CKPT_NAME"),
                io.String.Output("CKPT_NAME_STR"),
            ],
        )

    @classmethod
    def execute(cls, ckpt_name) -> io.NodeOutput:
        return io.NodeOutput(ckpt_name, ckpt_name)
