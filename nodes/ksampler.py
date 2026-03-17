"""KSampler with passthrough outputs for easy chaining."""

import comfy.sample
import comfy.samplers
import comfy.utils
import latent_preview
import torch

from comfy_api.latest import io


def common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative,
                    latent, denoise=1.0, disable_noise=False, start_step=None,
                    last_step=None, force_full_denoise=False):
    latent_image = latent["samples"]
    latent_image = comfy.sample.fix_empty_latent_channels(model, latent_image)

    if disable_noise:
        noise = torch.zeros(latent_image.size(), dtype=latent_image.dtype,
                            layout=latent_image.layout, device="cpu")
    else:
        batch_inds = latent.get("batch_index", None)
        noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)

    noise_mask = latent.get("noise_mask", None)

    callback = latent_preview.prepare_callback(model, steps)
    disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
    samples = comfy.sample.sample(
        model, noise, steps, cfg, sampler_name, scheduler,
        positive, negative, latent_image,
        denoise=denoise, disable_noise=disable_noise,
        start_step=start_step, last_step=last_step,
        force_full_denoise=force_full_denoise,
        noise_mask=noise_mask, callback=callback,
        disable_pbar=disable_pbar, seed=seed,
    )

    out = latent.copy()
    out["samples"] = samples
    return out


class AlruKSamplerPlus(io.ComfyNode):
    """KSampler that passes MODEL, CONDITIONING, and LATENT through outputs for easy chaining."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="AlruKSamplerPlus",
            display_name="KSampler+",
            category="sampling/Alru Tools",
            description="KSampler with passthrough outputs for easy chaining of multiple sampling steps.",
            inputs=[
                io.Model.Input("model", tooltip="The model used for denoising."),
                io.Int.Input("seed", default=0, min=0, max=0xFFFFFFFFFFFFFFFF,
                             control_after_generate=True,
                             tooltip="Random seed for noise generation."),
                io.Int.Input("steps", default=20, min=1, max=10000,
                             tooltip="Number of denoising steps."),
                io.Float.Input("cfg", default=8.0, min=0.0, max=100.0,
                               step=0.1, round=0.01,
                               tooltip="Classifier-Free Guidance scale."),
                io.Combo.Input("sampler_name",
                               options=comfy.samplers.KSampler.SAMPLERS,
                               tooltip="Sampling algorithm."),
                io.Combo.Input("scheduler",
                               options=comfy.samplers.KSampler.SCHEDULERS,
                               tooltip="Noise scheduler."),
                io.Conditioning.Input("positive", tooltip="Positive conditioning."),
                io.Conditioning.Input("negative", tooltip="Negative conditioning."),
                io.Latent.Input("latent_image", tooltip="Input latent image."),
                io.Float.Input("denoise", default=1.0, min=0.0, max=1.0,
                               step=0.01, tooltip="Denoising strength."),
            ],
            outputs=[
                io.Latent.Output("LATENT", tooltip="Denoised latent."),
                io.Model.Output("MODEL", tooltip="Passthrough model."),
                io.Conditioning.Output("POSITIVE", tooltip="Passthrough positive conditioning."),
                io.Conditioning.Output("NEGATIVE", tooltip="Passthrough negative conditioning."),
                io.Int.Output("SEED"),
                io.Int.Output("STEPS"),
                io.Float.Output("CFG"),
                io.Combo.Output("SAMPLER_NAME"),
                io.Combo.Output("SCHEDULER"),
                io.Float.Output("DENOISE"),
                io.String.Output("SAMPLER_NAME_STR"),
                io.String.Output("SCHEDULER_STR"),
            ],
        )

    @classmethod
    def execute(cls, model, seed, steps, cfg, sampler_name, scheduler,
                positive, negative, latent_image, denoise=1.0) -> io.NodeOutput:
        latent_out = common_ksampler(
            model, seed, steps, cfg, sampler_name, scheduler,
            positive, negative, latent_image, denoise=denoise,
        )
        return io.NodeOutput(
            latent_out, model, positive, negative,
            seed, steps, cfg, sampler_name, scheduler, denoise,
            sampler_name, scheduler,
        )
