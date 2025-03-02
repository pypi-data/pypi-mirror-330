# Gradio
examples = [
    [
        "Where can the driver see the car speed in this image? Please output segmentation mask.",
        "./resources/imgs/example1.jpg",
    ],
    [
        "Can you segment the food that tastes spicy and hot?",
        "./resources/imgs/example2.jpg",
    ],
    [
        "Assuming you are an autonomous driving robot, what part of the diagram would you manipulate to control the direction of travel? Please output segmentation mask and explain why.",
        "./resources/imgs/example1.jpg",
    ],
    [
        "What can make the woman stand higher? Please output segmentation mask and explain why.",
        "./resources/imgs/example3.jpg",
    ],
]
output_labels = ["Segmentation Output"]

title = "LISA: Reasoning Segmentation via Large Language Model"
description = """
<font size=4>
This is the online demo of LISA... \n
If multiple users are using it at the same time, they will enter a queue, which may delay some time. \n
**Note**: **Different prompts can lead to significantly varied results**. \n
**Note**: Please try to **standardize** your input text prompts to **avoid ambiguity**, and also pay attention to whether the **punctuations** of the input are correct. \n
**Usage**: <br>
&ensp;(1) To let LISA **segment something**, input prompt like: "Can you segment xxx in this image?", "What is xxx in this image? Please output segmentation mask."; <br>
&ensp;(2) To let LISA **output an explanation**, input prompt like: "What is xxx in this image? Please output segmentation mask and explain why."; <br>
&ensp;(3) To obtain **solely language output**, you can input like what you should do in current multi-modal LLM (e.g., LLaVA). <br>
Hope you can enjoy our work!
</font>
"""

demo_parameters = """## Model configuration parameters\n
The demo uses these parameters:
"""

article = """
<p style='text-align: center'>
<a href='https://arxiv.org/abs/2308.00692' target='_blank'>
Preprint Paper
</a>
\n
<p style='text-align: center'>
<a href='https://github.com/dvlab-research/LISA' target='_blank'>   Github Repo </a></p>
"""
