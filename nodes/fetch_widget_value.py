"""Fetch a widget value from another node in the workflow by node name and widget name."""

from comfy_api.latest import io


class FetchWidgetValue(io.ComfyNode):
    """Retrieves a widget value from another node in the current workflow.

    Looks up nodes by type, "Node name for S&R" property, or title.
    Can return a single value or concatenate values from all matching nodes.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="AlruFetchWidgetValue",
            display_name="Fetch Widget Value",
            category="utils/Alru Tools",
            inputs=[
                io.String.Input("node_name", multiline=False),
                io.String.Input("widget_name", multiline=False),
                io.Combo.Input("multiple", options=["no", "yes"], default="no"),
            ],
            outputs=[
                io.String.Output("value_string"),
                io.Float.Output("value_float"),
                io.Int.Output("value_int"),
            ],
            hidden=[
                io.Hidden.prompt,
                io.Hidden.extra_pnginfo,
            ],
        )

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        # Always re-execute — the target widget value may have changed
        return float("NaN")

    @classmethod
    def execute(cls, node_name, widget_name, multiple) -> io.NodeOutput:
        workflow = cls.hidden.extra_pnginfo["workflow"]
        prompt = cls.hidden.prompt
        multiple = multiple == "yes"

        results = []

        for node in workflow["nodes"]:
            node_id = None
            name = node["type"]

            # Check "Node name for S&R" property first
            if "properties" in node:
                if "Node name for S&R" in node["properties"]:
                    name = node["properties"]["Node name for S&R"]

            if name == node_name:
                node_id = node["id"]
            else:
                # Fall back to node title
                if "title" in node:
                    name = node["title"]
                if name == node_name:
                    node_id = node["id"]

            if node_id is None:
                continue

            values = prompt.get(str(node_id), {})
            if "inputs" in values and widget_name in values["inputs"]:
                v = values["inputs"][widget_name]
                if not multiple:
                    return _make_output(str(v))
                results.append(str(v))
            else:
                raise NameError(f"Widget not found: {node_name}.{widget_name}")

        if not results:
            raise NameError(f"Node not found: {node_name}")

        return _make_output(", ".join(results).strip(", "))


def _to_numeric(value: str) -> tuple[float, int]:
    """Try to parse a string as a number. Returns (0.0, 0) if not numeric."""
    try:
        f = float(value)
        return f, int(f)
    except (ValueError, TypeError):
        return 0.0, 0


def _make_output(value: str) -> io.NodeOutput:
    f, i = _to_numeric(value)
    return io.NodeOutput(value, f, i)
