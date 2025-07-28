import { app } from "../../scripts/app.js";

// 注册遮罩边缘检测节点的前端扩展
app.registerExtension({
    name: "ComfyUI.MaskEdgeDetection",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "MaskEdgeDetection") {
            // 在这里可以添加前端特定的行为
            // 例如自定义UI、验证等
            
            // 添加节点标题
            nodeType.prototype.getExtraMenuOptions = function(_, options) {
                options.push({
                    content: "关于遮罩边缘检测",
                    callback: () => {
                        alert("遮罩边缘检测节点：检测遮罩是否接触图像边缘\n输出：布尔值（true=接触边缘，false=未接触）");
                    }
                });
            };
        }
    }
});