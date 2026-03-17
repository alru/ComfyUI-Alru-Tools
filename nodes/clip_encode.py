"""CLIP Text Encode nodes with passthrough text output."""

from comfy_api.latest import io


def encode_text(clip, text):
    tokens = clip.tokenize(text)
    cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
    return [[cond, {"pooled_output": pooled}]]


class AlruCLIPTextEncodePositive(io.ComfyNode):
    """CLIP Text Encode (Positive) with text passthrough for chaining."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="AlruCLIPTextEncodePositive",
            display_name="Positive Prompt",
            category="conditioning/Alru Tools",
            inputs=[
                io.Clip.Input("clip"),
                io.String.Input("text", multiline=True),
            ],
            outputs=[
                io.Conditioning.Output("CONDITIONING"),
                io.Clip.Output("CLIP"),
                io.String.Output("TEXT"),
            ],
        )

    @classmethod
    def execute(cls, clip, text) -> io.NodeOutput:
        return io.NodeOutput(encode_text(clip, text), clip, text)


class AlruCLIPTextEncodeNegative(io.ComfyNode):
    """CLIP Text Encode (Negative) with text passthrough for chaining."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="AlruCLIPTextEncodeNegative",
            display_name="Negative Prompt",
            category="conditioning/Alru Tools",
            inputs=[
                io.Clip.Input("clip"),
                io.String.Input("text", multiline=True),
            ],
            outputs=[
                io.Conditioning.Output("CONDITIONING"),
                io.Clip.Output("CLIP"),
                io.String.Output("TEXT"),
            ],
        )

    @classmethod
    def execute(cls, clip, text) -> io.NodeOutput:
        return io.NodeOutput(encode_text(clip, text), clip, text)
