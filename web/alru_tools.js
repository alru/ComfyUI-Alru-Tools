import { app } from "../../scripts/app.js";

const NODE_COLORS = {
    "AlruCLIPTextEncodePositive": { color: "#232", bgcolor: "#353" },
    "AlruCLIPTextEncodeNegative": { color: "#322", bgcolor: "#533" },
};

app.registerExtension({
    name: "alru.tools.nodeColors",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        const colors = NODE_COLORS[nodeData.name];
        if (colors) {
            const onCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onCreated?.apply(this, arguments);
                this.color = colors.color;
                this.bgcolor = colors.bgcolor;
            };
        }
    },
});
